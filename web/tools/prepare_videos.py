from pathlib import Path
import sys, subprocess, json
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / '.tools'))
import imageio_ffmpeg
from PIL import Image, ImageOps

root = Path(__file__).resolve().parents[1]
out = root / 'dist' / 'assets' / 'videos'
out.mkdir(parents=True, exist_ok=True)
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
files = sorted(Path(r'C:\Users\mabe8\Desktop\oppo_movil-backup\videos').glob('*.mp4'))
report = []
for index, file in enumerate(files, 1):
    target = out / file.name
    if not target.exists():
        subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', '-i', str(file), '-map', '0:v:0', '-an', '-map_metadata', '-1', '-vf', 'scale=960:960:force_original_aspect_ratio=decrease:force_divisible_by=2,fps=25', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '27', '-pix_fmt', 'yuv420p', '-threads', '2', '-movflags', '+faststart', str(target)], check=True)
    frame = root / '_private' / (file.stem+'-0.jpg')
    im = Image.open(frame).convert('RGB')
    im.save(out / (file.stem+'.webp'), quality=82)
    entry = {'file': file.name, 'original_bytes': file.stat().st_size, 'web_bytes': target.stat().st_size, 'audio': False}
    report.append(entry)
    print(f'{index}/{len(files)} {file.name}: {target.stat().st_size/1024/1024:.1f} MB, sin audio', flush=True)
(root / '_private' / 'video-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
