# The atlas

This fork publishes three atlases. Each one is built only from the
institutions that publish its numbers, and every plate is drawn from CSVs
committed under `countries/<slug>/data`.

Method: [SOURCING_A_COUNTRY.md](SOURCING_A_COUNTRY.md), then
[ADDING_A_COUNTRY.md](ADDING_A_COUNTRY.md).

## Published

| Slug | Languages | Plates | Datasets |
|------|-----------|--------|----------|
| `brasil` | pt · en · ko · zh-Hans | 12 | 55 |
| `china` | zh-Hans · en · pt · ko | 12 | 55 |
| `south-korea` | ko · en · pt · zh-Hans | 12 | 58 |

Every country publishes in four locales: its own official language, English,
Portuguese and the other East Asian edition. Every plate is drawn in each of
them.

## Language policy

The locale codes are ISO language codes, not country codes: `ko` for Korean,
`zh-Hans` for Simplified Chinese, `pt` for Brazilian Portuguese, `en` for
English. Each locale directory carries a complete translation catalog, page
copy and rendered plates. The renderer fails the build on any untranslated
string, and `tests/test_catalogs.py` draws every plate in every locale to
prove it.

## Known problems, written down before they are hit

**China's problem is not the language.** The National Bureau of Statistics
publishes a full set of numbers; the question a reader will have is whether
to believe them. The atlas does not answer that question by leaving China
out or by substituting a Western estimate for an official one. It publishes
what the NBS publishes, marked as such, beside the international series —
World Bank, IMF, UN Comtrade — where those exist, and says in the notes where
the two disagree and by how much. Quarterly NBS evidence remains unavailable,
so the recession-band decision is explicitly pending rather than inferred
from positive annual growth.

**Brazil's series break and stay broken.** Homicides counted from death
certificates and police records are drawn side by side, never spliced; the
tax burden before and after its 2010 methodology change is annotated, not
smoothed across.

**Korea's political timeline is drawn separately from the data.** Presidencies
and shocks are annotation only. A shock band is drawn where the data moves,
not where the news broke.

**Number styles.** `AFFIX` and `CURRENCY_AFFIX` in `core/sitebuild.py` and
the unit rules in `core/i18n.py` are keyed by number style
(`core/numstyle.py`). `tests/test_numbers.py` fails on a locale or currency
with no form. The three currencies here — BRL, CNY and KRW — carry forms for
all four locales.
