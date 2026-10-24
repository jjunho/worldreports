"""The South Korea chapters: the cards, their copy and their provenance.

The title, blurb and alt text of each plate are the strings the standalone
site published, in all four languages. `alt` is written prose about what
the plate shows rather than a generated summary, which is why it is kept
verbatim: it is the only thing a reader using a screen reader gets.

`sources` lists the CSVs a plate draws, so the page can link a figure to
its own provenance rather than to the whole manifest.

Every chapter declares its spine topic (PLATE_SPINE.md). The alt text
describes the plate as drawn on the spine: the shared indicators in the
shared units, and Korea's own story in the lens slot where a topic has
one.
"""
from __future__ import annotations

MONEY, WORLD, PEOPLE = "money", "world", "people"


def headline(ctx) -> list[dict]:
    """The figures the page carries above the plates.

    The year is whatever the latest filled row turns out to be: stating a
    figure without its year is how a dashboard goes quietly stale.
    """
    return [
        ctx.stat(
            {"ko": '국내총생산', "en": 'GDP', "pt": 'PIB', "zh-Hans": '国内生产总值'},
            ctx.col('macro/gdp.csv', 'nominal_krw_tn'), 'money_tn', kind="level"),
        ctx.stat(
            {"ko": '1인당 GDP', "en": 'GDP per person', "pt": 'PIB por pessoa', "zh-Hans": '人均GDP'},
            ctx.col('macro/gdp.csv', 'gdp_per_capita_usd'), 'count', kind="level"),
        ctx.stat(
            {"ko": '인구', "en": 'Population', "pt": 'População', "zh-Hans": '人口'},
            ctx.col('macro/gdp.csv', 'population_mn'), 'pop_mn', kind="level"),
        ctx.stat(
            {"ko": '합계출산율', "en": 'Births per woman', "pt": 'Filhos por mulher', "zh-Hans": '平均每名妇女生育子女数'},
            ctx.col('social/population.csv', 'tfr'), 'dec2', kind="level"),
        ctx.stat(
            {"ko": '수출', "en": 'Exports', "pt": 'Exportações', "zh-Hans": '出口'},
            ctx.col('trade/trade.csv', 'exports'), 'usd_bn', kind="level"),
        ctx.stat(
            {"ko": '국가채무(D2)', "en": 'Public debt (D2)', "pt": 'Dívida pública (D2)', "zh-Hans": '公共债务（D2）'},
            ctx.col('fiscal/debt.csv', 'd2'), 'pct_gdp', kind="level"),
        ctx.stat(
            {"ko": '가계부채', "en": 'Household debt', "pt": 'Dívida das famílias', "zh-Hans": '住户债务'},
            ctx.col('macro/household_credit.csv', 'credit_pct_gdp'), 'pct_gdp', kind="level"),
        ctx.stat(
            {"ko": '65세 이상 빈곤율', "en": 'Poverty at 65+', "pt": 'Pobreza aos 65+', "zh-Hans": '65岁及以上人口贫困率'},
            ctx.col('social/poverty.csv', 'elderly_65'), 'pct', kind="level"),
        ctx.stat(
            {"ko": '자살률', "en": 'Suicide rate', "pt": 'Taxa de suicídio', "zh-Hans": '自杀率'},
            ctx.col('social/mortality.csv', 'suicide'), 'per100k', kind="level"),
        ctx.stat(
            {"ko": '순대외금융자산', "en": 'Net foreign assets', "pt": 'Ativos externos líquidos', "zh-Hans": '净对外金融资产'},
            ctx.col('macro/external.csv', 'net_usbi'), 'usd_bn', kind="level"),
    ]


def build(ctx) -> list[dict]:
    S = ctx.stat
    return [
        {
            "id": '01_economy', "topic": "economy", "n": '01', "family": MONEY,
            "title": ctx.text(ko='한국 경제', en='The Korean Economy',
                              pt='A Economia Coreana', **{"zh-Hans": '韩国经济'}),
            "blurb": ctx.text(
                ko='실질 성장, 1인당 소득, 물가, 일자리 — 다른 나라와 같은 축에서.',
                en='Real growth, income per person, prices and jobs, on the same scales as every other country.',
                pt='Crescimento real, renda por pessoa, preços e emprego, nas mesmas escalas de todos os outros países.', **{"zh-Hans": '实际增长、人均收入、物价与就业，采用与其他国家相同的刻度。'}),
            "alt": ctx.text(
                ko='한국 경제를 다룬 네 개 패널(2006–2026). 실질 GDP 성장률은 2020년(-0.7%)을 빼면 매년 플러스이고 2025년에는 1.1%로, 이보다 낮았던 해는 2009년과 2020년뿐이다. 1인당 GDP(세계은행, 경상 달러, 로그 눈금)는 약 22,600달러에서 36,200달러로 올랐고, 2009년과 2022년의 하락은 환율 때문이다. 소비자물가 상승률은 2019년 0.4%까지 내려갔다가 2022년 5.1%로 정점을 찍고 2% 목표 근처로 돌아왔다. 실업률은 내내 2.7%에서 4.0% 사이다.',
                en='Four panels on the Korean economy, 2006–2026. Real GDP growth is positive every year except 2020 (-0.7%) and is 1.1% in 2025, slower only in 2009 and 2020. GDP per person (World Bank, current dollars, log scale) rises from about US$22,600 to US$36,200, with dips in 2009 and 2022 caused by the won. Consumer price inflation falls to 0.4% in 2019, peaks at 5.1% in 2022 and returns to near the 2% target. Unemployment stays between 2.7% and 4.0% throughout.',
                pt='Quatro painéis sobre a economia coreana, 2006–2026. O crescimento real do PIB é positivo em todos os anos menos 2020 (-0,7%) e fica em 1,1% em 2025, mais lento só em 2009 e 2020. O PIB por pessoa (Banco Mundial, dólares correntes, escala log) sobe de cerca de US$22.600 para US$36.200, com quedas em 2009 e 2022 causadas pelo câmbio. A inflação ao consumidor cai para 0,4% em 2019, chega a 5,1% em 2022 e volta para perto da meta de 2%. O desemprego fica entre 2,7% e 4,0% o tempo todo.', **{"zh-Hans": '2006–2026年韩国经济的四个面板。除2020年（-0.7%）外，实际GDP每年均为正增长；2025年增长1.1%，仅2009年和2020年更低。人均GDP（世界银行，现价美元，对数刻度）从约22,600美元升至36,200美元，2009年和2022年的回落源于韩元汇率。居民消费价格通胀率在2019年降至0.4%，2022年达到5.1%的峰值，随后回到2%目标附近。失业率始终介于2.7%与4.0%之间。'}),
            "sources": ['macro/gdp.csv', 'intl/world.csv', 'macro/cpi.csv',
                        'macro/unemployment.csv'],
            "spark": ctx.col('macro/gdp.csv', 'real_growth'),
            "stats": [
                S({"ko": '실질 성장률', "en": 'Real growth', "pt": 'Crescimento real', "zh-Hans": '实际增长率'},
                  ctx.col('macro/gdp.csv', 'real_growth'), 'pct'),
                S({"ko": '물가상승률', "en": 'Inflation', "pt": 'Inflação', "zh-Hans": '通胀率'},
                  ctx.col('macro/cpi.csv', 'value'), 'pct'),
            ],
        },
        {
            "id": '02_fiscal', "topic": "fiscal", "n": '02', "family": MONEY,
            "title": ctx.text(ko='재정', en='Public Finances',
                              pt='Contas Públicas', **{"zh-Hans": '公共财政'}),
            "blurb": ctx.text(
                ko='일반정부가 GDP의 얼마를 거두고 쓰는지, 그 차이가 빚과 이자에 어떻게 쌓이는지.',
                en='What general government raises and spends as a share of GDP, and what the gap does to debt and interest.',
                pt='Quanto o governo geral arrecada e gasta como proporção do PIB, e o que a diferença faz com a dívida e os juros.', **{"zh-Hans": '广义政府收入与支出占GDP的比重，以及两者差额如何影响债务与利息。'}),
            "alt": ctx.text(
                ko='한국 재정을 다룬 네 개 패널. 일반정부 총수입과 총지출은 IMF 기준으로 2012년부터, 그 이전은 한국은행 국민계정으로 따로 그렸다. 2019년까지는 수입이 지출보다 많았고 2020년부터는 반대다. 재정수지는 2020년 -2.5%, 2024년 -2.6%다. 총부채(IMF, 한국의 D2와 같다)는 2012년 GDP의 33.5%에서 2025년 52.4%로, 중앙·지방정부 채무 D1은 27.0%에서 48.8%로 늘었다. 이자 지급은 GDP의 1~2%로 2025년 1.42%이지만, 이자 수입을 빼면 0.3%에 그친다.',
                en='Four panels on Korean public finances. General government revenue and expenditure are drawn from the IMF from 2012 and from the Bank of Korea national accounts before that, as separate segments. Revenue exceeds spending until 2019; spending is higher from 2020. The balance is -2.5% of GDP in 2020 and -2.6% in 2024. Gross debt (IMF, the same as Korea\'s D2) rises from 33.5% of GDP in 2012 to 52.4% in 2025, and central and local government debt, D1, from 27.0% to 48.8%. Interest paid stays between 1% and 2% of GDP, 1.42% in 2025, but only 0.3% net of the interest the state receives.',
                pt='Quatro painéis sobre as contas públicas coreanas. Receita e despesa do governo geral vêm do FMI a partir de 2012 e das contas nacionais do Banco da Coreia antes disso, em segmentos separados. A receita supera a despesa até 2019; a partir de 2020 a despesa é maior. O resultado é de -2,5% do PIB em 2020 e -2,6% em 2024. A dívida bruta (FMI, igual ao D2 coreano) sobe de 33,5% do PIB em 2012 para 52,4% em 2025, e a dívida do governo central e local, D1, de 27,0% para 48,8%. Os juros pagos ficam entre 1% e 2% do PIB, 1,42% em 2025, mas só 0,3% descontados os juros que o Estado recebe.', **{"zh-Hans": '韩国公共财政的四个面板。广义政府收支自2012年起采用国际货币基金组织数据，此前采用韩国银行国民账户，分段绘制。2019年以前收入高于支出，2020年起支出更高。收支差额在2020年为GDP的-2.5%，2024年为-2.6%。债务总额（国际货币基金组织口径，与韩国D2相同）从2012年GDP的33.5%升至2025年的52.4%；中央和地方政府债务D1从27.0%升至48.8%。利息支出保持在GDP的1%至2%之间，2025年为1.42%，但扣除政府利息收入后仅为0.3%。'}),
            "sources": ['fiscal/general_government_imf.csv', 'fiscal/government.csv',
                        'fiscal/debt.csv', 'fiscal/tax_burden.csv'],
            "spark": ctx.col('fiscal/general_government_imf.csv', 'gross_debt_pct_gdp'),
            "spark_level": True,
            "stats": [
                S({"ko": '총부채(IMF)', "en": 'Gross debt (IMF)', "pt": 'Dívida bruta (FMI)', "zh-Hans": '债务总额（国际货币基金组织）'},
                  ctx.col('fiscal/general_government_imf.csv', 'gross_debt_pct_gdp'), 'pct_gdp'),
                S({"ko": '재정수지', "en": 'Balance', "pt": 'Resultado', "zh-Hans": '收支差额'},
                  ctx.col('fiscal/general_government_imf.csv', 'balance_pct_gdp'), 'pct_gdp_s'),
            ],
        },
        {
            "id": '03_spending', "topic": "spending", "n": '03', "family": MONEY,
            "title": ctx.text(ko='돈이 가는 곳', en='Where the Money Goes',
                              pt='Para Onde Vai o Dinheiro', **{"zh-Hans": '资金流向'}),
            "blurb": ctx.text(
                ko='기능별 일반정부 지출, 그리고 경제와 정부의 투자.',
                en='General government outlays by function, and the investment the economy and the state make.',
                pt='Gastos do governo geral por função, e o investimento da economia e do Estado.', **{"zh-Hans": '按职能划分的广义政府支出，以及全社会与政府的投资。'}),
            "alt": ctx.text(
                ko='정부 지출을 다룬 네 개 패널. 기능별 지출을 일곱 묶음으로 쌓으면 GDP의 27.5%(2006년)에서 35.3%(2024년)로 늘고, 사회보호가 4.2%에서 9.2%로 가장 크게 늘었다. 나머지 기능의 합은 대체로 평평하다. 경제 전체의 투자율은 GDP의 30% 안팎이고, 그중 연구개발비는 2023년 4.94%로 이스라엘 다음이다. 정부 투자는 GDP의 4~5%이며 경기부양이 있었던 2009년 6.2%가 정점이다.',
                en='Four panels on Korean government spending. Outlays by function, stacked in seven groups, rise from 27.5% of GDP in 2006 to 35.3% in 2024, and social protection grows most, from 4.2% to 9.2%; all other functions together are roughly flat. Whole-economy investment stays near 30% of GDP; R&D alone is 4.94% of GDP in 2023, second only to Israel. Government investment runs at 4–5% of GDP, peaking at 6.2% in the 2009 stimulus.',
                pt='Quatro painéis sobre o gasto público coreano. O gasto por função, empilhado em sete grupos, sobe de 27,5% do PIB em 2006 para 35,3% em 2024, e a proteção social é a que mais cresce, de 4,2% para 9,2%; todas as outras funções juntas ficam praticamente estáveis. O investimento de toda a economia fica perto de 30% do PIB; só a P&D é 4,94% do PIB em 2023, atrás apenas de Israel. O investimento do governo fica em 4–5% do PIB, com pico de 6,2% no estímulo de 2009.', **{"zh-Hans": '韩国政府支出的四个面板。按职能分为七组堆叠显示的支出从2006年GDP的27.5%升至2024年的35.3%；社会保护增幅最大，从4.2%升至9.2%，其余职能合计大致持平。全社会投资保持在GDP的30%左右；2023年仅研发就占4.94%，仅次于以色列。政府投资约占GDP的4–5%，在2009年经济刺激期间达到6.2%的峰值。'}),
            "sources": ['fiscal/spending_by_function.csv', 'fiscal/investment.csv',
                        'fiscal/government.csv', 'fiscal/rnd.csv'],
            "spark": ctx.col('fiscal/spending_by_function.csv', 'total'),
            "spark_level": True,
            "stats": [
                S({"ko": '총지출', "en": 'Total outlays', "pt": 'Gasto total', "zh-Hans": '支出总额'},
                  ctx.col('fiscal/spending_by_function.csv', 'total'), 'pct_gdp'),
                S({"ko": '사회보호', "en": 'Social protection', "pt": 'Proteção social', "zh-Hans": '社会保护'},
                  ctx.col('fiscal/spending_by_function.csv', 'social_protection'), 'pct_gdp'),
            ],
        },
        {
            "id": '04_trade', "topic": "trade", "n": '04', "family": WORLD,
            "title": ctx.text(ko='대외무역', en='Foreign Trade',
                              pt='Comércio Exterior', **{"zh-Hans": '对外贸易'}),
            "blurb": ctx.text(
                ko='GDP의 40%를 넘게 수출하는 제조업 국가 — 반도체, 자동차, 선박, 그리고 중국에서 미국으로 옮겨 가는 수출.',
                en='A manufacturer that exports more than 40% of GDP: semiconductors, cars and ships, and a market shifting from China to the United States.',
                pt='Um fabricante que exporta mais de 40% do PIB: semicondutores, carros e navios, e um mercado que migra da China para os Estados Unidos.', **{"zh-Hans": '出口超过GDP的40%的制造业国家：半导体、汽车与船舶，以及由中国转向美国的出口市场。'}),
            "alt": ctx.text(
                ko='무역을 다룬 네 개 패널. 재화·서비스 수출은 GDP의 34.5%(2006년)에서 2012년 52.0%로 정점을 찍고 2025년 45.8%이며, 수입은 33.9%에서 40.6%다. 무역수지는 2008년 소폭 적자, 에너지 수입이 컸던 2022년 0.0%를 빼면 흑자다. 수출 중 중국 비중은 2018년 26.8%에서 2025년 18.4%로 내려왔고 미국은 17.3%로 올라왔으며, 베트남이 일본을 앞질렀다. 한국의 시선 패널은 기준연도별 주요 수출품으로, 반도체가 2025년 1,430억 달러다.',
                en='Four panels on Korean trade. Exports of goods and services rise from 34.5% of GDP in 2006 to a 52.0% peak in 2012 and stand at 45.8% in 2025; imports go from 33.9% to 40.6%. The trade balance is in surplus except for a small deficit in 2008 and 0.0% in 2022, the year of the energy bill. China\'s share of goods exports falls from 26.8% in 2018 to 18.4% in 2025 while the United States rises to 17.3%, and Vietnam overtakes Japan. The lens panel shows the main export products at five snapshot years, with semiconductors at US$143 billion in 2025.',
                pt='Quatro painéis sobre o comércio coreano. As exportações de bens e serviços sobem de 34,5% do PIB em 2006 para um pico de 52,0% em 2012 e ficam em 45,8% em 2025; as importações vão de 33,9% para 40,6%. O saldo é superavitário, exceto por um pequeno déficit em 2008 e 0,0% em 2022, o ano da conta de energia. A fatia da China nas exportações de bens cai de 26,8% em 2018 para 18,4% em 2025 enquanto os Estados Unidos sobem para 17,3%, e o Vietnã ultrapassa o Japão. O painel-lente mostra os principais produtos exportados em cinco anos de referência, com os semicondutores em US$143 bilhões em 2025.', **{"zh-Hans": '韩国贸易的四个面板。货物和服务出口从2006年GDP的34.5%升至2012年52.0%的峰值，2025年为45.8%；进口从33.9%升至40.6%。除2008年小幅逆差及能源进口负担沉重的2022年为0.0%外，贸易均为顺差。中国占货物出口的比重从2018年的26.8%降至2025年的18.4%，美国则升至17.3%，越南超过日本。专题面板展示五个选定年份的主要出口产品，2025年半导体出口为1,430亿美元。'}),
            "sources": ['trade/trade_gdp.csv', 'trade/trade.csv', 'trade/destinations.csv',
                        'trade/exports_products.csv'],
            "spark": ctx.col('trade/trade_gdp.csv', 'exports_pct_gdp'),
            "stats": [
                S({"ko": '수출', "en": 'Exports', "pt": 'Exportações', "zh-Hans": '出口'},
                  ctx.col('trade/trade_gdp.csv', 'exports_pct_gdp'), 'pct_gdp'),
                S({"ko": '상품수지', "en": 'Goods balance', "pt": 'Saldo de bens', "zh-Hans": '货物贸易差额'},
                  ctx.col('trade/trade.csv', 'balance'), 'usd_bn'),
            ],
        },
        {
            "id": '05_markets', "topic": "markets", "n": '05', "family": MONEY,
            "title": ctx.text(ko='돈과 시장', en='Money & Markets',
                              pt='Dinheiro e Mercados', **{"zh-Hans": '货币与市场'}),
            "blurb": ctx.text(
                ko='기준금리, 국고채 금리, 원화, 그리고 달러로 본 코스피 — 환율이 이야기의 절반이다.',
                en='The base rate, the bond yield, the won, and the KOSPI in dollars: the currency is half of the story.',
                pt='A taxa básica, o juro dos títulos, o won e o KOSPI em dólares: o câmbio é metade da história.', **{"zh-Hans": '基准利率、国债收益率、韩元和以美元计价的韩国综合股价指数：汇率是理解走势的一半。'}),
            "alt": ctx.text(
                ko='한국 금융시장을 다룬 네 개 패널. 한국은행 기준금리(연말)는 2020년 0.50%까지 내려갔다가 2023년 3.50%로 올랐다. 10년 만기 국고채 금리는 2006년 5.15%에서 2020년 1.50%로 바닥을 찍고 2025년 2.89%다. 원화를 2006=100 지수로 보면(위로 갈수록 강세) 2025년 66.9로, 연평균 환율이 951원에서 1,421원이 됐다. 달러로 환산한 코스피는 2025년 189.8로 S&P 500의 482.7에 크게 못 미친다.',
                en='Four panels on Korean markets. The Bank of Korea base rate (year-end) falls to 0.50% in 2020 and rises to 3.50% in 2023. The ten-year government bond yield falls from 5.15% in 2006 to a low of 1.50% in 2020 and is 2.89% in 2025. The won, as an index with 2006 = 100 where up is stronger, stands at 66.9 in 2025: the annual average went from ₩951 to ₩1,421 per dollar. The KOSPI in dollars reaches 189.8 in 2025, far behind the S&P 500 at 482.7.',
                pt='Quatro painéis sobre os mercados coreanos. A taxa básica do Banco da Coreia (fim de ano) cai para 0,50% em 2020 e sobe para 3,50% em 2023. O juro do título de dez anos cai de 5,15% em 2006 para a mínima de 1,50% em 2020 e está em 2,89% em 2025. O won, como índice com 2006 = 100 em que para cima é mais forte, fica em 66,9 em 2025: a média anual passou de ₩951 para ₩1.421 por dólar. O KOSPI em dólares chega a 189,8 em 2025, muito atrás do S&P 500, em 482,7.', **{"zh-Hans": '韩国市场的四个面板。韩国银行年末基准利率在2020年降至0.50%，2023年升至3.50%。10年期国债收益率从2006年的5.15%降至2020年1.50%的低点，2025年为2.89%。韩元指数以2006年＝100、上升代表升值，2025年为66.9；年平均汇率从每美元₩951变为₩1,421。以美元计价的韩国综合股价指数在2025年达到189.8，远低于标普500指数的482.7。'}),
            "sources": ['macro/base_rate.csv', 'macro/cpi.csv', 'markets/bond_10y.csv',
                        'macro/won.csv', 'markets/kospi.csv', 'markets/sp500.csv'],
            "spark": ctx.col('macro/won.csv', 'avg'),
            "stats": [
                S({"ko": '기준금리', "en": 'Base rate', "pt": 'Taxa básica', "zh-Hans": '基准利率'},
                  ctx.col('macro/base_rate.csv', 'value'), 'pct2', kind="level"),
                S({"ko": '국고채 10년', "en": '10-year yield', "pt": 'Juro de 10 anos', "zh-Hans": '10年期收益率'},
                  ctx.col('markets/bond_10y.csv', 'ktb_10y'), 'pct2'),
            ],
        },
        {
            "id": '06_people', "topic": "people", "n": '06', "family": PEOPLE,
            "title": ctx.text(ko='사람', en='People', pt='Pessoas', **{"zh-Hans": '民生'}),
            "blurb": ctx.text(
                ko='부유한 나라의 가난한 노년 — 줄어드는 불평등 옆의 OECD 최악 노인빈곤.',
                en="A rich country with a poor old age: falling inequality next to the OECD's worst elderly poverty.",
                pt='Um país rico com uma velhice pobre: desigualdade em queda ao lado da pior pobreza na terceira idade da OCDE.', **{"zh-Hans": '富裕国家，贫困晚年：不平等程度下降，却伴随着经合组织最严重的老年贫困。'}),
            "alt": ctx.text(
                ko='생활 수준을 다룬 네 개 패널. 지니계수(0–100)는 서로 다른 두 조사에서 나온 값이라 잇지 않고 따로 그렸다. 가계금융복지조사 기준으로 2011년 38.7에서 2024년 32.5로 낮아졌다. 중위소득 50% 미만 상대적 빈곤율은 18.5%에서 15.3%로 내려갔고, 세계은행의 하루 8.30달러 기준으로는 1% 미만이다. 최저임금은 정부가 쓰는 월 209시간으로 환산해 달러로 바꾸면 2006년 681달러에서 2021년 1,589달러로 오른 뒤 원화 약세로 1,500달러 안팎에 머문다. 한국의 시선 패널은 65세 이상 빈곤율로, 2024년 이전소득 후 35.9%, 이전소득 전 54.9%다.',
                en='Four panels on living standards in Korea. The Gini coefficient (0–100) comes from two surveys and is drawn as two separate lines, never joined; on the current survey it falls from 38.7 in 2011 to 32.5 in 2024. Relative poverty, below half the median income, falls from 18.5% to 15.3%; on the World Bank\'s US$8.30 a day line it is under 1%. The minimum wage, converted at the government\'s 209 hours a month and the year\'s average exchange rate, rises from US$681 a month in 2006 to US$1,589 in 2021 and then holds near US$1,500 as the won weakens. The lens shows poverty at 65 and over: 35.9% after transfers in 2024, against 54.9% before them.',
                pt='Quatro painéis sobre o padrão de vida na Coreia. O coeficiente de Gini (0–100) vem de duas pesquisas e aparece em duas linhas separadas, nunca emendadas; na pesquisa atual cai de 38,7 em 2011 para 32,5 em 2024. A pobreza relativa, abaixo de metade da renda mediana, cai de 18,5% para 15,3%; na linha de US$8,30 por dia do Banco Mundial fica abaixo de 1%. O salário mínimo, convertido pelas 209 horas mensais do governo e pelo câmbio médio do ano, sobe de US$681 por mês em 2006 para US$1.589 em 2021 e depois fica perto de US$1.500 com o won mais fraco. A lente mostra a pobreza aos 65 anos ou mais: 35,9% depois das transferências em 2024, contra 54,9% antes delas.', **{"zh-Hans": '韩国生活水平的四个面板。基尼系数（0–100）来自两项调查，绘制为两条独立曲线，不予拼接；现行调查显示该系数从2011年的38.7降至2024年的32.5。低于收入中位数一半的相对贫困率从18.5%降至15.3%；按世界银行每日8.30美元贫困线计算则低于1%。最低工资按政府采用的每月209小时及当年平均汇率换算，从2006年每月681美元升至2021年的1,589美元，随后因韩元贬值维持在1,500美元左右。专题展示65岁及以上人口贫困率：2024年转移支付后为35.9%，转移支付前为54.9%。'}),
            "sources": ['social/gini.csv', 'social/gini_wb.csv', 'social/poverty.csv',
                        'social/poverty_wb.csv', 'macro/minimum_wage.csv', 'macro/won.csv'],
            "spark": ctx.col('social/poverty.csv', 'elderly_65'),
            "spark_level": True,
            "stats": [
                S({"ko": '65세 이상 빈곤율', "en": 'Poverty at 65+', "pt": 'Pobreza aos 65+', "zh-Hans": '65岁及以上人口贫困率'},
                  ctx.col('social/poverty.csv', 'elderly_65'), 'pct', kind="level"),
                S({"ko": '상대적 빈곤율', "en": 'Relative poverty', "pt": 'Pobreza relativa', "zh-Hans": '相对贫困率'},
                  ctx.col('social/poverty.csv', 'relative'), 'pct', kind="level"),
            ],
        },
        {
            "id": '07_world', "topic": "world", "n": '07', "family": WORLD,
            "title": ctx.text(ko='세계 속의 한국', en='Korea in the World',
                              pt='A Coreia no Mundo', **{"zh-Hans": '世界中的韩国'}),
            "blurb": ctx.text(
                ko='달러로 본 경제 규모, 인간개발, 세계가 보는 청렴도, 그리고 외환보유액.',
                en='The size of the economy in dollars, human development, how the world scores Korea for integrity, and the reserves.',
                pt='O tamanho da economia em dólares, o desenvolvimento humano, como o mundo avalia a integridade da Coreia, e as reservas.', **{"zh-Hans": '以美元计价的经济规模、人类发展、国际社会对韩国清廉程度的评价，以及储备。'}),
            "alt": ctx.text(
                ko='한국의 국제적 위치를 다룬 네 개 패널. 명목 GDP는 2006년 1조 952억 달러에서 2025년 1조 8,724억 달러로 늘었다(로그 눈금). 인간개발지수는 0.871에서 0.937로 올라 0.900 기준선을 2012년에 넘었다. 부패인식지수는 2012년 56점에서 2024년 64점, 2025년 63점이며, 2012년 이전은 옛 0–10점 척도에 10을 곱해 옅게 그렸다. 외환보유액은 2,390억 달러에서 2025년 4,281억 달러로 늘었고, 한국은 2014년부터 순대외채권국이다.',
                en='Four panels placing Korea internationally. GDP in current dollars grows from US$1,095 billion in 2006 to US$1,872 billion in 2025 (log scale). The Human Development Index rises from 0.871 to 0.937, crossing the 0.900 line in 2012. The Corruption Perceptions Index score goes from 56 in 2012 to 64 in 2024 and 63 in 2025; the years before 2012, on the old 0–10 scale, are drawn paler, multiplied by ten. Official reserves grow from US$239 billion to US$428 billion in 2025, and Korea has been a net creditor to the rest of the world since 2014.',
                pt='Quatro painéis situando a Coreia no mundo. O PIB em dólares correntes cresce de US$1.095 bilhões em 2006 para US$1.872 bilhões em 2025 (escala log). O Índice de Desenvolvimento Humano sobe de 0,871 para 0,937 e cruza a linha de 0,900 em 2012. A pontuação no Índice de Percepção da Corrupção vai de 56 em 2012 para 64 em 2024 e 63 em 2025; os anos antes de 2012, na antiga escala de 0 a 10, aparecem mais claros, multiplicados por dez. As reservas crescem de US$239 bilhões para US$428 bilhões em 2025, e a Coreia é credora líquida do resto do mundo desde 2014.', **{"zh-Hans": '韩国国际地位的四个面板。现价美元GDP从2006年的1,095十亿美元升至2025年的1,872十亿美元（对数刻度）。人类发展指数从0.871升至0.937，2012年超过0.900。清廉指数从2012年的56分升至2024年的64分，2025年为63分；2012年以前采用旧版0–10分制，乘以10后以浅色绘制。官方储备从239十亿美元升至2025年的428十亿美元；韩国自2014年起成为净对外债权国。'}),
            "sources": ['intl/world.csv', 'macro/gdp.csv', 'social/hdi.csv', 'intl/cpi.csv',
                        'macro/reserves.csv', 'macro/external.csv'],
            "spark": ctx.col('intl/world.csv', 'gdp_usd_bn'),
            "stats": [
                S({"ko": 'GDP', "en": 'GDP', "pt": 'PIB', "zh-Hans": '国内生产总值'},
                  ctx.col('intl/world.csv', 'gdp_usd_bn'), 'usd_bn'),
                S({"ko": '부패인식지수', "en": 'CPI score', "pt": 'Nota no IPC', "zh-Hans": '清廉指数得分'},
                  ctx.col('intl/cpi.csv', 'score'), 'score100', kind="level"),
            ],
        },
        {
            "id": '08_demography', "topic": "demography", "n": '08', "family": PEOPLE,
            "title": ctx.text(ko='인구 전환', en="Korea's Demographic Transition",
                              pt='A Transição Demográfica Coreana', **{"zh-Hans": '韩国的人口转型'}),
            "blurb": ctx.text(
                ko='평시에 기록된 가장 낮은 출산율, 그리고 2020년에 정점을 지난 인구.',
                en='The lowest fertility rate ever recorded in peacetime, and a population that peaked in 2020.',
                pt='A menor taxa de fecundidade já registrada em tempos de paz, e uma população que atingiu o pico em 2020.', **{"zh-Hans": '和平时期有记录以来最低的生育率，以及2020年达到峰值的人口。'}),
            "alt": ctx.text(
                ko='인구를 다룬 네 개 패널. 인구를 2006=100 지수로 보면 2020년 5,184만 명에서 정점을 찍었고, 2024년 장래인구추계는 2072년 3,622만 명을 내다본다. 65세 이상 비중은 2025년 20.3%다. 합계출산율은 2023년 0.721로 세계 최저를 기록한 뒤 2025년 0.799로 조금 올랐으며 대체 수준 2.1에 한참 못 미친다. 인구 1천 명당 조출생률과 조사망률은 2020년에 교차했다. 자연증가는 2020년부터 마이너스이고(2025년 -2.1), 국제 순이동은 국경이 닫힌 2021년(-1.3)을 빼면 플러스다.',
                en='Four panels on Korean demography. The population, indexed to 2006, peaks at 51.84 million in 2020, and the official 2024 projection has 36.2 million by 2072; 20.3% of people are 65 or older in 2025. The total fertility rate hits a world-low 0.721 in 2023 and recovers slightly to 0.799 in 2025, far below the replacement level of 2.1. The crude birth and death rates per 1,000 cross in 2020. Natural increase is negative from 2020 (-2.1 per 1,000 in 2025), while net international migration is positive in every year except 2021 (-1.3), when the borders closed.',
                pt='Quatro painéis sobre a demografia coreana. A população, indexada a 2006, atinge o pico de 51,84 milhões em 2020, e a projeção oficial de 2024 prevê 36,2 milhões em 2072; 20,3% das pessoas têm 65 anos ou mais em 2025. A taxa de fecundidade total chega ao mínimo mundial de 0,721 em 2023 e se recupera levemente para 0,799 em 2025, muito abaixo da reposição de 2,1. As taxas brutas de natalidade e mortalidade por 1.000 se cruzam em 2020. O crescimento natural é negativo desde 2020 (-2,1 por 1.000 em 2025), enquanto a migração internacional líquida é positiva em todos os anos menos 2021 (-1,3), quando as fronteiras fecharam.', **{"zh-Hans": '韩国人口的四个面板。以2006年为基期的人口指数在2020年达到峰值，当年人口为5,184万；2024年官方预测显示2072年人口为3,620万。2025年65岁及以上人口占20.3%。总和生育率在2023年降至全球最低的0.721，2025年略回升至0.799，远低于2.1的更替水平。每千人粗出生率与粗死亡率在2020年交叉。自然增长自2020年起为负，2025年为每千人-2.1；国际净迁移除边境关闭的2021年（-1.3）外均为正。'}),
            "sources": ['social/population.csv', 'social/vital.csv', 'social/migration.csv'],
            "spark": ctx.col('social/vital.csv', 'tfr'),
            "stats": [
                S({"ko": '합계출산율', "en": 'Fertility rate', "pt": 'Fecundidade', "zh-Hans": '生育率'},
                  ctx.col('social/vital.csv', 'tfr'), 'dec3'),
                S({"ko": '인구', "en": 'Population', "pt": 'População', "zh-Hans": '人口'},
                  ctx.col('social/population.csv', 'pop_mn'), 'pop_mn',
                  year=ctx.LAST_FULL_YEAR),
            ],
        },
        {
            "id": '09_safety', "topic": "security", "n": '09', "family": PEOPLE,
            "title": ctx.text(ko='안전', en='Safety', pt='Segurança', **{"zh-Hans": '安全'}),
            "blurb": ctx.text(
                ko='타인으로부터는 세계에서 가장 안전하고, 자기 자신으로부터는 OECD에서 가장 위험한 나라.',
                en='One of the safest countries in the world from other people, and the most dangerous in the OECD from oneself.',
                pt='Um dos países mais seguros do mundo em relação aos outros, e o mais perigoso da OCDE em relação a si mesmo.', **{"zh-Hans": '就他人造成的伤害而言，韩国是全球最安全的国家之一；就自身伤害而言，却是经合组织中最危险的国家。'}),
            "alt": ctx.text(
                ko='폭력과 사고에 의한 사망을 다룬 네 개 패널. 살인(타살) 사망률은 로그 눈금에 그렸고, 통계청 사망원인통계의 사망자 수를 같은 통계의 분모(주민등록 연앙인구)로 나눈 값이다. 2014년 10만 명당 1.01명에서 2025년 0.48명(246명)으로 줄었고, UNODC 수치도 1명 안팎이다. 자살률은 2011년 31.7명으로 정점을 찍었고 2025년 27.8명으로 OECD 최고다. 도로교통사고 사망률(경찰 집계)은 13.1명에서 4.9명으로 줄었다. 한국의 시선 패널은 산재보험 적용 근로자 10만 명당 사고사망으로, 9.6명에서 3.8명으로 절반 넘게 줄었지만 업무상 질병을 포함한 사망자 수는 2006년 2,238명, 2025년 2,248명으로 줄지 않았다.',
                en='Four panels on violent and accidental death. The homicide rate is drawn on a log scale: Statistics Korea\'s count of deaths from assault over the same release\'s own denominator, the mid-year registered population. It falls from 1.01 per 100,000 in 2014 to 0.48 in 2025 (246 deaths), with UNODC\'s series also near 1. Suicide peaks at 31.7 per 100,000 in 2011 and is 27.8 in 2025, the highest in the OECD. Road deaths (police count) fall from 13.1 to 4.9 per 100,000. The lens shows workplace accident deaths per 100,000 insured workers, down from 9.6 to 3.8, while the number of deaths, which includes occupational disease, does not fall: 2,238 in 2006, 2,248 in 2025.',
                pt='Quatro painéis sobre mortes violentas e acidentais. A taxa de homicídios aparece em escala log: a contagem de mortes por agressão da Statistics Korea sobre o denominador da própria publicação, a população registrada no meio do ano. Cai de 1,01 por 100 mil em 2014 para 0,48 em 2025 (246 mortes), com a série do UNODC também perto de 1. O suicídio atinge 31,7 por 100 mil em 2011 e está em 27,8 em 2025, o mais alto da OCDE. As mortes no trânsito (contagem policial) caem de 13,1 para 4,9 por 100 mil. A lente mostra as mortes por acidente de trabalho por 100 mil trabalhadores segurados, que caem de 9,6 para 3,8, enquanto o número de mortes, que inclui doença ocupacional, não cai: 2.238 em 2006, 2.248 em 2025.', **{"zh-Hans": '暴力与意外死亡的四个面板。他杀死亡率采用对数刻度，以韩国统计厅袭击死亡人数除以同一发布资料中的年中登记人口。该比率从2014年每10万人1.01人降至2025年的0.48人（246人死亡），联合国毒品和犯罪问题办公室序列也约为1人。自杀率在2011年达到每10万人31.7人的峰值，2025年为27.8人，为经合组织最高。警方统计的道路死亡率从每10万人13.1人降至4.9人。专题展示每10万名参保职工的工伤事故死亡人数，从9.6人降至3.8人；但包括职业病的死亡总人数并未下降：2006年为2,238人，2025年为2,248人。'}),
            "sources": ['social/homicide.csv', 'social/mortality.csv', 'social/vital.csv',
                        'social/security_intl.csv', 'social/road.csv', 'social/workplace.csv'],
            "spark": ctx.col('social/mortality.csv', 'suicide'),
            "stats": [
                S({"ko": '자살률', "en": 'Suicide rate', "pt": 'Taxa de suicídio', "zh-Hans": '自杀率'},
                  ctx.col('social/mortality.csv', 'suicide'), 'per100k'),
                S({"ko": '교통사고 사망률', "en": 'Road deaths', "pt": 'Mortes no trânsito', "zh-Hans": '道路死亡'},
                  ctx.col('social/road.csv', 'road_rate'), 'per100k'),
            ],
        },
        {
            "id": '10_credit', "topic": "credit", "n": '10', "family": MONEY,
            "title": ctx.text(ko='가계부채와 신용의 가격',
                              en='Household Debt & the Price of Credit',
                              pt='Dívida das Famílias e o Preço do Crédito', **{"zh-Hans": '住户债务与信贷成本'}),
            "blurb": ctx.text(
                ko='한국의 가계는 이 나라가 1년간 생산하는 것과 맞먹는 빚을 지고 있다. 그 대가로 무엇을 지불하고, 얼마가 연체되는가.',
                en='Korean households owe almost as much as the whole economy produces in a year. What they pay for it, and how much of it goes unpaid.',
                pt='As famílias coreanas devem quase tanto quanto a economia inteira produz em um ano. Quanto pagam por isso, e quanto fica em atraso.', **{"zh-Hans": '韩国住户债务几乎相当于全国一年的经济产出。其偿债成本如何，又有多少未能按时偿还？'}),
            "alt": ctx.text(
                ko='가계신용을 다룬 네 개 패널. 가계부채는 BIS 기준(가계·비영리단체, 전체 대출기관)으로 GDP의 65.0%에서 2021년 98.6%로 정점을 찍고 2025년 88.1%이며, 대상이 더 좁은 한국은행 가계신용은 그보다 낮은 73.9%다. 잔액은 2025년 말 1,979조 원이다. 신규 주택담보대출과 일반신용대출 금리는 기준금리를 따라 2020년 무렵 바닥을 찍고 2년 만에 뛰었다. 은행 대출 연체율은 내내 낮아 가계는 2012년 1.1%가 정점이다. 한국의 시선 패널은 BIS 가계 원리금상환비율로, 가처분소득의 9.9%(2014년)에서 12.2%(2023년)로 올랐다.',
                en='Four panels on Korean household credit. Household debt on the BIS measure (households and non-profits, all lenders) rises from 65.0% of GDP to a 98.6% peak in 2021 and is 88.1% in 2025; the Bank of Korea\'s narrower household credit series runs lower, at 73.9%. The stock is ₩1,979 trillion at the end of 2025. New mortgage and unsecured lending rates follow the base rate to a trough around 2020 and jump within two years. Bank loan delinquency stays low throughout, with households peaking at 1.1% in 2012. The lens shows the BIS household debt service ratio, up from 9.9% of disposable income in 2014 to 12.2% in 2023.',
                pt='Quatro painéis sobre o crédito às famílias na Coreia. A dívida das famílias na medida do BIS (famílias e instituições sem fins lucrativos, todos os credores) sobe de 65,0% do PIB para o pico de 98,6% em 2021 e está em 88,1% em 2025; a série mais estreita do Banco da Coreia fica abaixo, em 73,9%. O estoque é de ₩1.979 trilhões no fim de 2025. Os juros de novos financiamentos imobiliários e de empréstimos sem garantia acompanham a taxa básica até um mínimo por volta de 2020 e saltam em dois anos. A inadimplência bancária fica baixa o tempo todo, com o pico das famílias em 1,1% em 2012. A lente mostra o comprometimento de renda das famílias medido pelo BIS, que sobe de 9,9% da renda disponível em 2014 para 12,2% em 2023.', **{"zh-Hans": '韩国住户信贷的四个面板。国际清算银行口径的住户债务（住户及非营利机构，所有贷款机构）从GDP的65.0%升至2021年98.6%的峰值，2025年为88.1%；韩国银行范围较窄的住户信贷序列较低，为73.9%。2025年末余额为₩1,979万亿。新增住房抵押贷款和无抵押贷款利率随基准利率在2020年前后触底，并在两年内跃升。银行贷款逾期率始终较低，住户逾期率在2012年达到1.1%的峰值。专题展示国际清算银行住户偿债比率，从2014年可支配收入的9.9%升至2023年的12.2%。'}),
            "sources": ['macro/household_bis.csv', 'macro/household_credit.csv',
                        'macro/credit_terms.csv', 'macro/base_rate.csv'],
            "spark": ctx.col('macro/household_bis.csv', 'credit_pct_gdp_q4'),
            "spark_level": True,
            "stats": [
                S({"ko": '가계부채(BIS)', "en": 'Household debt (BIS)', "pt": 'Dívida das famílias (BIS)', "zh-Hans": '住户债务（国际清算银行）'},
                  ctx.col('macro/household_bis.csv', 'credit_pct_gdp_q4'), 'pct_gdp', kind="level"),
                S({"ko": '원리금상환비율', "en": 'Debt service ratio', "pt": 'Serviço da dívida', "zh-Hans": '偿债比率'},
                  ctx.col('macro/household_bis.csv', 'dsr_pct_q4'), 'pct', kind="level"),
            ],
        },
        {
            "id": '11_mortality', "topic": "mortality", "n": '11', "family": PEOPLE,
            "title": ctx.text(ko='사망', en='Mortality', pt='Mortalidade', **{"zh-Hans": '死亡'}),
            "blurb": ctx.text(
                ko='한국이 늙으면서 인구 대비 사망이 늘고, 팬데믹은 그 위에 얹혔다.',
                en='Deaths per head rise because Korea is older; the pandemic sits on top of that.',
                pt='As mortes por habitante sobem porque a Coreia está mais velha; a pandemia veio por cima disso.', **{"zh-Hans": '人均死亡人数上升源于韩国人口老龄化；疫情在此基础上进一步推高死亡。'}),
            "alt": ctx.text(
                ko='사망을 다룬 네 개 패널. 조사망률은 인구 1천 명당 5.0명(2006년)에서 팬데믹이 겹친 2022년 7.28명으로 정점을 찍었고 2025년 7.13명이다. 2015–2019년 연평균 사망자 287,237명과 비교한 초과사망은 2022년 +29.8%이며, 연령 표준화를 하지 않아 고령화만으로도 위로 기운다. 사망신고서 기준 코로나19 사망률은 2022년 10만 명당 61.0명(31,280명)이 정점이다. 한국의 시선 패널은 주요 사망원인으로, 암이 134.8명에서 177.1명으로 가장 많고, 폐렴은 9.4명에서 60.8명으로 늘어 심장 질환에 다가섰으며, 뇌혈관 질환은 61.7명에서 48.7명으로 줄었다.',
                en='Four panels on deaths in Korea. The crude death rate rises from 5.0 per 1,000 in 2006 to a pandemic peak of 7.28 in 2022 and is 7.13 in 2025. Excess deaths, against the 2015–2019 average of 287,237 a year, reach +29.8% in 2022; the measure is not age-adjusted, so ageing alone tilts it upward. COVID-19 deaths, counted from death certificates, peak at 61.0 per 100,000 in 2022 (31,280 deaths). The lens shows the big killers per 100,000: cancer, the largest, from 134.8 to 177.1; pneumonia from 9.4 to 60.8, closing on heart disease; and stroke down from 61.7 to 48.7.',
                pt='Quatro painéis sobre as mortes na Coreia. A taxa bruta de mortalidade sobe de 5,0 por 1.000 em 2006 para o pico pandêmico de 7,28 em 2022 e está em 7,13 em 2025. O excesso de mortes, contra a média de 287.237 por ano em 2015–2019, chega a +29,8% em 2022; a medida não é ajustada por idade, então só o envelhecimento já a empurra para cima. As mortes por COVID-19, contadas pelos atestados de óbito, atingem o pico de 61,0 por 100 mil em 2022 (31.280 mortes). A lente mostra as grandes causas de morte por 100 mil: o câncer, a maior, de 134,8 para 177,1; a pneumonia, de 9,4 para 60,8, se aproximando das doenças do coração; e o AVC caindo de 61,7 para 48,7.', **{"zh-Hans": '韩国死亡情况的四个面板。粗死亡率从2006年每千人5.0人升至疫情期间2022年7.28人的峰值，2025年为7.13人。相较2015–2019年年均287,237人，2022年超额死亡达到+29.8%；该指标未经年龄调整，老龄化本身即可推高数值。按死亡证明统计的新冠死亡率在2022年达到每10万人61.0人（31,280人死亡）的峰值。专题展示每10万人的主要死因：癌症最多，从134.8人升至177.1人；肺炎从9.4人升至60.8人，接近心脏病；脑卒中从61.7人降至48.7人。'}),
            "sources": ['social/mortality.csv', 'social/vital.csv', 'social/covid.csv'],
            "spark": ctx.col('social/mortality.csv', 'all_causes'),
            "stats": [
                S({"ko": '조사망률(10만 명당)', "en": 'Deaths per 100,000', "pt": 'Óbitos por 100 mil', "zh-Hans": '每10万人死亡人数'},
                  ctx.col('social/mortality.csv', 'all_causes'), 'per100k'),
                S({"ko": '코로나19 사망(누적)', "en": 'COVID-19 deaths', "pt": 'Mortes por COVID-19', "zh-Hans": '新冠死亡人数'},
                  ctx.col('social/covid.csv', 'deaths'), 'count', kind="total"),
            ],
        },
        {
            "id": '12_migration', "topic": "migration", "n": '12', "family": PEOPLE,
            "title": ctx.text(ko='국제이동', en='Migration', pt='Migração', **{"zh-Hans": '迁移'}),
            "blurb": ctx.text(
                ko='90일을 초과해 들어오고 나간 사람, 그리고 인구주택총조사가 집계한 국내 거주 외국인.',
                en='People who enter or leave for more than 90 days, and resident foreign citizens counted by the census.',
                pt='Pessoas que entram ou saem por mais de 90 dias, e cidadãos estrangeiros residentes contados pelo censo.', **{"zh-Hans": '出入境停留超过90天的人口，以及人口普查统计的常住外国公民。'}),
            "alt": ctx.text(
                ko='한국의 국제이동을 다룬 네 개 패널. 입국자와 출국자는 내·외국인을 모두 포함한 90일 초과 국제이동으로, 인구 1천 명당 비율은 2025년 각각 13.3명과 11.8명이다. 순이동은 국경이 닫힌 2021년에만 마이너스다. 등록센서스가 11월 1일 기준으로 집계한 국내 거주 외국인은 2022년 175만 2천 명(3.4%)에서 2024년 204만 3천 명(3.9%)으로 늘었다. 이는 출생지가 아니라 국적 기준이다. 한국의 시선 패널은 같은 90일 초과 순이동을 내국인과 외국인으로 나눈다.',
                en='Four panels on migration in South Korea. Immigration and emigration count Korean and foreign citizens entering or leaving for more than 90 days; in 2025 they are 13.3 and 11.8 per 1,000 residents. Net migration is negative only in 2021, when the borders closed. The register census counts 1.752 million resident foreign citizens (3.4%) in 2022 and 2.043 million (3.9%) in 2024, at 1 November; this is citizenship, not birthplace. The lens splits the same >90-day net flow between Korean and foreign citizens.',
                pt='Quatro painéis sobre a migração na Coreia do Sul. Imigração e emigração contam cidadãos coreanos e estrangeiros que entram ou saem por mais de 90 dias; em 2025 são 13,3 e 11,8 por mil habitantes. A migração líquida só é negativa em 2021, quando as fronteiras fecharam. O censo de registros conta 1,752 milhão de cidadãos estrangeiros residentes (3,4%) em 2022 e 2,043 milhões (3,9%) em 2024, em 1º de novembro; é um corte por cidadania, não por local de nascimento. A lente separa o mesmo fluxo líquido de mais de 90 dias entre cidadãos coreanos e estrangeiros.', **{"zh-Hans": '韩国迁移情况的四个面板。迁入和迁出包括出入境停留超过90天的韩国及外国公民；2025年分别为每千名居民13.3人和11.8人。净迁移仅在边境关闭的2021年为负。登记普查以11月1日为时点，2022年常住外国公民为175.2万人（3.4%），2024年为204.3万人（3.9%）；这是国籍口径，而非出生地口径。专题将同一超过90天的净迁移流量划分为韩国公民和外国公民。'}),
            "sources": ['social/migration.csv',
                        'migration/foreign_residents_census.csv',
                        'migration/flows_by_citizenship.csv',
                        'social/population.csv'],
            "spark": ctx.col('social/migration.csv', 'net'),
            "stats": [
                S({"ko": '순이동', "en": 'Net migration', "pt": 'Migração líquida', "zh-Hans": '净迁移'},
                  ctx.col('social/migration.csv', 'net'), 'count', kind="flow"),
                S({"ko": '외국인 비중', "en": 'Foreign-citizen share',
                   "pt": 'Parcela de cidadãos estrangeiros', "zh-Hans": '外国公民占比'},
                  ctx.col('migration/foreign_residents_census.csv',
                          'foreign_citizen_share_pct'), 'pct', kind="level"),
            ],
        },
    ]
