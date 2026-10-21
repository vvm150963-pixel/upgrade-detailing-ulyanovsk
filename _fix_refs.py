# -*- coding: utf-8 -*-
"""Дочинка: root redirect -> /site/, старая страница -> photos/ и granat-v1/."""
import re

root = open("index.html", encoding="utf-8").read().replace("deploy/", "site/")
open("index.html", "w", encoding="utf-8").write(root)

p = r"site-v2-src\index.html"
s = (open(p, encoding="utf-8").read()
     .replace("/фотовидео/", "/photos/")
     .replace("/страница-А-гранат/", "/granat-v1/")
     .replace("?v=20261021b", ""))
open(p, "w", encoding="utf-8").write(s)

print("root redirect ->", "site/" if 'url=site/' in root else 'НЕ ОК')
print("кириллических путей в старой странице осталось =",
      len(re.findall(r'/(?:фотовидео|страница-А)', s)))
