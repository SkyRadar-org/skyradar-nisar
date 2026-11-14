"""Playback mosaics: for every acquisition date, the most recent valid observation of each pixel (any track).

A single NISAR pass covers only 37-83 % of the AOI, so playing the raw frames makes the water layer shrink and grow
with every swath. The mosaic of frame j shows, per pixel, the latest observation made on or before that date by any
track, as long as it is at most MAX_AGE_DAYS old. Nothing is interpolated:
  * pixels keep a measured state (water / dry) from a real pass; older observations are drawn fainter,
  * pixels not observed within MAX_AGE_DAYS stay un-coloured under a grey veil ("no recent data"),
  * a pixel that flips state for a single pass and flips back (speckle) is replaced by its neighbours' state
    (temporal median of previous / current / next valid observation, only when both are <= MEDIAN_WINDOW_DAYS away),
  * the output is half resolution (2x2 average + 3x3 box blur) so edges are soft instead of pixel-hard.
Raw per-acquisition frames (water/, radar/) are untouched and remain the source of all statistics.

    python -m skyradar_nisar.composite        # reads and updates data/web/manifest.json
Outputs: data/web/composite/<key>.webp (water + no-data veil, RGBA) and <key>_radar.jpg (radar mosaic).
"""
import datetime as dt
import json

import numpy as np
from PIL import Image

from . import config as C

MAX_AGE_DAYS = 12          # about one repeat cycle of a track; older pixels count as "not observed"
MEDIAN_WINDOW_DAYS = 30    # neighbours further away are not used to cancel a one-pass flip
ALPHA_FRESH, ALPHA_STALE = 200, 90
WATER_RGB = (30, 110, 230)
VEIL_RGB, VEIL_ALPHA = (110, 120, 135), 70
RADAR_VALID_MIN = 6        # radar JPEG is black outside the swath
STRIP = 128                # rows per processing strip (keeps memory low)
NONE, DRY, WATER, NODATA = 255, 0, 1, 2


def _even(a):
    """Replicate the last row / column when a dimension is odd, so 2x2 averaging keeps the same bounds."""
    pad = [(0, a.shape[ax] % 2) if ax < 2 else (0, 0) for ax in range(a.ndim)]
    return np.pad(a, pad, mode="edge") if any(p[1] for p in pad) else a


def _dilate(m, r):
    for ax in (0, 1):
        out = m.copy()
        for k in range(1, r + 1):
            sl_a = [slice(None)] * 2; sl_b = [slice(None)] * 2
            sl_a[ax] = slice(k, None); sl_b[ax] = slice(None, -k)
            out[tuple(sl_a)] |= m[tuple(sl_b)]
            out[tuple(sl_b)] |= m[tuple(sl_a)]
        m = out
    return m


def _close(m, r=2):
    """Fill JPEG-noise holes inside the swath (dilate, then erode)."""
    return ~_dilate(~_dilate(m, r), r)


def _box3(a):
    p = np.pad(a.astype(np.float32), 1, mode="edge")
    h, w = a.shape
    return sum(p[i:i + h, j:j + w] for i in range(3) for j in range(3)) / 9.0


def _load(out_dir, frames):
    states, radars = [], []
    for f in frames:
        water = np.asarray(Image.open(out_dir / f["png"]))[..., 3] > 0
        rad_img = Image.open(out_dir / f["radar_jpg"]).convert("RGB")
        if rad_img.size != (water.shape[1], water.shape[0]):   # radar is exported at a coarser scale on the same bounds
            rad_img = rad_img.resize((water.shape[1], water.shape[0]), Image.NEAREST)
        rad = np.asarray(rad_img)
        valid = _close(rad.max(-1) > RADAR_VALID_MIN) | water
        s = np.where(valid, water.astype(np.uint8), NODATA).astype(np.uint8)
        s = _even(s)
        rad = _even(rad)
        h, w = s.shape
        radars.append(rad.reshape(h // 2, 2, w // 2, 2, 3).mean((1, 3)).astype(np.uint8))
        states.append(s)
    return np.stack(states), np.stack(radars)


def _smooth_strip(S, day):
    """Cancel pixels that differ from both the previous and the next valid observation when those two agree."""
    T, h, w = S.shape
    valid = S != NODATA
    d = day[:, None, None]
    pv = np.empty_like(S); pdy = np.empty((T, h, w), np.int16)
    last_s = np.full((h, w), NONE, np.uint8); last_d = np.full((h, w), -30000, np.int16)
    for i in range(T):
        pv[i], pdy[i] = last_s, last_d
        last_s = np.where(valid[i], S[i], last_s); last_d = np.where(valid[i], day[i], last_d)
    nx = np.empty_like(S); ndy = np.empty((T, h, w), np.int16)
    last_s = np.full((h, w), NONE, np.uint8); last_d = np.full((h, w), 30000, np.int16)
    for i in range(T - 1, -1, -1):
        nx[i], ndy[i] = last_s, last_d
        last_s = np.where(valid[i], S[i], last_s); last_d = np.where(valid[i], day[i], last_d)
    spike = (valid & (pv != NONE) & (nx == pv) & (S != pv)
             & ((d - pdy) <= MEDIAN_WINDOW_DAYS) & ((ndy - d) <= MEDIAN_WINDOW_DAYS))
    return np.where(spike, pv, S)


def _mosaic(S, day):
    T, H, W = S.shape
    H2, W2 = H // 2, W // 2
    wf = np.zeros((T, H2, W2), np.uint8); of = np.zeros_like(wf); age = np.zeros_like(wf)
    li = np.full((T, H2, W2), -1, np.int8)
    share = np.zeros((T, T), np.int64)   # share[j, i]: observed pixels of mosaic j that come from frame i
    for r0 in range(0, H, STRIP):
        sm = _smooth_strip(S[:, r0:r0 + STRIP], day)
        valid = S[:, r0:r0 + STRIP] != NODATA
        h = sm.shape[1]
        last_s = np.full((h, W), NONE, np.uint8); last_d = np.full((h, W), -30000, np.int16); last_i = np.full((h, W), -1, np.int8)
        for j in range(T):
            upd = valid[j]
            last_s = np.where(upd, sm[j], last_s); last_d = np.where(upd, day[j], last_d); last_i = np.where(upd, j, last_i)
            a = day[j] - last_d
            obs = (last_s != NONE) & (a <= MAX_AGE_DAYS)
            wat = obs & (last_s == WATER)
            rs = slice(r0 // 2, r0 // 2 + h // 2)
            wf[j, rs] = wat.reshape(h // 2, 2, W2, 2).sum((1, 3))
            of[j, rs] = obs.reshape(h // 2, 2, W2, 2).sum((1, 3))
            age[j, rs] = np.clip(a[::2, ::2], 0, 255)
            li[j, rs] = np.where(obs[::2, ::2], last_i[::2, ::2], -1)
            share[j] += np.bincount(last_i[obs].astype(np.int64), minlength=T)
    return wf, of, age, li, share


def _render_water(wf, of, age):
    wb = _box3(wf) / 4.0
    ob = _box3(of) / 4.0
    ageb = _box3(age.astype(np.float32) * of) / np.maximum(_box3(of), 1e-3)
    fade = np.clip(ageb / MAX_AGE_DAYS, 0, 1)
    aw = np.clip((wb - 0.10) / 0.5, 0, 1) * (ALPHA_FRESH - (ALPHA_FRESH - ALPHA_STALE) * fade) / 255
    av = VEIL_ALPHA / 255 * np.clip(1 - ob, 0, 1)
    a = aw + av * (1 - aw)
    rgb = np.zeros(a.shape + (3,), np.float32)
    nz = a > 1e-4
    for c in range(3):
        rgb[..., c] = np.where(nz, (WATER_RGB[c] * aw + VEIL_RGB[c] * av * (1 - aw)) / np.where(nz, a, 1), 0)
    return np.dstack([rgb, a[..., None] * 255]).round().astype(np.uint8)


def build(out_dir=None):
    out_dir = out_dir or C.WEB
    mpath = out_dir / "manifest.json"
    manifest = json.loads(mpath.read_text(encoding="utf-8"))
    frames = manifest["frames"]
    if not frames:
        return
    d0 = dt.date.fromisoformat(frames[0]["date"]).toordinal()
    day = np.array([dt.date.fromisoformat(f["date"]).toordinal() - d0 for f in frames], np.int16)
    S, R = _load(out_dir, frames)
    wf, of, age, li, share = _mosaic(S, day)
    cdir = out_dir / "composite"
    cdir.mkdir(exist_ok=True)
    items = []
    for j, f in enumerate(frames):
        k = f["key"]
        Image.fromarray(_render_water(wf[j], of[j], age[j])).save(cdir / f"{k}.webp", lossless=False, quality=88, alpha_quality=90, method=4)
        idx = np.clip(li[j], 0, None).astype(np.int64)
        rad = np.take_along_axis(R, idx[None, :, :, None], axis=0)[0]
        rad[li[j] < 0] = 0
        Image.fromarray(rad).save(cdir / f"{k}_radar.jpg", quality=60, optimize=True)
        total = max(int(share[j].sum()), 1)
        sources = [dict(date=frames[i]["date"], track=frames[i]["track"], share_pct=round(100 * int(share[j, i]) / total, 1))
                   for i in range(j + 1) if share[j, i] / total >= 0.0005]
        items.append(dict(key=k, date=f["date"], track=f["track"], png=f"composite/{k}.webp", radar_jpg=f"composite/{k}_radar.jpg",
                          observed_pct=round(100 * float(of[j].mean()) / 4, 1), sources=sources))
    manifest["composites"] = items
    manifest["composite_rule"] = dict(
        max_age_days=MAX_AGE_DAYS, median_window_days=MEDIAN_WINDOW_DAYS, resolution_divisor=2,
        note="Per pixel: latest valid observation from any track, at most max_age_days old; older = fainter, none = grey veil. "
             "Single-pass flips are cancelled by a temporal median. Visual aid only: statistics use the raw frames.")
    mpath.write_text(json.dumps(manifest, indent=1, ensure_ascii=False), encoding="utf-8")
    print(len(items), "composite frames written to", cdir)


if __name__ == "__main__":
    build()
