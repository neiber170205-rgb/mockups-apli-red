# Maquetación · Sistema de pedidos para restaurantes

Bocetos de las pantallas del proyecto individual de **Desarrollo Básico de
Aplicaciones en Red** (Unidad 2 · FESC · Cúcuta).

## 👉 Ver los bocetos

**https://neiber170205-rgb.github.io/mockups-apli-red/**

42 pantallas agrupadas por quién las usa. Cada una abre a tamaño real.

| Rol | Qué hace | Cuántas |
|---|---|---|
| **Comensal** | Escanea el QR de la mesa y pide desde su celular. No inicia sesión | 4 |
| **Mesero** | Toma el pedido en su teléfono, con PIN y geocerca | 6 |
| **Cocina** | Pantalla táctil compartida. Fondo oscuro, se lee a un metro | 7 |
| **Caja** | Abre el turno, cobra y cuadra. Sin turno no se abre ni una mesa | 4 |
| **Acceso** | Entrada al sistema: producto → sede → persona | 3 |
| **Administración** | Listados y fichas, en pares | 18 |

## Qué hay en el repo

```
docs/            el sitio que publica GitHub Pages
  index.html       galería agrupada por rol
  bocetos/         una página por pantalla, abre sola en el navegador
  ENLACES.txt      los 42 enlaces, para pegar en el documento
mockups/         la fuente de los bocetos
  *.dc.html        cada pantalla como componente de diseño
  canvas.json      posición, agrupación y títulos en el lienzo
```

Las páginas de `docs/bocetos/` se **generan** desde `mockups/`: se les quita el
envoltorio del editor de diseño y se les añade una barra para volver al índice.
Editar la maquetación se hace en `mockups/`, nunca en `docs/`.

## Una pantalla no está

**Toma de pedido** (la del mesero armando el pedido) es un prototipo con lógica
—cuenta líneas, calcula el total, bloquea los platos agotados— y no funciona
como página estática. Vive solo en el lienzo de diseño.
