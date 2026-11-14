"""Download 2025 commune boundaries (OpenStreetMap, admin_level=6 after the district level was abolished).

    python -m skyradar_nisar.communes
Uses Overpass (tags only, fast) then Nominatim `lookup` for polygons (<= 50 ids/request).
Data (c) OpenStreetMap contributors, ODbL 1.0.
"""
import json, time, urllib.parse, urllib.request
from shapely.geometry import shape, mapping
from . import config as C

OVERPASS = ["https://overpass.kumi.systems/api/interpreter", "https://overpass-api.de/api/interpreter"]
UA = {"User-Agent": "skyradar-nisar/0.1 (NASA Space Apps 2026)"}


def _overpass(q):
    for url in OVERPASS:
        try:
            req = urllib.request.Request(url, data=urllib.parse.urlencode({"data": q}).encode(), headers=UA)
            return json.load(urllib.request.urlopen(req, timeout=200))
        except Exception as ex:
            print("overpass failed", url, ex)
    raise RuntimeError("all Overpass endpoints failed")


def main():
    W, S, E, N = C.AOI
    els = _overpass(f'[out:json][timeout:150];rel["boundary"="administrative"]["admin_level"~"^(4|6)$"]({S},{W},{N},{E});out tags;')["elements"]
    vn = [e for e in els if not e["tags"].get("name", "").startswith(("ខេត្ត", "ឃុំ", "ស្រុក"))]  # drop Cambodian units
    tags = {e["id"]: e["tags"] for e in vn}
    geo = {}
    ids = list(tags)
    for i in range(0, len(ids), 50):
        q = urllib.parse.urlencode({"osm_ids": ",".join(f"R{x}" for x in ids[i:i + 50]), "format": "geojson", "polygon_geojson": 1})
        fc = json.load(urllib.request.urlopen(urllib.request.Request("https://nominatim.openstreetmap.org/lookup?" + q, headers=UA), timeout=120))
        for f in fc["features"]:
            geo[f["properties"]["osm_id"]] = shape(f["geometry"])
        time.sleep(2)
    prov = {k: g for k, g in geo.items() if tags[k]["admin_level"] == "4"}
    feats = []
    for k, g in geo.items():
        if tags[k]["admin_level"] != "6" or g.geom_type not in ("Polygon", "MultiPolygon"):
            continue
        p = next((tags[pk]["name"] for pk, pg in prov.items() if g.representative_point().within(pg)), None)
        if p is None:   # outside Vietnam (e.g. Cambodian districts with Latin names)
            continue
        feats.append({"type": "Feature", "properties": {"osm_id": k, "name": tags[k]["name"], "province": p,
                                                        "wikidata": tags[k].get("wikidata")}, "geometry": mapping(g)})
    out = C.DATA / "boundaries"; out.mkdir(parents=True, exist_ok=True)
    (out / "communes_aoi.geojson").write_text(json.dumps({"type": "FeatureCollection", "features": feats}, ensure_ascii=False), encoding="utf-8")
    print(len(feats), "communes written")


if __name__ == "__main__":
    main()
