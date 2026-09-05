# -*- coding: utf-8 -*-
"""Comprueba las páginas de docs/bocetos en varios tamaños de ventana:
que NO haya scroll de página, que el boceto quepa dentro de su marco, que el
panel derecho scrollee por dentro y que la escala sea la misma en los dos ejes.

Uso:  python3 herramientas/verificar_visor.py <ancho>x<alto> [más tamaños]
Escribe un HTML en el scratchpad; hay que abrirlo con firefox --screenshot."""
import json, pathlib, sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SALIDA = sys.argv[1]
TAMANOS = [tuple(int(x) for x in t.split('x')) for t in sys.argv[2:]] or [(1920, 1080)]

BOC = RAIZ / 'docs' / 'bocetos'
CSS = (BOC / 'visor.css').read_text(encoding='utf-8')
JS = (BOC / 'visor.js').read_text(encoding='utf-8')

def enlinea(h):
    # El iframe se escribe con document.write, así que su URL base es
    # about:blank y las rutas relativas no resuelven: se meten en línea.
    h = h.replace('<link rel="stylesheet" href="visor.css">', '<style>' + CSS + '</style>')
    h = h.replace('<script src="visor.js"></script>', '<script>' + JS + '</script>')
    return h

paginas = sorted(x for x in BOC.glob('*.html'))
datos = [{"n": p.name, "html": enlinea(p.read_text(encoding='utf-8'))} for p in paginas]

MEDIDOR = r"""
(function(){
  var D = JSON.parse(document.getElementById('datos').textContent);
  var T = JSON.parse(document.getElementById('tam').textContent);
  var out = [], n = 0;
  T.forEach(function(t){
    D.forEach(function(a){
      var fr = document.createElement('iframe');
      fr.style.cssText = 'position:absolute;left:-99999px;top:0;border:0;width:'+t[0]+'px;height:'+t[1]+'px';
      document.body.appendChild(fr);
      var d = fr.contentDocument;
      d.open(); d.write(a.html); d.close();
      n++;
      var l = [];
      var de = d.documentElement, bd = d.body;
      if (de.scrollHeight - de.clientHeight > 2) l.push('SCROLL DE PAGINA ' + (de.scrollHeight - de.clientHeight));
      if (de.scrollWidth - de.clientWidth > 2) l.push('SCROLL HORIZONTAL ' + (de.scrollWidth - de.clientWidth));
      if (bd.scrollHeight - bd.clientHeight > 2) l.push('BODY DESBORDA ' + (bd.scrollHeight - bd.clientHeight));
      var bo = d.querySelector('.bo');
      if (!bo) l.push('sin .bo');
      else {
        var cs = d.defaultView.getComputedStyle(bo);
        var m = cs.transform.match(/matrix\(([-\d.]+),\s*([-\d.]+),\s*([-\d.]+),\s*([-\d.]+)/);
        if (m) {
          var sx = parseFloat(m[1]), sy = parseFloat(m[4]);
          if (Math.abs(sx - sy) > 0.001) l.push('ESCALA DEFORMADA ' + sx.toFixed(3) + '/' + sy.toFixed(3));
          if (sx <= 0.02) l.push('ESCALA CASI CERO ' + sx.toFixed(3));
          var caja = bo.parentElement;
          var espW = Math.abs(caja.clientWidth - bo.offsetWidth * sx);
          var espH = Math.abs(caja.clientHeight - bo.offsetHeight * sy);
          if (espW > 2 || espH > 2) l.push('CAJA MAL DIMENSIONADA ' + Math.round(espW) + 'x' + Math.round(espH));
        } else l.push('sin transform');
      }
      var pan = d.querySelector('.panel, aside');
      if (pan && pan.scrollHeight - pan.clientHeight > 2 && d.defaultView.getComputedStyle(pan).overflowY === 'visible')
        l.push('PANEL DESBORDA SIN SCROLL');
      if (l.length) out.push(t[0] + 'x' + t[1] + '  ' + a.n + '\n      ' + l.join('\n      '));
      fr.remove();
    });
  });
  document.documentElement.innerHTML =
    '<body style="margin:0;background:#fff"><pre style="font:12px/16px monospace;color:#000;padding:10px;margin:0">'
    + 'COMPROBACIONES ' + n + '   CON PROBLEMA ' + out.length + '\n\n'
    + (out.slice(0,40).join('\n') || '(ninguno)') + '</pre></body>';
})();
"""

doc = ('<!doctype html><html><head><meta charset="utf-8"></head><body style="margin:0">'
       '<script id="datos" type="application/json">' + json.dumps(datos, ensure_ascii=False).replace('</script', '<\\/script') + '</script>'
       '<script id="tam" type="application/json">' + json.dumps(TAMANOS) + '</script>'
       '<script>' + MEDIDOR + '</script></body></html>')
pathlib.Path(SALIDA).write_text(doc, encoding='utf-8')
print("páginas: %d · tamaños: %s -> %s" % (len(datos), TAMANOS, SALIDA))
