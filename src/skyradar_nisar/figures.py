"""Figures for the slides / project page (docs/figures).

    python -m skyradar_nisar.figures
  fig1_water_timeseries.png   % of land under water per track, NISAR vs DSWx-S1 (same pixels)
  fig2_validation_optical.png F1 vs optical DSWx-HLS, NISAR vs Sentinel-1, per date
  fig3_commune_examples.png   water % per track for example communes (early vs late recession)
"""
import csv, json, datetime as dt
from collections import defaultdict
import numpy as np, rasterio
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.dates as mdates
from . import config as C
from .water import permanent_water

OUT = C.ROOT / "docs" / "figures"
COL = {"047D": "#1f6feb", "083A": "#e8590c", "148D": "#2f9e44"}


def _rd(p):
    with rasterio.open(p) as s:
        return s.read(1)


def fig1():
    P = C.PROCESSED; qa = json.loads((P / "qa.json").read_text(encoding="utf-8"))
    s1 = {k: _rd(P / f"dswx_s1/{k}_WTR.tif") for k in qa if (P / f"dswx_s1/{k}_WTR.tif").exists()}
    perm = permanent_water(list(s1.values()))
    ser = defaultdict(list)
    for k in sorted(qa):
        w = _rd(P / f"water/{k}_water.tif"); valid = w != 255
        if k in s1:
            ok = valid & np.isin(s1[k], [0, 1, 3]) & ~perm
            if ok.mean() < 0.05:   # same rule as calibrate: almost no Sentinel-1 overlap (e.g. most 148D dates)
                continue
            ser[k[11:]].append((dt.date.fromisoformat(k[:10]), np.mean(w[ok] == 1) * 100, np.mean(s1[k][ok] == 1) * 100))
    fig, ax = plt.subplots(figsize=(10, 4.2))
    for trk, rows in ser.items():
        x, n, d = zip(*rows)
        ax.plot(x, n, "-o", c=COL[trk], label=f"NISAR L-band, track {trk}")
        ax.plot(x, d, "--", c=COL[trk], alpha=.55, label=f"Sentinel-1 DSWx, same pixels ({trk})")
    ax.axvline(dt.date(2026, 11, 1), c="k", lw=1, ls=":"); ax.text(dt.date(2026, 11, 1), ax.get_ylim()[1] * .95, " sowing window\n opens 1 Nov", fontsize=8, va="top")
    ax.set_ylabel("% of land under water"); ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    ax.set_title("Mekong Delta (Long Xuyen Quadrangle + Dong Thap Muoi), 2026 flood season")
    ax.grid(alpha=.3); ax.legend(fontsize=7, ncol=2); fig.tight_layout(); fig.savefig(OUT / "fig1_water_timeseries.png", dpi=150)


def fig2():
    rows = list(csv.DictReader(open(C.PROCESSED / "validation/vs_dswx_hls.csv", encoding="utf-8")))
    rows.sort(key=lambda r: r["key"])
    lab = [r["key"][5:10].replace("-", "/") + "\n" + r["key"][11:] for r in rows]
    x = np.arange(len(rows)); w = .38
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(x - w / 2, [float(r["nisar"]) for r in rows], w, color="#1f6feb", label="NISAR L-band (this work)")
    ax.bar(x + w / 2, [float(r["s1"]) for r in rows], w, color="#adb5bd", label="Sentinel-1 C-band (OPERA DSWx-S1)")
    ax.set_xticks(x, lab, fontsize=7); ax.set_ylim(0, 1); ax.set_ylabel("F1 vs optical water (DSWx-HLS)")
    ax.set_title("Independent check against optical water maps (clear-sky pixels, ±2 days)")
    ax.set_ylim(0, 1.12); ax.legend(fontsize=8, loc="upper left", ncol=2, frameon=False); ax.grid(axis="y", alpha=.3); fig.tight_layout(); fig.savefig(OUT / "fig2_validation_optical.png", dpi=150)


def fig3(names=("Xã Sơn Kiên", "Xã Hòn Đất", "Xã Tây Phú", "Xã Vĩnh Hanh")):
    rows = list(csv.DictReader(open(C.PROCESSED / "stats/commune_water_by_date.csv", encoding="utf-8")))
    fig, axes = plt.subplots(1, len(names), figsize=(12, 3.2), sharey=True)
    for ax, nm in zip(axes, names):
        for trk in COL:
            rr = sorted([r for r in rows if r["commune"] == nm and r["track"] == trk and float(r["valid_km2"]) >= 5], key=lambda r: r["date"])
            if rr:
                ax.plot([dt.date.fromisoformat(r["date"]) for r in rr], [float(r["water_pct"]) for r in rr], "-o", ms=3, c=COL[trk], label=trk)
        ax.axvline(dt.date(2026, 11, 1), c="k", lw=1, ls=":")
        ax.set_title(nm.replace("Xã ", ""), fontsize=10); ax.xaxis.set_major_formatter(mdates.DateFormatter("%b")); ax.grid(alpha=.3)
    axes[0].set_ylabel("% of commune under water"); axes[0].legend(fontsize=7, title="track", title_fontsize=7)
    fig.suptitle("Commune timelines: early recession (Tay Phu, Vinh Hanh) vs still flooded after 1 Nov (Son Kien, Hon Dat)", fontsize=10)
    fig.tight_layout(); fig.savefig(OUT / "fig3_commune_examples.png", dpi=150)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    fig1(); fig2(); fig3()
    print("figures in", OUT)


if __name__ == "__main__":
    main()
