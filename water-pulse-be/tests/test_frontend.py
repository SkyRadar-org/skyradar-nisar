from collections import Counter

from fastapi.testclient import TestClient

from app.data import store
from app.main import app

c = TestClient(app)
BASE = "/api/frontend"


def test_scenes_bounds_maturity_and_assets():
    scenes = c.get(f"{BASE}/scenes").json()
    assert len(scenes) == 33
    assert {s["track"] for s in scenes} == {"047D", "083A", "148D"}
    for scene in scenes:
        w, s, e, n = scene["bounds"]
        assert 104 < w < e < 107 and 10 < s < n < 12
        assert scene["maturity"] == ("validated" if scene["date"] >= "2026-10-22" else "provisional")
        assert c.get(scene["waterPng"]).content.startswith(b"\x89PNG")
        assert c.get(scene["radarJpg"]).content.startswith(b"\xff\xd8")


def test_commune_uses_sowing_track_without_merging_observations():
    features = c.get(f"{BASE}/communes").json()["features"]
    assert len(features) == 140
    counts = Counter()
    for feature in features:
        p = feature["properties"]
        oid = int(p["osm_id"])
        assert feature["id"] == str(oid)
        sowing = store().sowing.get(oid)
        if sowing:
            assert p["coverage_sufficient"]
            assert p["last_date"] == sowing["status_date"]
            assert p["reference_track"] == sowing["status_track"]
            assert p["last_pct"] == sowing["status_pct"]
            counts[sowing["status"]] += 1
        else:
            assert p["status"] == "uncertain" and not p["coverage_sufficient"]
        if not store().series[oid]:
            assert p["last_pct"] is None and p["peak_pct"] is None and p["last_date"] is None
        rows = [r for r in store().series[oid] if r["track"] == p["reference_track"]]
        assert p["max_flooded_km2"] == max((r["water_km2"] for r in rows), default=None)
    assert counts == {"ready": 53, "draining": 40, "still_wet": 38}
    son_kien = next(f["properties"] for f in features if f["id"] == "15416586")
    assert son_kien["status"] == "not_receded" and son_kien["last_pct"] == 78.2


def test_choropleth_and_series_match_source_per_track():
    rows = c.get(f"{BASE}/communes/15416586/series").json()
    assert {r["track"] for r in rows} == {"047D", "083A", "148D"}
    for row in rows:
        values = c.get(f"{BASE}/choropleth", params={"date": row["date"], "track": row["track"]}).json()
        assert values["15416586"] == row["water_pct"]
    assert c.get(f"{BASE}/communes/1/series").status_code == 404
    assert c.get(f"{BASE}/choropleth", params={"date": "1900-01-01", "track": "047D"}).status_code == 404
    assert c.get(f"{BASE}/choropleth", params={"date": "2026-10-27", "track": "invalid"}).status_code == 422


def test_composite_playback_assets_and_values():
    scenes = c.get(f"{BASE}/scenes").json()
    for scene in scenes:
        comp = scene["composite"]
        assert comp and comp["maxAgeDays"] == 12 and comp["observedPct"] > 30
        assert c.get(comp["png"]).content[:4] == b"RIFF" and c.get(comp["simplePng"]).content[:4] == b"RIFF"
        assert c.get(comp["radar"]).content[:4] == b"RIFF"
        # the newest contributing pass is the scene itself
        assert comp["sources"][-1]["date"] == scene["date"] and comp["sources"][-1]["track"] == scene["track"]
    assert sum(s["composite"]["observedPct"] > 80 for s in scenes) >= 28   # only the 25 Jul -> 11 Aug acquisition gap is thin
    first = c.get(f"{BASE}/choropleth/composite", params={"date": scenes[0]["date"], "track": scenes[0]["track"]}).json()
    exact = c.get(f"{BASE}/choropleth", params={"date": scenes[0]["date"], "track": scenes[0]["track"]}).json()
    assert first and all(v["age"] == 0 and v["pct"] == exact[k] for k, v in first.items() if k in exact and v["age"] == 0)
    last = scenes[-1]
    values = c.get(f"{BASE}/choropleth/composite", params={"date": last["date"], "track": last["track"]}).json()
    assert len(values) >= len(c.get(f"{BASE}/choropleth", params={"date": last["date"], "track": last["track"]}).json())
    assert all(0 <= v["age"] <= 12 and 0 <= v["pct"] <= 100 for v in values.values())
    assert c.get(f"{BASE}/choropleth/composite", params={"date": "1900-01-01", "track": "047D"}).status_code == 404
    assert c.get(f"{BASE}/choropleth/composite", params={"date": "2026-10-27", "track": "bad"}).status_code == 422


def test_area_does_not_invent_reference_totals():
    area = c.get(f"{BASE}/area").json()
    assert len(area) == 33
    for point in area:
        expected = sum(r["water_km2"] for rows in store().series.values() for r in rows
                       if (r["date"], r["track"]) == (point["date"], point["track"]))
        assert point["nisar_km2"] == round(expected, 2)
        assert point["dswx_km2"] is None


def test_validation_excludes_calibration_and_preserves_hls_values():
    validation = c.get(f"{BASE}/validation").json()
    assert len(validation["vsDswxS1"]) == 25
    assert len(validation["vsHls"]) == 16
    assert sum(r["f1_nisar"] > r["f1_s1"] for r in validation["vsHls"]) == 14
    for result, source in zip(validation["vsHls"], store().validation["vs_dswx_hls"]):
        assert result["f1_nisar"] == source["nisar"]
        assert result["precision_nisar"] is None
    # Do not offer misleading merged-track summary layers.
    assert c.get(f"{BASE}/summary").json() == []


def test_swot_comparison_source():
    scenes = c.get(f"{BASE}/scenes").json()
    linked = [s for s in scenes if s["swot"]]
    assert linked and all(s["swot"]["daysApart"] <= 2 for s in linked)
    assert c.get(linked[0]["swot"]["png"]).content.startswith(b"\x89PNG")
    same_day = next(s for s in scenes if s["date"] == "2026-10-15" and s["track"] == "047D")
    assert same_day["swot"] == {"date": "2026-10-15", "png": "/static/swot/2026-10-15.png", "daysApart": 0}
    rows = c.get(f"{BASE}/communes/15416586/swot").json()
    assert rows and all(0 <= r["water_pct"] <= 100 for r in rows)
    v = c.get(f"{BASE}/validation").json()["vsSwot"]
    assert len(v) == 13
    both = [r for r in v if r["f1_s1"] is not None]
    assert sum(r["f1_nisar_same_px"] > r["f1_s1"] for r in both) == 11 and len(both) == 12
    assert c.get(f"{BASE}/communes/1/swot").status_code == 404
