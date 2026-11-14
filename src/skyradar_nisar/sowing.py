"""Sowing-readiness check per commune: water on the latest image of each track around the sowing window.

    python -m skyradar_nisar.sowing [YYYY-MM-DD]     # reference date, default 2026-11-01 (An Giang winter-spring window)
Outputs: data/processed/stats/sowing_check.csv, docs/figures/fig5_sowing_check.png
Status rule (per commune): the MOST RECENT image among tracks covering >= 50 % of the commune (worst case across tracks kept as worst_*):
  still_wet  >= 30 % of the commune under water on the latest image
  draining   10-30 %
  ready      < 10 %
"""
import csv, json, sys
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from shapely.geometry import shape
from . import config as C

LEVELS = [("ready", 0, 10, "#2f9e44"), ("draining", 10, 30, "#f59f00"), ("still_wet", 30, 101, "#7048e8")]


def status(p):
    return next(name for name, lo, hi, _ in LEVELS if lo <= p < hi)


def main(ref="2026-11-01"):
    rows = list(csv.DictReader(open(C.PROCESSED / "stats/commune_water_by_date.csv")))
    latest = {}
    for r in rows:
        if float(r["valid_km2"]) < 5:
            continue
        k = (r["osm_id"], r["track"])
        if k not in latest or r["date"] > latest[k]["date"]:
            latest[k] = r
    out = {}
    for (oid, trk), r in latest.items():
        e = out.setdefault(oid, dict(osm_id=oid, commune=r["commune"], province=r["province"], per_track={}))
        e["per_track"][trk] = (r["date"], float(r["water_pct"]), float(r["valid_km2"]))
    table = []
    for e in out.values():
        pt = e["per_track"]
        worst_trk, (wd, wp, _) = max(pt.items(), key=lambda kv: kv[1][1])
        # status = most recent image among tracks that cover >= 50 % of the best-covered track (avoid edge slivers)
        cover = max(v[2] for v in pt.values())
        cur_trk, (d, p, _) = max(((t, v) for t, v in pt.items() if v[2] >= 0.5 * cover), key=lambda kv: kv[1][0])
        table.append(dict(osm_id=e["osm_id"], commune=e["commune"], province=e["province"], ref_date=ref,
                          latest_dates=";".join(f"{t}:{v[0]}" for t, v in sorted(pt.items())),
                          water_pct_by_track=";".join(f"{t}:{v[1]:.1f}" for t, v in sorted(pt.items())),
                          status_track=cur_trk, status_date=d, status_pct=round(p, 1), status=status(p),
                          worst_track=worst_trk, worst_date=wd, worst_pct=round(wp, 1), worst_status=status(wp),
                          tracks_agree=len({status(v[1]) for v in pt.values()}) == 1))
    table.sort(key=lambda r: -r["status_pct"])
    with open(C.PROCESSED / "stats/sowing_check.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(table[0])); w.writeheader(); w.writerows(table)
    cnt = {name: sum(r["status"] == name for r in table) for name, *_ in LEVELS}
    print("communes:", len(table), cnt, "| tracks agree on status:", sum(r["tracks_agree"] for r in table))
    for r in table[:10]:
        print(f"  {r['commune']:22s} {r['province']:18s} {r['water_pct_by_track']}  -> {r['status']}")

    # map
    fc = json.loads((C.DATA / "boundaries" / "communes_aoi.geojson").read_text())
    st = {int(r["osm_id"]): r for r in table}
    fig, ax = plt.subplots(figsize=(10.5, 6.2))
    for f in fc["features"]:
        g = shape(f["geometry"]); r = st.get(f["properties"]["osm_id"])
        col = next(c for n, *_, c in LEVELS if r and n == r["status"]) if r else "#e9ecef"
        for poly in (g.geoms if g.geom_type == "MultiPolygon" else [g]):
            ax.fill(*poly.exterior.xy, color=col, alpha=.85, lw=0)
            ax.plot(*poly.exterior.xy, color="white", lw=.4)
    for r in table[:6]:
        f = next(x for x in fc["features"] if str(x["properties"]["osm_id"]) == str(r["osm_id"]))
        c = shape(f["geometry"]).representative_point()
        ax.annotate(f"{r["commune"].replace("Xã ", "").replace("Phường ", "")}\n{r["status_pct"]:.0f}%", (c.x, c.y), fontsize=6.5, ha="center")
    from shapely.ops import unary_union
    W, S, E, N = unary_union([shape(f["geometry"]) for f in fc["features"] if f["properties"]["osm_id"] in st]).bounds
    ax.set_aspect(1 / np.cos(np.radians(10.6))); ax.set_xlim(W - .01, E + .01); ax.set_ylim(S - .01, N + .01)
    ax.legend(handles=[Patch(color=c, label=f"{n.replace('_', ' ')} ({lo}–{min(hi, 100)} % water)") for n, lo, hi, c in LEVELS] +
              [Patch(color="#e9ecef", label="no data")], fontsize=7, loc="upper left", bbox_to_anchor=(1.01, 1.0), frameon=False)
    ax.set_title(f"Sowing readiness on the latest NISAR images (27 Oct – 3 Nov 2026), window opens {ref}\n"
                 "status from the most recent image covering the commune; © OpenStreetMap contributors", fontsize=9)
    ax.set_xticks([]); ax.set_yticks([])
    fig.tight_layout(); (C.ROOT / "docs" / "figures").mkdir(parents=True, exist_ok=True)
    fig.savefig(C.ROOT / "docs" / "figures" / "fig5_sowing_check.png", dpi=150)


if __name__ == "__main__":
    main(*sys.argv[1:2])
