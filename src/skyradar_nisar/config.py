"""Project configuration: area of interest, NISAR tracks, water rule, paths."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
RAW = DATA / "raw"            # large intermediate rasters (git-ignored)
PROCESSED = DATA / "processed"  # 20 m GeoTIFFs, water maps, summaries (git-ignored)
WEB = DATA / "web"            # small package consumed by the web app (committed)

# Demo AOI: Long Xuyen Quadrangle + Dong Thap Muoi (Mekong Delta), lon/lat (W, S, E, N)
AOI = (104.95, 10.25, 106.0, 11.0)
EPSG = 32648          # WGS 84 / UTM 48N (native grid of the NISAR GCOV frames over the AOI)
RES = 20              # output pixel size (m); GCOV 40 MHz is 10 m, averaged 2x2 in power

# NISAR GCOV frames covering the AOI (track + direction + frame + mode + polarization)
TRACKS = {
    "047D": "_047_D_083_4005_DHDH_",
    "083A": "_083_A_007_4005_DHDH_",
    "148D": "_148_D_083_4005_DHDH_",
}
START, END = "2026-06-01", "2026-11-30"

# Water rule calibrated against OPERA DSWx-S1 on 2026-06-17 and 2026-09-21 (track 047D)
TH_HH_DB = -14.0
TH_HV_DB = -22.0
MMU_PX = 75           # minimum mapping unit: 3 ha at 20 m (same as DSWx)
PERMANENT_MIN_DATES = 20  # DSWx-S1 open water on >= this many dates -> permanent water (rivers, canals)

FLOOD_SEASON_START = "2026-08-01"
NODATA_DB = -32768    # int16 nodata for dB*100 rasters
