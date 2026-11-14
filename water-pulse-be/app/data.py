"""Load the static NISAR data package (produced by skyradar-nisar `export_web`) into memory once at startup."""
import csv, json, os
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

_HERE = Path(__file__).resolve().parents[1]
# data folder: $WATER_PULSE_DATA, else ./data (bundled for deploy by scripts/sync_data.sh), else the pipeline output ../data/web
DATA_DIR = Path(os.environ.get("WATER_PULSE_DATA") or next((p for p in (_HERE / "data", _HERE.parent / "data" / "web")
                                                         if (p / "manifest.json").exists()), _HERE / "data"))


def _num(v):
    if v in (None, "", "None"):
        return None
    try:
        f = float(v)
        return int(f) if f.is_integer() and "." not in str(v) else f
    except ValueError:
        return {"True": True, "False": False}.get(v, v)


def _csv(name):
    p = DATA_DIR / "stats" / name
    if not p.exists():
        return []
    with open(p, newline="", encoding="utf-8") as fh:
        return [{k: _num(v) for k, v in r.items()} for r in csv.DictReader(fh)]


def _sowing_row(r):
    """Turn 'latest_dates' / 'water_pct_by_track' strings into a structured per-track list."""
    dates = dict(x.split(":", 1) for x in str(r.pop("latest_dates", "")).split(";") if ":" in x)
    pcts = dict(x.split(":", 1) for x in str(r.pop("water_pct_by_track", "")).split(";") if ":" in x)
    r["per_track"] = [{"track": t, "date": dates.get(t), "water_pct": float(pcts[t])} for t in sorted(pcts)]
    return r


class Store:
    def __init__(self):
        self.manifest = json.loads((DATA_DIR / "manifest.json").read_text(encoding="utf-8"))
        self.communes = json.loads((DATA_DIR / "communes.geojson").read_text(encoding="utf-8"))
        self.by_id = {f["properties"]["osm_id"]: f for f in self.communes["features"]}
        self.series = defaultdict(list)
        for r in _csv("commune_water_by_date.csv"):
            self.series[r["osm_id"]].append(r)
        for v in self.series.values():
            v.sort(key=lambda r: (r["date"], r["track"]))
        self.timing = _csv("commune_flood_timing.csv")
        self.flood_class = {r["osm_id"]: r for r in _csv("commune_flood_class.csv")}
        self.sowing = {r["osm_id"]: _sowing_row(r) for r in _csv("sowing_check.csv")}
        for f in self.communes["features"]:   # numbers in timing come as strings from the CSV export
            t = f["properties"].get("timing") or {}
            if isinstance(t, str):
                t = json.loads(t)
            f["properties"]["timing"] = {trk: {k: _num(v) for k, v in d.items()} for trk, d in t.items()}
        self.swot_series = defaultdict(list)   # SWOT (Ka-band) water % per commune, comparison source
        if (DATA_DIR / "stats" / "commune_swot_by_date.csv").exists():
            for r in _csv("commune_swot_by_date.csv"):
                self.swot_series[r["osm_id"]].append(r)
        cal = DATA_DIR / "stats" / "calibration.json"
        self.validation = dict(calibration=json.loads(cal.read_text(encoding="utf-8")) if cal.exists() else None,
                               vs_dswx_s1=_csv("vs_dswx_s1.csv"), vs_dswx_hls=_csv("vs_dswx_hls.csv"),
                               vs_swot=_csv("vs_swot.csv") if (DATA_DIR / "stats" / "vs_swot.csv").exists() else [])

    def commune_summary(self, oid):
        f = self.by_id[oid]
        p = dict(f["properties"])
        if isinstance(p.get("timing"), str):
            p["timing"] = json.loads(p["timing"])
        p["flood_release"] = self.flood_class.get(oid)
        p["sowing"] = self.sowing.get(oid)
        return p


@lru_cache(maxsize=1)
def store() -> Store:
    return Store()
