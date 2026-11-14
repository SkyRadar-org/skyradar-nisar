"""Common 20 m UTM grid over the AOI; aggregation of 10 m GCOV into it; dB*100 int16 GeoTIFF I/O."""
import numpy as np, rasterio
from rasterio.transform import from_origin
from pyproj import Transformer
from . import config as C


class Grid:
    def __init__(self, aoi=C.AOI, epsg=C.EPSG, res=C.RES):
        tr = Transformer.from_crs(4326, epsg, always_xy=True)
        xs, ys = tr.transform([aoi[0], aoi[2], aoi[0], aoi[2]], [aoi[1], aoi[1], aoi[3], aoi[3]])
        self.x0 = np.floor(min(xs) / res) * res; self.y0 = np.ceil(max(ys) / res) * res
        self.nx = int(np.ceil((max(xs) - self.x0) / res)); self.ny = int(np.ceil((self.y0 - min(ys)) / res))
        self.res, self.epsg = res, epsg
        self.transform = from_origin(self.x0, self.y0, res, res)
        self.shape = (self.ny, self.nx)

    def from_native(self, a, x0c, y0c, spacing):
        """Place a native array (first pixel CENTRE at x0c, y0c; square pixels `spacing` m) on the grid,
        averaging in the linear (power) domain. Native grids are aligned to the output grid at 10/20 m."""
        k = int(round(self.res / spacing))
        cx = int(round(((x0c - spacing / 2) - self.x0) / spacing)); cy = int(round((self.y0 - (y0c + spacing / 2)) / spacing))
        big = np.full((self.ny * k, self.nx * k), np.nan, np.float32)
        r0, c0 = max(cy, 0), max(cx, 0)
        r1, c1 = min(cy + a.shape[0], self.ny * k), min(cx + a.shape[1], self.nx * k)
        if r1 > r0 and c1 > c0:
            big[r0:r1, c0:c1] = a[r0 - cy:r1 - cy, c0 - cx:c1 - cx]
        if k == 1:
            return big
        with np.errstate(all="ignore"):
            return np.nanmean(big.reshape(self.ny, k, self.nx, k), axis=(1, 3))

    def profile(self, dtype="int16", nodata=C.NODATA_DB):
        return dict(driver="GTiff", height=self.ny, width=self.nx, count=1, dtype=dtype, crs=f"EPSG:{self.epsg}",
                    transform=self.transform, nodata=nodata, compress="deflate", predictor=2 if dtype != "uint8" else 1,
                    tiled=True, blockxsize=512, blockysize=512)


def write_db(path, db, grid):
    v = np.where(np.isfinite(db), np.round(db * 100), C.NODATA_DB).astype(np.int16)
    with rasterio.open(path, "w", **grid.profile()) as dst:
        dst.write(v, 1); dst.update_tags(units="dB*100", scale="0.01")


def read_db(path):
    with rasterio.open(path) as s:
        a = s.read(1)
    out = a.astype(np.float32) / 100
    out[a == C.NODATA_DB] = np.nan
    return out
