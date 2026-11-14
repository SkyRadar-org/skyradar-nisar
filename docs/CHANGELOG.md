# Changelog

## 2026-11-14 — Full-commune coverage gate and reproducible assessment (Codex, Gemini reviewed)

- Select the newest acquisition observing ≥50% of each full OSM commune and ≥5 km², before rounding; retain partial observations as evidence only. Search all acquisitions so a newer sliver cannot replace an older eligible pass on the same track.
- Regenerate the committed assessment CSV: 43 low, 39 moderate, 33 high water-share assessments, plus 16 partial CSV records; 25/140 communes lack an eligible assessment overall.
- Add area_km2 / observed_pct to the frontend API, guard no_flood behind sufficient coverage, expose status=partial and partial_count in the original API.
- Rebuild CSV-based figures without Earthdata/raster inputs; replace partially observed examples with Vĩnh Hưng and Phương Thịnh. Water share uses the observed-area denominator and is not a sowing recommendation.
- Update method, submission draft, API/data documentation and handoff. Preserve original review evidence, with an explicit correction about the existing disclosure wrapper in Overview.
- Regression and UI evidence, Gemini static reviews and release status: `verification/ux-implementation-20261114/README.md`. No production release is implied by this branch.

## 2026-11-14 — Export aligned radar images for the evidence view (Codex)

- Add radarJpg to frontend scene metadata, using the existing processed image for the same acquisition. Original FastAPI routes and scientific datasets remain unchanged.
- Extend scene tests to verify JPEG signatures for all 33 radar images; all 11 backend tests pass.
- The sibling water-pulse-fe repository contains the purpose-first UX changes, three Gemini review rounds, real-data observation tests and production verification.

## 2026-11-14 — Restore Cloud handoff for Cloudflare Pages (Codex)

- Restored all tracked patches and additional source files from the Cloud handoff on a separate branch, preserving the original transfer bundle.
- Frontend uses the same-origin `/api/frontend/*` snapshot through an advanced-mode Pages Worker; the original FastAPI routes remain available in the backend source.
- Verified locally: 11 backend tests, 4 generated-Worker tests, complete Cloudflare build (179 API snapshots, 33 scenes, 140 communes, 333 files).
- Frontend additionally fixes missing values appearing first in descending table sort and limits native NISAR GIBS zoom to 10. Browser verified 140 table rows and six missing observations last in both directions.
- Gemini 4 Argon High reviewed the supplied source in two static-analysis rounds; Codex executed tests and corrected overbroad claims in the first review.
- Production deployment is tracked in the sibling frontend repository’s `docs/LOCAL_DEPLOYMENT.md`; no PR, merge, backend main branch or GitHub Actions were created.
