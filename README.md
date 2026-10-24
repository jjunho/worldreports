# worldreports.io

Plates of official statistics, one country at a time.

Three atlases — Brazil, China and South Korea — built only from the numbers
each country's own institutions publish. 36 plates, 12 country-language
editions, 168 committed datasets, 2006 to 2026. Each country is published in
Portuguese, Korean, Simplified Chinese and English.

This is a fork of **[worldreports.io](https://worldreports.io)** containing
only Brazil, China and South Korea.

Every chart is regenerated from CSVs committed in this repository. Nothing
reads an API at draw time, so a figure on a page and the file behind it
cannot drift apart, and any plate can be reproduced from the commit it was
built at.

---

## What is here

```
countries/<slug>/      one country, and nothing of any other
  country.yaml           its name, languages, palette, years, currency
  data/                  the committed CSVs every plate is drawn from
  SOURCES.yaml           who publishes each file and how it is refreshed
  provenance.json        which CSVs each plate was watched reading
  plates.py              the drawing code
  chapters.py            the cards: titles, blurbs, headline figures
  i18n.json              the plate strings, translated
  ui.json                the masthead line, the dek, the reading notes
  events.py              its recessions, shocks and political calendar
  fetch/                 the refreshers (the only code that uses the network)
  output/                the rendered plates, committed
  tests/                 what can only be asked of this country

core/                  everything the three share, and no country's name
  country.py             the Country object — and the isolation boundary
  style.py               the figure: palette, header, footer, fonts
  plotting.py            the one CSV reader, and the drawing primitives
  i18n.py                the translation engine
  context.py             what a plate is handed
  render.py              draw one country, or all of them
  thumbs.py              the card-sized copies
  provenance.py          watch a plate draw and record what it read
  sitebuild.py           the cards' numbers, formatted per language
  page.py                the static pages
  qa.py                  the layout checker

site/                  the page chrome: one stylesheet, one script, one catalog
tests/                 everything that must hold for every country
```

## Running it

```sh
pip install -r requirements.txt
make                      # render, thumbnail, record provenance, build, test
make serve                # build _site and serve it on :8000
make C=brasil charts      # just one country's plates
make test                 # everything, including the slow render suites
```

Korean and Chinese plates need a CJK font (`fonts-noto-cjk` on Debian and Ubuntu). The
build refuses to draw a language it has no font for rather than publishing
a page of empty boxes.

## The rule everything rests on

**No code that draws one country's plate may read another country's data.**

Three atlases that used to be separate repositories now share a checkout, and
the failure that matters is not a crash. It is a Korean number on a
Brazilian plate, which nobody notices, because both are plausible.

So the rule is mechanical, not a convention:

- every read goes through `core.country.within`, which resolves the path
  and refuses anything outside `countries/<slug>/` — a `..` segment, an
  absolute path and a symlink pointing out are all caught by the same test;
- `tests/test_isolation.py` draws every plate and builds every card with
  the filesystem watched, and fails on any read outside the country's own
  directory. It is verified to catch a deliberate breach;
- `core.provenance` records what each plate actually read, and
  `tests/test_sources.py` checks every recorded file is one the country's
  own manifest declares;
- `tests/test_core.py` reads the shared code and fails if it names a
  country at all — in code; a comment may explain one.

Adding a country is therefore a directory, not an edit to anything shared.
**[ADDING_A_COUNTRY.md](ADDING_A_COUNTRY.md)** is the mechanics;
**[SOURCING_A_COUNTRY.md](SOURCING_A_COUNTRY.md)** is the research that
comes first — which eleven questions an atlas answers, which institution
answers each of them, and the traps that have already produced a wrong
published chart here.

## Where the numbers come from

Each country's `SOURCES.yaml` names every CSV, who publishes it, and how
it is refreshed; each page prints that table with the years read off the
files themselves rather than off the manifest. A dataset is official
unless the manifest says otherwise, and any series here that is not —
a market reading or a redistributor's estimate — says so in the file and
on the page.

Fetchers never overwrite a curated number. They write what they pulled to
a sidecar beside it — `<name>_check.csv` or `<name>_from_<source>.csv` —
so a bad upstream day shows up as a diff a person reads, not as a plate
that quietly changed. No plate is ever drawn from a sidecar, and a test
enforces that.

### What proved hardest

Source difficulty has two distinct forms. China is the hardest access
problem: the NBS machine interface returns HTTP 403, Customs returns 412,
and several central-bank and fiscal series endpoints could not be isolated.
Brazil and Korea are the harder normalization problems, because
available-looking figures often measure different things: police records
against death certificates in Brazil, and a presidential timeline against
quarterly data in Korea. Each is published as a separate, labelled series
rather than averaged into one line.

The practical lesson is to keep access failure separate from comparability
failure. A statistic may not exist, may exist but resist reliable fetching,
or may have a nearby proxy with a different definition. Those cases remain
separate here rather than being hidden behind a plausible substitute.

## Reading the plates honestly

- **The running year is not a full year.** Annual totals stop at the last
  complete year; a reading that is genuinely current — a debt stock, a
  policy rate, a closing price — is marked as the latest point instead.
- **Broken series are left broken.** Where two sources measure the same
  idea differently, both are drawn and the difference is named. They are
  never spliced into one line.
- **A figure is a picture of a table.** Every plate on every page carries
  the committed files it was drawn from, and the page carries the table
  itself wherever the country declares one, so a reader who cannot see the
  chart still has the numbers.

## Licence

Code is MIT. The data belongs to the institutions that published it; each
file's source is named in its country's `SOURCES.yaml`.
