# -*- coding: utf-8 -*-
"""Собирает _deploy: страница + медиа с английскими именами (без кириллицы в путях)."""
import re
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(r"D:\Z GR\Апгрейд")
DEP = ROOT / "_deploy"

if DEP.exists():
    shutil.rmtree(DEP)
(DEP / "media").mkdir(parents=True)
(DEP / "assets").mkdir(parents=True)

# 1. путь -> красивое английское имя
SPECIAL = {
    "/фотовидео/сar_ceramic_coating-1__1024.jpg_2K_20261021100603.jpg": "keramika.jpg",
    "/фотовидео/Sports_running_engine_2K_20261019180542.jpg": "asphalt_base.jpg",
}
TRANSLIT = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e", "ж": "zh",
    "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o",
    "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f", "х": "h", "ц": "c",
    "ч": "ch", "ш": "sh", "щ": "sch", "ъ": "", "ы": "y", "ь": "", "э": "e",
    "ю": "yu", "я": "ya",
}

def ascii_name(src):
    if src in SPECIAL:
        return SPECIAL[src]
    stem = Path(src).stem.split(".")[0]  # срезаем .jpg_2K_метку
    ext = Path(src).suffix.lower() or ".jpg"
    name = "".join(TRANSLIT.get(ch, ch if ch.isascii() and (ch.isalnum() or ch == "_") else "_") for ch in stem.lower())
    while "__" in name:
        name = name.replace("__", "_")
    return name + ext

page = (ROOT / "страница-А-гранат-v2" / "index.html").read_text(encoding="utf-8")
paths = sorted(set(re.findall(r'/(?:фотовидео|страница-А-гранат/assets)/[^"?]+', page)))
# + фон из JS (encodeURI)
paths += ["/фотовидео/Sports_running_engine_2K_20261019180542.jpg"]
mapping = {}
for src in paths:
    if src.startswith("/фотовидео/"):
        fname = ascii_name(src)
        shutil.copy2(ROOT / src.lstrip("/"), DEP / "media" / fname)
        mapping[src] = "/media/" + fname
    else:
        fname = Path(src).name
        shutil.copy2(ROOT / src.lstrip("/"), DEP / "assets" / fname)
        mapping[src] = "/assets/" + fname

# 2. новая страница с ASCII-путями
out = page
for old, new in mapping.items():
    out = out.replace(old + "?v=20261021b", new).replace(old, new)
out = out.replace("?v=20261021b", "")  # версии больше не нужны
(DEP / "index.html").write_text(out, encoding="utf-8")

# 3. конфигуратор плёнки
shutil.copy2(ROOT / "demo-okleyka.html", DEP / "demo-okleyka.html")

# 4. корневой index: редирект на deploy
(ROOT / "index.html").write_text(
    '<!DOCTYPE html><meta charset="utf-8">'
    '<meta http-equiv="refresh" content="0; url=deploy/">'
    '<script>location.replace("deploy/");</script>'
    '<p><a href="deploy/">UPGRADE — открыть сайт</a></p>', encoding="utf-8")

print("скопировано файлов:", len(mapping) + 2)
for old, new in sorted(mapping.items()):
    print(f"  {new}  <-  {old}")
print("проверка путей в новой странице: кириллицы в src/href =",
      len(re.findall(r'(?:src|href)="[^"]*/(?:фотовидео|страница-А)', out)))
