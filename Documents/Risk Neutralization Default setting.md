Introduction
From now on when you simulate non–Risk Neutralized Alphas, you will see another set of PnLs and performance metrics. These new calculated statistics comes from the hypothesis case what if your Alpha is Risk Neutralized (using various Risk setting in Neutralization for Alphas for example “Slow Factors”, “Fast Factors”, “Slow + Fast Factors”).

These metrics won’t be calculated for Alpha already simulate with Risk Neutralization in setting.

If you don’t understand Risk-Neutralized Alpha concept, please check out this documentation.

Where to find the metrics
The new UI on simulation results page looks like this:

risk_neu_metric.png
The IS Summary also has new aggregate data:

risk_neu_metric2.png
How to use the metrics in your Alpha research
From these stats, you can examine how good does your Alphas capture market anomalies that's not in the risk factor databases.

Because the calculation isn’t exactly the same with Risk Neutralization in setting, the platform uses new technique to speed up the computation. So you will see a bit different performance between Risk Neutralized metrics and actual Risk Neutralization settings (in particular turnover won’t change in the Risk Neutralized metrics but normal Risk Neutralization settings can affect it).

In your Alphas optimization process or Alpha submission selections, you should rank Alphas by the ratio between Risk Neutralized Metrics' sharpe and original Alpha sharpe or between Risk Neutralized Metrics' returns and original Alpha returns and choose the one with higher ratio. An Alpha that retains more of its performance after Risk Neutralization means it's less susceptible to risk factors’ drawdown & volatility and maybe less correlated too.

