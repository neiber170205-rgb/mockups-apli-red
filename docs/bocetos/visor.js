/* ==========================================================================
   Visor de bocetos. Sin dependencias, sin imágenes, sin build.
   Va al final del <body>.

   Idea única: el boceto es de tamaño fijo y no se puede reflowear, así que lo
   único que se transforma en toda la página es .bo — y a su padre .pantalla se
   le fija ancho×escala por alto×escala, porque transform NO cambia la caja de
   layout y si no queda un hueco del tamaño original. El cromo del aparato no
   lleva transform: se dibuja ya escalado con calc(var(--s) * …px).
   ========================================================================== */
(function () {
  'use strict';

  var app = document.getElementById('app');
  if (!app) return;

  var esc      = document.getElementById('escenario');
  var aparato  = document.getElementById('aparato');
  var pantalla = document.getElementById('pantalla');
  var bo       = document.getElementById('bo');
  var col      = document.getElementById('col');
  var panel    = document.getElementById('panel');
  var cuerpo   = document.getElementById('panel-cuerpo');
  var pie      = document.getElementById('panel-pie');

  var W = parseFloat(app.style.getPropertyValue('--w')) || 1280;
  var H = parseFloat(app.style.getPropertyValue('--h')) || 820;

  /* El generador ya distingue movil / panel / escritorio, pero el ancho manda:
     el artboard de 812 px son dos pantallas de celular lado a lado y no cabe
     dentro de un iPhone. */
  if (app.dataset.tipo === 'movil' && W > 480) app.dataset.tipo = 'panel';
  var TIPO   = app.dataset.tipo;
  var MOVIL  = TIPO === 'movil';
  var CORTE  = MOVIL ? 874 : 820;      /* alto de una pantalla real */
  var MAX_AJUSTE = MOVIL ? 1.5 : 2;    /* hasta dónde puede crecer el encaje solo */
  var MIN_ESC = 0.05, MAX_ESC = 6;

  var cs = getComputedStyle(app);
  function medida(v) { return parseFloat(cs.getPropertyValue(v)) || 0; }
  function limita(v, a, b) { return v < a ? a : (v > b ? b : v); }
  function porc(v) { return Math.round(v * 100) + ' %'; }

  var NOMBRE = MOVIL ? 'iPhone 17 Pro' : (TIPO === 'panel' ? 'Dos celulares' : 'Escritorio');

  /* ---------- 1 · textos que se rellenan solos ---------- */
  /* {{TITULO}} aparece UNA vez en el HTML; de ahí se copia a la barra y a la
     barra de direcciones falsa, para que el generador no tenga que sustituir
     el mismo marcador en tres sitios. */
  var titulo = (document.getElementById('panel-tit').textContent || '').trim();
  var ruta = document.getElementById('ruta');
  var pastilla = document.getElementById('pastilla');
  if (ruta) ruta.textContent = titulo;
  if (pastilla) pastilla.textContent = titulo;

  var etiquetaTam = W + ' × ' + H + ' px';
  var fTam = document.getElementById('f-tam');
  var fTipo = document.getElementById('f-tipo');
  var fEsc = document.getElementById('f-esc');
  var lblMedida = document.getElementById('medida');
  if (fTam) fTam.textContent = etiquetaTam;
  if (fTipo) fTipo.textContent = MOVIL ? 'Celular · iPhone 17 Pro simulado'
            : (TIPO === 'panel' ? 'Dos pantallas de celular' : 'Ventana de escritorio');
  if (lblMedida) lblMedida.textContent = NOMBRE + ' · ' + etiquetaTam;

  /* bloques que el generador puede dejar vacíos */
  ['b-puntos', 'b-nota', 'panel-pie'].forEach(function (id) {
    var el = document.getElementById(id);
    if (!el) return;
    var lista = el.querySelector('ul');
    var vacio = lista ? lista.children.length === 0 : !el.textContent.trim() && !el.querySelector('a,p,li');
    if (vacio) el.remove();
  });

  /* las bandas del teléfono se pintan del color de fondo real del boceto, para
     que no se vea la costura entre la barra de estado y la pantalla */
  try {
    var fondo = getComputedStyle(bo).backgroundColor;
    if (fondo && fondo !== 'rgba(0, 0, 0, 0)' && fondo !== 'transparent') {
      app.style.setProperty('--g-banda', fondo);
    }
  } catch (e) {}

  /* ---------- 2 · encaje ---------- */
  var usuario = 1;      /* 1 = ajustado a la pantalla */
  var ajuste = 1, escala = 1, ultW = -1, ultH = -1, pedido = 0;

  function hueco() {
    var e = getComputedStyle(esc);
    var px = parseFloat(e.paddingLeft) + parseFloat(e.paddingRight);
    var py = parseFloat(e.paddingTop) + parseFloat(e.paddingBottom);
    return { w: Math.max(40, esc.clientWidth - px), h: Math.max(40, esc.clientHeight - py) };
  }

  function altoVisible() {
    return app.dataset.modo === 'real' ? Math.min(H, CORTE) : H;
  }

  /* La escala es la MISMA en los dos ejes: un solo min(), nunca dos factores. */
  function calculaAjuste(hv, d) {
    var marco = medida('--marco'), sup = medida('--bsup'), inf = medida('--binf');
    var s;
    if (MOVIL) {
      /* el teléfono escala entero: bisel, isla y botones incluidos */
      s = Math.min(d.w / (W + 2 * marco), d.h / (hv + 2 * marco + sup + inf));
    } else {
      /* la barra de la ventana se queda a 1:1 y nítida; sólo escala el boceto */
      s = Math.min(d.w / W, Math.max(20, d.h - sup) / hv);
    }
    return (isFinite(s) && s > 0) ? Math.min(s, MAX_AJUSTE) : 1;
  }

  function aplicar() {
    var hv = altoVisible();
    var d = hueco();
    ultW = d.w; ultH = d.h;

    ajuste = calculaAjuste(hv, d);
    escala = limita(ajuste * usuario, MIN_ESC, MAX_ESC);

    app.style.setProperty('--hv', String(hv));
    app.style.setProperty('--s', String(escala));

    var txt = porc(escala);
    var bPct = document.getElementById('pct');
    if (bPct) {
      bPct.textContent = txt;
      bPct.title = 'Ajustar a la pantalla  (0) · ahora ' + txt;
    }
    if (fEsc) fEsc.textContent = txt + (Math.abs(usuario - 1) < 0.001 ? ' · ajustada' : '');

    esc.classList.toggle('desbordado',
      aparato.offsetWidth > d.w + 1 || aparato.offsetHeight > d.h + 1);
  }

  function reprograma() {
    if (pedido) return;
    pedido = requestAnimationFrame(function () { pedido = 0; aplicar(); });
  }

  /* ---------- 3 · zoom ---------- */
  /* El escenario es un contenedor con scroll: acercar es cambiar la escala y
     corregir el scroll para que el punto bajo el cursor no se mueva. */
  function zoomA(nuevo, cx, cy) {
    nuevo = limita(nuevo, MIN_ESC / Math.max(ajuste, 0.0001), MAX_ESC / Math.max(ajuste, 0.0001));
    var r0 = aparato.getBoundingClientRect();
    var ax = r0.width ? (cx - r0.left) / r0.width : 0.5;
    var ay = r0.height ? (cy - r0.top) / r0.height : 0.5;
    if (Math.abs(nuevo - usuario) < 0.0005) return;
    usuario = nuevo;
    aplicar();
    var r1 = aparato.getBoundingClientRect();
    esc.scrollLeft += (r1.left + ax * r1.width) - cx;
    esc.scrollTop += (r1.top + ay * r1.height) - cy;
  }

  function centro() {
    var r = esc.getBoundingClientRect();
    return { x: r.left + r.width / 2, y: r.top + r.height / 2 };
  }
  function paso(f) { var c = centro(); zoomA(usuario * f, c.x, c.y); }
  function ajustarTodo() {
    usuario = 1; aplicar();
    esc.scrollTo ? esc.scrollTo(0, 0) : (esc.scrollLeft = esc.scrollTop = 0);
  }
  function tamanoReal(cx, cy) {
    var c = (cx == null) ? centro() : { x: cx, y: cy };
    zoomA(1 / Math.max(ajuste, 0.0001), c.x, c.y);
  }

  document.getElementById('mas').addEventListener('click', function () { paso(1.25); });
  document.getElementById('menos').addEventListener('click', function () { paso(1 / 1.25); });
  document.getElementById('pct').addEventListener('click', ajustarTodo);
  var bUno = document.getElementById('uno');
  if (bUno) bUno.addEventListener('click', function () { tamanoReal(null, null); });

  esc.addEventListener('dblclick', function (e) {
    if (Math.abs(usuario - 1) > 0.001) ajustarTodo();
    else tamanoReal(e.clientX, e.clientY);
  });

  esc.addEventListener('wheel', function (e) {
    if (!(e.ctrlKey || e.metaKey)) return;      /* rueda sola = desplazar, nativo */
    e.preventDefault();
    zoomA(usuario * Math.exp(-e.deltaY * (e.deltaMode === 1 ? 0.026 : 0.0016)), e.clientX, e.clientY);
  }, { passive: false });

  /* arrastrar para desplazar, sólo cuando el boceto no cabe: si cabe, el ratón
     sigue sirviendo para seleccionar el texto del boceto */
  var arr = null;
  esc.addEventListener('pointerdown', function (e) {
    if (e.button !== 0 || !esc.classList.contains('desbordado')) return;
    arr = { x: e.clientX, y: e.clientY, sl: esc.scrollLeft, st: esc.scrollTop, id: e.pointerId };
    esc.classList.add('arrastrando');
    try { esc.setPointerCapture(e.pointerId); } catch (_) {}
  });
  esc.addEventListener('pointermove', function (e) {
    if (!arr || e.pointerId !== arr.id) return;
    esc.scrollLeft = arr.sl - (e.clientX - arr.x);
    esc.scrollTop = arr.st - (e.clientY - arr.y);
  });
  function suelta(e) {
    if (!arr || (e && e.pointerId !== arr.id)) return;
    try { esc.releasePointerCapture(arr.id); } catch (_) {}
    arr = null;
    esc.classList.remove('arrastrando');
  }
  esc.addEventListener('pointerup', suelta);
  esc.addEventListener('pointercancel', suelta);

  /* ---------- 4 · artboard completo / pantalla real ---------- */
  /* El botón sólo aparece con los artboards claramente más altos que una
     pantalla (1280×1720, 390×1220…). Con 812×844 o 1280×940 recortar 20 o 120
     píxeles no enseña nada y sólo estorba. */
  var bModo = document.getElementById('modo');
  if (bModo && H > CORTE * 1.15) {
    bModo.hidden = false;
    bModo.addEventListener('click', function () {
      var real = app.dataset.modo === 'real';
      app.dataset.modo = real ? 'completo' : 'real';
      bModo.textContent = real ? 'Ver como pantalla real' : 'Ver el boceto completo';
      bModo.setAttribute('aria-pressed', String(!real));
      pantalla.scrollTop = 0;
      aplicar();
    });
  }

  /* ---------- 5 · cromo, ficha y ampliar ---------- */
  function alterna(boton, clase, textos) {
    if (!boton) return;
    boton.addEventListener('click', function () {
      var on = app.classList.toggle(clase);
      boton.setAttribute('aria-pressed', String(clase === 'sin-cromo' ? !on : on));
      if (textos) boton.textContent = on ? textos[1] : textos[0];
      aplicar();
    });
  }
  alterna(document.getElementById('cromo'), 'sin-cromo', null);
  alterna(document.getElementById('ficha'), 'sin-ficha', ['Ocultar ficha', 'Ver ficha']);

  var bAmp = document.getElementById('ampliar');
  var txtAmp = document.getElementById('ampliar-txt');
  var pedirPleno = col.requestFullscreen || col.webkitRequestFullscreen;
  var salirPleno = document.exitFullscreen || document.webkitExitFullscreen;

  function enPleno() {
    return !!(document.fullscreenElement || document.webkitFullscreenElement) ||
           app.classList.contains('pleno');
  }
  function pintaAmpliar() {
    if (txtAmp) txtAmp.textContent = enPleno() ? 'Reducir' : 'Ampliar';
    bAmp.setAttribute('aria-pressed', String(enPleno()));
    reprograma();
  }
  function respaldo() { app.classList.add('pleno'); pintaAmpliar(); }
  function cierraPleno() {
    if (document.fullscreenElement || document.webkitFullscreenElement) {
      try { salirPleno.call(document); } catch (_) {}
    }
    app.classList.remove('pleno');
    pintaAmpliar();
  }
  function alternaPleno() {
    if (enPleno()) { cierraPleno(); return; }
    if (pedirPleno) {
      var p;
      try { p = pedirPleno.call(col); } catch (_) { respaldo(); return; }
      if (p && p.catch) p.catch(respaldo); else setTimeout(function () {
        if (!document.fullscreenElement && !document.webkitFullscreenElement) respaldo();
      }, 120);
    } else respaldo();
  }
  bAmp.addEventListener('click', alternaPleno);
  document.addEventListener('fullscreenchange', pintaAmpliar);
  document.addEventListener('webkitfullscreenchange', pintaAmpliar);

  /* ---------- 6 · teclado ---------- */
  /* Las flechas NO cambian de pantalla: cuando el boceto está acercado son lo
     único razonable para desplazarse, y el escenario ya las atiende de forma
     nativa. Para saltar de boceto van [ y ]. */
  var anterior = null, siguiente = null;
  if (pie) {
    var a = pie.querySelector('a.mov[rel="prev"]'), b = pie.querySelector('a.mov[rel="next"]');
    if (a) { anterior = a.getAttribute('href'); a.title = 'Anterior  ( [ )'; }
    if (b) { siguiente = b.getAttribute('href'); b.title = 'Siguiente  ( ] )'; }
  }

  document.addEventListener('keydown', function (e) {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    var t = e.target;
    if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable)) return;
    var k = e.key;
    if (k === 'Escape') { if (app.classList.contains('pleno')) { cierraPleno(); e.preventDefault(); } return; }
    if (k === '+' || k === '=') { paso(1.25); }
    else if (k === '-' || k === '_') { paso(1 / 1.25); }
    else if (k === '0') { ajustarTodo(); }
    else if (k === '1') { tamanoReal(null, null); }
    else if (k === 'f' || k === 'F') { alternaPleno(); }
    else if (k === 'c' || k === 'C') { var bc = document.getElementById('cromo'); if (bc) bc.click(); }
    else if (k === 'p' || k === 'P') { var bf = document.getElementById('ficha'); if (bf) bf.click(); }
    else if (k === 'm' || k === 'M') { if (bModo && !bModo.hidden) bModo.click(); }
    else if (k === '[' && anterior) { location.href = anterior; }
    else if (k === ']' && siguiente) { location.href = siguiente; }
    else return;
    e.preventDefault();
  });

  /* ---------- 7 · «hay más» en la ficha ---------- */
  function marcaScroll() {
    if (!cuerpo || !panel) return;
    panel.classList.toggle('hay-mas',
      cuerpo.scrollHeight - cuerpo.clientHeight - cuerpo.scrollTop > 12);
  }
  if (cuerpo) {
    cuerpo.addEventListener('scroll', marcaScroll, { passive: true });
    if (window.ResizeObserver) new ResizeObserver(marcaScroll).observe(cuerpo);
  }

  /* ---------- 8 · recalcular ---------- */
  if (window.ResizeObserver) {
    new ResizeObserver(function () {
      var d = hueco();
      if (Math.abs(d.w - ultW) < 1 && Math.abs(d.h - ultH) < 1) return;
      reprograma();
    }).observe(esc);
  }
  window.addEventListener('resize', reprograma);
  window.addEventListener('orientationchange', reprograma);
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(reprograma).catch(function () {});
  }
  window.addEventListener('load', reprograma);

  aplicar();
  marcaScroll();
})();