"""Localized chapter cards and headline figures for China."""
MONEY, WORLD, PEOPLE = "money", "world", "people"


def _bn(series, divisor):
    return [(year, value / divisor) for year, value in series]


def _text(ctx, zh, en, pt, ko):
    return ctx.text(**{"zh-Hans": zh, "en": en, "pt": pt, "ko": ko})


def headline(ctx):
    return [
        ctx.stat(_text(ctx, "人均GDP（美元）", "GDP per person, US$", "PIB por pessoa, US$", "1인당 GDP, 달러"),
                 ctx.col("economy/gdp_pc_usd.csv", "gdp_per_person_usd"), "count"),
        ctx.stat(_text(ctx, "人口", "Population", "População", "인구"),
                 _bn(ctx.col("demography/population_intl.csv", "population"), 1_000_000_000), "dec2", kind="level"),
        ctx.stat(_text(ctx, "实际增长", "Real growth", "Crescimento real", "실질성장률"),
                 ctx.col("economy/gdp_growth_intl.csv", "wb_real_growth_pct"), "pct_s"),
        ctx.stat(_text(ctx, "通胀", "Inflation", "Inflação", "물가상승률"),
                 ctx.col("economy/inflation_intl.csv", "wb_cpi_inflation_pct"), "pct"),
        ctx.stat(_text(ctx, "失业率", "Unemployment", "Desemprego", "실업률"),
                 ctx.col("economy/unemployment_intl.csv", "unemployment_pct"), "pct", kind="level"),
        ctx.stat(_text(ctx, "政府债务", "Government debt", "Dívida pública", "정부부채"),
                 ctx.col("fiscal/debt_intl_pct_gdp.csv", "gg_gross_debt_pct_gdp"), "pct_gdp", kind="level"),
    ]


COPY = {
"economy": ({"zh-Hans":"经济","en":"The Economy","pt":"A Economia","ko":"경제"}, {"zh-Hans":"世界银行和IMF勾勒出放缓但仍为正的增长；国家统计局序列待机器渠道恢复后并列。","en":"World Bank and IMF trace slower but still positive growth; the NBS series will sit beside them when its machine channel returns.","pt":"Banco Mundial e FMI mostram crescimento mais lento, ainda positivo; a série do NBS ficará ao lado quando o canal automatizado voltar.","ko":"세계은행과 IMF는 둔화되었으나 여전히 양수인 성장률을 보여 준다. NBS 시계열은 기계 접근 경로가 복구되면 별도로 병기한다."}),
"fiscal": ({"zh-Hans":"公共财政","en":"Public Finances","pt":"Contas Públicas","ko":"공공재정"}, {"zh-Hans":"IMF统一口径给出收支、余额、利息与广义债务；财政部较窄的预算口径仍保持分开。","en":"One IMF vintage supplies flows, balances, interest and broad debt; the narrower MOF budget perimeter remains separate.","pt":"Uma única edição do FMI fornece fluxos, saldos, juros e dívida ampla; o perímetro orçamentário mais estreito do Ministério permanece separado.","ko":"동일 IMF 작성 기준으로 세입·세출, 재정수지, 이자와 광의 부채를 제공하며, 범위가 더 좁은 재정부 예산 통계는 별도로 유지한다."}),
"spending": ({"zh-Hans":"钱花在哪里","en":"Where the Money Goes","pt":"Para Onde Vai o Dinheiro","ko":"재정 지출의 용도"}, {"zh-Hans":"统一口径职能支出仍不可得；可比的全经济投资率揭示长期高于40%的平台。","en":"Comparable spending functions remain unavailable; the whole-economy investment rate reveals the long plateau above 40%.","pt":"Funções comparáveis de gasto seguem indisponíveis; a taxa de investimento da economia revela o longo patamar acima de 40%.","ko":"비교 가능한 기능별 지출은 아직 확보되지 않았으나, 경제 전체 투자율은 40%를 웃도는 장기간의 고원을 보여 준다."}),
"trade": ({"zh-Hans":"贸易","en":"Trade","pt":"Comércio","ko":"무역"}, {"zh-Hans":"国际收支开放度可跨国比较；2023年Comtrade海关快照仅保留在中国视角面板。","en":"Balance-of-payments openness remains comparable; the 2023 Comtrade customs snapshot stays in China's lens panel.","pt":"A abertura pelo balanço de pagamentos permanece comparável; o retrato aduaneiro Comtrade de 2023 fica no painel de perspectiva da China.","ko":"국제수지 기준 무역개방도는 비교 가능하며, 2023년 Comtrade 통관 현황은 중국 심층 패널에만 제시한다."}),
"markets": ({"zh-Hans":"货币与市场","en":"Money and Markets","pt":"Dinheiro e Mercados","ko":"통화와 시장"}, {"zh-Hans":"人民币采用统一口径年度汇率；央行中间价、CFETS收盘价和LPR制度绝不拼接。","en":"The renminbi uses the harmonised annual rate; the PBoC fixing, CFETS close and LPR regimes are never spliced.","pt":"O renminbi usa a taxa anual harmonizada; fixing do PBoC, fechamento CFETS e regimes da LPR nunca são emendados.","ko":"위안화는 조화된 연간 환율을 사용하며, PBoC 고시환율, CFETS 종가 및 LPR 체계는 서로 이어 붙이지 않는다."}),
"credit": ({"zh-Hans":"信贷","en":"Credit","pt":"Crédito","ko":"신용"}, {"zh-Hans":"BIS住户信贷与更广义的私人部门偿债率并列展示；银行不良率仍是全系统口径。","en":"BIS household credit sits beside the broader private-sector debt-service ratio; the NPL reading remains bank-wide.","pt":"O crédito familiar do BIS aparece ao lado da razão de serviço da dívida do setor privado mais amplo; a leitura de NPL continua cobrindo todo o sistema bancário.","ko":"BIS 가계신용과 범위가 더 넓은 민간부문 원리금 상환비율을 병기하며, 부실채권 비율은 은행 전체 기준이다."}),
"people": ({"zh-Hans":"民生","en":"People","pt":"Pessoas","ko":"국민생활"}, {"zh-Hans":"调查基尼和国际贫困线不是国家统计局基尼或中国国家贫困线。","en":"The survey Gini and international poverty lines are not the NBS Gini or China's national poverty line.","pt":"O Gini de pesquisas e as linhas internacionais não são o Gini do NBS nem a linha nacional de pobreza da China.","ko":"조사 지니계수와 국제빈곤선은 NBS 지니계수나 중국 국가빈곤선과 다르다."}),
"world": ({"zh-Hans":"世界中的中国","en":"China in the World","pt":"A China no Mundo","ko":"세계 속 중국"}, {"zh-Hans":"美元规模、HDI、清廉指数和储备来自四个明确标注的国际体系。","en":"Dollar size, HDI, the corruption index and reserves come from four explicitly labelled international systems.","pt":"Tamanho em dólar, IDH, índice de corrupção e reservas vêm de quatro sistemas internacionais explicitamente rotulados.","ko":"달러 기준 규모, 인간개발지수, 부패인식지수와 준비자산은 명확히 표시된 네 국제 통계 체계에서 가져온다."}),
"demography": ({"zh-Hans":"人口","en":"Demography","pt":"Demografia","ko":"인구구조"}, {"zh-Hans":"出生率在2022年低于死亡率；普查换基与联合国人口版本不得拼接。","en":"Births fell below deaths in 2022; census rebases and the UN population vintage must not be spliced.","pt":"Nascimentos ficaram abaixo das mortes em 2022; revisões censitárias e a edição populacional da ONU não podem ser emendadas.","ko":"2022년 출생률이 사망률을 하회했으며, 인구총조사 기준 개편 자료와 UN 인구 작성 기준 자료는 이어 붙이지 않는다."}),
"security": ({"zh-Hans":"安全","en":"Security","pt":"Segurança","ko":"안전"}, {"zh-Hans":"凶杀、自杀和道路死亡仅采用UNODC和WHO可比序列，并明确缺少国家序列。","en":"Homicide, suicide and road deaths use only the comparable UNODC and WHO series, with the missing national series declared.","pt":"Homicídios, suicídios e mortes no trânsito usam apenas séries comparáveis da UNODC e OMS, declarando a ausência das nacionais.","ko":"살인, 자살 및 도로교통 사망은 비교 가능한 UNODC와 WHO 시계열만 사용하며, 국가 시계열의 부재를 명시한다."}),
"mortality": ({"zh-Hans":"死亡","en":"Mortality","pt":"Mortalidade","ko":"사망"}, {"zh-Hans":"现有统一口径死亡率可绘制；一致的死亡人数、超额死亡和死因表仍不可得。","en":"The harmonised death rate can be drawn; consistent death counts, excess deaths and causes remain unavailable.","pt":"A taxa harmonizada de mortalidade pode ser desenhada; contagens consistentes, excesso e causas seguem indisponíveis.","ko":"조화된 사망률은 도표화할 수 있으나, 일관된 사망자 수, 초과사망 및 사망원인 자료는 아직 확보되지 않았다."}),
"migration": ({"zh-Hans":"迁移","en":"Migration","pt":"Migração","ko":"인구이동"}, {"zh-Hans":"净迁移估计、国际移民存量快照和城镇化不是边境流量或户口统计。","en":"Net-migration estimates, migrant-stock snapshots and urbanisation are not border flows or hukou statistics.","pt":"Estimativas de saldo migratório, retratos do estoque e urbanização não são fluxos de fronteira nem estatísticas de hukou.","ko":"순이동 추정치, 국제이주자 현황과 도시화율은 국경 이동 흐름이나 호적 통계가 아니다."}),
}

SERIES = {
"economy": ("economy/gdp_growth_intl.csv", "wb_real_growth_pct", "pct_s"),
"fiscal": ("fiscal/debt_intl_pct_gdp.csv", "gg_gross_debt_pct_gdp", "pct_gdp"),
"spending": ("economy/gfcf_pct_gdp.csv", "gfcf_pct_gdp", "pct_gdp"),
"trade": ("trade/trade_intl_openness.csv", "trade_pct_gdp", "pct_gdp"),
"markets": ("markets/fx_cny_per_usd.csv", "cny_per_usd_avg", "dec2"),
"credit": ("credit/npl_intl.csv", "npl_pct", "pct"),
"people": ("people/gini_intl.csv", "gini", "dec2"),
"world": ("economy/gdp_usd.csv", "gdp_usd", "usd_bn"),
"demography": ("demography/population_intl.csv", "population", "pop_mn"),
"security": ("security/security_intl.csv", "homicide_per_100k", "per100k"),
"mortality": ("demography/vital_intl.csv", "death_rate_per_1000", "dec2"),
"migration": ("migration/urban_share_intl.csv", "urban_share_pct", "pct"),
}


def build(ctx):
    families = [MONEY, MONEY, MONEY, WORLD, MONEY, MONEY, PEOPLE, WORLD,
                PEOPLE, PEOPLE, PEOPLE, PEOPLE]
    out = []
    for i, ((topic, (title, blurb)), family) in enumerate(zip(COPY.items(), families), 1):
        rel, col, spec = SERIES[topic]
        series = ctx.col(rel, col)
        if topic == "world": series = _bn(series, 1_000_000_000)
        if topic == "demography": series = _bn(series, 1_000_000)
        rendered = ctx.text(**title)
        out.append({"id": f"{i:02d}-{topic}", "topic": topic, "n": f"{i:02d}",
                    "family": family, "title": rendered,
                    "blurb": ctx.text(**blurb), "spark": series,
                    "stats": [ctx.stat(rendered, series, spec)]})
    return out
