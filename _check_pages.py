# -*- coding: utf-8 -*-
"""Проверка: все корневые пути страницы и все файлы в репо должны отвечать 200 на GitHub Pages."""
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(r"D:\Z GR\Апгрейд")
BASE = "https://vvm150963-pixel.github.io/upgrade-detailing-ulyanovsk/"

# 1. пути, на которые ссылается страница v2
html = (ROOT / "страница-А-гранат-v2" / "index.html").read_text(encoding="utf-8")
used = set(re.findall(r'(?:src|href|poster)=["\'](/[^"\']+)', html))
print(f"страница ссылается на {len(used)} корневых путей")

# 2. реальные файлы проекта (кроме служебных)
skip_dirs = {".git", ".taste-skill", "страница-А", "страница-А-гранат", "inspect"}
files = set()
for p in ROOT.rglob("*"):
    if p.is_file():
        rel = p.relative_to(ROOT).as_posix()
        if not rel.startswith(tuple(skip_dirs)) and rel not in ("_agents_log.py", "_check_sizes.py", "_fix_prices.py", "_photo_sheet.py", "_photo_sheet.jpg", "ЗАПРОС-клиенту.md", ".gitignore"):
            files.add("/" + urllib.parse.quote(rel))

bad = []
for path in sorted(used | files):
    url = BASE + path
    try:
        r = subprocess.run(["curl", "-s", "-o", "nul", "-w", "%{http_code}", "-I", url],
                           capture_output=True, text=True, timeout=30)
        code = r.stdout.strip()
    except Exception as e:
        code = "ERR " + str(e)[:40]
    if not code.startswith("2"):
        bad.append((code, path))

print("ИТОГ:", "все в порядке" if not bad else f"{len(bad)} битых путей:")
for code, path in bad:
    print(f"  {code}  {path}")
