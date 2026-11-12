# -*- coding: utf-8 -*-
"""Rebuild everything in the one order that works.  python3 build/all.py
(Each step is an existing generator; this file only fixes their order so pages are never left half-updated.)"""
import subprocess, sys, os
H = os.path.dirname(os.path.abspath(__file__))
STEPS = [['validate.py'], ['reader.py', 'soc'], ['reader.py', 'phil'], ['reader.py', 'tabar'], ['reader.py', 'tarikh'],
         ['wiki_home.py'], ['iran_page.py'], ['tools_data.py'], ['world.py'], ['lands.py'], ['core_pages.py'], ['library_curate.py'], ['library_page.py'],
         ['collection_page.py'], ['sakht_page.py'], ['sakht_day.py'], ['sakht_work.py'], ['coverage.py'], ['selfmap.py'], ['hidden_bridges.py'], ['story.py'],
         ['review_page.py'], ['flows_page.py'], ['plan_page.py'], ['birds_page.py'], ['why_page.py'], ['log_page.py'], ['crumbs.py'], ['sitemap.py'], ['crumbs.py'], ['atlas_source.py'], ['nav.py'], ['validate.py']]
for st in STEPS:
    r = subprocess.run([sys.executable, os.path.join(H, st[0])] + st[1:], capture_output=True, text=True)
    last = (r.stdout.strip().split('\n') or [''])[-1][:110]
    print(('ok  ' if r.returncode == 0 else 'FAIL'), ' '.join(st).ljust(22), last if r.returncode == 0 else r.stderr.strip().split('\n')[-1][:160])
    if r.returncode: sys.exit(1)
