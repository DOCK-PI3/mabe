from pathlib import Path
import sys, subprocess
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / '.tools'))
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageOps

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
source = Path(r'C:\Users\mabe8\Desktop\oppo_movil-backup\videos')
out = Path(__file__).resolve().parents[1] / '_private'
files = sorted(source.glob('*.mp4'))
for batch in range(0, len(files), 8):
    sheet = Image.new('RGB', (1200, 1000), '#dddddd')
    draw = ImageDraw.Draw(sheet)
    for j, file in enumerate(files[batch:batch+8]):
        for k, time in enumerate([1, 7]):
            frame = out / f'{file.stem}-{k}.jpg'
            subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', '-ss', str(time), '-i', str(file), '-frames:v', '1', '-vf', 'scale=500:-2', str(frame)], check=True)
            im = Image.open(frame)
            im.thumbnail((280,210))
            x, y = (j%4)*300, (j//4)*500+k*230
            sheet.paste(im, (x+(300-im.width)//2,y))
        draw.text(((j%4)*300+4,(j//4)*500+461), f'{batch+j+1}: {file.stem}', fill='#111')
    path = out / f'videos-{batch//8+1}.jpg'
    sheet.save(path)
    print(path)
