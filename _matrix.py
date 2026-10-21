# -*- coding: utf-8 -*-
"""Матрица: имитируем браузерные заголовки в curl на одно и то же фото."""
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
URL = ("https://vvm150963-pixel.github.io/upgrade-detailing-ulyanovsk/"
       "%D1%84%D0%BE%D1%82%D0%BE%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE/"
       "%D1%82%D0%BE%D0%BD%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B0.jpg_2K_20261021100844.jpg")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"

variants = [
    ("a) обычный curl (HTTP/1.1, без UA)", []),
    ("b) UA Chrome", ["-A", UA]),
    ("c) Accept-Encoding браузера", ["-H", "Accept-Encoding: gzip, deflate, br, zstd"]),
    ("d) Accept картинки", ["-H", "Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"]),
    ("e) HTTP/2", ["--http2"]),
    ("f) HTTP/1.1 принудительно", ["--http1.1"]),
    ("g) всё вместе", ["--http2", "-A", UA,
                       "-H", "Accept-Encoding: gzip, deflate, br, zstd",
                       "-H", "Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"]),
]

for name, extra in variants:
    r = subprocess.run(["curl", "-s", "-o", "nul", "-w", "%{http_code}", "--max-time", "20"] + extra + [URL],
                       capture_output=True, text=True)
    print(f"{name}: {r.stdout.strip()} {r.stderr.strip()[:60]}")
