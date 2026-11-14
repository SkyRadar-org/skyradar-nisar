"""Adapter for water-pulse-fe. Original API responses remain unchanged."""
import datetime as dt
from collections import defaultdict
from functools import lru_cache
from typing import Literal

from fastapi import APIRouter, HTTPException

from .data import store

router = APIRouter(prefix="/api/frontend", tags=["frontend"])
Track = Literal["047D", "083A", "148D"]


def _composite_of(key: str):
    c = store().composites.get(key)
    if c is None:
        return None
    v = f"?v={store().composite_version}"
    return dict(png=f"/static/{c['png']}{v}", simplePng=f"/static/{c['simple_png']}{v}", radar=f"/static/{c['radar']}{v}",
                maxAgeDays=store().composite_max_age,
                observedPct=c["observed_pct"], sources=c["sources"])


@router.get("/scenes")
def scenes():
    m = store().manifest
    (s, w), (n, e) = m["bounds"]
    return [dict(date=f["date"], track=f["track"], maturity=f["maturity"],
                 bounds=[w, s, e, n], waterPng=f"/static/{f['png']}",
                 radarJpg=f"/static/{f['radar_jpg']}" if f.get("radar_jpg") else None,
                 gibsDate=f.get("gibs_date", f["date"]),
                 composite=_composite_of(f["key"])) for f in m["frames"]]


@lru_cache(maxsize=1)
def commune_collection():
    data = store()
    features = []
    for feature in data.communes["features"]:
        p = feature["properties"]
        oid = p["osm_id"]
        rows = data.series[oid]
        sowing = data.sowing.get(oid)
        # The data team's sowing assessment selects the latest >=50%-covered image.
        # No assessment means insufficient coverage, never a dry/no-flood observation.
        last = next((r for r in rows if sowing and r["track"] == sowing["status_track"]
                     and r["date"] == sowing["status_date"]), None)
        if last is None and rows:
            last = max(rows, key=lambda r: (r["date"], r["valid_km2"]))
        track = last["track"] if last else None
        timing = p.get("timing", {}).get(track, {})
        track_rows = [r for r in rows if r["track"] == track]
        peak = max(track_rows, key=lambda r: r["water_pct"], default=None)
        peak_pct = timing.get("peak_pct", peak["water_pct"] if peak else None)
        status = {"ready": "receded", "draining": "uncertain", "still_wet": "not_receded"}.get(
            sowing["status"] if sowing else None, "uncertain")
        area = p.get("area_km2")
        observed = 100 * last["valid_km2"] / area if last and area and area > 0 else None
        sufficient = bool(sowing and sowing["status"] != "partial" and observed is not None and observed >= 50)
        if not sufficient:
            status = "uncertain"
        if sufficient and peak_pct is not None and peak_pct < 5:
            status = "no_flood"
        props = dict(osm_id=str(oid), name=p["name"], province=p["province"],
                     area_km2=area, observed_pct=round(observed, 6) if observed is not None else None,
                     valid_km2=last["valid_km2"] if last else None,
                     first_flood_date=timing.get("first_date_ge20pct"),
                     peak_pct=peak_pct, peak_date=timing.get("peak_date", peak["date"] if peak else None),
                     half_date=timing.get("halved_after_peak"),
                     recession_date=timing.get("halved_after_peak"),
                     last_pct=last["water_pct"] if last else None, last_date=last["date"] if last else None,
                     max_flooded_km2=max((r["water_km2"] for r in track_rows), default=None),
                     status=status, reference_track=track, coverage_sufficient=sufficient)
        features.append(dict(type="Feature", id=str(oid), properties=props, geometry=feature["geometry"]))
    return dict(type="FeatureCollection", features=features)


@router.get("/communes")
def communes():
    return commune_collection()


@router.get("/communes/{osm_id}/series")
def series(osm_id: int):
    if osm_id not in store().by_id:
        raise HTTPException(404, "Commune not found")
    return [{k: r[k] for k in ("date", "track", "water_pct", "water_km2", "valid_km2")}
            for r in store().series[osm_id]]


@router.get("/choropleth")
def choropleth(date: str, track: Track):
    if not any(f["date"] == date and f["track"] == track for f in store().manifest["frames"]):
        raise HTTPException(404, "Scene not found")
    return {str(oid): r["water_pct"] for oid, rows in store().series.items()
            for r in rows if r["date"] == date and r["track"] == track}


@router.get("/choropleth/composite")
def choropleth_composite(date: str, track: Track):
    """Playback companion of the mosaic: per commune, its latest observation on or before (date, track) that covers
    >= 50 % of the commune's best-covered pass and is at most max_age days old. Returns {osm_id: {pct, age, date, track}}."""
    if not any(f["date"] == date and f["track"] == track for f in store().manifest["frames"]):
        raise HTTPException(404, "Scene not found")
    now = dt.date.fromisoformat(date)
    max_age = store().composite_max_age
    out = {}
    for oid, rows in store().series.items():
        best_valid = max((r["valid_km2"] for r in rows), default=0)
        eligible = [r for r in rows if (r["date"], r["track"]) <= (date, track) and r["valid_km2"] >= 0.5 * best_valid]
        if not eligible:
            continue
        r = max(eligible, key=lambda x: (x["date"], x["track"]))
        age = (now - dt.date.fromisoformat(r["date"])).days
        if age <= max_age:
            out[str(oid)] = dict(pct=r["water_pct"], age=age, date=r["date"], track=r["track"])
    return out


@router.get("/area")
def area():
    totals = defaultdict(float)
    for rows in store().series.values():
        for r in rows:
            totals[r["date"], r["track"]] += r["water_km2"]
    # Validation is measured on a different overlap; do not invent full-area DSWx totals.
    return [dict(date=d, track=t, nisar_km2=round(v, 2), dswx_km2=None)
            for (d, t), v in sorted(totals.items())]


@router.get("/summary")
def summary():
    # Committed timing PNGs combine tracks. Omit them until per-track exports exist.
    return []


@router.get("/validation")
def validation():
    v = store().validation
    hls = []
    for r in v["vs_dswx_hls"]:
        date, track = r["key"].split("_")
        hls.append(dict(date=date, track=track, f1_nisar=r["nisar"], f1_s1=r["s1"],
                        recall_nisar=r["nisar_recall"], recall_s1=r["s1_recall"],
                        precision_nisar=None, precision_s1=None,
                        nisar_only_true_pct=r["nisar_only_is_optical_water_pct"]))
    s1 = [dict(date=r["key"].split("_")[0], track=r["key"].split("_")[1], f1=r["f1"])
          for r in v["vs_dswx_s1"] if r["role"] == "validation"]
    swot = [dict(swotDate=r["swot_date"], nisar=r["nisar"], daysApart=r["days_apart"], overlapKm2=r["overlap_km2"],
                 swotWaterPct=r["swot_water_pct"], nisarWaterPct=r["nisar_water_pct"],
                 f1_nisar=r["nisar_f1"], f1_s1=r["s1_f1"], f1_nisar_same_px=r["nisar_f1_same_px"],
                 f1_swot_vs_optical=r["swot_vs_optical_f1"], f1_nisar_vs_optical=r["nisar_vs_optical_f1"])
            for r in v.get("vs_swot", [])]
    return dict(vsHls=hls, vsDswxS1=s1, vsSwot=swot, notes=[
        "SWOT (Ka-band, NASA/CNES) is a third independent radar: f1_nisar / f1_s1 score each map against SWOT on the same pixels.",
        "DSWx-S1 calibration dates are excluded from validation statistics.",
        "HLS precision and comparable full-area DSWx totals are not supplied by the dataset.",
        "Area totals sum the observed commune areas per acquisition, not the entire AOI.",
        "Commune summary statistics use one reference track; time series retain every track.",
    ])
