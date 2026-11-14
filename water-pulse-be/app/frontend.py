"""Adapter for water-pulse-fe. Original API responses remain unchanged."""
from collections import defaultdict
from functools import lru_cache
from typing import Literal

from fastapi import APIRouter, HTTPException

from .data import store

router = APIRouter(prefix="/api/frontend", tags=["frontend"])
Track = Literal["047D", "083A", "148D"]


@router.get("/scenes")
def scenes():
    m = store().manifest
    (s, w), (n, e) = m["bounds"]
    return [dict(date=f["date"], track=f["track"], maturity=f["maturity"],
                 bounds=[w, s, e, n], waterPng=f"/static/{f['png']}",
                 radarJpg=f"/static/{f['radar_jpg']}" if f.get("radar_jpg") else None,
                 gibsDate=f.get("gibs_date", f["date"])) for f in m["frames"]]


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
        if sowing and peak_pct is not None and peak_pct < 5:
            status = "no_flood"
        props = dict(osm_id=str(oid), name=p["name"], province=p["province"],
                     valid_km2=last["valid_km2"] if last else None,
                     first_flood_date=timing.get("first_date_ge20pct"),
                     peak_pct=peak_pct, peak_date=timing.get("peak_date", peak["date"] if peak else None),
                     half_date=timing.get("halved_after_peak"),
                     recession_date=timing.get("halved_after_peak"),
                     last_pct=last["water_pct"] if last else None, last_date=last["date"] if last else None,
                     max_flooded_km2=max((r["water_km2"] for r in track_rows), default=None),
                     status=status, reference_track=track, coverage_sufficient=bool(sowing))
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
    return dict(vsHls=hls, vsDswxS1=s1, notes=[
        "DSWx-S1 calibration dates are excluded from validation statistics.",
        "HLS precision and comparable full-area DSWx totals are not supplied by the dataset.",
        "Area totals sum the observed commune areas per acquisition, not the entire AOI.",
        "Commune summary statistics use one reference track; time series retain every track.",
    ])
