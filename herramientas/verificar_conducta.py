# -*- coding: utf-8 -*-
"""Aprieta los botones del visor y comprueba que las invariantes aguantan:
sin scroll de página, caja del boceto = ancho×escala por alto×escala, y la
misma escala en los dos ejes. Cubre zoom, 1:1, ajustar, cromo, ocultar ficha,
«pantalla real», ampliar (respaldo .pleno) y Escape."""
import json, pathlib, sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SALIDA = sys.argv[1]
TAM = tuple(int(x) for x in (sys.argv[2] if len(sys.argv) > 2 else '1600x900').split('x'))

BOC = RAIZ / 'docs' / 'bocetos'
CSS = (BOC / 'visor.css').read_text(encoding='utf-8')
JS = (BOC / 'visor.js').read_text(encoding='utf-8')


def enlinea(h):
    h = h.replace('<link rel="stylesheet" href="visor.css">', '<style>' + CSS + '</style>')
    return h.replace('<script src="visor.js"></script>', '<script>' + JS + '</script>')


datos = [{"n": p.name, "html": enlinea(p.read_text(encoding='utf-8'))}
         for p in sorted(BOC.glob('*.html'))]

MEDIDOR = r"""
(function(){
  var D = JSON.parse(document.getElementById('datos').textContent);
  var T = JSON.parse(document.getElementById('tam').textContent);
  var out = [], n = 0;

  function revisa(d, etiqueta, nombre){
    var l = [], de = d.documentElement;
    if (de.scrollHeight - de.clientHeight > 2) l.push('scroll de página ' + (de.scrollHeight - de.clientHeight));
    if (de.scrollWidth - de.clientWidth > 2) l.push('scroll horizontal ' + (de.scrollWidth - de.clientWidth));
    var bo = d.getElementById('bo');
    if (!bo) { l.push('sin .bo'); }
    else {
      var cs = d.defaultView.getComputedStyle(bo);
      var m = cs.transform.match(/matrix\(([-\d.]+),\s*([-\d.]+),\s*([-\d.]+),\s*([-\d.]+)/);
      if (!m) l.push('sin transform');
      else {
        var sx = parseFloat(m[1]), sy = parseFloat(m[4]);
        if (Math.abs(sx - sy) > 0.001) l.push('escala deformada ' + sx.toFixed(3) + '/' + sy.toFixed(3));
        if (!(sx > 0.02)) l.push('escala ' + sx);
        var caja = bo.parentElement;
        var app = d.getElementById('app');
        var real = app && app.dataset.modo === 'real';
        // En «pantalla real» la caja se RECORTA a propósito al alto de una
        // pantalla de verdad y el boceto se desliza dentro: ahí el alto
        // esperado no es alto×escala, es min(alto, corte)×escala.
        var corte = (app && app.dataset.tipo === 'movil') ? 874 : 820;
        var altoEsp = real ? Math.min(bo.offsetHeight, corte) : bo.offsetHeight;
        var dw = Math.abs(caja.clientWidth - bo.offsetWidth * sx);
        var dh = Math.abs(caja.clientHeight - altoEsp * sy);
        if (dw > 2 || dh > 2) l.push('caja mal dimensionada ' + Math.round(dw) + 'x' + Math.round(dh));
        if (real) {
          var cc = d.defaultView.getComputedStyle(caja);
          if (cc.overflowY !== 'auto' && cc.overflowY !== 'scroll') l.push('recortada SIN scroll');
          if (caja.scrollHeight - caja.clientHeight < 2) l.push('recortada pero no hay nada que deslizar');
        }
      }
    }
    if (l.length) out.push(nombre + '  [' + etiqueta + ']\n      ' + l.join('\n      '));
  }

  function pulsa(d, id){ var b = d.getElementById(id); if (b && !b.hidden) { b.click(); return true; } return false; }

  D.forEach(function(a){
    var fr = document.createElement('iframe');
    fr.style.cssText = 'position:absolute;left:-99999px;top:0;border:0;width:'+T[0]+'px;height:'+T[1]+'px';
    document.body.appendChild(fr);
    var d = fr.contentDocument;
    d.open(); d.write(a.html); d.close();
    n++;
    revisa(d, 'inicio', a.n);
    pulsa(d, 'mas');  revisa(d, 'zoom +1', a.n);
    pulsa(d, 'mas');  revisa(d, 'zoom +2', a.n);
    pulsa(d, 'uno');  revisa(d, '1:1', a.n);
    pulsa(d, 'pct');  revisa(d, 'ajustar', a.n);
    pulsa(d, 'cromo'); revisa(d, 'sin cromo', a.n);
    pulsa(d, 'cromo'); revisa(d, 'cromo otra vez', a.n);
    pulsa(d, 'ficha'); revisa(d, 'sin ficha', a.n);
    pulsa(d, 'ficha'); revisa(d, 'ficha otra vez', a.n);
    if (pulsa(d, 'modo')) { revisa(d, 'pantalla real', a.n); pulsa(d, 'modo'); revisa(d, 'completo otra vez', a.n); }
    var amp = d.getElementById('ampliar');
    if (amp) {
      amp.click(); revisa(d, 'ampliado', a.n);
      d.dispatchEvent(new d.defaultView.KeyboardEvent('keydown', {key:'Escape', bubbles:true}));
      revisa(d, 'tras Escape', a.n);
      if (d.getElementById('app').classList.contains('pleno')) out.push(a.n + '  [Escape no cerró el ampliado]');
    }
    fr.remove();
  });

  document.documentElement.innerHTML =
    '<body style="margin:0;background:#fff"><pre style="font:12px/16px monospace;color:#000;padding:10px;margin:0">'
    + 'PÁGINAS ' + n + '   FALLOS ' + out.length + '\n\n'
    + (out.slice(0,30).join('\n') || '(ninguno)') + '</pre></body>';
})();
"""

doc = ('<!doctype html><html><head><meta charset="utf-8"></head><body style="margin:0">'
       '<script id="datos" type="application/json">' + json.dumps(datos, ensure_ascii=False).replace('</script', '<\\/script') + '</script>'
       '<script id="tam" type="application/json">' + json.dumps(list(TAM)) + '</script>'
       '<script>' + MEDIDOR + '</script></body></html>')
pathlib.Path(SALIDA).write_text(doc, encoding='utf-8')
print("páginas: %d · ventana %dx%d -> %s" % (len(datos), TAM[0], TAM[1], SALIDA))
