# Maquetación · Sistema de pedidos para restaurantes

Bocetos de las pantallas del proyecto individual de **Desarrollo Básico de
Aplicaciones en Red** (Unidad 2 · FESC · Cúcuta).

## 👉 Ver los bocetos

**https://neiber170205-rgb.github.io/mockups-apli-red/**

54 pantallas agrupadas por quién las usa. Cada boceto se abre dentro de un
simulador —iPhone 17 Pro si es de celular, ventana de escritorio si no— con la
explicación de la pantalla al lado, zoom y un botón para ampliar.

| Rol | Qué hace | Cuántas |
|---|---|---|
| **Plataforma** | El operador del SaaS: quién es cliente y qué paga | 6 |
| **Comensal** | Escanea el QR de la mesa y pide desde su celular. No inicia sesión | 4 |
| **Mesero** | Toma el pedido en su teléfono, con PIN y geocerca | 7 |
| **Cocina** | Pantalla táctil compartida. Fondo oscuro, se lee a un metro | 7 |
| **Caja** | Abre el turno, cobra y cuadra. Sin turno no se abre ni una mesa | 4 |
| **Acceso** | Entrada al sistema: producto → sede → persona | 3 |
| **Administración** | Listados y fichas, en pares | 23 |

## Qué hay en el repo

```
docs/            el sitio que publica GitHub Pages  ← GENERADO
  index.html       galería agrupada por rol
  carta/           la primera página construida en HTML5
  bocetos/         una página por pantalla, con simulador y descripción
    visor.css        el visor: simulador, zoom, ampliar, panel
    visor.js         la escala, el zoom y los atajos
mockups/         la FUENTE de los bocetos
  *.dc.html        cada pantalla como componente de diseño
  canvas.json      tamaño, posición, agrupación y títulos
herramientas/    lo que convierte mockups/ en docs/
  generar_docs.py       regenera las 54 páginas y la galería
  bocetos_comun.py      acota el CSS del boceto a .bo y clasifica el dispositivo
  descripciones.json    qué hace cada pantalla, para el panel de la derecha
  plantilla_visor.html  el esqueleto de la página
  verificar_visor.py    comprueba que ninguna página desborde la ventana
  verificar_conducta.py aprieta zoom, cromo, ampliar… y revisa las invariantes
```

`docs/bocetos/` es **derivado**. La maquetación se edita en `mockups/`, nunca en
`docs/`, y antes de cada commit hay que correr:

```bash
python3 herramientas/generar_docs.py
```
