"""Search NASA CMR for NISAR GCOV and OPERA DSWx granules (no login needed for search)."""
import json, re, urllib.parse, urllib.request

CMR = "https://cmr.earthdata.nasa.gov/search/granules.json"


def granules(short_name, bbox, start, end, page_size=2000):
    out, page = [], 1
    while True:
        q = urllib.parse.urlencode({"short_name": short_name, "bounding_box": ",".join(map(str, bbox)), "page_size": page_size,
                                    "page_num": page, "temporal": f"{start}T00:00:00Z,{end}T23:59:59Z"})
        batch = json.load(urllib.request.urlopen(f"{CMR}?{q}", timeout=120))["feed"]["entry"]
        out += batch
        if len(batch) < page_size:
            return out
        page += 1


def https_link(g, suffix):
    return next((l["href"] for l in g["links"] if l["href"].startswith("https") and l["href"].endswith(suffix)), None)


def gcov_acquisitions(bbox, start, end, tracks):
    """Newest version (validated > provisional, then highest CRID) of each (track, date)."""
    sel = {}
    for sn, maturity in [("NISAR_L2_GCOV_PROVISIONAL_V1", "provisional"), ("NISAR_L2_GCOV_V1", "validated")]:
        for g in granules(sn, bbox, start, end):
            t = g["title"]
            trk = next((k for k, pat in tracks.items() if pat in t), None)
            if not trk:
                continue
            crid = re.search(r"_([PX]\d{5})_", t).group(1)
            key = (trk, g["time_start"][:10])
            rank = (maturity == "validated", crid)
            if key not in sel or rank > sel[key]["rank"]:
                sel[key] = dict(track=trk, date=key[1], title=t, url=https_link(g, ".h5"), crid=crid, maturity=maturity, rank=rank)
    return sorted(sel.values(), key=lambda j: (j["date"], j["track"]))
