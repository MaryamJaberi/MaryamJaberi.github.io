import json, urllib.request, time
from shapely.geometry import shape, mapping
from shapely.ops import unary_union
AGES = {"rodinia":1000,"ediacaran":575,"cambrian":520,"devonian":390,"carboniferous":310,"permian":260,"end-permian":252,"jurassic":160,"cretaceous":90,"kpg":66,"eocene":50}
out = {}
for era, age in AGES.items():
    url = f"https://gws.gplates.org/reconstruct/coastlines/?time={age}&model=MERDITH2021"
    d = json.load(urllib.request.urlopen(url, timeout=120))
    rings = []
    parts = []
    for f in d["features"]:
        try:
            g = shape(f["geometry"]).buffer(0)
        except Exception:
            continue
        if not g.is_empty: parts.append(g)
    # merge the plate fragments so only real outlines are drawn, not every block boundary
    merged = unary_union([p.buffer(0.3) for p in parts]).buffer(-0.3)
    for g in [merged]:
        geoms = getattr(g, "geoms", [g])
        for p in geoms:
            if p.area < 1.2: continue
            s = p.simplify(0.35, preserve_topology=True)
            ext = getattr(s, "exterior", None)
            if ext is None: continue
            pts = [[round(x,1), round(y,1)] for x, y in ext.coords]
            if len(pts) >= 4: rings.append(pts)
    pt = json.load(urllib.request.urlopen(f"https://gws.gplates.org/reconstruct/reconstruct_points/?points=51.4,35.7&time={age}&model=MERDITH2021", timeout=60))
    try:
        c = pt["coordinates"][0] if "coordinates" in pt else pt["features"][0]["geometry"]["coordinates"]
    except Exception:
        c = None
    if c and abs(c[0]) > 360: c = None
    out[era] = {"age": age, "rings": rings, "iran": c}
    print(era, age, len(rings), sum(len(r) for r in rings), c, flush=True)
    time.sleep(1)
js = "/* Present-day coastlines rotated to past positions (Merdith et al. 2021 plate model, via the GPlates Web Service, gws.gplates.org), simplified for the web.\n   iran = where today's Tehran sat at that time. Built by build-paleo.py. */\nwindow.PALEO=" + json.dumps(out, separators=(",",":")) + ";\n"
open("paleo.js","w").write(js)
print(len(js))
