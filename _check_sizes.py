import glob, os
from PIL import Image

files = [
    r'D:\Z GR\Апгрейд\фотовидео',
]
for d in files:
    for p in sorted(glob.glob(os.path.join(d, '*'))):
        n = os.path.basename(p)
        if not any(ext in n.lower() for ext in ('.jpg', '.webp', '.png')):
            continue
        try:
            w, h = Image.open(p).size
            mark = '4:3' if abs(w / h - 4 / 3) < 0.02 else ''
            print(f'{w}x{h}  {w / h:.2f}  {mark:4} {n}')
        except Exception as e:
            print('ERR', n, e)
