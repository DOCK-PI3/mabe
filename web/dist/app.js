(() => {
  'use strict';
  const config = window.SITE_CONFIG;
  const items = window.PORTFOLIO;
  const videoItems = items.filter(item => item.type === 'video');
  const featuredVideos = videoItems.slice(0, 3);
  const style = document.body.dataset.style;
  const main = document.querySelector('main');
  const imagePath = id => `assets/images/${id}.webp`;
  const esc = text => String(text).replace(/[&<>"']/g, ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const heroCopy = '<p class="hero-description">Pladur, pasta, pintura, Placostic y reformas generales en Las Palmas. Un recorrido por los espacios, los detalles y el trabajo que hay detrás.</p><a class="primary" href="#trabajos">Ver los trabajos</a>';
  const heroes = {
    cuaderno: `<section class="hero blueprint"><div class="hero-text"><p class="hero-kicker">De la estructura al acabado</p><h1>El oficio<br>se ve en <br>los detalles.</h1>${heroCopy}</div><div class="blueprint-photos"><button class="hero-photo main-photo" data-item="IMG20251127145356" aria-label="Ampliar reforma de techo"><img src="${imagePath('IMG20251127145356')}" alt="Techo de pladur junto a un ventanal, durante la obra" fetchpriority="high"><span>Techos, volúmenes y encuentros</span></button><button class="hero-photo detail-photo" data-item="IMG20260309185150" aria-label="Ampliar mueble de pladur"><img src="${imagePath('IMG20260309185150')}" alt="Mueble a medida realizado con pladur"><span>Hecho a medida</span></button><p class="handnote">Cada remate cuenta.</p></div></section>`,
    cine: `<section class="hero cinema"><img class="cinema-bg" src="${imagePath('IMG20251127145401')}" alt="Una reforma interior junto a un gran ventanal con vistas al mar" fetchpriority="high"><div class="cinema-top"><span>Espacios en transformación</span><a href="#videos">Ver la obra en movimiento</a></div><div class="cinema-title"><h1>Hay trabajo<br>detrás de<br>cada espacio.</h1><div>${heroCopy}</div></div><span class="cinema-caption">Pladur en ejecución / Interior junto al mar</span></section>`,
    taller: `<section class="hero material"><div class="material-copy"><p class="hero-kicker">Materia, manos y cuidado</p><h1>Darle forma.<br>Darle vida.</h1>${heroCopy}<div class="material-tags"><span>Pladur</span><span>Pasta</span><span>Pintura</span><span>Placostic</span><span>Reformas</span></div></div><div class="sample-stack"><button class="sample-main" data-item="IMG20260309185150" aria-label="Ampliar mueble a medida"><img src="${imagePath('IMG20260309185150')}" alt="Mueble de pladur con estantes y huecos"><span>De una idea<br>a una pieza.</span></button><button class="sample-detail" data-item="IMG20260909093936" aria-label="Ampliar detalle de molduras"><img src="${imagePath('IMG20260909093936')}" alt="Detalle de molduras y encuentros en un techo"><span>El acabado también importa</span></button></div></section>`
  };
  const services = [['Pladur','Tabiques, falsos techos, revestimientos y soluciones a medida.'],['Pasta y Placostic','Preparación de superficies, tratamiento de juntas y remates.'],['Pintura','Paredes, techos y acabados que dan el último paso a un espacio.'],['Reformas','Intervenciones para renovar y mejorar los espacios.']];
  main.innerHTML = `${heroes[style]}
    <section class="services section" id="oficio"><div class="section-head"><h2>Lo que hago</h2><p>Desde lo que sostiene un espacio<br>hasta lo que se ve al terminar.</p></div><div class="service-list">${services.map(([title,description])=>`<article><h3>${title}</h3><p>${description}</p></article>`).join('')}</div></section>
    <section class="work section" id="trabajos"><div class="section-head"><h2>${style==='cuaderno'?'El archivo de obra':style==='cine'?'Espacios y detalles':'El muestrario de trabajos'}</h2><p>Fotos del proceso, estructuras y acabados.<br>Abre cada imagen para ver los detalles.</p></div><div class="filter-row" aria-label="Filtrar trabajos">${['Todo','Pladur','Acabados','Reformas','Vídeos'].map((name,i)=>`<button class="filter ${i===0?'active':''}" aria-pressed="${i===0}" data-filter="${name}">${name}</button>`).join('')}<span id="result-count" role="status"></span></div><div class="gallery" id="gallery"></div><div class="load-wrap"><button class="secondary" id="load-more">Mostrar más trabajos</button></div><p class="empty-state" id="empty" hidden>No hay trabajos en esta categoría todavía.</p></section>
    <section class="transformation section"><div class="comparison-copy"><h2>Una intervención.<br>Un cambio visible.</h2><p>El mismo lavadero, antes y después. Desliza para comparar el estado inicial con el resultado.</p><span>Reformas / Lavadero</span></div><div class="comparison"><div class="comparison-images"><img src="${imagePath('IMG20260813140153')}" alt="Lavadero después de la intervención" loading="lazy"><div class="before-layer"><img src="${imagePath('IMG20260813124216')}" alt="Lavadero antes de la intervención" loading="lazy"></div><span class="compare-label before-label">Antes</span><span class="compare-label after-label">Después</span><div class="comparison-line" aria-hidden="true"><span>↔</span></div><input type="range" min="0" max="100" value="50" aria-label="Comparar lavadero antes y después"></div><p>Mueve el control con el dedo, el ratón o las flechas del teclado.</p></div></section>
    <section class="video-section section" id="videos"><div class="section-head"><h2>La obra en movimiento</h2><p>Recorridos reales del trabajo.<br>Todos los vídeos tienen la pista de audio eliminada.</p></div><div class="video-strip">${featuredVideos.map(item=>`<button class="video-card" data-item="${item.id}"><img loading="lazy" src="${item.poster}" alt="${esc(item.title)}"><span class="play-icon" aria-hidden="true">▶</span><span class="video-title">${esc(item.title)}</span><span class="silent">Sin audio</span></button>`).join('')}</div><button class="secondary all-videos">Ver los ${videoItems.length} vídeos</button></section>
    <section class="contact section" id="contacto"><p>Pladur · Acabados · Reformas</p><h2>Tu espacio,<br>tu próximo proyecto.</h2><div class="contact-content"></div></section>`;
  document.querySelectorAll('[data-brand]').forEach(el=>el.textContent=config.name);
  const contact = document.querySelector('.contact-content');
  if (config.location) { const p = document.createElement('p'); p.textContent=config.location; contact.append(p); }
  const methods=[];
  if (config.whatsapp) methods.push(['WhatsApp',`https://wa.me/${config.whatsapp.replace(/\D/g,'')}`]);
  if (config.phone) methods.push(['Llamar',`tel:${config.phone.replace(/[^+\d]/g,'')}`]);
  if (config.email) methods.push(['Escribir un correo',`mailto:${config.email}`]);
  methods.forEach(([label,href])=>{const a=document.createElement('a');a.textContent=label;a.href=href;a.className='primary';contact.append(a)});
  if(!methods.length) {const p=document.createElement('p');p.textContent='Información de contacto próximamente.';contact.append(p)}
  let activeFilter='Todo', limit=12, filtered=[];
  const gallery=document.querySelector('#gallery');
  function renderGallery() {
    filtered=items.filter(item=>activeFilter==='Todo'||(activeFilter==='Vídeos'?item.type==='video':item.category===activeFilter));
    gallery.innerHTML=filtered.slice(0,limit).map(item=>`<button class="work-card ${item.type}" data-item="${item.id}"><div class="work-image"><img src="${item.poster}" alt="${esc(item.title)}" loading="lazy">${item.type==='video'?'<span class="play-icon" aria-hidden="true">▶</span><span class="silent">Sin audio</span>':''}<span class="expand">${item.type==='video'?'Reproducir':'Ampliar'}</span></div><div class="work-caption"><span>${esc(item.title)}</span><small>${item.category}</small></div></button>`).join('');
    document.querySelector('#result-count').textContent=`${filtered.length} ${filtered.length===1?'archivo':'archivos'}`;
    document.querySelector('#load-more').hidden=limit>=filtered.length;
    document.querySelector('#empty').hidden=filtered.length>0;
  }
  function setFilter(name){activeFilter=name;limit=12;document.querySelectorAll('.filter').forEach(button=>{const selected=button.dataset.filter===name;button.classList.toggle('active',selected);button.setAttribute('aria-pressed',String(selected))});renderGallery()}
  document.querySelectorAll('.filter').forEach(button=>button.addEventListener('click',()=>setFilter(button.dataset.filter)));
  document.querySelector('#load-more').addEventListener('click',()=>{limit+=12;renderGallery()});
  document.querySelector('.all-videos').addEventListener('click',()=>{setFilter('Vídeos');document.querySelector('#trabajos').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'})});
  const comparison=document.querySelector('.comparison-images');
  comparison.querySelector('input').addEventListener('input',event=>comparison.style.setProperty('--split',`${event.target.value}%`));
  const dialog=document.querySelector('#viewer');
  const stage=dialog.querySelector('.viewer-stage');
  let currentIndex=0, viewerItems=items, lastFocus=null;
  function stopVideo(){const video=stage.querySelector('video');if(video){video.pause();video.removeAttribute('src');video.load()}}
  function showItem(item){
    stopVideo();currentIndex=viewerItems.findIndex(x=>x.id===item.id);
    dialog.querySelector('#viewer-title').textContent=item.title;
    dialog.querySelector('.viewer-position').textContent=`${currentIndex+1} / ${viewerItems.length}`;
    stage.replaceChildren();
    if(item.type==='image'){const img=document.createElement('img');img.src=item.src;img.alt=item.title;stage.append(img);}
    else {
      // Public MP4 files contain video only: the import removes the audio stream.
      const video=document.createElement('video');video.src=item.src;video.poster=item.poster;video.playsInline=true;video.preload='metadata';video.setAttribute('playsinline','');
      const controls=document.createElement('div');controls.className='video-controls';
      controls.innerHTML='<button class="video-toggle" type="button">Reproducir</button><input type="range" min="0" max="100" value="0" step="0.1" aria-label="Posición del vídeo"><span class="video-time">0:00</span><span>Sin audio</span><button class="video-fullscreen" type="button">Pantalla completa</button>';
      stage.append(video,controls);
      const toggle=controls.querySelector('.video-toggle'), seek=controls.querySelector('input'), time=controls.querySelector('.video-time');
      const format=s=>`${Math.floor(s/60)}:${String(Math.floor(s%60)).padStart(2,'0')}`;
      const play=()=>video.play().catch(()=>{time.textContent='Pulsa Reproducir para iniciar'});
      toggle.addEventListener('click',()=>video.paused?play():video.pause());
      video.addEventListener('click',()=>video.paused?play():video.pause());
      video.addEventListener('play',()=>toggle.textContent='Pausar');video.addEventListener('pause',()=>toggle.textContent='Reproducir');
      video.addEventListener('timeupdate',()=>{if(Number.isFinite(video.duration)){seek.value=String(video.currentTime/video.duration*100);time.textContent=`${format(video.currentTime)} / ${format(video.duration)}`}});
      video.addEventListener('error',()=>{time.textContent='No se pudo cargar el vídeo.';toggle.disabled=true});
      seek.addEventListener('input',()=>{if(Number.isFinite(video.duration))video.currentTime=Number(seek.value)/100*video.duration});
      controls.querySelector('.video-fullscreen').addEventListener('click',()=>{if(stage.requestFullscreen)stage.requestFullscreen().catch(()=>{});else if(video.webkitEnterFullscreen)video.webkitEnterFullscreen()});
      play();
    }
  }
  document.addEventListener('click',event=>{const button=event.target.closest('[data-item]');if(!button)return;const item=items.find(x=>x.id===button.dataset.item);if(!item)return;lastFocus=button;viewerItems=button.closest('.gallery')?filtered:items;showItem(item);dialog.showModal();document.body.classList.add('modal-open');dialog.querySelector('.viewer-close').focus()});
  const close=()=>dialog.close();dialog.querySelector('.viewer-close').addEventListener('click',close);
  dialog.addEventListener('click',event=>{if(event.target===dialog)close()});
  dialog.addEventListener('close',()=>{stopVideo();stage.replaceChildren();document.body.classList.remove('modal-open');if(lastFocus?.isConnected)lastFocus.focus()});
  const change=step=>showItem(viewerItems[(currentIndex+step+viewerItems.length)%viewerItems.length]);
  dialog.querySelector('.viewer-prev').addEventListener('click',()=>change(-1));dialog.querySelector('.viewer-next').addEventListener('click',()=>change(1));
  dialog.addEventListener('keydown',event=>{if(event.target.matches('input'))return;if(event.key==='ArrowLeft'){event.preventDefault();change(-1)}if(event.key==='ArrowRight'){event.preventDefault();change(1)}});
  renderGallery();
})();
