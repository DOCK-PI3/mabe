from pathlib import Path
import sys, subprocess, re, json, hashlib
from PIL import Image, ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'.tools'))
import imageio_ffmpeg
root=Path(__file__).resolve().parents[1];source=Path(r'C:\Users\mabe8\Desktop\oppo_movil-backup')
out=root/'_private'/'recovered';out.mkdir(parents=True,exist_ok=True)
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
baseline=json.loads((root/'_private'/'baseline-catalog.json').read_text(encoding='utf-8'))
old={x['id'] for x in baseline if x['type']=='video'}
records=[]
sources={p.stem:p for p in source.rglob('*.mp4')}
for file_id in sorted(old|sources.keys()):
    file=sources.get(file_id,root/'dist'/'assets'/'videos'/(file_id+'.mp4'))
    probe=subprocess.run([ffmpeg,'-hide_banner','-i',str(file)],capture_output=True,text=True,encoding='utf-8',errors='replace').stderr
    match=re.search(r'Duration: (\d+):(\d+):([\d.]+)',probe)
    if not match: raise RuntimeError(str(file))
    duration=int(match[1])*3600+int(match[2])*60+float(match[3])
    packet_hash=subprocess.run([ffmpeg,'-v','error','-i',str(file),'-map','0:v:0','-c','copy','-f','hash','-hash','sha256','-'],capture_output=True,text=True,check=True).stdout.strip()
    record={'id':file_id,'file':str(file),'status':'existing' if file_id in old else 'candidate','duration':duration,'video_sha256':packet_hash,'frames':[]}
    for n,fraction in enumerate([0.1,0.5,0.9]):
        target=out/f'{file_id}-{n}.jpg'
        subprocess.run([ffmpeg,'-v','error','-y','-ss',str(duration*fraction),'-i',str(file),'-frames:v','1','-vf','scale=360:360:force_original_aspect_ratio=decrease',str(target)],check=True)
        im=Image.open(target).convert('L').resize((9,8));px=list(im.getdata())
        bits=sum((px[y*9+x]>px[y*9+x+1])<<(y*8+x) for y in range(8) for x in range(8))
        record['frames'].append(f'{bits:016x}')
    records.append(record)
    print(f'Revisado {file_id}',flush=True)
duplicates=[];similar=[]
for i,a in enumerate(records):
    for b in records[i+1:]:
        if a['video_sha256']==b['video_sha256']: duplicates.append([a['id'],b['id']])
        elif abs(a['duration']-b['duration'])<2:
            distances=[(int(x,16)^int(y,16)).bit_count() for x,y in zip(a['frames'],b['frames'])]
            if max(distances)<15: similar.append({'a':a['id'],'b':b['id'],'distances':distances})
new=[r for r in records if r['status']=='candidate']
for start in range(0,len(new),8):
    sheet=Image.new('RGB',(1200,1000),'#e5e7eb');draw=ImageDraw.Draw(sheet)
    for j,r in enumerate(new[start:start+8]):
        for n in range(3):
            im=Image.open(out/f'{r["id"]}-{n}.jpg');im.thumbnail((288,138))
            x,y=(j%4)*300,(j//4)*500+n*146
            sheet.paste(im,(x+(300-im.width)//2,y))
        draw.text(((j%4)*300+5,(j//4)*500+443),f'{start+j+1}: {r["id"]}',fill='#111')
        draw.text(((j%4)*300+5,(j//4)*500+464),f'{r["duration"]} s',fill='#111')
    sheet.save(out/f'videos-{start//8+1}.jpg')
(out/'video-audit.json').write_text(json.dumps({'records':records,'duplicates':duplicates,'similar':similar},indent=2),encoding='utf-8')
print(json.dumps({'new':len(new),'duplicates':duplicates,'similar':similar}))
