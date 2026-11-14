"""Water classification from NISAR GCOV dB rasters (rule calibrated against OPERA DSWx-S1)."""
import numpy as np
from scipy import ndimage
from . import config as C


def water_map(hh_db, hv_db, th_hh=C.TH_HH_DB, th_hv=C.TH_HV_DB, mmu=C.MMU_PX):
    """Open water on land: HH and HV both dark, connected patches >= mmu pixels. Returns (water, valid)."""
    valid = np.isfinite(hh_db) & np.isfinite(hv_db)
    m = (hh_db < th_hh) & (hv_db < th_hv) & valid
    if mmu > 1:
        lab, _ = ndimage.label(m)
        size = np.bincount(lab.ravel()); keep = size >= mmu; keep[0] = False
        m = keep[lab]
    return m, valid


def permanent_water(dswx_s1_stack, min_dates=C.PERMANENT_MIN_DATES):
    """Rivers/canals/lakes: DSWx-S1 open water (class 1) on >= min_dates dates, buffered by one pixel."""
    count = np.sum([w == 1 for w in dswx_s1_stack], axis=0)
    return ndimage.binary_dilation(count >= min_dates, iterations=1)
