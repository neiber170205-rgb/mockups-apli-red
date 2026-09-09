# -*- coding: utf-8 -*-
"""Compila docs/informe/informe.html a PDF y DOCX con formato APA.

Por qué existe: LibreOffice en modo headless NO carga las imágenes que el HTML
referencia por ruta —las descarta sin avisar y deja el hueco en blanco—, así que
antes de convertir hay que incrustarlas como data URI. El HTML de origen se deja
con rutas normales para poder editarlo y verlo en el navegador.

    python3 herramientas/generar_informe.py
"""
import base64, mimetypes, pathlib, re, shutil, subprocess, sys, tempfile

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DIR = RAIZ / 'docs' / 'informe'
FUENTE = DIR / 'informe.html'


def incrusta(html, base):
    def _sub(m):
        ruta = base / m.group(1)
        if not ruta.exists():
            sys.exit('falta la imagen: %s' % ruta)
        tipo = mimetypes.guess_type(ruta.name)[0] or 'image/png'
        b64 = base64.b64encode(ruta.read_bytes()).decode()
        return 'src="data:%s;base64,%s"' % (tipo, b64)
    return re.sub(r'src="([^":]+\.(?:png|jpg|jpeg|gif))"', _sub, html)


html = incrusta(FUENTE.read_text(encoding='utf-8'), DIR)
tmp = pathlib.Path(tempfile.mkdtemp())
(tmp / 'informe.html').write_text(html, encoding='utf-8')

for destino in ('pdf', 'docx:MS Word 2007 XML'):
    subprocess.run(['soffice', '--headless', '--convert-to', destino,
                    '--outdir', str(tmp), str(tmp / 'informe.html')],
                   capture_output=True, timeout=300)

for ext in ('pdf', 'docx'):
    origen = tmp / ('informe.%s' % ext)
    if not origen.exists():
        sys.exit('LibreOffice no produjo el %s' % ext)
    shutil.copy(origen, DIR / ('informe.%s' % ext))
    print('  %-16s %d KB' % ('informe.' + ext, origen.stat().st_size // 1024))

shutil.rmtree(tmp, ignore_errors=True)
