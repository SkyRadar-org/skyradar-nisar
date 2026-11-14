import re
import struct

from fastapi.testclient import TestClient

from app.data import store
from app.main import app

c = TestClient(app)
URL = "/api/frontend/summary"
TRACKS = {"047D", "083A", "148D"}


def png_header(data):
    """(width, height, colour type) from the PNG IHDR chunk; colour type 6 = RGBA."""
    assert data.startswith(b"\x89PNG\r\n\x1a\n") and data[12:16] == b"IHDR"
    w, h = struct.unpack(">II", data[16:24])
    return w, h, data[25]


def test_one_layer_per_track_and_kind_never_merged():
    layers = c.get(URL).json()
    assert len(layers) == 6
    assert {(l["track"], l["kind"]) for l in layers} == {(t, k) for t in TRACKS for k in ("first_flood_date", "recession_date")}
    assert len({l["id"] for l in layers}) == 6
    for l in layers:
        assert l["id"] == f"{l['kind']}_{l['track']}"
        assert l["track"] in l["title"]
        assert l["png"].endswith(f"_{l['track']}.png")   # never the merged summary/first_flood.png or recession.png


def test_layers_align_with_scenes_and_serve_pngs():
    scene = c.get("/api/frontend/scenes").json()[0]
    w, h, _ = png_header(c.get(scene["waterPng"]).content)
    for l in c.get(URL).json():
        assert l["bounds"] == scene["bounds"]
        r = c.get(l["png"])
        assert r.status_code == 200
        assert png_header(r.content) == (w, h, 6)


def test_legend_matches_manifest_scale_and_track_dates():
    m = store().manifest
    for l in c.get(URL).json():
        key = l["kind"].replace("_date", "")
        stops = m["timing_scale"][key]["stops"]
        assert all(re.fullmatch(r"#[0-9a-f]{6}", e["color"]) and e["label"] for e in l["legend"])
        assert [e["color"] for e in l["legend"][:len(stops)]] == [s["color"] for s in stops]
        assert l["range"] == [stops[0]["date"], stops[-1]["date"]]
        frames = sorted(f["date"] for f in m["frames"] if f["track"] == l["track"] and f["date"] >= "2026-08-01")
        assert l["seasonDates"] == frames and l["lastDate"] == frames[-1]
        if l["kind"] == "recession_date":
            assert len(l["legend"]) == len(stops) + 1
            assert l["legend"][-1]["color"] == m["timing_scale"]["still_wet"]["color"]
        else:
            assert len(l["legend"]) == len(stops)
