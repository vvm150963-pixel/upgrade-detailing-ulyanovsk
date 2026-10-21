# -*- coding: utf-8 -*-
"""Финальная проверка фото кейсов и ленты на GitHub Pages."""
import subprocess
import sys
import urllib.parse

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BASE = "https://vvm150963-pixel.github.io/upgrade-detailing-ulyanovsk/%D1%84%D0%BE%D1%82%D0%BE%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE/"

files = [
    "кузов_до.png_2K_20261021120810.jpg",
    "кузов_после.png_2K_20261021121120.jpg",
    "фара_до.png_2K_20261021121729.jpg",
    "фара_после.png_2K_20261021122215.jpg",
    "хим_до.jpg_2K_20261021122550.jpg",
    "хим1_после.jpg_2K_20261021123031.jpg",
    "тонировка.jpg_2K_20261021100844.jpg",
]

fails = 0
for name in files:
    url = BASE + urllib.parse.quote(name)
    r = subprocess.run(["curl", "-s", "-o", "nul", "-w", "%{http_code}", "-I", url],
                       capture_output=True, text=True, timeout=30)
    code = r.stdout.strip()
    print(f"  {code}  {name}")
    if not code.startswith("2"):
        fails += 1

print("Готово:", "все фото живые" if fails == 0 else f"НЕ работающих: {fails}")
