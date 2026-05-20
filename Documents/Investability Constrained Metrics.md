Introduction
When evaluating Alpha performance, various metrics can be used. One metric of them is Alpha Performance after Investability Constraint.

Investability Constraints ensure that the positions taken by an Alpha are within the liquidity limits of the instruments. This helps avoid significant market impact, which can negatively affect the Alpha's profitability. An Alpha that performs well under Investability Constraints will potentially have higher capacity and liquidity.

For example:

Consider two Alphas that allocate weights to stock X, scaled to a book size of $20 million:

Alphas	Allocation (million $)	Average Daily Volume of Stock X (million $)
A	5	50
B	0.1	50
Alpha A's position is harder to change because it represents 10% of the average daily volume (ADV) of stock X. In contrast, Alpha B's position has more room for adjustment. This difference can have a significant impact when considering thousands of stocks in a universe.

Where to find the metrics
You can find the Investability Constrained Metrics on the new simulation results page. The page displays the Alpha's PnL under Investability Constraint conditions.

Investability _1.png
Additionally, the IS Summary now includes new aggregate data for Alpha performance after applying Investability Constraints.

Investability _2.png
How to use the metric in your Alpha research
Performance Consistency: Ensure that Alphas do not lose too much performance under Investability Constraints compared to their base performance. Alphas that have good Investability Constraints Sharpe are likely to have good After-cost Sharpe also which will help improve your Combine Alpha Performance in Genius.
Optimization Metrics: Consultants can leverage Investability Constrained Metrics as a metric to enhance your Alpha optimization process. Here’re some tips to create Alphas which such performance:
An Alpha which captures signal in the liquid instruments space of the market may have higher Investability Constrained Performance. This is especially true for cases of medium to high turnover like Alphas in Price Volume, News, Options, etc. category. You should either control the liquidity profile of your signals or lower the turnover of the illiquid part of them. Please checkout some forum post about these technique in the References.
An Alpha with low turnover in general may be less impacted by these constraint for example Alphas in category Fundamental, Model, … Because it changes position in low frequency, thus its performance relies less on the liquidity of the instruments. Please checkout some forum post about creating low turnover Alphas in the References.
Alpha Submissions Selection: Use these metrics as a filter for selecting Alphas, especially in regions like ASI and GLB. Alphas that perform well under these constraints can possibily add significant value and may result in higher value factor and weight factor because they scale better when the booksize increases.
Apply Max Trade Settings to your Alpha: In order to convert your Alphas into Investability Constrained Alphas, you can change the Max Trade option in Simulation Settings to ON. Please read this documentation for further information.
max_trade_settings.png
References
Research Papers:

The market impact of large trading orders: Correlated order flow, asymmetric liquidity and efficient prices
The Impact of Large Orders in Electronic Markets
BRAIN Forum posts & Articles:

Tips for Success in the High Capacity Alphas Competition
How to Improve After Cost Performance
What is liquidity?
What's After cost Sharpe ratio?
Can you explain what decay is?
Do you recommend higher or lower Decay?