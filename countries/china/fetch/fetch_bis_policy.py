#!/usr/bin/env python3
"""Refresh China's policy/lending rate, split at the 2019 LPR reform.

Usage:  python3 -I countries/china/fetch/fetch_bis_policy.py

BIS dataflow WS_CBPOL, series D.CN, daily end-of-period. The BIS compiles the
series from the People's Bank of China and states the break in its own
COMPILATION attribute: the official 1-year lending rate until 19 Aug 2019,
the 1-year LPR from 20 Aug 2019. This fetcher keeps the two regimes in two
columns and never splices them; 2019 carries a partial-year average in each.

Annual values here are simple averages of the daily observations, matching
the annual-average convention of the other rate series on the plate.

Checks: the payload must be the CN series with the expected compilation
note, at least 10,000 observations from 1996, and the annual averages for
2010 and 2025 are spot-checked before anything is written.

Output: data/markets/policy_rate_bis_from_bis.csv
Curated: data/markets/policy_rate.csv (promoted after review).
"""
from __future__ import annotations

import math
import re
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "markets"
URL = "https://stats.bis.org/api/v1/data/WS_CBPOL/D.CN"
BREAK = "2019-08-20"
FIRST, LAST = 2006, 2025
SPOT = {2010: ("official", 5.364), 2025: ("lpr", 3.033)}

OBS = re.compile(r'<Obs TIME_PERIOD="([^"]+)" OBS_VALUE="([^"]+)"')


def main() -> int:
    with urllib.request.urlopen(URL, timeout=60) as response:
        text = response.read().decode("utf-8")
    if "SOURCE_REF=\"People's Bank of China\"" not in text:
        raise RuntimeError("BIS payload is not the PBoC-sourced CN series")
    if "From 20 Aug 2019 onwards: Loan Prime Rate" not in text:
        raise RuntimeError("BIS payload lost the LPR compilation note")
    observations = OBS.findall(text)
    if len(observations) < 10_000:
        raise RuntimeError(f"only {len(observations)} observations — capped?")

    buckets = defaultdict(list)
    for day, raw in observations:
        try:
            value = float(raw)
        except ValueError:
            continue
        if math.isnan(value):
            continue
        year = int(day[:4])
        if FIRST <= year <= LAST:
            regime = "official" if day < BREAK else "lpr"
            buckets[(year, regime)].append(value)

    rows = {}
    for year in range(FIRST, LAST + 1):
        official = buckets.get((year, "official"))
        lpr = buckets.get((year, "lpr"))
        rows[year] = (
            sum(official) / len(official) if official else None,
            sum(lpr) / len(lpr) if lpr else None,
        )
    for year, (regime, want) in SPOT.items():
        got = rows[year][0] if regime == "official" else rows[year][1]
        if got is None or abs(got - want) > 0.05:
            raise RuntimeError(f"{year} {regime} = {got}, expected {want}")

    DATA.mkdir(parents=True, exist_ok=True)
    out = DATA / "policy_rate_bis_from_bis.csv"
    with out.open("w", encoding="utf-8", newline="") as fh:
        fh.write("year,official_lending_1y,lpr_1y\n")
        for year, (official, lpr) in rows.items():
            fh.write(f"{year},"
                     f"{'' if official is None else f'{official:.3f}'},"
                     f"{'' if lpr is None else f'{lpr:.3f}'}\n")
    print(f"  {len(observations)} daily observations, {FIRST}-{LAST}")
    print(f"  wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
