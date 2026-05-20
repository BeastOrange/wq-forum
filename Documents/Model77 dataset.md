Getting Started with Model77 Dataset (Analysts' Factor Model)

The model77 dataset provides a rich collection of metrics spanning valuation ratios, earnings quality, financial health, momentum indicators, and risk measures.
Valuation Metrics: Book-to-Market, Cash-to-Price, Free Cash Flow-to-Price, EBITDA-to-Enterprise Value, etc.
Earnings Indicators: Earnings surprises, analyst revisions, earnings growth projections
Quality Measures: Return on Equity, Asset Turnover, Cash Flow metrics, Altman Z-Score
Momentum Signals: Price performance over various timeframes, relative strength measures
Risk Metrics: Volatility measures, beta, implied volatility, bankruptcy scores
When working with fields that have limited coverage (below 70%), focus your testing on highly liquid subsets like TOP1000 or TOPSP500 where data availability is typically better. Alternatively, you may backfill missing values over reasonable lookback periods (e.g., 252 days), but be cautious as excessive backfilling of high-frequency metrics can introduce noise and diminish signal validity.
Example Alpha Ideas

mdl77_fa_ebitdaev (TTM EBITDA-to-Enterprise Value): This metric identifies companies with strong operational earnings relative to their total capital structure, highlighting potential undervaluation. Go long on stocks with comparatively high EBITDA yields and short those with extremely low or negative values that indicate operational struggles.
mdl77_400_sue (Standardized Unexpected Earnings): Positive earnings surprises create information shocks that frequently lead to persistent post-announcement price drifts. Go long on companies with significant positive earnings surprises while avoiding those with extreme positive surprises that may be prone to reversal.
mdl77_ocfast (Operating Cash Flow to Assets): Superior cash generation relative to asset base indicates efficient operations and high-quality earnings. Go long on companies with strong and improving cash flow generation while avoiding those showing significant deterioration in this metric.
mdl77_opricemomentumfactor_actrtn6m (6-Month Active Return with 1-Month Lag): Medium-term price momentum with a one-month lag captures persistent price trends while avoiding short-term reversals. Go long on stocks with strong lagged six-month returns and short stocks with significant negative returns while filtering out recent earnings announcement with days_from_last_change() operator.
mdl77_altmanz (Altman Z Score): This comprehensive bankruptcy risk indicator identifies companies with solid financial foundations and are less vulnerable to economic downturns. Go long on stocks with high financial stability during periods of market uncertainty and short companies with distress signals.