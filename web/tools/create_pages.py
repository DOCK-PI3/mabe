from pathlib import Path
import json,hashlib
from html import escape
root = Path(__file__).resolve().parents[1] / 'dist'
config=json.loads((root/'config.js').read_text(encoding='utf-8').split('=',1)[1].strip().rstrip(';'))
name=escape(config['name'])
location=escape(config['location'])
versions={file:hashlib.sha256((root/file).read_bytes()).hexdigest()[:12] for file in ['config.js','catalog.js','app.js','styles.css']}
themes = {'cuaderno': 'Cuaderno de obra', 'cine': 'Obra en escena', 'taller': 'Materia y oficio'}
for theme, title in themes.items():
    selected = theme == 'cuaderno'
    home = 'index.html' if selected else theme+'.html'
    comparison_link = '' if selected else '<a class="back-proposals" href="index.html">Volver a la web</a>'
    footer_links = '<a href="#trabajos">Explorar los trabajos</a>' if selected else '<a href="index.html">Volver a la web principal</a>'
    page_title = f'{name} · {location}' if selected else f'{name} · {title} · {location}'
    page = f'''<!doctype html>
<html lang="es"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{page_title}</title>
<meta name="description" content="{name}. Pladur, pasta, pintura, Placostic y reformas en {location}. Fotografías del proceso y vídeos reales de los trabajos.">
<meta name="theme-color" content="{'#284bdf' if theme=='cuaderno' else '#181c20' if theme=='cine' else '#e5dbf9'}">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%23203bdd'/%3E%3Cpath d='M12 46V18l20 17 20-17v28' fill='none' stroke='white' stroke-width='7'/%3E%3C/svg%3E">
<link rel="stylesheet" href="styles.css?v={versions['styles.css']}"><script src="config.js?v={versions['config.js']}" defer></script><script src="catalog.js?v={versions['catalog.js']}" defer></script><script src="app.js?v={versions['app.js']}" defer></script>
</head><body class="{theme}" data-style="{theme}">
<a class="skip" href="#main">Saltar al contenido</a>
<header class="site-header"><a class="brand" href="{home}"><span class="brand-mark" aria-hidden="true">M</span><span class="brand-name" data-brand>{name}</span></a><nav aria-label="Navegación principal"><a href="#trabajos">Trabajos</a><a href="#oficio">El oficio</a><a href="#videos">Vídeos</a><a href="https://dock-pi3.github.io/Pladur-Studio-3D/" target="_blank" rel="noopener noreferrer" title="Se abre en una nueva pestaña o ventana">Crea tu mueble</a><a href="#contacto">Contacto</a></nav>{comparison_link}</header>
<main id="main"><noscript>Activa JavaScript para explorar las fotos y vídeos de los trabajos.</noscript></main>
<footer class="site-footer"><span><span data-brand>{name}</span> / {location}</span>{footer_links}</footer>
<dialog id="viewer" aria-labelledby="viewer-title"><div class="viewer-header"><h2 id="viewer-title">Trabajo</h2><button class="viewer-close" type="button">Cerrar</button></div><div class="viewer-stage"></div><div class="viewer-footer"><button class="viewer-prev" aria-label="Trabajo anterior" type="button">Anterior</button><span class="viewer-position" aria-live="polite"></span><button class="viewer-next" aria-label="Trabajo siguiente" type="button">Siguiente</button></div></dialog>
</body></html>'''
    (root / (theme+'.html')).write_text(page, encoding='utf-8')
    if selected:
        (root / 'index.html').write_text(page, encoding='utf-8')
print('Cuaderno de obra preparado como web principal; versiones alternativas conservadas.')
