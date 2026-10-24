"""The brasil chapters: the cards, their copy and their headline figures.

Editorial copy lives here. Every number is read from this country's CSVs at
build time by the context, so a figure on a card and the same figure on its
plate cannot disagree.

`spec` names how a figure is written, not what it means — see
core.sitebuild.NUMFMT and AFFIX. `kind` says whether it is current:
'flow' for an annual total that is only comparable once the year is
complete, 'level' for a stock or a rate read at a moment, 'projection' for
an official forward estimate.
"""
from __future__ import annotations

MONEY, WORLD, PEOPLE = "money", "world", "people"


def per_100k(ctx, count_col, pop_mn_col):
    """(year, rate) pairs: a count over the same year's population in
    millions, ×100,000 — the same conversion the plates draw."""
    pop = dict(pop_mn_col)
    return [(y, v / (pop[y] * 1e6) * 1e5) for y, v in count_col if y in pop]


def trillions(pairs):
    """Convert a series stored in billions of reais to trillions."""
    return [(year, value / 1_000) for year, value in pairs]


def headline(ctx) -> list[dict]:
    """The figures the page leads with, above the plates.

    Six readings that frame everything below, computed from this country's
    CSVs at build time rather than typed in, so a refetch moves them
    instead of leaving the page quietly describing last year.

    `kind` is the load-bearing argument. An annual total or average is a
    flow: it stops at the last complete year, because the running year's
    partial figure is not comparable with the ones before it. A stock or a
    population estimate is a level, read at a moment and genuinely
    current. The year is printed under each figure by the page, from the
    row it was actually read from, so the labels do not repeat it.
    """
    return [
        ctx.stat({"pt": 'PIB', "en": 'GDP', "ko": "국내총생산", "zh-Hans": "国内生产总值"},
                 trillions(ctx.col("macro/gdp.csv", "nominal_rbi")),
                 "money_tn1"),
        ctx.stat({"pt": 'PIB por pessoa, US$', "en": 'GDP per person, US$', "ko": "1인당 GDP, US$", "zh-Hans": "人均GDP，美元"},
                 ctx.col("macro/gdp.csv", "gdp_per_capita_usd"), "count"),
        ctx.stat({"pt": 'População', "en": 'Population', "ko": "인구", "zh-Hans": "人口"},
                 ctx.col("macro/gdp.csv", "population_mn"), "pop_mn", kind="level"),
        ctx.stat({"pt": 'IPCA', "en": 'Inflation (IPCA)', "ko": "물가상승률 (IPCA)", "zh-Hans": "通胀（IPCA）"},
                 ctx.col("macro/ipca.csv", "value"), "pct"),
        ctx.stat({"pt": 'Desemprego', "en": 'Unemployment', "ko": "실업률", "zh-Hans": "失业率"},
                 ctx.col("macro/unemployment.csv", "value"), "pct"),
        ctx.stat({"pt": 'Dívida bruta', "en": 'Gross public debt', "ko": "공공 총부채", "zh-Hans": "公共总债务"},
                 ctx.col("fiscal/debt.csv", "gross"), "pct_gdp", kind="level"),
    ]


def build(ctx) -> list[dict]:
    chapters = [
        {
            "id": "01_economy", "topic": "economy", "n": "01", "family": MONEY,
            "title": ctx.text(en="The Brazilian Economy", pt="A Economia Brasileira", ko="브라질 경제", **{"zh-Hans": "巴西经济"}),
            "blurb": ctx.text(en="Real growth, income per person in dollars, inflation "
                "against the target and unemployment at a series low.", pt="Crescimento real, renda por pessoa em dólares, inflação "
                "contra a meta e desemprego na mínima da série.", ko="실질성장, 달러 기준 1인당 소득, 목표 대비 물가상승률과 시계열 최저 실업률.", **{"zh-Hans": "实际增长、美元计价人均收入、通胀与目标的比较，以及序列最低失业率。"}),
            "spark": ctx.col("macro/gdp.csv", "nominal_rbi"),
            "stats": [
                ctx.stat({"en": "GDP", "pt": "PIB", "ko": "국내총생산", "zh-Hans": "国内生产总值"},
                     trillions(ctx.col("macro/gdp.csv", "nominal_rbi")),
                     "money_tn1"),
                ctx.stat({"en": "Real growth", "pt": "Crescimento real", "ko": "실질성장", "zh-Hans": "实际增长"},
                     ctx.col("macro/gdp.csv", "real_growth"), "pct_s"),
                ctx.stat({"en": "Inflation", "pt": "Inflação", "ko": "물가상승률", "zh-Hans": "通胀"},
                     ctx.col("macro/ipca.csv", "value"), "pct"),
            ],
        },
        {
            "id": "02_fiscal", "topic": "fiscal", "n": "02", "family": MONEY,
            "title": ctx.text(en="Balance, Debt & Interest", pt="Resultado, Dívida e Juros", ko="재정수지, 부채와 이자", **{"zh-Hans": "财政收支、债务与利息"}),
            "blurb": ctx.text(en="General government on the IMF's basis, beside the "
                "measures Brazil argues in: the primary result, DBGG gross debt and the "
                "interest bill.", pt="O governo geral pelo critério do FMI, ao lado das "
                "medidas do debate brasileiro: resultado primário, dívida bruta DBGG e a "
                "conta de juros.", ko="IMF 기준 일반정부와 브라질의 주요 지표: 기초재정수지, DBGG 총부채와 이자비용.", **{"zh-Hans": "IMF口径的一般政府与巴西讨论中的指标并列：基本财政收支、DBGG总债务及利息支出。"}),
            "spark": ctx.col("fiscal/general_government.csv", "gross_debt_pct_gdp"),
            "spark_level": True,
            "stats": [
                ctx.stat({"en": "Gross debt (IMF)", "pt": "Dívida bruta (FMI)", "ko": "총부채 (IMF)", "zh-Hans": "总债务（IMF）"},
                     ctx.col("fiscal/general_government.csv", "gross_debt_pct_gdp"),
                     "pct_gdp", kind="level"),
                ctx.stat({"en": "Overall balance", "pt": "Resultado nominal", "ko": "종합재정수지", "zh-Hans": "总体财政收支"},
                     ctx.col("fiscal/general_government.csv", "balance_pct_gdp"),
                     "pct_gdp_s"),
                ctx.stat({"en": "Interest (NFSP)", "pt": "Juros (NFSP)", "ko": "이자 (NFSP)", "zh-Hans": "利息（NFSP）"},
                     ctx.col("fiscal/nfsp.csv", "interest"), "pct_gdp"),
            ],
        },
        {
            "id": "03_spending", "topic": "spending", "n": "03", "family": MONEY,
            "title": ctx.text(en="Where the Money Goes", pt="Para Onde Vai o Dinheiro", ko="돈은 어디로 가는가", **{"zh-Hans": "资金流向"}),
            "blurb": ctx.text(en="Spending by function — social protection against "
                "everything else — and how little the economy invests.", pt="Gasto por função — a proteção social contra todo o "
                "resto — e quão pouco a economia investe.", ko="기능별 지출 — 사회보호와 그 외 전체 — 그리고 경제의 낮은 투자 수준.", **{"zh-Hans": "按职能划分的支出——社会保护与其余全部——以及经济的低投资水平。"}),
            "spark": ctx.col("fiscal/spending_by_function_rbi.csv", "previdencia"),
            "stats": [
                ctx.stat({"en": "Pensions", "pt": "Previdência", "ko": "연금", "zh-Hans": "养老金"},
                     ctx.col("fiscal/spending_by_function_rbi.csv", "previdencia"), "money_bn"),
                ctx.stat({"en": "Health", "pt": "Saúde", "ko": "보건", "zh-Hans": "卫生"},
                     ctx.col("fiscal/spending_by_function_rbi.csv", "saude"), "money_bn"),
                ctx.stat({"en": "Investment", "pt": "Investimento", "ko": "투자", "zh-Hans": "投资"},
                     ctx.col("fiscal/spending_by_function_rbi.csv", "investimento_gnd4"), "money_bn"),
            ],
        },
        {
            "id": "06_trade", "topic": "trade", "n": "06", "family": WORLD,
            "title": ctx.text(en="Foreign Trade", pt="Comércio Exterior", ko="대외무역", **{"zh-Hans": "对外贸易"}),
            "blurb": ctx.text(en="A commodity-heavy export machine, a diversified import "
                "bill, and China replacing everyone else.", pt="Uma pauta de exportação pesada em commodities, uma conta de "
                "importação diversificada, e a China substituindo todo mundo.", ko="원자재 중심 수출, 다변화된 수입, 다른 교역국을 대체하는 중국.", **{"zh-Hans": "以大宗商品为主的出口、多元化进口，以及逐步取代其他伙伴的中国。"}),
            "spark": ctx.col("trade/trade.csv", "balance"),
            "stats": [
                ctx.stat({"en": "Exports", "pt": "Exportações", "ko": "수출", "zh-Hans": "出口"},
                     ctx.col("trade/trade.csv", "exports"), "usd_bn"),
                ctx.stat({"en": "Imports", "pt": "Importações", "ko": "수입", "zh-Hans": "进口"},
                     ctx.col("trade/trade.csv", "imports"), "usd_bn"),
                ctx.stat({"en": "Balance", "pt": "Saldo", "ko": "무역수지", "zh-Hans": "贸易差额"},
                     ctx.col("trade/trade.csv", "balance"), "usd_bn_s"),
            ],
        },
        {
            "id": "04_markets", "topic": "markets", "n": "04", "family": MONEY,
            "title": ctx.text(en="Money & Markets", pt="Moeda e Mercados", ko="통화와 시장", **{"zh-Hans": "货币与市场"}),
            "blurb": ctx.text(en="Brazilian equities in reais, in dollars, and beside the "
                "S&P 500 — the currency is half the story.", pt="A bolsa brasileira em reais, em dólares e ao lado do "
                "S&P 500 — o câmbio é metade da história.", ko="헤알과 달러 기준 브라질 주식, S&P 500과의 비교 — 환율이 이야기의 절반.", **{"zh-Hans": "雷亚尔与美元计价的巴西股票及其与S&P 500的比较——汇率是关键因素之一。"}),
            "spark": ctx.col("macro/dollar.csv", "eop"),
            "spark_level": True,
            "stats": [
                ctx.stat({"en": "USD/BRL", "pt": "Dólar", "ko": "USD/BRL", "zh-Hans": "USD/BRL"},
                     ctx.col("macro/dollar.csv", "eop"), "money2", kind="level"),
                ctx.stat({"en": "Selic", "pt": "Selic", "ko": "Selic", "zh-Hans": "Selic"},
                     ctx.col("macro/selic.csv", "value"), "pct2", kind="level"),
                ctx.stat({"en": "Ibovespa", "pt": "Ibovespa", "ko": "Ibovespa", "zh-Hans": "Ibovespa"},
                     ctx.col("markets/ibov.csv", "close"), "count", kind="level"),
            ],
        },
        {
            "id": "08_people", "topic": "people", "n": "08", "family": PEOPLE,
            "title": ctx.text(en="Inequality, Poverty & Wages", pt="Desigualdade, Pobreza e Salários", ko="불평등, 빈곤과 임금", **{"zh-Hans": "不平等、贫困与工资"}),
            "blurb": ctx.text(en="Inequality, how far poverty actually fell, and a "
                "minimum wage that gained far more in reais than in dollars.", pt="A desigualdade, quanto a pobreza realmente caiu e "
                "um salário mínimo que ganhou muito mais em reais do que em dólares.", ko="불평등, 실제 빈곤 감소폭, 달러보다 헤알 기준으로 훨씬 크게 오른 최저임금.", **{"zh-Hans": "不平等、贫困实际降幅，以及雷亚尔计价增幅远高于美元计价的最低工资。"}),
            "spark": ctx.col("social/poverty.csv", "poverty_pct"),
            "stats": [
                ctx.stat({"en": "Gini (IBGE)", "pt": "Gini (IBGE)", "ko": "지니계수 (IBGE)", "zh-Hans": "基尼系数（IBGE）"},
                     ctx.col("social/gini.csv", "ibge"), "dec3"),
                ctx.stat({"en": "Poverty, US$8.30 a day", "pt": "Pobreza, US$ 8,30 por dia", "ko": "빈곤, 하루 US$8.30", "zh-Hans": "贫困，每日8.30美元"},
                     ctx.col("social/poverty.csv", "poverty_pct"), "pct"),
                ctx.stat({"en": "Minimum wage, R$ a month", "pt": "Salário mínimo, R$ por mês", "ko": "최저임금, 월 R$", "zh-Hans": "最低工资，每月雷亚尔"},
                     ctx.col("macro/minimum_wage.csv", "value"), "count",
                     kind="level"),
            ],
        },
        {
            "id": "07_world", "topic": "world", "n": "07", "family": WORLD,
            "title": ctx.text(en="Brazil in the World", pt="O Brasil no Mundo", ko="세계 속 브라질", **{"zh-Hans": "世界中的巴西"}),
            "blurb": ctx.text(en="The economy in dollars, how the UNDP and Transparency "
                "International score Brazil, and the reserves behind the real.", pt="A economia em dólares, como o PNUD e a Transparência "
                "Internacional avaliam o Brasil, e as reservas por trás do real.", ko="달러 기준 경제, UNDP와 Transparency International의 브라질 평가, 헤알화를 뒷받침하는 외환보유액.", **{"zh-Hans": "美元计价经济、UNDP与Transparency International对巴西的评价，以及支撑雷亚尔的储备。"}),
            "spark": ctx.col("macro/reserves.csv", "eop_usbi"),
            "spark_level": True,
            "stats": [
                ctx.stat({"en": "Reserves", "pt": "Reservas", "ko": "외환보유액", "zh-Hans": "储备"},
                     ctx.col("macro/reserves.csv", "eop_usbi"), "usd_bn", kind="level"),
                ctx.stat({"en": "Corruption index", "pt": "Índice de corrupção", "ko": "부패지수", "zh-Hans": "腐败指数"},
                     ctx.col("international/cpi.csv", "score"), "score100"),
                ctx.stat({"en": "HDI", "pt": "IDH", "ko": "인간개발지수", "zh-Hans": "人类发展指数"},
                     ctx.col("social/hdi.csv", "value"), "dec3"),
            ],
        },
        {
            "id": "09_demographics", "topic": "demography", "n": "09", "family": PEOPLE,
            "title": ctx.text(en="The Demographic Transition", pt="A Transição Demográfica", ko="인구 전환", **{"zh-Hans": "人口转型"}),
            "blurb": ctx.text(en="Fertility down a third since 2000. The population peaks in "
                "2041 and shrinks from 2042.", pt="Fecundidade um terço menor desde 2000. A população atinge o "
                "pico em 2041 e encolhe a partir de 2042.", ko="2000년 이후 출산율 3분의 1 감소. 인구는 2041년 정점을 찍고 2042년부터 감소.", **{"zh-Hans": "生育率自2000年以来下降三分之一。人口于2041年达峰，自2042年起减少。"}),
            "spark": [p for p in ctx.col("social/population.csv", "tfr") if p[0] <= 2040],
            "spark_level": True,
            "stats": [
                ctx.stat({"en": "Fertility rate", "pt": "Taxa de fecundidade", "ko": "출산율", "zh-Hans": "生育率"},
                     ctx.col("social/population.csv", "tfr"), "dec2", year=2024),
                ctx.stat({"en": "Births", "pt": "Nascimentos", "ko": "출생아 수", "zh-Hans": "出生数"},
                     ctx.col("social/population.csv", "births"), "count", year=2024),
                ctx.stat({"en": "Population", "pt": "População", "ko": "인구", "zh-Hans": "人口"},
                     ctx.col("social/population.csv", "pop_mn"), "pop_mn",
                     year=2026, kind="projection"),
            ],
        },
        {
            "id": "10_security", "topic": "security", "n": "10", "family": PEOPLE,
            "title": ctx.text(en="Violence", pt="Violência", ko="폭력", **{"zh-Hans": "暴力"}),
            "blurb": ctx.text(en="Homicides falling while recorded deaths resulting from police intervention rise — two "
                "measurement systems, deliberately not spliced.", pt="Homicídios caindo enquanto os óbitos registrados decorrentes de intervenção policial aumentam — "
                "dois sistemas de medição, deliberadamente não emendados.", ko="살인은 감소하지만 경찰 개입에 따른 등록 사망은 증가 — 의도적으로 연결하지 않은 두 측정체계.", **{"zh-Hans": "凶杀下降，而记录的警方干预致死人数上升——两套测量体系，刻意不作拼接。"}),
            "spark": ctx.col("social/homicides.csv", "rate"),
            "stats": [
                ctx.stat({"en": "Homicide rate", "pt": "Taxa de homicídios", "ko": "살인율", "zh-Hans": "凶杀率"},
                     ctx.col("social/homicides.csv", "rate"), "per100k"),
                ctx.stat({"en": "Deaths following police intervention", "pt": "Mortes decorrentes de intervenção policial", "ko": "경찰 개입에 따른 사망", "zh-Hans": "警方干预致死"},
                     per_100k(ctx, ctx.col("social/violence_fbsp.csv", "police_killings"),
                              ctx.col("social/population.csv", "pop_mn")), "per100k"),
                ctx.stat({"en": "Femicides", "pt": "Feminicídios", "ko": "여성살해", "zh-Hans": "杀害女性"},
                     ctx.col("social/violence_fbsp.csv", "femicides"), "count"),
            ],
        },
        {
            "id": "11_epidemics", "topic": "mortality", "n": "11", "family": PEOPLE,
            "title": ctx.text(en="Mortality & Epidemics", pt="Mortalidade e Epidemias", ko="사망과 유행병", **{"zh-Hans": "死亡与疫情"}),
            "blurb": ctx.text(en="COVID killed 425,218 in 2021 alone. Dengue set its record "
                "in 2024, and influenza in 2025.", pt="A COVID matou 425.218 só em 2021. A dengue bateu recorde "
                "em 2024, e a influenza em 2025.", ko="COVID로 2021년에만 425,218명 사망. 뎅기열은 2024년, 인플루엔자는 2025년에 최고치.", **{"zh-Hans": "仅2021年COVID就造成425,218人死亡。登革热于2024年创纪录，流感则在2025年。"}),
            # the COVID column is the striking one but it is two orders of
            # magnitude above the others and nearly flat since 2023; dengue
            # carries the shape a sparkline can actually show
            "spark": ctx.col("social/epidemic_deaths.csv", "dengue"),
            "stats": [
                ctx.stat({"en": "Registered deaths", "pt": "Óbitos registrados", "ko": "등록 사망", "zh-Hans": "登记死亡"},
                     ctx.col("social/deaths.csv", "registered"), "count"),
                ctx.stat({"en": "COVID-19 deaths", "pt": "Óbitos por COVID-19", "ko": "COVID-19 사망", "zh-Hans": "COVID-19死亡"},
                     ctx.col("social/epidemic_deaths.csv", "covid"), "count"),
                ctx.stat({"en": "Dengue deaths", "pt": "Óbitos por dengue", "ko": "뎅기열 사망", "zh-Hans": "登革热死亡"},
                     ctx.col("social/epidemic_deaths.csv", "dengue"), "count"),
            ],
        },
        {
            "id": "05_credit", "topic": "credit", "n": "05", "family": MONEY,
            "title": ctx.text(en="Credit & Household Debt", pt="Crédito e Endividamento", ko="신용과 가계부채", **{"zh-Hans": "信贷与家庭债务"}),
            "blurb": ctx.text(en="Households owe half a year's income and pay 38% a year to "
                "borrow. Debt service and arrears are at series highs.", pt="As famílias devem meio ano de renda e pagam 38% ao ano para "
                "tomar emprestado. Serviço da dívida e inadimplência no topo "
                "da série.", ko="가계부채는 반년 소득 규모이며 차입금리는 연 38%. 원리금 상환부담과 연체는 시계열 최고.", **{"zh-Hans": "家庭负债相当于半年收入，借款年利率为38%。偿债支出与逾期均处序列高位。"}),
            "spark": ctx.col("macro/household_debt.csv", "debt_income"),
            "spark_level": True,
            "stats": [
                # all three are point-in-time readings, not annual totals,
                # so the August 2026 value is genuinely the current one
                ctx.stat({"en": "Household debt", "pt": "Endividamento das famílias", "ko": "가계부채", "zh-Hans": "家庭债务"},
                     ctx.col("macro/household_debt.csv", "debt_income"), "pct",
                     kind="level"),
                ctx.stat({"en": "Rate paid by households", "pt": "Juros pagos pelas famílias", "ko": "가계 차입금리", "zh-Hans": "家庭借款利率"},
                     ctx.col("macro/credit.csv", "rate_pf"), "pct", kind="level"),
                ctx.stat({"en": "Credit / GDP", "pt": "Crédito / PIB", "ko": "신용 / GDP", "zh-Hans": "信贷／GDP"},
                     ctx.col("macro/credit.csv", "credit_gdp"), "pct_gdp",
                     kind="level"),
            ],
        },
        {
            "id": "12_migration", "topic": "migration", "n": "12", "family": PEOPLE,
            "title": ctx.text(en="Migration, on compatible definitions", pt="Migração, em definições compatíveis", ko="국제이동, 호환되는 정의 기준", **{"zh-Hans": "迁移，按可兼容定义"}),
            "blurb": ctx.text(en="Modelled net migration and census stocks; unresolved gross components stay visibly pending.", pt="Migração líquida modelada e estoques censitários; componentes brutos incompatíveis ficam visivelmente pendentes.", ko="모형 순이동과 총조사 인구; 미해결 총이동 구성요소는 명시적으로 보류.", **{"zh-Hans": "模型净迁移与普查存量；未厘清的总流量组成部分明确标为待解决。"}),
            "spark": ctx.col("migration/stock_census.csv", "foreign_born_pct"),
            "spark_level": True,
            "stats": [ctx.stat({"en": "Foreign-born", "pt": "Nascidos no exterior", "ko": "외국 출생", "zh-Hans": "外国出生"}, ctx.col("migration/stock_census.csv", "foreign_born_pct"), "pct", kind="level")],
        },
    ]

    # Plate numbers are assigned by family — money 01-05, world 06-07,
    # people 08-11 — so sorting by id is what groups the index page. The
    # editorial blocks above stay in the order they were written, because
    # moving them would make every future diff look like a rewrite.
    chapters.sort(key=lambda c: c["id"])

    return chapters
