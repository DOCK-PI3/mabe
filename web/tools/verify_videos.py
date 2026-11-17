from pathlib import Path
import subprocess, sys, re, json
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / '.tools'))
import imageio_ffmpeg
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
root=Path(__file__).resolve().parents[1]
files=sorted((root/'dist'/'assets'/'videos').glob('*.mp4'))
report=[]
verified=[]
audit_path=root/'_private'/'recovered'/'video-audit.json'
source_durations={r['id']:r['duration'] for r in json.loads(audit_path.read_text(encoding='utf-8'))['records']} if audit_path.exists() else {}
for file in files:
    probe=subprocess.run([ffmpeg,'-hide_banner','-i',str(file)],capture_output=True,text=True,encoding='utf-8',errors='replace').stderr
    if 'Audio:' in probe: raise RuntimeError(f'Pista de audio encontrada: {file.name}')
    if 'Video: h264' not in probe: raise RuntimeError(f'Vídeo no compatible: {file.name}')
    subprocess.run([ffmpeg,'-hide_banner','-loglevel','error','-ss','1','-i',str(file),'-frames:v','1','-f','null','-'],check=True,capture_output=True)
    duration=re.search(r'Duration: ([\d:.]+)',probe).group(1)
    hours,minutes,seconds=duration.split(':')
    duration_seconds=int(hours)*3600+int(minutes)*60+float(seconds)
    source_duration=source_durations.get(file.stem)
    if source_duration is not None and abs(source_duration-duration_seconds)>1:
        raise RuntimeError(f'Duración inesperada en {file.name}: {source_duration} -> {duration_seconds}')
    verified.append({'file':file.name,'codec':'h264','audioStreams':0,'durationSeconds':duration_seconds,'sourceDurationSeconds':source_duration,'decodeCheck':True})
    report.append(f'{file.name}: H.264; duración {duration}; sin pista de audio; decodificación correcta')
(root/'_private'/'verified-videos.txt').write_text('\n'.join(report),encoding='utf-8')
(root/'media-video-verification.json').write_text(json.dumps(verified,indent=2),encoding='utf-8')
print(f'{len(report)} vídeos verificados: H.264, decodificables y sin audio.')
