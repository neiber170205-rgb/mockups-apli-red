# -*- coding: utf-8 -*-
"""Regenera docs/ a partir de mockups/ + herramientas/descripciones.json.

docs/bocetos es DERIVADO: hay que correr esto antes de cada commit, o la
galería publicada se queda vieja.
    python3 herramientas/generar_docs.py
"""
import html, json, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from bocetos_comun import RAIZ, DOCS, piezas, slug, dispositivo, lienzo

HERR = RAIZ / 'herramientas'
PLANTILLA = (HERR / 'plantilla_visor.html').read_text(encoding='utf-8')
DESC = json.loads((HERR / 'descripciones.json').read_text(encoding='utf-8'))

NOMBRE_TIPO = {'movil': 'un celular', 'escritorio': 'un computador', 'panel': 'un celular · dos estados'}

DESC_GRUPO = {
    'plataforma': 'El nivel de encima: quién es cliente de la plataforma y qué paga. Solo lo ve el operador del SaaS.',
    'comensal': 'Lo que ve quien se sienta a la mesa y escanea el QR. Sin instalar nada y sin cuenta.',
    'mesero': 'El teléfono del mesero: tomar el pedido, mirar un plato, revisar y enviar a cocina.',
    'cocina': 'La pantalla del pase, pensada para verse de lejos y tocarse con las manos ocupadas.',
    'caja': 'Abrir el turno, cobrar la mesa, cuadrar y cerrar.',
    'acceso': 'Entrar al sistema: por contraseña, por sede y el acceso rápido del mesero.',
    'admin': 'La configuración del restaurante: salón, carta, cocina, personas y los informes.',
}


def esc(t):
    return html.escape(t or '', quote=True)


def mov(a, dir_):
    if not a:
        return ''
    return ('<a class="mov" rel="%s" href="%s.html">'
            '<span class="mov-dir">%s</span>'
            '<span class="mov-tit">%s</span></a>') % (
        'prev' if dir_ == 'ant' else 'next', slug(a['title']),
        'Anterior' if dir_ == 'ant' else 'Siguiente', esc(a['title']))


def pagina(a, ant, sig):
    css, cuerpo = piezas(a['file'])
    d = DESC.get(a['file'])
    if d is None:
        raise SystemExit('falta la descripción de %s' % a['file'])
    tipo = dispositivo(a)
    puntos = "".join('<li>%s</li>' % esc(p) for p in d['puntos'])
    nota = ('<h2 class="rotulo">Nota</h2><p>%s</p>' % esc(d['nota'])) if d.get('nota', '').strip() else ''

    cuerpo_html = PLANTILLA
    for k, v in [('ES_MOVIL', tipo), ('ANCHO', str(a['w'])), ('ALTO', str(a['h'])),
                 ('TITULO', esc(a['title'])), ('GRUPO', esc(PAGINAS[a['page']])),
                 ('QUIEN', esc(d['quien'])), ('RESUMEN', esc(d['resumen'])),
                 ('PUNTOS', puntos), ('NOTA', nota),
                 ('ANT', mov(ant, 'ant')), ('SIG', mov(sig, 'sig')),
                 ('BOCETO', cuerpo)]:
        cuerpo_html = cuerpo_html.replace('{{%s}}' % k, v)

    return """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(tit)s &middot; Pedidos</title>
<meta name="description" content="%(res)s">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;family=JetBrains+Mono:wght@400;500&amp;display=swap">
<link rel="stylesheet" href="visor.css">
<style>
/* --- CSS del boceto, acotado a .bo por acota_css() --- */
%(css)s
</style>
</head>
<body>
%(cuerpo)s
<script src="visor.js"></script>
</body>
</html>
""" % {'tit': esc(a['title']), 'res': esc(d['resumen']), 'css': css, 'cuerpo': cuerpo_html}


def galeria(cv, orden):
    ind = (DOCS / 'index.html').read_text(encoding='utf-8')
    sec = []
    for p in cv['pages']:
        de = [a for a in orden if a['page'] == p['id']]
        if not de:
            continue
        idsec = 'administracion' if p['id'] == 'admin' else p['id']
        enlaces = "\n".join(
            '        <a class="b" href="bocetos/%s.html"><span class="n">%s</span>'
            '<span class="q">%s</span></a>' % (slug(a['title']), esc(a['title']),
                                               esc(DESC[a['file']]['quien']))
            for a in de)
        sec.append("""    <section id="%s">
      <h2>%s <span class="c">%d</span></h2>
      <p class="d">%s</p>
      <div class="rej">
%s
      </div>
    </section>""" % (idsec, esc(p['name']), len(de), DESC_GRUPO.get(p['id'], ''), enlaces))
    ini = ind.index('    <section id=')
    fin = ind.rindex('</section>') + len('</section>')
    ind = ind[:ini] + "\n".join(sec) + ind[fin:]
    ind = re.sub(r'Bocetos de las \d+ pantallas', 'Bocetos de las %d pantallas' % len(orden), ind)
    # la tarjeta de la galería ahora lleva dos líneas: título y quién la usa
    if '.b .q{' not in ind:
        ind = ind.replace(
            "  .b:hover{",
            "  .b{flex-direction:column;align-items:flex-start;gap:3px;justify-content:center}\n"
            "  .b .q{font-size:11.5px;font-weight:500;color:var(--fg2)}\n"
            "  .b:hover{")
    (DOCS / 'index.html').write_text(ind, encoding='utf-8')


cv = lienzo()
PAGINAS = {p['id']: p['name'] for p in cv['pages']}
orden = cv['artboards']
for i, a in enumerate(orden):
    ant = orden[i - 1] if i > 0 else None
    sig = orden[i + 1] if i < len(orden) - 1 else None
    (DOCS / 'bocetos' / (slug(a['title']) + '.html')).write_text(pagina(a, ant, sig), encoding='utf-8')
galeria(cv, orden)

vivos = {slug(a['title']) + '.html' for a in orden} | {'visor.css', 'visor.js'}
for f in (DOCS / 'bocetos').iterdir():
    if f.name not in vivos:
        f.unlink()
        print("  borrado (ya no existe):", f.name)
print("bocetos: %d · galería actualizada" % len(orden))
