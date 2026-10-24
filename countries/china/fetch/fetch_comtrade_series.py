#!/usr/bin/env python3
"""Refresh China's goods-export destination shares, 2006–2025.

Usage:  python3 -I countries/china/fetch/fetch_comtrade_series.py

UN Comtrade, public PREVIEW endpoint (no key): annual C/A/HS, reporter 156
(China), cmdCode TOTAL, flow X (exports), every partner, one year per query.
The preview endpoint 429s when polled fast, so requests are spaced and
retried.

This is the time series behind the spine's `trade.destinations` panel. It is
a harmonised cross-check on partner shares, NOT GACC's national customs
series: GACC's machine layer is 412-blocked (SOURCES.yaml pending), and the
two must never be spliced. The panel says "UN Comtrade" in its footer.

Scope: the ten partners that matter across the window — the top eight in
2025 plus Germany and the Russian Federation, both large buyers earlier.
All values are the reporter's own customs values in US$.

Checks before anything is written: every year must hold 100+ partner rows,
one World row, the reporter and flow requested, TOTAL as the product, and
partner rows must sum to the World total within 1%. Known World totals are
spot-checked for 2006, 2023 and 2025.

Output: data/trade/trade_comtrade_partners_from_comtrade.csv
Curated: data/trade/trade_comtrade_partners.csv (promoted after review;
the header there records the definition and the blocked GACC counterpart).
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "trade"
CACHE = ROOT / "cache" / "comtrade"

API = ("https://comtradeapi.un.org/public/v1/preview/C/A/HS"
       "?reporterCode=156&period={period}&flowCode={flow}&cmdCode=TOTAL"
       "&format=json")
PERIODS = tuple(range(2006, 2026))
FLOW = "X"
REPORTER = 156
WORLD = 0

# Comtrade legacy numeric partner codes. Names match the plate catalog keys.
PARTNERS = (
    (842, "United States"),
    (344, "China (Hong Kong SAR)"),
    (704, "Viet Nam"),
    (392, "Japan"),
    (410, "Korea, Rep."),
    (699, "India"),
    (276, "Germany"),
    (528, "Netherlands"),
    (643, "Russian Federation"),
    (458, "Malaysia"),
)

# World goods exports, US$, read off the preview on 2026-10-24.
SPOT = {
    2006: 968935601013.0,
    2023: 3379747834884.0,
    2025: 3776380766122.0,
}


def validate(year: int, payload: dict) -> list[dict]:
    rows = payload.get("data")
    if not isinstance(rows, list) or len(rows) < 100:
        raise ValueError(f"{year}: only {len(rows or [])} partner rows")
    if payload.get("count") != len(rows):
        raise ValueError(f"{year}: count {payload.get('count')} != {len(rows)}")
    if any(r.get("reporterCode") != REPORTER or r.get("flowCode") != FLOW
           for r in rows):
        raise ValueError(f"{year}: payload holds another reporter or flow")
    if any(r.get("cmdCode") != "TOTAL" for r in rows):
        raise ValueError(f"{year}: payload is not the TOTAL aggregate")
    world = [r for r in rows if r.get("partnerCode") == WORLD]
    if len(world) != 1 or not world[0].get("primaryValue"):
        raise ValueError(f"{year}: no single World (partnerCode 0) row")
    got = world[0]["primaryValue"]
    want = SPOT.get(year)
    if want is not None and abs(got - want) / want > 0.02:
        raise ValueError(f"{year}: World total {got:,.0f} moved >2% from "
                         f"the verified {want:,.0f}")
    parts = sum(r["primaryValue"] for r in rows
                if r.get("partnerCode") not in (WORLD, REPORTER))
    # The reporter's own re-imports stay in the World denominator but are
    # not a partner; compare the rest against World minus that row.
    own = sum(r["primaryValue"] for r in rows
              if r.get("partnerCode") == REPORTER)
    if abs(parts + own - got) / got > 0.01:
        raise ValueError(f"{year}: partners sum {parts + own:,.0f} vs "
                         f"World {got:,.0f} — silent row cap")
    return rows


def fetch(year: int) -> list[dict]:
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / f"comtrade_series_{year}_{FLOW}.json"
    if path.exists():
        try:
            return validate(year, json.loads(path.read_text(encoding="utf-8")))
        except Exception as e:  # noqa: BLE001
            print(f"  stale cache {path.name}: {e}", file=sys.stderr)
            path.unlink()
    url = API.format(period=year, flow=FLOW)
    last: Exception | None = None
    for attempt in range(6):
        try:
            with urllib.request.urlopen(url, timeout=60) as response:
                raw = response.read()
            payload = json.loads(raw)
            rows = validate(year, payload)
            path.write_bytes(raw)
            return rows
        except Exception as e:  # noqa: BLE001
            last = e
            wait = 5 * (attempt + 1)
            print(f"  {year}: {e}; retrying in {wait}s", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError(f"{year}: {last}")


def main() -> int:
    out = []
    for year in PERIODS:
        rows = fetch(year)
        world = next(r for r in rows if r["partnerCode"] == WORLD)["primaryValue"]
        by_code = {r["partnerCode"]: r["primaryValue"] for r in rows}
        print(f"  {year}: World US${world / 1e9:,.1f}bn")
        for code, name in PARTNERS:
            value = by_code.get(code)
            if value is None or value <= 0:
                continue
            out.append((year, name, value, value / world * 100))
        time.sleep(2.5)

    sidecar = DATA / "trade_comtrade_partners_from_comtrade.csv"
    with sidecar.open("w", encoding="utf-8", newline="") as fh:
        fh.write("year,partner,exports_usd,share_pct\n")
        for year, name, value, share in out:
            fh.write(f'{year},"{name}",{value:.0f},{share:.2f}\n')
    print(f"\nwrote {sidecar} ({len(out)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
