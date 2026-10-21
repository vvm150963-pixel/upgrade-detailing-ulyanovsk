# -*- coding: utf-8 -*-
"""Добавляет к корневым путям страницы параметр версии (?v=...) — сбрасывает кеш 404 на CDN."""
import re

p = r"страница-А-гранат-v2/index.html"
V = "v=20261021b"

s = open(p, encoding="utf-8").read()

def bump(path):
    if path.startswith(("/фотовидео/", "/страница-А-гранат/")):
        return path + "?" + V
    return path

s2 = re.sub(r'((?:src|href|poster)=)"([^"]+)"',
            lambda m: m.group(1) + '"%s"' % bump(m.group(2)),
            s)

open(p, "w", encoding="utf-8").write(s2)
print("путей с ?v:", s2.count("?" + V))
