What is Reversion and Momentum (RAM) Factor?
Reversion Factor:
The short-term reversion factor captures the phenomenon where stocks that have recently underperformed tend to generate higher returns in the near future, while stocks that have recently outperformed are more likely to experience declines. This behavior is based on the idea that markets often overreact to short-term events, causing temporary mispricing. As these inefficiencies are corrected, oversold stocks recover, and overbought stocks pull back. The reversion factor typically operates within a 5-day time horizon and leverages mean reversion by overweighting recently underperforming stocks and underweighting recently outperforming stocks.

Momentum Factor:
The momentum factor identifies stocks that exhibit consistent price trends based on recent performance. Stocks with positive excess returns in the recent past tend to continue their upward trajectory, while stocks with negative excess returns persist in their downward trend. This trend-following behavior is based on the principle that established price trends are more likely to continue than reverse. Momentum is typically calculated as the cumulative excess return over the last 12 months.

Benefits of RAM Neutralization
RAM Neutralization adjusts Alpha to reduce exposure to the Reversion and Momentum factors derived from stock price data.

Neutralize Momentum Factor: Reduces exposure to crowded trades during strong momentum trends, minimizing risks during market corrections.
Neutralize Short-Term Reversion Factor: Hedges Alphas against mean-reversion signals, reducing unwanted risks.
Remove influence of Price: Helps eliminate the effect of price in unrelated Alphas, such as fundamental metrics like ‘eps/close.’
Improve Performance: Mitigates risks during market drawdowns, improving Sharpe Ratio, reducing drawdowns, and balances turnover benefits with transaction costs for better Alpha performance.
How to Simulate RAM Risk-Neutralized Alphas
30.png
Below is an example configuration for simulating RAM risk-neutralized Alphas:

{
"instrumentType": "EQUITY",
"region": "USA",
"universe": "TOP3000",
"delay": 1,
"decay": 0,
"neutralization": "REVERSION_AND_MOMENTUM",
"truncation": 0.1,
"pasteurization": "ON",
"unitHandling": "VERIFY",
"nanHandling": "ON",
"language": "FASTEXPR",
"visualization": false
}

