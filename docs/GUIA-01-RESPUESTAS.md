# Guía de Autoaprendizaje 01 — Diseño, HTML5, XHTML y Metadatos

**Desarrollo Básico de Aplicaciones en Red** · Unidad 2 · 01 de septiembre de 2026
Neiber Danilo Araque Pacheco

**Proyecto:** sistema de pedidos para restaurante — *La Cava del Llano*

**Todo el trabajo está aquí:**
### https://neiber170205-rgb.github.io/mockups-apli-red

Desde esa página se llega a los 42 bocetos y a la primera versión construida.

---

## Paso 1 · Recupera tu proyecto

**¿Quién es el usuario principal?**
El comensal sentado en la mesa. Escanea el código QR del mantel y pide desde su
propio celular, sin instalar nada y sin crear cuenta.

**¿Qué necesidad debe atender la página?**
Ver qué hay para comer, cuánto cuesta y qué se acabó — sin tener que llamar al
mesero y esperar a que llegue.

**¿Qué debe encontrar primero ese usuario?**
La comida. Por eso los platos empiezan en el primer tercio de la pantalla: arriba
solo van el nombre del restaurante y el número de mesa, que ocupan 90 píxeles.

**¿Qué información es indispensable y cuál puede quedar en segundo plano?**
Indispensable: nombre del plato, precio y si está disponible. En segundo plano:
la descripción, la foto y de qué está hecho — eso se ve al tocar el plato, sin
salir de la carta.

**¿Cómo se relaciona esta página con el cliente web que identificaste?**
Es el cliente más difícil de los cuatro: un teléfono desconocido, con una versión
de navegador que no controlo y con el wifi del local saturado. Por eso la página
no descarga fuentes ni depende de JavaScript para leerse.

---

## Paso 2 · Diseña la maquetación antes del código

Boceto: en el enlace de arriba, **Comensal › 1 · Carta**.

Lo que pedía la lista, y dónde está:

| Elemento | En el boceto |
|---|---|
| Encabezado / identificación | Monograma, «La Cava del Llano», «Mesa 5 · Terraza» |
| Zona principal de contenido | Las cuatro secciones de la carta con sus platos |
| Navegación o enlaces | Los cuatro botones de sección, y cada plato abre su detalle |
| Información relevante | Precio, «Agotado», «Hoy sale sin ensalada» |
| Recurso multimedia | Hueco 16:10 por plato, hoy con el aviso «Todavía sin foto» |
| Pie de página | Aviso de precios y datos de la sede |

Antes de esta pantalla hice las otras 41 del sistema (mesero, cocina, caja y
administración), y por eso la carta salió tan directa: ya sabía qué información
llega hasta ella y cuál se queda en otras pantallas.

---

## Paso 3 · HTML5 y XHTML

Comparé sobre mi propio archivo, no en abstracto: qué tendría que cambiar de la
carta si la escribiera en XHTML.

| Aspecto | HTML5 | XHTML |
|---|---|---|
| Apertura | `<!doctype html>` y `<html lang="es">`, dos renglones | DOCTYPE largo con su DTD, `xmlns` y `xml:lang` |
| Etiquetas vacías | `<meta charset="utf-8">` sin barra final | Hay que cerrarlas: `<meta ... />`. En mi página son 8 |
| Atributos booleanos | `disabled` a secas | `disabled="disabled"`. Es el que deshabilita el botón del plato agotado |
| Etiquetas disponibles | `header`, `nav`, `main`, `section`, `article`, `figure`, `data` | XHTML 1.0 no las tiene: todo volvería a ser `<div class="...">` |
| El SVG de la foto | El navegador sabe que es SVG solo | Necesita `xmlns` o no dibuja nada — perdería los 12 iconos |
| Ante un error | Repara y sigue: la página se ve, quizá torcida | Si se sirve como XML, se detiene y muestra el error |

**¿Qué diferencias de sintaxis o estructura considero más importantes?**
Las dos últimas. La de las etiquetas es la que más se nota: mi carta se apoya
entera en `header`, `nav`, `main`, `section`, `article` y `figure`, y ninguna
existe en XHTML 1.0 — pasar a XHTML sería rehacer los 13 platos como `div`s y
perder justo la semántica del Paso 5. La del manejo de errores es la que más
importa en la práctica.

**¿Cuál enfoque resulta más conveniente para mi ejercicio y por qué?**
HTML5. Es una carta que se abre por QR con el wifi del local: si una tilde mal
codificada tumba la página entera, el comensal se queda sin carta. Que el
navegador repare y muestre la carta algo torcida es preferible a que no muestre
nada.

**Un matiz que casi todo el mundo dice mal:** esto no es «lenguaje viejo contra
nuevo». XHTML5 existe y es este mismo HTML5 escrito con sintaxis XML. Y el rigor
de XHTML solo actúa si el servidor lo entrega como `application/xhtml+xml`; una
página con DOCTYPE de XHTML servida como `text/html` se lee con las reglas de
HTML — parece estricta y no lo es.

---

## Paso 4 · Metadatos

**¿Qué información describen los metadatos?**
Datos sobre el documento que no se ven en la pantalla pero que otros programas
leen: la codificación, cómo debe verse en un móvil, si un buscador puede
indexarla, con qué color pintar la barra del navegador.

**¿Qué metadatos considero necesarios para mi proyecto?**
Solo dos son imprescindibles de verdad:

- **`charset="utf-8"`** — sin él, «Patacón» y «maíz» salen rotos.
- **`viewport`** — sin él el móvil simula una pantalla de escritorio y encoge
  todo. Y a propósito **no** lleva `user-scalable=no`: bloquear el zoom sobre un
  precio incumple las pautas de accesibilidad.

Los otros son útiles pero secundarios: `robots`, `referrer`, `theme-color`,
`description` y `author`.

**¿Qué diferencias encontré al trabajar con HTML5 y XHTML?**
En los metadatos, la sintaxis: en XHTML las ocho etiquetas del `<head>` tendrían
que cerrarse con `/>`. Y una de fondo: en HTML5 el `<meta charset>` fija la
codificación; parseado como XML se ignora y manda la cabecera HTTP.

**¿Qué metadatos incluiría y por qué?**
Los cinco de arriba, pero **revisando las justificaciones me di cuenta de que
tres estaban infladas**, y prefiero decirlo:

- **`robots: noindex`** no es un candado, es una petición. Google la respeta; un
  scraper no tiene por qué. Y para leerla, el bot ya se descargó la dirección con
  el token dentro. La defensa de verdad es que el token caduque al cerrar la
  cuenta — y eso va en el servidor, no en una etiqueta.
- **`referrer: no-referrer`** aporta menos de lo que parece: los navegadores de
  hoy ya mandan solo el origen hacia fuera por defecto. Lo dejo porque no cuesta
  nada, no porque resuelva algo.
- **`theme-color`** no es universal: Safari y Chrome la respetan, Firefox la
  ignora. Es una mejora, no una garantía.

Y hay una **contradicción** que también dejo anotada: escribí `description` para
que un buscador la muestre y tres líneas más abajo le prohíbo indexar la página.
La mantengo por si algún día la carta se publica sin token, pero hoy está inerte.

---

## Paso 5 · Define la estructura de tu página

| Sección | Contenido previsto | Propósito para el usuario |
|---|---|---|
| `header` | Nombre del restaurante, sede, mesa y estado de la sesión | Confirmar que escaneó el QR correcto — la mesa es la única pista |
| `nav` | Enlaces a las cuatro secciones de la carta | Llegar a los postres sin recorrer 13 platos |
| `main` | Las cuatro secciones | Es la carta |
| `section` | Un grupo de platos con su título | Agrupar como agrupa una carta de papel |
| `article` | Un plato: foto, nombre, descripción, precio, botón | Es la unidad que se decide y se pide |
| `figure` | Hueco de la foto con su pie | Ver el plato antes de pedirlo |
| Barra fija | Cuántos platos van y cuánto suman | Saber la cuenta antes de que llegue |
| `footer` | Aviso de precios y datos de la sede | Resolver la duda de «¿esto lleva impuestos?» |

---

## Paso 6 · Construye la primera versión

Página: en el enlace de arriba, **Primera página construida**.

- [x] La estructura responde al boceto
- [x] El contenido corresponde al proyecto — los 13 platos y sus precios reales
- [x] La organización permite identificar la información principal
- [x] Incluye los metadatos que justifiqué
- [x] Incorpora los enlaces y recursos previstos
- [x] El documento puede abrirse en un navegador

Dos archivos: `index.html` con la estructura y `estilos.css` con la presentación.
Separados a propósito — si mañana cambia el color de la marca, no se toca el HTML.

---

## Paso 7 · Comprueba lo que construiste

**¿La página quedó organizada como la diseñaste?**
Sí. Cambió una cosa: en el boceto los platos van en una columna, y en pantallas
anchas los puse en dos. Una fila de 900 píxeles de ancho no se lee.

**¿El contenido principal es fácil de identificar?**
Sí. Los platos ocupan casi toda la pantalla y el precio va en negrita alineado
con el nombre.

**¿La estructura responde a la necesidad del usuario?**
Sí, y en dos detalles que salieron del negocio: el plato agotado **no se
esconde** —si desaparece, el comensal lo busca y termina preguntando por él— y el
que perdió un ingrediente avisa *antes* de pedirse, no cuando llega a la mesa.

**¿Encontraste algún problema de sintaxis o estructura?**
Dos, revisando:

1. **No había `<h1>`.** El nombre del restaurante estaba en un `<p>`, así que la
   jerarquía arrancaba en `<h2>`. Corregido.
2. **El botón del pedido enlazaba a `#`**, un enlace muerto. Ahora va a la
   pantalla siguiente del recorrido.

**¿Qué cambiarías en una segunda versión?**
Las fotos reales, que hoy son un hueco. Y el botón «Añadir» todavía no hace nada:
falta el JavaScript que arme el pedido y lo mande al servidor.

---

## Control de calidad inicial

Ocho criterios para revisar las próximas páginas:

1. **Valida sin errores** en el validador del W3C.
2. **Tiene un solo `<h1>`** y la jerarquía de encabezados no salta niveles.
3. **Se entiende sin CSS** — si se desactiva la hoja de estilos, el orden del
   documento sigue teniendo sentido.
4. **Ningún objetivo táctil mide menos de 44 píxeles.** Se toca con el dedo.
5. **Contraste mínimo 4.5:1** en el texto. *(Ya encontré uno que no cumple: el
   ámbar de los avisos está en 4.20:1 y hay que corregirlo.)*
6. **Se recorre entera con el tabulador**, y se ve dónde está el foco.
7. **Nada esencial depende de JavaScript**: sin él, la carta se lee.
8. **Abre en menos de 2 segundos** con la conexión del local.

---

## Conecta con la arquitectura web

> Usuario → Cliente → Solicitud → Servidor → Respuesta

**¿Qué parte de tu página responde directamente a una necesidad del usuario?**
La lista de platos con su precio y su disponibilidad. Todo lo demás está para
llegar hasta ahí.

**¿Qué papel cumple el cliente web al mostrar tu página?**
Interpreta el HTML y el CSS y los pinta. No decide nada: no calcula totales, no
sabe si un plato se acabó y no comprueba si el comensal está en el restaurante.
Todo eso lo dice el servidor, porque el celular del cliente no es de confianza.

**¿Qué información podría solicitar el usuario posteriormente?**
El detalle de un plato, agregarlo al pedido, enviarlo y seguir cómo va en cocina.

**¿Qué respuesta esperaría recibir?**
JSON sobre HTTPS. Para el seguimiento, la pantalla pregunta cada dos segundos
diciendo hasta dónde había leído; si no hay novedad, la respuesta es mínima.
HTTPS no es opcional: los navegadores solo entregan la ubicación en conexiones
seguras, y sin ubicación no funciona la regla de que solo se pide desde el local.

---

## Producto a entregar

1. **Boceto** — Comensal › 1 · Carta
2. **Comparación HTML5 vs XHTML** — Paso 3
3. **Análisis de metadatos** — Paso 4
4. **Primera página construida** — Primera página construida
5. **Comprobación y control de calidad** — Paso 7 y la lista de ocho criterios
6. **Justificación de decisiones** — repartida en cada paso

---

## Lista de verificación

- [x] Partí de mi proyecto individual
- [x] Diseñé la maquetación antes de programar
- [x] Comparé HTML5 y XHTML
- [x] Diferencié sus características de sintaxis relevantes
- [x] Analicé los metadatos
- [x] Justifiqué qué metadatos utilizaré
- [x] Construí una primera versión HTML
- [x] Comprobé la página en el navegador
- [x] Relacioné el resultado con las necesidades del usuario y el proyecto
