#!/usr/bin/env python3
"""Publish an explicit allowlist; historical HTML and source files stay private to deployment."""
from pathlib import Path
import re, shutil, json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_site'
if OUT.exists():shutil.rmtree(OUT)
OUT.mkdir()
for name in ['index.html','index.en.html','index.ko.html']:
    page=ROOT/name;shutil.copy2(page,OUT/name)
    for asset in re.findall(r'(?:src|href)="([^"]+\.(?:css|js))"',page.read_text()):
        shutil.copy2(ROOT/asset,OUT/asset)
shutil.copytree(ROOT/'assets',OUT/'assets')
# Compatibility URLs only redirect to the selected presentation; they never serve v1.
for page in [*ROOT.glob('version2*.html'),*ROOT.glob('projects/*.html')]:
    dest=OUT/page.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(page,dest)
assert not (OUT/'archive').exists()
print('Packaged only the selected portfolio, runtime assets and compatibility redirects.')
