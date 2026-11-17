from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parents[1];private=root/'_private'/'recovered'
baseline=json.loads((root/'_private'/'baseline-catalog.json').read_text(encoding='utf-8'))
photos=json.loads((private/'photo-additions.json').read_text(encoding='utf-8'))
videos=json.loads((private/'video-additions.json').read_text(encoding='utf-8'))
audit=json.loads((private/'audit.json').read_text(encoding='utf-8'))
by_index={r.get('review_index'):r['id'] for r in audit['records'] if 'review_index' in r}
highlights=[by_index[i] for i in [65,95,101,117,123,149,162,166,198,221,69,109]]
photos.sort(key=lambda x:(highlights.index(x['id']) if x['id'] in highlights else len(highlights),x['id']))
video_titles=[('VID-20250416-WA0010','Estructura y recorrido del falso techo','Pladur'),('VID-20250505-WA0009','Volúmenes y techos en un espacio amplio','Pladur'),('VID-20250521-WA0002','Placas y huecos de instalaciones','Pladur'),('VID-20250521-WA0008','Encuentros y montaje del techo','Pladur'),('VID-20250716-WA0007','Montaje de una placa durante la obra','Pladur'),('VID-20250722-WA0007','Tabiques y techos en ejecución','Pladur'),('VID-20250731-WA0001','Encuentro superior de un ventanal','Pladur'),('VID-20250731-WA0014','Revestimiento de techo en interior','Pladur'),('VID-20250801-WA0005','Perfiles y placas junto al ventanal','Pladur'),('VID_20250324_130840','Remates de paredes y molduras','Acabados'),('VID_20250324_130925','Estado de un encuentro en el suelo','Reformas'),('VID_20250324_134410','Acabados de techo y molduras','Acabados'),('VID_20250415_144608','Estructura y montaje de un techo','Pladur'),('VID_20250520_165104','Placas y registros de un falso techo','Pladur'),('VID_20250523_125333','Recorrido por techos y volúmenes','Pladur'),('VID_20250731_131839','Instalaciones y remates de un techo','Pladur')]
for item in videos:
    _,item['title'],item['category']=next(x for x in video_titles if x[0]==item['id'])
featured=['VID_20250523_125333','VID_20250324_134410','VID-20250722-WA0007']
videos.sort(key=lambda x:featured.index(x['id']) if x['id'] in featured else len(featured))
source_hashes={(r['id'],r['type']):r['sha256'] for r in audit['records']}
items=[];ids=set();hashes={};skipped=[]
for item in photos+videos+baseline:
    if item['id'] in ids:continue
    digest=source_hashes.get((item['id'],item['type']),item.get('sourceSha256'))
    if digest and digest in hashes:
        skipped.append({'id':item['id'],'same_as':hashes[digest]});continue
    if digest:item['sourceSha256']=digest;hashes[digest]=item['id']
    ids.add(item['id']);items.append(item)
catalog='// Catálogo de trabajos. Nuevas incorporaciones primero; sin copias repetidas.\nwindow.PORTFOLIO = '+json.dumps(items,indent=2,ensure_ascii=False)+';\n'
(root/'dist'/'catalog.js').write_text(catalog,encoding='utf-8')
assets=[]
for item in items:
    file=root/'dist'/item['src']
    assets.append({'id':item['id'],'type':item['type'],'sourceSha256':item.get('sourceSha256'),'webSha256':hashlib.file_digest(file.open('rb'),'sha256').hexdigest(),'bytes':file.stat().st_size})
(root/'media-manifest.json').write_text(json.dumps(assets,indent=2,ensure_ascii=False),encoding='utf-8')
report={'added_photos':len(photos),'added_videos':len(videos),'total_photos':sum(i['type']=='image' for i in items),'total_videos':sum(i['type']=='video' for i in items),'duplicates_skipped':skipped,'web_bytes':sum(x['bytes'] for x in assets)}
(private/'import-summary.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))
