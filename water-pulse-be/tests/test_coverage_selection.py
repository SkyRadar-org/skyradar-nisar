"""Regression fixtures for the commune-area gate, independent of the real CSV counts."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from skyradar_nisar.sowing import assess_communes


def row(date="2026-10-27", valid=60, track="047D", pct=35):
    return dict(osm_id="1", commune="Example", province="Example", date=date,
                track=track, valid_km2=str(valid), water_pct=str(pct))


def assess(rows, area=100):
    return assess_communes(rows, [dict(properties=dict(osm_id=1, area_km2=area))])


def test_newer_sliver_does_not_replace_older_eligible_image_even_on_same_track():
    for track in ("047D", "083A"):
        result = assess([row(valid=90), row(date="2026-11-03", valid=46, track=track)])[0]
        assert result["status_date"] == "2026-10-27" and result["observed_pct"] == 90
        assert result["status"] == "still_wet"


def test_coverage_threshold_is_applied_before_rounding_and_at_exact_boundary():
    assert assess([row(valid=49.9999)])[0]["status"] == "partial"
    assert assess([row(valid=50)])[0]["status"] == "still_wet"
    assert assess([row(valid=36.73)], area=73.93)[0]["status"] == "partial"


def test_missing_area_and_no_observations_are_not_dry_assessments():
    result = assess([row(pct=0)], area=None)[0]
    assert result["status"] == "partial" and result["observed_pct"] is None
    assert assess([]) == []
    assert assess([row(valid=4.9)]) == []


def test_same_day_selection_and_water_bins_are_deterministic():
    rows = [row(valid=60, track="047D", pct=0), row(valid=80, track="083A", pct=10)]
    assert assess(rows) == assess(list(reversed(rows)))
    assert assess(rows)[0]["status"] == "draining"
    assert assess([row(pct=9.9)])[0]["status"] == "ready"
    assert assess([row(pct=30)])[0]["status"] == "still_wet"
