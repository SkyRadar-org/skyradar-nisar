"""Controlled flood release (xả lũ) signature per commune + figure.

    python -m skyradar_nisar.release
Hypothesis: in dyke-protected 3-crop sub-regions, gates are opened in mid-August (river still below alarm level 1)
and fields are pumped dry in late September - early October while the river is still near its peak. Natural overbank
flooding instead rises with the river and lingers after it falls. Classes (per commune, one track, peak >= 30 %):
  A  water >= 50 % of peak by 18 Aug AND halved before 5 Oct  -> timing consistent with controlled release
  C  still >= 50 % of peak at the last image                  -> late / persistent flooding
  B  other
NISAR measures water on the field, not its cause; areas exceed planned release areas, so natural flooding is mixed in.
Outputs: data/processed/stats/commune_flood_class.csv, docs/figures/fig4_flood_release.png
"""
import csv, collections, datetime as dt
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.dates as mdates
from . import config as C

# Tan Chau (Tien river) water level reported in the press, m (context only; not official observations)
RIVER = [("2026-08-17", 2.80), ("2026-08-22", 2.81), ("2026-08-26", 3.09), ("2026-09-30", 3.45), ("2026-10-06", 2.82),
         ("2026-10-14", 2.62), ("2026-10-19", 2.16)]
NAMED = ["Xã Bình Mỹ", "Xã Thạnh Mỹ Tây", "Xã Bình Thạnh Đông"]   # communes named in 2026 flood-release news
TRACK_PREF = {"047D": 0, "083A": 1, "148D": 2}
COL = {"047D": "#1f6feb", "083A": "#e8590c", "148D": "#2f9e44"}


def classify(rows):
    ser = collections.defaultdict(list)
    for r in rows:
        if float(r["valid_km2"]) >= 5:
            ser[(r["osm_id"], r["commune"], r["province"], r["track"])].append((r["date"], float(r["water_pct"])))
    best = {}
    for (oid, c, p, t), s in ser.items():
        seas = sorted(x for x in s if x[0] >= C.FLOOD_SEASON_START)
        if not seas:
            continue
        pk_d, pk = max(seas, key=lambda x: x[1])
        if pk < 30:
            continue
        onset = next((a for a, b in seas if b >= 0.5 * pk), None)
        half = next((a for a, b in seas if a > pk_d and b < 0.5 * pk), None)
        last_d, last = seas[-1]
        cls = "A" if onset and onset <= "2026-08-18" and half and half <= "2026-10-05" else ("C" if last >= 0.5 * pk else "B")
        rec = dict(osm_id=oid, commune=c, province=p, track=t, onset50=onset, peak_pct=round(pk, 1), peak_date=pk_d,
                   halved=half, last_date=last_d, last_pct=round(last, 1), cls=cls)
        if oid not in best or TRACK_PREF[t] < TRACK_PREF[best[oid]["track"]]:
            best[oid] = rec
    return list(best.values())


def figure(rows):
    fig, axes = plt.subplots(1, len(NAMED), figsize=(13, 3.6), sharey=True)
    for ax, nm in zip(axes, NAMED):
        for trk, c in COL.items():
            rr = sorted([r for r in rows if r["commune"] == nm and r["track"] == trk], key=lambda r: r["date"])
            if rr:
                ax.plot([dt.date.fromisoformat(r["date"]) for r in rr], [float(r["water_pct"]) for r in rr], "-o", ms=3, c=c, label=f"NISAR {trk}")
        ax2 = ax.twinx()
        ax2.plot([dt.date.fromisoformat(d) for d, _ in RIVER], [v for _, v in RIVER], "k--", lw=1.2)
        ax2.set_ylim(1.5, 4.0); ax2.axhline(3.0, c="k", lw=.6, alpha=.4)
        ax2.set_ylabel("Tan Chau river level (m)" if ax is axes[-1] else ""); ax2.tick_params(labelright=ax is axes[-1])
        ax.axvspan(dt.date(2026, 9, 21), dt.date(2026, 10, 5), color="#ffe066", alpha=.35)
        ax.set_title(nm.replace("Xã ", "") + " (named in 2026 flood-release plan)", fontsize=9)
        ax.xaxis.set_major_locator(mdates.MonthLocator()); ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
        ax.grid(alpha=.3)
    axes[0].set_ylabel("% of commune under water"); axes[0].legend(fontsize=7, loc="upper left")
    fig.suptitle("Water enters in mid-Aug while the river is below alarm level 1 (3.0 m, dashed = river level) and leaves in late Sep - "
                 "early Oct while the river peaks (yellow):\nthe timing of a controlled flood release (gates opened, then pumped out), "
                 "not of natural recession", fontsize=9)
    fig.tight_layout()
    out = C.ROOT / "docs" / "figures"; out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / "fig4_flood_release.png", dpi=150)


def main():
    rows = list(csv.DictReader(open(C.PROCESSED / "stats/commune_water_by_date.csv")))
    best = classify(rows)
    with open(C.PROCESSED / "stats/commune_flood_class.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(best[0])); w.writeheader(); w.writerows(best)
    print(collections.Counter(r["cls"] for r in best))
    figure(rows)


if __name__ == "__main__":
    main()
