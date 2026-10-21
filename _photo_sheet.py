# -*- coding: utf-8 -*-
# Контакт-лист фото Апгрейда: сетка миниатюр с подписями и разрешениями
import os
from PIL import Image, ImageDraw, ImageFont

BASE = r"D:\Z GR\Апгрейд"
FILES = [
    ("фотовидео", "апп.jpg"), ("фотовидео", "броня.jpg"), ("фотовидео", "линзы.jpg"),
    ("фотовидео", "оклейка.jpg"), ("фотовидео", "полировка фар.jpg"), ("фотовидео", "полировка.jpg"),
    ("фотовидео", "сar_ceramic_coating-1__1024.jpg"), ("фотовидео", "тонировка.jpg"),
    ("фотовидео", "химчистка.jpg"), ("фотовидео", "шумоизоляция.jfif"),
    ("фотовидео", "автосвет.jfif"), ("фотовидео", "антиграв.jpg"),
    ("фотовидео", "ремонт стекол.webp"),
    ("страница-А", "assets/vk-1.jpg"), ("страница-А", "assets/vk-2.jpg"),
    ("страница-А", "assets/vk-3.jpg"), ("страница-А", "assets/vk-6.jpg"),
]
TW, TH, PAD, LABEL = 300, 200, 10, 26
cols = 5
rows = (len(FILES) + cols - 1) // cols
W = cols * (TW + PAD) + PAD
H = rows * (TH + LABEL + PAD) + PAD
sheet = Image.new("RGB", (W, H), (24, 24, 28))
d = ImageDraw.Draw(sheet)
try:
    font = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 14)
except Exception:
    font = ImageFont.load_default()

for i, (sub, name) in enumerate(FILES):
    p = os.path.join(BASE, sub, name)
    r, c = divmod(i, cols)
    x = PAD + c * (TW + PAD)
    y = PAD + r * (TH + LABEL + PAD)
    try:
        im = Image.open(p).convert("RGB")
        res = f"{im.width}x{im.height}"
        scale = min(TW / im.width, TH / im.height)
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))))
        sheet.paste(im, (x + (TW - im.width) // 2, y + (TH - im.height) // 2))
        label = f"{name.split('/')[-1][:30]}  {res}"
    except Exception as e:
        d.rectangle([x, y, x + TW, y + TH], fill=(60, 20, 20))
        label = f"{name.split('/')[-1][:30]}  BITO!"
    d.text((x, y + TH + 4), label, fill=(230, 230, 230), font=font)

out = os.path.join(BASE, "_photo_sheet.jpg")
sheet.save(out, quality=86)
print("OK:", out)
