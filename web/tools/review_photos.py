from pathlib import Path
from PIL import Image, ImageOps, ImageDraw

source = Path(r'C:\Users\mabe8\Desktop\oppo_movil-backup')
out = Path(__file__).resolve().parents[1] / '_private'
files = sorted(source.glob('*.jpg'))
for batch in range(0, len(files), 16):
    sheet = Image.new('RGB', (1200, 1200), '#e0e0e0')
    draw = ImageDraw.Draw(sheet)
    for j, file in enumerate(files[batch:batch+16]):
        im = ImageOps.exif_transpose(Image.open(file))
        im.thumbnail((284, 258))
        x, y = (j % 4)*300, (j // 4)*300
        sheet.paste(im, (x+(300-im.width)//2, y))
        draw.text((x+8, y+263), f'{batch+j+1}: {file.stem}', fill='#111111')
    path = out / f'photos-{batch//16+1}.jpg'
    sheet.save(path)
    print(path)
