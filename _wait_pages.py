# -*- coding: utf-8 -*-
"""Ждём окончания сборки Pages и проверяем фото до/после."""
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
GH = r"C:\Program Files\GitHub CLI\gh.exe"
API = "repos/vvm150963-pixel/upgrade-detailing-ulyanovsk/pages/builds/latest"

for i in range(40):
    r = subprocess.run([GH, "api", API, "--jq", ".status"], capture_output=True, text=True)
    status = r.stdout.strip()
    print(f"{i*15}с: {status}")
    if status in ("built", "errored"):
        break
    time.sleep(15)

r = subprocess.run([GH, "api", API, "--jq", "{status: .status, error: .error.message, commit: .commit}"],
                   capture_output=True, text=True)
print(r.stdout.strip())
