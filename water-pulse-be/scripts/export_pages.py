"""Export the tested frontend API plus data assets for Cloudflare Pages Workers.

This does not run the satellite pipeline or require Earthdata credentials.
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import frontend
from app.data import DATA_DIR, store


def export(out: Path, template: Path):
    out = out.resolve()
    if not (out / "index.html").is_file():
        raise ValueError("Output must be the frontend build directory containing index.html")
    if out == DATA_DIR.resolve() or out in DATA_DIR.resolve().parents or DATA_DIR.resolve() in out.parents:
        raise ValueError("Output must not overlap the source dataset")
    files = {}

    def write(route, filename, value):
        target = out / "api-data" / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(",", ":")), encoding="utf-8")
        files[route] = "/api-data/" + filename

    scenes = frontend.scenes()
    collection = frontend.communes()
    write("/health", "health.json", dict(status="ok", frames=len(scenes), communes=len(collection["features"])))
    for name, value in [("scenes", scenes), ("communes", collection), ("area", frontend.area()),
                        ("summary", frontend.summary()), ("validation", frontend.validation())]:
        write(f"/api/frontend/{name}", f"{name}.json", value)
    for oid in store().by_id:
        write(f"/api/frontend/communes/{oid}/series", f"series/{oid}.json", frontend.series(oid))
        write(f"/api/frontend/communes/{oid}/swot", f"swot/{oid}.json", frontend.swot_series(oid))
    for scene in scenes:
        date, track = scene["date"], scene["track"]
        write(f"/api/frontend/choropleth?date={date}&track={track}", f"choropleth/{date}_{track}.json",
              frontend.choropleth(date, track))
        write(f"/api/frontend/choropleth/composite?date={date}&track={track}", f"choropleth-composite/{date}_{track}.json",
              frontend.choropleth_composite(date, track))
    shutil.copytree(DATA_DIR, out / "static", dirs_exist_ok=True)
    source = template.read_text(encoding="utf-8")
    if source.count("__API_FILES__") != 1:
        raise ValueError("Worker template needs exactly one API manifest marker")
    (out / "_worker.js").write_text(source.replace("__API_FILES__", json.dumps(files)), encoding="utf-8")
    (out / "_routes.json").write_text(json.dumps(dict(version=1, include=["/api/*", "/health"], exclude=[])), encoding="utf-8")
    (out / "_headers").write_text("/static/*\n  Cache-Control: public, max-age=300\n  X-Content-Type-Options: nosniff\n", encoding="utf-8")
    assets = [p for p in out.rglob("*") if p.is_file()]
    oversized = [str(p.relative_to(out)) for p in assets if p.stat().st_size > 25 * 1024 * 1024]
    if oversized or len(assets) > 20000:
        raise ValueError(f"Pages asset limits exceeded: {len(assets)} files; oversized={oversized}")
    print(f"Exported {len(files)} API responses, {len(scenes)} scenes, {len(collection['features'])} communes; "
          f"{len(assets)} files, largest {max(p.stat().st_size for p in assets):,} bytes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--worker-template", required=True, type=Path)
    args = parser.parse_args()
    export(args.out, args.worker_template)
