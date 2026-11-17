"""Read-only source audit: hashes, duplicate candidates and private contact sheets."""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageChops, ImageStat
import hashlib, json

root=Path(__file__).resolve().parents[1]
source=Path(r'C:\Users\mabe8\Desktop\oppo_movil-backup')
out=root/'_private'/'recovered'
out.mkdir(parents=True,exist_ok=True)
baseline=json.loads((root/'_private'/'baseline-catalog.json').read_text(encoding='utf-8'))
existing={x['id'] for x in baseline}
excluded={'IMG20250825163127','IMG20250825163203','IMG20250825163219','IMG20250825163226','IMG20250928233359'}
files=sorted((p for p in source.rglob('*') if p.is_file() and p.suffix.lower() in {'.jpg','.jpeg','.png','.webp','.mp4','.mov','.m4v'}),key=lambda p:(p.stem not in existing,str(p)))
seen_bytes={};seen_pixels={};records=[];small_images={}
for file in files:
    digest=hashlib.file_digest(file.open('rb'),'sha256').hexdigest()
    record={'file':str(file.relative_to(source)),'id':file.stem,'bytes':file.stat().st_size,'sha256':digest,'type':'video' if file.suffix.lower() in {'.mp4','.mov','.m4v'} else 'image'}
    if file.stem in excluded: record['status']='excluded'
    elif digest in seen_bytes: record.update(status='duplicate_bytes',duplicate_of=seen_bytes[digest])
    else:
        seen_bytes[digest]=record['file']
        if record['type']=='image':
            im=ImageOps.exif_transpose(Image.open(file)).convert('RGB')
            pix=hashlib.sha256(str(im.size).encode()+im.tobytes()).hexdigest()
            record['pixel_sha256']=pix
            if pix in seen_pixels: record.update(status='duplicate_pixels',duplicate_of=seen_pixels[pix])
            else:
                seen_pixels[pix]=record['file']
                thumb=im.resize((128,128),Image.Resampling.LANCZOS)
                tiny=im.convert('L').resize((9,8),Image.Resampling.LANCZOS)
                px=list(tiny.getdata());bits=sum((px[y*9+x]>px[y*9+x+1])<<(y*8+x) for y in range(8) for x in range(8))
                record['dhash']=f'{bits:016x}';record['size']=im.size
                small_images[record['file']]=thumb
                record['status']='existing' if file.stem in existing else 'candidate'
        else: record['status']='existing' if file.stem in existing else 'candidate'
    records.append(record)
images=[r for r in records if r['type']=='image' and 'dhash' in r]
near=[]
for index,a in enumerate(images):
    for b in images[index+1:]:
        distance=(int(a['dhash'],16)^int(b['dhash'],16)).bit_count()
        if distance<=7:
            diff=ImageStat.Stat(ImageChops.difference(small_images[a['file']],small_images[b['file']]))
            near.append({'a':a['file'],'b':b['file'],'distance':distance,'mean_difference':round(sum(diff.mean)/3,2)})
candidates=[r for r in records if r['type']=='image' and r['status']=='candidate']
for start in range(0,len(candidates),30):
    sheet=Image.new('RGB',(1200,1200),'#e5e7eb');draw=ImageDraw.Draw(sheet)
    for j,r in enumerate(candidates[start:start+30]):
        im=ImageOps.exif_transpose(Image.open(source/r['file'])).convert('RGB');im.thumbnail((188,204))
        x,y=(j%6)*200,(j//6)*240
        sheet.paste(im,(x+(200-im.width)//2,y))
        draw.text((x+4,y+206),str(start+j+1)+': '+r['id'],fill='#111')
        r['review_index']=start+j+1
    sheet.save(out/f'photos-{start//30+1}.jpg')
audit={'records':records,'similar_candidates':near,'missing_existing':[x['id'] for x in baseline if x['id'] not in {r['id'] for r in records}]}
(out/'audit.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False),encoding='utf-8')
from collections import Counter
print(json.dumps({'counts':dict(Counter((r['type']+':'+r['status']) for r in records)),'similar_candidates':near,'sheets':(len(candidates)+29)//30},ensure_ascii=False))
