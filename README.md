# Mabe Betancor varios Trabajos y reformas · Las Palmas

Portfolio de pladur, pasta, pintura, Placostic y reformas generales. El diseño elegido es **Cuaderno de obra**, ya aplicado a la portada principal `web/dist/index.html`.

| Propuesta | Archivo | Dirección visual |
| --- | --- | --- |
| Cuaderno de obra | `web/dist/cuaderno.html` | Azul de plano, fotografías superpuestas y archivo de obra |
| Obra en escena | `web/dist/cine.html` | Fotografía panorámica, fondo oscuro y galería cinematográfica |
| Materia y oficio | `web/dist/taller.html` | Muestrario violeta y naranja, piezas curvas y composiciones asimétricas |

La web principal incluye filtros, visor de fotografías con teclado, vídeos sin sonido, carga progresiva de la galería y un comparador antes/después del lavadero. Se han retirado los enlaces de selección del diseño. `cuaderno.html` conserva el mismo contenido para que el enlace inicial siga funcionando. Las alternativas permanecen como referencia y la antigua página de selección se guarda en `web/propuestas.html`, fuera de la carpeta de publicación.

## Abrir la web

Puedes abrir `web/dist/index.html` directamente en tu navegador. Para una vista previa con reproducción y búsqueda dentro de los vídeos:

```powershell
npm run dev
```

Abre la dirección que aparece: `http://127.0.0.1:4173/`. No hay paquetes que instalar. Solo necesitas Node.js 18 o posterior. `npm run check` comprueba el catálogo y las rutas locales.

## Datos pendientes

El nombre confirmado es **Mabe Betancor varios Trabajos y reformas**. La zona confirmada es **Las Palmas**. Todavía faltan los datos de contacto. Edita `web/dist/config.js`; los enlaces de WhatsApp, teléfono y correo solo aparecen al rellenarlos. Introduce WhatsApp con prefijo internacional, por ejemplo `34` seguido del número real. No se han inventado teléfonos, testimonios, clientes ni direcciones.

Después de cambiar el nombre, la zona, los estilos o el catálogo, ejecuta `web/tools/create_pages.py` con Python. Lee la identidad desde `config.js`, regenera las páginas y actualiza las versiones de los archivos para evitar que el navegador muestre contenido antiguo. Mantiene Cuaderno de obra como portada principal.

## Material incorporado

- 268 fotografías, optimizadas a WebP (máximo 1800 píxeles), sin metadatos EXIF. Incluyen las 229 fotos de trabajos recuperadas el 17 de noviembre de 2026.
- 32 vídeos completos, convertidos a MP4 H.264, máximo 960 píxeles y 25 fps, **sin pista de audio**, con miniaturas independientes y carga al abrir el visor. Incluyen los 16 vídeos recuperados en esta actualización.
- Los cuatro documentos excluidos son `IMG20250825163127.jpg`, `IMG20250825163203.jpg`, `IMG20250825163219.jpg` y `IMG20250825163226.jpg`.
- También se dejó fuera `IMG20250928233359.jpg`, una fotografía nocturna de la fachada de un hotel que no muestra un trabajo identificable.
- Se excluyó `20210416_224026.jpg`, una fotografía personal de una mascota, y se mantuvo fuera el PDF de documentación.
- Tus originales permanecen intactos en su carpeta. No forman parte de este proyecto.
- Las fotos y vídeos públicos ocupan unos 216 MB (206 MiB), más las miniaturas. Ningún archivo supera 100 MB.

Se compararon huellas SHA-256 de archivos, píxeles de fotografías y contenido de vídeo, además de revisar las tomas visualmente parecidas. No se encontraron duplicados exactos entre las incorporaciones; se conservaron las tomas distintas de una misma obra. `web/media-manifest.json` registra las huellas de los archivos y `npm run check` comprueba que no haya IDs o contenidos repetidos. Los 32 MP4 se verificaron sin pistas de audio con `web/tools/verify_videos.py`. El sonido se eliminó de las copias con `-map 0:v:0 -an`; el reproductor no utiliza el atributo `muted` como sustituto de esa eliminación.

Las categorías y los títulos se describen por el contenido visible de las fotos y los vídeos. Conviene confirmar qué obras y acabados quieres destacar al elegir el diseño definitivo. La galería no atribuye un producto concreto a una foto cuando no se puede verificar visualmente.

## Añadir lo que recuperes del otro móvil

1. Revisa el material y separa documentos o imágenes que no quieras publicar.
2. Guarda copias optimizadas en `web/dist/assets/images/` o `web/dist/assets/videos/`. Para vídeo, elimina la pista de audio y crea una miniatura WebP con el mismo nombre base.
3. Añade la entrada en `web/dist/catalog.js`, con `id`, `type` (`image` o `video`), `category` (`Pladur`, `Acabados` o `Reformas`), `title`, `src` y `poster`. Conserva la huella `sourceSha256` cuando esté disponible.
4. Ejecuta `node web/tools/update-manifest.mjs`, regenera las páginas con `web/tools/create_pages.py`, ejecuta `npm run check` y verifica los vídeos con `web/tools/verify_videos.py` antes de revisar la vista previa.

Los scripts de preparación en `web/tools/` son auxiliares: requieren Python, Pillow e imageio-ffmpeg y usan la carpeta original de esta sesión. No se necesitan para abrir ni publicar la web. El conversor local y los archivos de revisión están excluidos de Git mediante `.gitignore`.

## Preparado para GitHub Pages

El proyecto no depende de un servicio de pago, una base de datos ni un proceso de compilación. Todas las rutas son relativas, también válidas en `usuario.github.io/nombre-del-repositorio/`.

Cuando completes los datos de contacto:

1. Revisa la web principal en `web/dist/index.html`. El diseño elegido ya está aplicado y los enlaces de comparación se han retirado.
2. El proyecto ya tiene un repositorio Git local con rama `main`. Crea el repositorio remoto en GitHub y sube el proyecto. No subas la carpeta del móvil, `.tools` ni `web/_private`.
3. En **Settings → Pages → Build and deployment**, selecciona **GitHub Actions**.
4. El flujo `.github/workflows/pages.yml` publica **únicamente `web/dist`** cuando subas cambios a `main`. También puedes ejecutarlo manualmente. Sigue la [documentación oficial de GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

**Aún no se ha creado un repositorio remoto ni se ha publicado la web.** El estilo y el nombre están elegidos; quedan pendientes los datos de contacto.

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
