# -*- coding: utf-8 -*-
"""Проверка после переименований: root redirect, чистота старой страницы, site/index."""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

root = open("index.html", encoding="utf-8").read()
print("root redirect ->", "OK /site/" if "site/" in root else "ПРОБЛЕМА: " + root[:100])

s = open(r"site-v2-src\index.html", encoding="utf-8").read()
print("старая страница: кириллических путей осталось =",
      len(re.findall(r'/(?:фотовидео|страница-А)', s)))

si = open(r"site\index.html", encoding="utf-8").read()
print("site/index.html: размер", len(si), "символов;",
      "кириллических путей =", len(re.findall(r'/(?:фотовидео|страница-А)', si)),
      "; ссылок на /media/ =", si.count('"/media/'),
      "; на /assets/ =", si.count('"/assets/'))

demo = open(r"site\demo-okleyka.html", encoding="utf-8").read()
print("demo-okleyka.html: размер", len(demo), "; локальных кириллических путей =",
      len(re.findall(r'/(?:фотовидео|страница-А)', demo)))
