# Builds mideast.json for Ganjoor No: land (minus big lakes) and a few rivers, clipped and projected.
# Source: Natural Earth 1:50m (public domain). Run: python3 build_me.py
import json, math
from shapely.geometry import shape, box, mapping
from shapely.ops import unary_union
LON0, LON1, LAT0, LAT1 = 26, 70, 17, 44
K = 24
C = math.cos(math.radians((LAT0 + LAT1) / 2))
W = round((LON1 - LON0) * K * C); H = round((LAT1 - LAT0) * K)
def P(lon, lat): return ((lon - LON0) * K * C, (LAT1 - lat) * K)
clip = box(LON0 - 1, LAT0 - 1, LON1 + 1, LAT1 + 1)
land = unary_union([shape(f["geometry"]).buffer(0) for f in json.load(open("ne_50m_land.geojson"))["features"]]).intersection(clip)
lakes = unary_union([shape(f["geometry"]).buffer(0) for f in json.load(open("ne_50m_lakes.geojson"))["features"] if shape(f["geometry"]).area > 0.3]).intersection(clip)
land = land.difference(lakes).simplify(0.06)
def ring(coords):
    pts = [P(x, y) for x, y in coords]
    return "M" + "L".join(f"{x:.0f},{y:.0f}" for x, y in pts) + "Z"
def poly_path(g):
    out = []
    for p in getattr(g, "geoms", [g]):
        if p.geom_type != "Polygon" or p.area < 0.05: continue
        out.append(ring(p.exterior.coords) + "".join(ring(i.coords) for i in p.interiors))
    return "".join(out)
rivers = []
for f in json.load(open("ne_50m_rivers_lake_centerlines.geojson"))["features"]:
    name = (f["properties"].get("name") or "")
    if name not in ("Nile", "Euphrates", "Tigris", "Amu Darya", "Syr Darya", "Karun", "Helmand", "Indus", "Kura", "Aras", "Zeravshan"): continue
    g = shape(f["geometry"]).intersection(clip).simplify(0.05)
    for l in getattr(g, "geoms", [g]):
        if l.geom_type != "LineString" or l.length < 0.5: continue
        pts = [P(x, y) for x, y in l.coords]
        rivers.append("M" + "L".join(f"{x:.0f},{y:.0f}" for x, y in pts))
out = {"source": "Natural Earth 1:50m (public domain), built by build_me.py", "bbox": [LON0, LON1, LAT0, LAT1], "k": K, "c": round(C, 6), "w": W, "h": H, "land": poly_path(land), "rivers": "".join(rivers)}
json.dump(out, open("mideast.json", "w"), ensure_ascii=False, separators=(",", ":"))
print(W, H, len(out["land"]), len(out["rivers"]))
