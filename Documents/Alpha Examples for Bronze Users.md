Social Media Effect
Hypothesis

Poorly performing stocks are discussed more in general on social media platforms and thus they might have a higher relative sentiment volume, thus consider to short those stocks.

Implementation

You apply negative weights if there's more sentiment volume, which we can do through social media data fields.

1
-scl12_buzz
Simulation Settings
Region	Universe	Language	Decay	Delay	Truncation	Neutralization	Pasteurization	NaN Handling	Unit Handling	Max Trade
USA	TOP3000	Fast Expression	0	1	0.01	Industry	On	Off	Verify	Off
Valuation Disconnect Swing Short
Hypothesis

Value and Momentum in stocks is typically uncorrelated and a stock with high momentum and value score correlation suggests a disconnect between the stock's price and its intrinsic value - thus we short these stocks

Implementation

Use ts_corr() to measure the relationship between valuation score and momentum score over the past 3 years. Using ts_backfill() operator to backfill unavailable data during previous days.

Hint to Improve Alpha

Compare the stocks in the same group using group operators and model data.

1
-ts_corr(ts_backfill(fscore_momentum,66),ts_backfill(fscore_value,66),756)
Simulation Settings
Region	Universe	Language	Decay	Delay	Truncation	Neutralization	Pasteurization	NaN Handling	Unit Handling	Max Trade
USA	TOP200	Fast Expression	0	1	0.08	Industry	On	Off	Verify	Off
Network Dependence
Hypothesis

A higher hub score in the data field indicates that a company's customers have many connections, while a lower score suggests a more concentrated set of partners. If a company's customers have lower hub scores, it means they have fewer partners and potentially rely on the company. This can be positive for the stock as it indicates a lower risk of the company being replaced. Therefore, investing in such stocks for the long term may be a good idea

Implementation

Long stocks of companies whose hub score of customers are low over the past two years using price volume data.

Hint to Improve Alpha

Can using some cross-sectional operators on top of the expression improve the performance of the idea?

1
-ts_mean(pv13_ustomergraphrank_hub_rank,504)
Simulation Settings
Region	Universe	Language	Decay	Delay	Truncation	Neutralization	Pasteurization	NaN Handling	Unit Handling	Max Trade
USA	TOP1000	Fast Expression	0	1	0.08	Industry	On	Off	Verify	Off
