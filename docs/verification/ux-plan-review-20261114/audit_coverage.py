"""Đối chiếu UX_PLAN từ CSV đã commit; không thay pipeline hoặc dữ liệu sản phẩm."""

import collections
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def read_csv(name):
    with (ROOT / "data/web/stats" / name).open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


def water_group(value):
    return "ready" if value < 10 else "draining" if value < 30 else "still_wet"


def main():
    features = json.loads((ROOT / "data/boundaries/communes_aoi.geojson").read_text())["features"]
    areas = {str(f["properties"]["osm_id"]): float(f["properties"]["area_km2"]) for f in features}
    by_commune = collections.defaultdict(list)
    for row in read_csv("commune_water_by_date.csv"):
        by_commune[row["osm_id"]].append(row)
    counters = {name: collections.Counter() for name in (
        "current", "plan_guard_selected", "true_area_latest_per_track", "true_area_all_acquisitions"
    )}
    partial = []
    for oid, rows in by_commune.items():
        latest = {}
        for row in rows:
            if float(row["valid_km2"]) < 5:
                continue
            old = latest.get(row["track"])
            if old is None or row["date"] > old["date"]:
                latest[row["track"]] = row
        if not latest:
            continue
        best = max(float(row["valid_km2"]) for row in latest.values())
        current = max(
            (row for row in latest.values() if float(row["valid_km2"]) >= 0.5 * best),
            key=lambda row: row["date"],
        )
        observed = 100 * float(current["valid_km2"]) / areas[oid]
        group = water_group(float(current["water_pct"]))
        counters["current"][group] += 1
        counters["plan_guard_selected"][group if observed >= 50 else "partial"] += 1
        for policy, candidates in (
            ("true_area_latest_per_track", list(latest.values())),
            ("true_area_all_acquisitions", rows),
        ):
            eligible = [row for row in candidates if float(row["valid_km2"]) >= 5
                        and float(row["valid_km2"]) >= 0.5 * areas[oid]]
            selected = max(eligible, key=lambda row: (row["date"], row["track"])) if eligible else None
            counters[policy][water_group(float(selected["water_pct"])) if selected else "partial"] += 1
        if observed < 50:
            partial.append({
                "osm_id": oid, "name": current["commune"], "area_km2": areas[oid],
                "selected_valid_km2": float(current["valid_km2"]),
                "selected_observed_pct": round(observed, 4),
                "best_latest_observed_pct": round(100 * best / areas[oid], 4),
                "selected_date": current["date"], "selected_track": current["track"],
                "current_status": group,
            })
    hls = read_csv("vs_dswx_hls.csv")
    swot = read_csv("vs_swot.csv")
    paired = [row for row in swot if row["nisar_f1_same_px"] and row["s1_f1"]]
    result = {
        "source_counts": {"boundaries": len(areas), "series": sum(map(len, by_commune.values())),
                          "sowing": len(read_csv("sowing_check.csv"))},
        "old_counts": dict(collections.Counter(row["status"] for row in read_csv("sowing_check.csv"))),
        "policies": {name: dict(counts) for name, counts in counters.items()},
        "partial_selected": sorted(partial, key=lambda row: row["selected_observed_pct"]),
        "hls": {"rows": len(hls), "unique_dates": len({row["key"][:10] for row in hls}),
                "wins": sum(float(row["nisar"]) > float(row["s1"]) for row in hls)},
        "swot": {"rows": len(swot), "comparable_rows": len(paired),
                 "same_pixel_wins": sum(float(row["nisar_f1_same_px"]) > float(row["s1_f1"])
                                        for row in paired)},
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
