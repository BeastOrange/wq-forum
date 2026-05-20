Getting Started with sentiment1 dataset (Research Sentiment Data)

The sentiment1 dataset combines sentiment metrics with earnings estimations and surprises for U.S.-listed companies.
It provides insights into market mood, analyst consensus, and earnings-based signals.
Key fields include sentiment scores, ratios of analyst buy/sell recommendations, earnings surprises, and dispersion among analyst estimates.
Sentiment scores are dynamic with higher turnover in nature, while analyst and earnings metrics are slower-moving signals.
Use smoothing decay operations to manage high-frequency sentiment data and be considerate when using long lookback periods (>63 days) as older events may lose relevance.
The dataset has coverage of approximately 2000 on TOP3000. Do try your ideas on more liquid universes such as TOP1000 and TOPSP500 but ensure sufficient long & short count to avoid overfitting.
Example Alpha Ideas

Positive sentiment indicates market confidence, while negative sentiment signals potential downside. Go long on stocks with bullish sentiment (snt1_cored1_score > 5) and short on stocks with bearish sentiment (snt1_cored1_score < -5).
Positive earnings surprises often lead to upward price movements. Go long on stocks with positive earnings surprises using snt1_d1_earningssurprise.
A strong analyst consensus combined with sufficient analyst coverage reflects market confidence. Go long on stocks with a high ratio of analyst buys over sells using snt1_d1_buyrecpercent, filtering out stocks with low analyst coverage with snt1_d1_analystcoverage