Momentum after news
Hypothesis

After news is released, if a stock takes a longer time to rise, it may show strong evidence of upward momentum, and it could be beneficial to take a long position in it.

Implementation

Use the fundamental data field 'nws12_prez_4l' to capture this hypothesis. Backfill it with two years of data to ensure there is no drop in coverage.

Hint to improve the Alpha

Can increasing weight on more liquid stocks (Stocks with high volume) help pass the sub-universe test?

1
ts_backfill(vec_avg(nws12_prez_4l),504)
Simulation Settings
Region	Universe	Language	Decay	Delay	Truncation	Neutralization	Pasteurization	NaN Handling	Unit Handling	Max Trade
USA	TOP500	Fast Expression	0	1	0.08	Industry	On	Off	Verify	Off
Pretax Income
Hypothesis

Pretax income is a good measure of a company's financial health and profitability. Companies with increasing pretax income may have good growth prospects and higher potential for increasing stock price. Thus, you tend to long stocks with increasing pretax income and short stocks with decreasing pretax income.

Implementation

Use the time-series rank operator to compare the trend of the fundamental data field pretax income over the past 2 years, and use the quantile operator to normalize the result.

Hints to Implement

Boost the signal with sales data. For example, if the company has higher sales, it is more likely to outperform.

1
quantile(ts_rank(pretax_income,250))
Simulation Settings
Region	Universe	Language	Decay	Delay	Truncation	Neutralization	Pasteurization	NaN Handling	Unit Handling	Max Trade
USA	TOP3000	Fast Expression	4	1	0.01	Market	On	Off	Verify	Off
Operating Earnings Yield
Hypothesis

If the operating income of a company is currently higher than its past 1 year history, buy the company’s stock and vice-versa.

Implementation

Using ts_rank to identify current performance of the company compared to its own history, using the fundamental data field "operating_income".

Hints to Implement

Rather than comparing the value directly, can calculating a ratio that includes stock market moves, improve the signal?

1
ts_rank(operating_income,252)
Simulation Settings
Region	Universe	Language	Decay	Delay	Truncation	Neutralization	Pasteurization	NaN Handling	Unit Handling	Max Trade
USA	TOP3000	Fast Expression	0	1	0.08	Subindustry	On	Off	Verify	Off
Appreciation of liabilities
Hypothesis

An increase in the fair value of liabilities could indicate a higher cost than expected. This may deteriorate the company's financial health, potentially leading to lower profitability or financial distress.

Implementation

Go short when there is an increase in the fair value of liabilities within a year and long when the opposite occurs using fundamental data.

Hints to Implement

Could observing the increase over a shorter period improve accuracy?

1
-ts_rank(fn_liab_fair_val_l1_a,252)
Simulation Settings
Region	Universe	Language	Decay	Delay	Truncation	Neutralization	Pasteurization	NaN Handling	Unit Handling	Max Trade
USA	TOP3000	Fast Expression	0	1	0.08	Subindustry	On	Off	Verify	Off
Deferred Revenue
Hypothesis

Firms with high deferred revenue will surprise the market in the future when the deferred revenue is recognized.

Implementation

fnd6_drc field refers to deferred revenue. To improve the coverage of the datafield, ts_backfill operator is applied. Deferred revenue is divided by total assets to account for the size of a firm.

Hints to Implement

Instead of relying on the raw value of the ratio to decide weights of stocks, use cross-sectional operators. Utilize group based operators to compare across similar stocks.

1
ts_backfill(fnd6_drc, 252)/assets
Simulation Settings
Region	Universe	Language	Decay	Delay	Truncation	Neutralization	Pasteurization	NaN Handling	Unit Handling	Max Trade
USA	TOP3000	Fast Expression	0	1	1	Sector	On	Off	Verify	Off
Reducing debt
Hypothesis: Take a long position in companies whose debt has decreased compared to the past, and conversely, take a short position in companies whose debt has increased.


Implementation: Use the fundamental data ‘debt’ to capture this hypothesis. Use the time-series quantile operator to compare the trend of the fundamental data field over the past six months.


Hint to improve the Alpha: Utilize the operator’s driver parameter to transform it into a different distribution.

1
-ts_quantile(debt, 126)
Simulation Settings
Region	Universe	Language	Decay	Delay	Truncation	Neutralization	Pasteurization	NaN Handling	Unit Handling	Max Trade
USA	TOP3000	Fast Expression	0	1	0.01	Market	On	Off	Verify	Off
Power of leverage
Hypothesis: Companies with high liability-to-asset ratios – excluding those with poor financial health or weak cashflows – often leverage debt as a strategic tool to pursue aggressive growth initiatives. By effectively utilizing financial leverage, these firms are more likely to deliver outsized returns, as they reinvest borrowed capital into high-potential opportunities.


Implementation: Use the ‘liabilities’ and ‘assets’ to design the ratio.


Hint to improve the Alpha: This ratio can vary significantly across industries. Would it be worth considering alternative neutralization settings?

1
liabilities/assets
Simulation Settings
Region	Universe	Language	Decay	Delay	Truncation	Neutralization	Pasteurization	NaN Handling	Unit Handling	Max Trade
USA	TOP3000	Fast Expression	0	1	0.01	Market	On	Off	Verify	Off
