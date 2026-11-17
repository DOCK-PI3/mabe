"""Incremental import from the reviewed audit. Originals are never modified."""
from pathlib import Path
from PIL import Image, ImageOps
import sys,json,subprocess,re,hashlib

root=Path(__file__).resolve().parents[1]
source=Path(r'C:\Users\mabe8\Desktop\oppo_movil-backup')
private=root/'_private'/'recovered'
audit=json.loads((private/'audit.json').read_text(encoding='utf-8'))
baseline=json.loads((root/'_private'/'baseline-catalog.json').read_text(encoding='utf-8'))
personal={'20210416_224026'}
# Reviewed groups describe visible work, without attributing an unverified product.
groups=[(1,2,'Instalaciones sobre el falso techo','Pladur'),(3,5,'Preparación y remate de tabiques','Acabados'),(6,10,'Placas, juntas y encuentros del techo','Pladur'),(11,18,'Perfilería y montaje de tabiques','Pladur'),(19,29,'Distribución interior en obra','Pladur'),(30,40,'Encuentros sobre puertas y pasos','Pladur'),(41,47,'Estructura del falso techo','Pladur'),(48,56,'Techos y volúmenes en un espacio amplio','Pladur'),(57,62,'Perfilería y recorrido de instalaciones','Pladur'),(63,70,'Volúmenes curvos en el techo','Pladur'),(71,75,'Huecos circulares en pladur','Pladur'),(76,77,'Registro integrado en pared','Pladur'),(78,79,'Revestimiento interior en ejecución','Pladur'),(80,84,'Estructura y revestimiento a media altura','Pladur'),(85,87,'Aislamiento y remates en techo','Pladur'),(88,100,'Armario y estantes de pladur','Pladur'),(101,107,'Exterior de vivienda','Reformas'),(108,109,'Preparación de techos en interior','Pladur'),(110,111,'Estructura exterior en ejecución','Reformas'),(112,114,'Reparación y remate del techo','Acabados'),(116,120,'Techo, iluminación y encuentros sobre puertas','Pladur'),(121,121,'Preparación de un encuentro entre paredes','Acabados'),(122,125,'Suelos y acabados en pasillo','Reformas'),(126,126,'Preparación de pared en interior','Acabados'),(127,132,'Aislamiento y revestimiento interior','Pladur'),(133,136,'Huecos y aislamiento en tabique','Pladur'),(137,139,'Preparación de paredes y remates','Acabados'),(140,149,'Aislamiento y estructura del techo','Pladur'),(150,161,'Montaje de falsos techos','Pladur'),(162,164,'Volúmenes en un techo exterior','Pladur'),(165,169,'Cubierta y remates exteriores','Reformas'),(170,172,'Remates del falso techo','Pladur'),(173,176,'Revestimiento y acabado de paredes','Acabados'),(177,177,'Vista exterior del edificio','Reformas'),(178,180,'Registro y encuentros en falso techo','Pladur'),(181,181,'Exterior durante la reforma','Reformas'),(182,191,'Perfilería y montaje del falso techo','Pladur'),(192,196,'Techos y registros en pasillo','Pladur'),(197,206,'Techo modular y remates de pasillo','Pladur'),(207,211,'Tabiques y distribución interior','Pladur'),(212,214,'Revestimiento interior en ejecución','Pladur'),(215,215,'Tabiques en un espacio amplio','Pladur'),(216,224,'Placas y tratamiento de juntas','Pladur'),(225,225,'Detalle de placas y perfilería','Pladur'),(226,227,'Estancia con falso techo','Pladur'),(228,228,'Hueco de puerta durante la obra','Reformas'),(229,230,'Recorrido de un pasillo en reforma','Pladur')]

def public_item(record,title,category):
    kind=record['type'];folder='images' if kind=='image' else 'videos';ext='webp' if kind=='image' else 'mp4'
    return {'id':record['id'],'type':kind,'category':category,'title':title,'src':f'assets/{folder}/{record["id"]}.{ext}','poster':f'assets/{folder}/{record["id"]}.webp','sourceSha256':record['sha256']}

mode=sys.argv[1] if len(sys.argv)>1 else 'photos'
if mode=='photos':
    target=root/'dist'/'assets'/'images';target.mkdir(parents=True,exist_ok=True)
    additions=[]
    for r in audit['records']:
        if r['type']!='image' or r['status']!='candidate' or r['id'] in personal:continue
        index=r['review_index']
        start,end,title,category=next(g for g in groups if g[0]<=index<=g[1])
        if end>start:title+=f' · vista {index-start+1}'
        file=target/(r['id']+'.webp')
        if not file.exists():
            im=ImageOps.exif_transpose(Image.open(source/r['file'])).convert('RGB')
            im.thumbnail((1800,1800));im.save(file,quality=83,method=5)
        additions.append(public_item(r,title,category))
        if len(additions)%30==0:print(f'{len(additions)} fotos preparadas',flush=True)
    (private/'photo-additions.json').write_text(json.dumps(additions,indent=2,ensure_ascii=False),encoding='utf-8')
    print(f'{len(additions)} fotos nuevas preparadas; originales intactos.',flush=True)
elif mode=='videos':
    sys.path.insert(0,str(root.parent/'.tools'));import imageio_ffmpeg
    ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
    va=json.loads((private/'video-audit.json').read_text(encoding='utf-8'))
    duplicates=set()
    for a,b in va['duplicates']:
        old={i['id'] for i in baseline};duplicates.add(b if a in old else a if b in old else max(a,b))
    target=root/'dist'/'assets'/'videos';target.mkdir(parents=True,exist_ok=True)
    additions=[]
    for r in audit['records']:
        if r['type']!='video' or r['status']!='candidate' or r['id'] in duplicates:continue
        file=target/(r['id']+'.mp4');temp=target/(r['id']+'.partial.mp4')
        if not file.exists():
            subprocess.run([ffmpeg,'-hide_banner','-loglevel','error','-y','-i',str(source/r['file']),'-map','0:v:0','-an','-map_metadata','-1','-vf','scale=960:960:force_original_aspect_ratio=decrease:force_divisible_by=2,fps=25','-c:v','libx264','-preset','veryfast','-crf','27','-pix_fmt','yuv420p','-threads','2','-movflags','+faststart',str(temp)],check=True)
            temp.replace(file)
        probe=subprocess.run([ffmpeg,'-hide_banner','-i',str(file)],capture_output=True,text=True,encoding='utf-8',errors='replace').stderr
        if 'Audio:' in probe or 'Video: h264' not in probe:raise RuntimeError(f'Vídeo no válido o con audio: {file}')
        im=Image.open(private/(r['id']+'-1.jpg')).convert('RGB');im.save(target/(r['id']+'.webp'),quality=82)
        additions.append(public_item(r,'Recorrido de reforma recuperado','Reformas'))
        print(f'{len(additions)}/16 {r["id"]}: {file.stat().st_size/1024/1024:.1f} MiB, sin pista de audio',flush=True)
    (private/'video-additions.json').write_text(json.dumps(additions,indent=2,ensure_ascii=False),encoding='utf-8')
else:raise SystemExit('Usa photos o videos')
