from fastapi.testclient import TestClient
from app.main import app

c = TestClient(app)
SON_KIEN = 15416586


def test_health():
    r = c.get("/health").json()
    assert r["status"] == "ok" and r["frames"] >= 22 and r["communes"] >= 100


def test_manifest_and_frames():
    m = c.get("/api/manifest").json()
    assert {"bounds", "frames", "gibs_template", "attribution"} <= set(m)
    f = c.get("/api/frames", params={"track": "047D"}).json()
    assert f and all(x["track"] == "047D" for x in f)
    assert c.get(f[0]["png_url"]).status_code == 200
    assert c.get(f[0]["radar_url"]).status_code == 200


def test_commune_and_series():
    p = c.get(f"/api/communes/{SON_KIEN}").json()
    assert p["name"] == "Xã Sơn Kiên" and p["sowing"]["status"] == "partial"
    s = c.get(f"/api/communes/{SON_KIEN}/series").json()
    assert {x["track"] for x in s} >= {"047D", "083A"} and s == sorted(s, key=lambda x: (x["date"], x["track"]))
    assert c.get("/api/communes/1").status_code == 404


def test_sowing_ranking_release_validation():
    sc = c.get("/api/sowing-check", params={"status": "still_wet"}).json()
    assert sc["communes"] and all(x["status"] == "still_wet" for x in sc["communes"])
    assert sc["counts_all"] == {"ready": 43, "draining": 39, "still_wet": 33}
    assert sc["partial_count"] == 16
    partial = c.get("/api/sowing-check", params={"status": "partial"}).json()["communes"]
    assert len(partial) == 16 and all(p["observed_pct"] < 50 for p in partial)
    rk = c.get("/api/ranking", params={"limit": 5}).json()
    assert len(rk) == 5 and rk[0]["last_pct"] >= rk[-1]["last_pct"]
    assert all(x["cls"] == "A" for x in c.get("/api/flood-release", params={"cls": "A"}).json())
    v = c.get("/api/validation").json()
    assert v["calibration"]["th_hh_db"] == -14.0 and len(v["vs_dswx_hls"]) >= 10


def test_numbers_are_typed():
    p = c.get(f"/api/communes/{SON_KIEN}").json()
    t = p["timing"]["047D"]
    assert isinstance(t["peak_pct"], float) and (t["halved_after_peak"] is None or isinstance(t["halved_after_peak"], str))
    pt = p["sowing"]["per_track"]
    assert {x["track"] for x in pt} == {"047D", "083A", "148D"} and all(isinstance(x["water_pct"], float) for x in pt)


def test_search_provinces_gzip_cache():
    r = c.get("/api/search", params={"q": "son kien"}).json()
    assert r and r[0]["name"] == "Xã Sơn Kiên"
    assert c.get("/api/search", params={"q": "đồng tháp"}).json()
    pv = c.get("/api/provinces").json()
    assert {"Tỉnh An Giang", "Tỉnh Đồng Tháp"} <= {p["province"] for p in pv}
    assert sum(p["communes"] for p in pv) == c.get("/health").json()["communes"]
    g = c.get("/api/communes", headers={"Accept-Encoding": "gzip"})
    assert g.headers.get("content-encoding") == "gzip" and "max-age" in g.headers.get("cache-control", "")
