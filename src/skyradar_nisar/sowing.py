"""Water-share assessment from the newest acquisition covering >=50% of the OSM commune.

    python -m skyradar_nisar.sowing [YYYY-MM-DD] [--stats-dir PATH]

Uses processed statistics when available, otherwise committed web CSVs. Publishes the
assessment CSV to data/web/stats and draws fig5 without requiring Earthdata or rasters.
The legacy ready/draining/still_wet codes describe water-share bins, not soil readiness
or a measured recession trend. Water share is relative to the observed area.
"""
import argparse
import csv
import json
import math
from pathlib import Path
from . import config as C

LEVELS = [("ready", 0, 10, "#2f9e44"), ("draining", 10, 30, "#f59f00"), ("still_wet", 30, 101, "#7048e8")]


def status(p):
    return next(name for name, lo, hi, _ in LEVELS if lo <= p < hi)


def assess_communes(rows, features, ref="2026-11-01"):
    areas = {str(f["properties"]["osm_id"]): f["properties"].get("area_km2") for f in features}
    by = {}
    for row in rows:
        if float(row["valid_km2"]) >= 5:
            by.setdefault(str(row["osm_id"]), []).append(row)
    table = []
    for oid, observations in by.items():
        area = float(areas.get(oid) or 0)
        area = area if math.isfinite(area) and area > 0 else None
        latest = {}
        for r in observations:
            if r["track"] not in latest or r["date"] > latest[r["track"]]["date"]:
                latest[r["track"]] = r
        eligible = [r for r in observations if area and float(r["valid_km2"]) >= 0.5 * area]
        best = max(float(r["valid_km2"]) for r in latest.values())
        fallback = [r for r in latest.values() if float(r["valid_km2"]) >= 0.5 * best]
        selected = max(eligible or fallback, key=lambda r: (r["date"], float(r["valid_km2"]), r["track"]))
        worst = max(latest.values(), key=lambda r: float(r["water_pct"]))
        pct = float(selected["water_pct"])
        observed = 100 * float(selected["valid_km2"]) / area if area else None
        covered_tracks = [r for r in latest.values() if area and float(r["valid_km2"]) >= 0.5 * area]
        table.append(dict(
            osm_id=oid, commune=selected["commune"], province=selected["province"], ref_date=ref,
            area_km2=area, observed_pct=round(observed, 6) if observed is not None else None,
            latest_dates=";".join(f"{t}:{r['date']}" for t, r in sorted(latest.items())),
            water_pct_by_track=";".join(f"{t}:{float(r['water_pct']):.1f}" for t, r in sorted(latest.items())),
            status_track=selected["track"], status_date=selected["date"], status_pct=round(pct, 1),
            status=status(pct) if eligible else "partial",
            worst_track=worst["track"], worst_date=worst["date"], worst_pct=float(worst["water_pct"]),
            worst_status=status(float(worst["water_pct"])),
            tracks_agree=len(covered_tracks) >= 2 and len({status(float(r["water_pct"])) for r in covered_tracks}) == 1,
        ))
    return sorted(table, key=lambda r: (-r["status_pct"], r["osm_id"]))


def draw_map(table, fc):
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    from shapely.geometry import shape
    from shapely.ops import unary_union

    st = {str(r["osm_id"]): r for r in table}
    colors = {name: color for name, _, _, color in LEVELS} | {"partial": "#cbd5e1"}
    fig, ax = plt.subplots(figsize=(10.5, 6.2))
    for f in fc["features"]:
        g = shape(f["geometry"])
        r = st.get(str(f["properties"]["osm_id"]))
        col = colors[r["status"]] if r else "#f1f5f9"
        for poly in (g.geoms if g.geom_type == "MultiPolygon" else [g]):
            ax.fill(*poly.exterior.xy, color=col, alpha=.85, lw=0)
            ax.plot(*poly.exterior.xy, color="white", lw=.4)
    for r in [r for r in table if r["status"] != "partial"][:6]:
        f = next(x for x in fc["features"] if str(x["properties"]["osm_id"]) == r["osm_id"])
        c = shape(f["geometry"]).representative_point()
        ax.annotate(f"{r['commune'].replace('Xã ', '').replace('Phường ', '')}\n{r['status_pct']:.0f}%", (c.x, c.y), fontsize=6.5, ha="center")
    W, S, E, N = unary_union([shape(f["geometry"]) for f in fc["features"]]).bounds
    ax.set_aspect(1 / np.cos(np.radians(10.6)))
    ax.set_xlim(W - .01, E + .01); ax.set_ylim(S - .01, N + .01)
    labels = {"ready": "low (<10%)", "draining": "moderate (10–<30%)", "still_wet": "high (>=30%)"}
    ax.legend(handles=[Patch(color=c, label=f"{labels[n]} observed water") for n, lo, hi, c in LEVELS] +
              [Patch(color=colors["partial"], label="insufficient commune coverage"), Patch(color="#f1f5f9", label="no assessment")],
              fontsize=7, loc="upper left", bbox_to_anchor=(1.01, 1.0), frameon=False)
    assessed = [r for r in table if r["status"] != "partial"]
    dates = sorted(r["status_date"] for r in assessed)
    period = f"{dates[0]} – {dates[-1]}" if dates else "no eligible acquisitions"
    ax.set_title(f"Latest water share: {len(assessed)} communes with >=50% area observed ({period})\n"
                 "Water share refers to observed area; not a sowing recommendation. © OpenStreetMap contributors", fontsize=9)
    ax.set_xticks([]); ax.set_yticks([])
    fig.tight_layout(); (C.ROOT / "docs/figures").mkdir(parents=True, exist_ok=True)
    fig.savefig(C.ROOT / "docs/figures/fig5_sowing_check.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def main(ref="2026-11-01", stats_dir=None):
    stats = Path(stats_dir) if stats_dir else next(
        p for p in [C.PROCESSED / "stats", C.WEB / "stats"] if (p / "commune_water_by_date.csv").exists())
    with (stats / "commune_water_by_date.csv").open(encoding="utf-8", newline="") as source:
        rows = list(csv.DictReader(source))
    fc = json.loads((C.DATA / "boundaries/communes_aoi.geojson").read_text(encoding="utf-8"))
    table = assess_communes(rows, fc["features"], ref)
    if not table:
        raise ValueError("No observations with at least 5 km2; assessment was not overwritten")
    for target in {stats / "sowing_check.csv", C.WEB / "stats/sowing_check.csv"}:
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(table[0]), lineterminator="\n"); w.writeheader(); w.writerows(table)
    counts = {name: sum(r["status"] == name for r in table) for name in ["ready", "draining", "still_wet", "partial"]}
    print("Assessment counts:", counts)
    draw_map(table, fc)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ref", nargs="?", default="2026-11-01")
    parser.add_argument("--stats-dir", type=Path)
    args = parser.parse_args()
    main(args.ref, args.stats_dir)
