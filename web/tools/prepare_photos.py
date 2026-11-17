from pathlib import Path
from PIL import Image, ImageOps

source = Path(r'C:\Users\mabe8\Desktop\oppo_movil-backup')
out = Path(__file__).resolve().parents[1] / 'dist' / 'assets' / 'images'
out.mkdir(parents=True, exist_ok=True)
excluded = {'IMG20250825163127','IMG20250825163203','IMG20250825163219','IMG20250825163226','IMG20250928233359'}
for file in sorted(source.glob('*.jpg')):
    if file.stem in excluded:
        continue
    im = ImageOps.exif_transpose(Image.open(file)).convert('RGB')
    im.thumbnail((1800,1800))
    im.save(out / (file.stem+'.webp'), quality=83, method=5)
print(f'{len(list(out.glob("*.webp")))} fotos optimizadas; EXIF eliminado; originales conservados.')
