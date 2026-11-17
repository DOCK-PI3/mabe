# Mabe Betancor varios Trabajos y reformas · Las Palmas

Portfolio de pladur, pasta, pintura, Placostic y reformas generales. 

La web principal incluye filtros, visor de fotografías con teclado, vídeos sin sonido, carga progresiva de la galería y un comparador antes/después del lavadero. Se han retirado los enlaces de selección del diseño. `cuaderno.html` conserva el mismo contenido para que el enlace inicial siga funcionando. Las alternativas permanecen como referencia y la antigua página de selección se guarda en `web/propuestas.html`, fuera de la carpeta de publicación.


## Estructura

```text
web/dist/                 Web lista para servir y publicar
  index.html              Web principal: Cuaderno de obra
  cuaderno.html           Mismo contenido, enlace compatible
  cine.html               Alternativa conservada como referencia
  taller.html             Alternativa conservada como referencia
  config.js               Nombre, zona y contacto
  catalog.js              Catálogo compartido
  app.js                  Galería, visor, vídeo y comparador
  styles.css              Diseño y adaptación móvil
  assets/                 Solo las copias públicas optimizadas
web/tools/                Vista previa, comprobaciones y preparación
.github/workflows/        Publicación preparada para GitHub Pages
```
