# -*- coding: utf-8 -*-
"""Piezas compartidas para generar docs/ a partir de mockups/."""
import json, pathlib, re, unicodedata

RAIZ = pathlib.Path(__file__).resolve().parent.parent
MOCK = RAIZ / 'mockups'
DOCS = RAIZ / 'docs'

# Los siete selectores GLOBALES que traen los helmets. Todo lo demás ya va
# por clase (.kds, .lg, .pin, .le, .th-hija) y vive dentro del boceto.
# Sin esto, `body{background:var(--canvas)}` y `a{color:…}` del boceto pisan
# la página de la galería, y `:root` mete sus 26 variables en el documento.
GLOBALES = {
    ':root':                   '.bo',
    '*':                       '.bo *',
    'body':                    '.bo',
    'a':                       '.bo a',
    'a:hover':                 '.bo a:hover',
    '::-webkit-scrollbar':     '.bo ::-webkit-scrollbar',
    '::-webkit-scrollbar-thumb': '.bo ::-webkit-scrollbar-thumb',
}


def acota_css(css):
    """Reescribe los selectores de primer nivel para que nada del boceto se
    escape del contenedor .bo. Solo toca profundidad 0."""
    sal, prof, sel, i = [], 0, '', 0
    for ch in css:
        if ch == '{':
            if prof == 0:
                s = sel.strip()
                sal.append(('\n' if sal else '') + GLOBALES.get(s, s) + '{')
                sel = ''
            else:
                sal.append(ch)
            prof += 1
        elif ch == '}':
            prof -= 1
            sal.append(ch)
        elif prof == 0:
            sel += ch
        else:
            sal.append(ch)
    return "".join(sal)


def piezas(archivo):
    """Devuelve (css_acotado, cuerpo) de un .dc.html."""
    s = (MOCK / archivo).read_text(encoding='utf-8')
    helmet = s[s.index('<helmet>') + 8:s.index('</helmet>')]
    css = "\n".join(re.findall(r'<style>(.*?)</style>', helmet, re.S))
    cuerpo = s[s.index('</helmet>') + 9:]
    cuerpo = cuerpo[:cuerpo.index('</x-dc>')].strip()
    return acota_css(css), cuerpo


def slug(t):
    t = t.replace('›', ' ').replace('·', ' ')
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-zA-Z0-9]+', '-', t).strip('-').lower()


def dispositivo(a):
    if a['w'] <= 430:
        return 'movil'
    if a['w'] < 1000:
        return 'panel'     # Geocerca: dos pantallas de celular lado a lado
    return 'escritorio'


def lienzo():
    return json.loads((MOCK / 'canvas.json').read_text(encoding='utf-8'))
