The following performance tests are run till the end of the In-Sample Period.
The 'Submit Alpha' button (in the Submission tab of the simulation results panel) is used to start out-of-sample (OS) testing for Alphas meeting the performance and correlation cutoffs
Only submitted Alphas are considered for scoring. Submitted Alphas show up on the Out-of-Sample tab of the Alphas page.
Below table is for submission test for Alphas

Submission Tests for Alphas
article_6_core_requirements.png
Fitness
At least “Average”: Greater than 1.3 for Delay-0 or Greater than 1 for Delay-1
Sharpe
Greater than 2 for Delay-0 Alphas or Greater than 1.25 for Delay-1 Alphas
Turnover
1% < Turnover < 70%
Weight test
Max weight in any stock < 10%. This measures if sufficient number of stocks are assigned weight for sufficient days in a year. Number varies with simulation universe (Top 3000, Top 2000 etc.)
Sub universe test
The Sharpe in the sub universe must be higher than at least one threshold. These thresholds scale down Sharpe with sub universe size. You can find detailed example below.
Self-Correlation
<0.7 PnL correlation. Or Sharpe at least 10% greater than other correlated Alphas submitted by user
Self-correlation
Alphas can also qualify if their Sharpe is greater, by 10% or more, than that of all Alphas with which their correlation is higher than the cutoff.
For example, if your earlier submitted Alpha X has a Sharpe of 3.18, you can submit a highly correlated Alpha Y, if its Sharpe is 3.5 or more
This allows for making improvements to an existing Alpha.
The Sharpe value used for this comparison (3.18) is visible in the correlation summary table in the simulation results.
Self correlation operates on a four-year window whereas the inner correlation operates on the intersect of the selected Alpha's PnL time periods.
Weight
Alphas are also tested on the distribution of Alpha weights across stocks. Alphas can fail this test if:

Too few stocks are assigned weight for significant number of days in a year. Note that assigning zero weights to all stocks at the start of the simulation does not fail this condition, it only applies after the Alpha starts assigning weights. The exact number of minimum stocks varies with the simulation universe.
Alpha weight is too concentrated in any one stock. For example, if one stock has 30 percent of all Alpha weight, it will fail this test.
Sub Universe Test
Sub-universe test is one of the robustness tests performed on an Alpha by the BRAIN platform before submission. In simple words, it ensures that your Alpha works not only in the universe you are trying to submit, but that it would also work in the next more liquid (or smaller) universe to some extent.

E. g. if you are trying to submit an Alpha on USA TOP3000, the platform will also check its performance on USA TOP1000. If it performs poorly, then it means that your Alpha is generating most of the profit on the non-liquid portion of stocks, which is one of the signs that your Alpha is not robust enough and most likely will not perform as well as expected in out-of-sample testing. That’s why such Alphas are not allowed to be submitted on Brain.

Technical details:

The threshold to pass the sub-universe test is defined by the formula:
subuniverse_sharpe >= 0.75 * sqrt(subuniverse_size / alpha_universe_size) * alpha_sharpe

Sub-Universe Sharpe is calculated using PnL of Alpha obtained through the following process (notice that it is similar to the Sharpe of an Alpha simulated in the sub-universe, but not exactly the same, as you will see in the example below):
Pasteurize to the target universe, that is, for all stocks not in the sub-universe, assign value of NaN
Apply market neutralization to resulting set (subtract mean of all values from each value) and then scale Alpha back to original size.
Calculate PnL using resulting Alpha values
Consider an Alpha in USA TOP3000 which fails sub-universe test:

check111.png
subinverse 6.png
Notice cutoff 0.75 * sqrt(subuniverse_size / alpha_universe_size) * alpha_sharpe = 0.75 * sqrt(1000 / 3000) * 2.73 = 1.18

Let’s check this Alpha performance on next more liquid universe, TOP1000

subuniverse 5.png
subinverse 6.png
As you see, Sharpe ratio degraded significantly to 1.17, less than the cutoff of 1.18.

article_6_subuniverse_test.png
Tips to help you improve your Alpha(s) and pass the sub-universe test:

Avoid using multipliers related to the size of the company in your Alphas, e.g. rank(-assets), 1 – rank(cap), etc. These multipliers may significantly shift the distribution of your Alpha weights to more/less liquid side and it may affect the sub-universe performance
Try decaying separately the liquid and non-liquid parts of your signal. As a proxy for liquidity you can use cap or volume*close, for example instead of
“ts_decay_linear(signal, 10)”
you can try
“ts_decay_linear(signal, 5) * rank(volume*close) + ts_decay_linear(signal, 10) * (1 – rank(volume*close))”
Check out your Alpha improvements step by step, maybe one of them resulted in better stats, but at the same time Alpha started to fail sub-universe test?
Try these tips to improve overall Sharpe of your Alpha
If nothing helps - don’t get upset. Some signals are just not robust. It is always sad to discard an Alpha with good IS performance, but remember: your long-term success as a quant depends on how your Alphas will perform in out-of-sample, not during in-sample simulation. Most likely, you just dodged a bad Alpha.
Special Alpha Types
article_6_special_alpha_types.png
ATOM Alphas
ATOM Alphas are Alphas that use fields from only 1 dataset. The following grouping fields are excluded when counting datasets and do not disqualify an Alpha from being an ATOM: currency, country, exchange, sector, industry, subindustry, market
Using the inst_pnl operator will be counted as using the pv1 dataset. Therefore, inst_pnl(<field_from_non_pv1_dataset>) will not qualify as an ATOM Alpha
ATOM Alphas can skip the IS Ladder Sharpe test. ATOM Alphas must pass regular IS tests and the 2Y Sharpe test.
Pyramid Alphas
Pyramids are defined as a combination of region, delay, and dataset category. Example: USA-D1-analyst represents a pyramid for USA region, Delay-1, and analyst dataset category
A single Alpha can belong to multiple pyramids if the Alpha uses multiple data fields from different categories. Pyramid Alphas are Alphas that contribute to a maximum of 2 pyramids.
The following grouping fields are excluded when counting pyramids and do not disqualify an Alpha from being a pyramid: currency, country, exchange, sector, industry, subindustry, market. Example: An Alpha using two pyramids + neutralization fields will still count as contributing to only 2 pyramids and qualifies as a Pyramid Alpha
Power Pool Alphas
Criteria for Power Pool Alphas:

Sharpe >= 1.0
Number of unique operators <= 8
Number of unique data fields (excluding grouping fields) <= 3
Grouping fields: country, industry, subindustry, currency, market, sector, exchange
Self-Correlation of just your Power Pool Alphas <= 0.5.
Once you tag an Alpha as power pool, it stays in the self-correlation pool even if you untag it later
Turnover should be between 1%-70% (both inclusive)
USA Delay 1
You may find out more about Power Pool Alphas here.

Sub-Geography Sharpe Cutoff for GLB Alphas
Submission Criteria	Threshold
AMER Sharpe	≥ 1
APAC Sharpe	≥ 1
EMEA Sharpe	≥ 1
GLB Alphas are subject to additional sub-geography Sharpe cutoff criteria. These criteria ensure that your Alpha isn’t just performing well globally but is also delivering consistent returns across all three geographies. The goal is to avoid over-reliance on a single geography and encourage a more balanced contribution to your overall PnL.

Tips to Improve Sharpe Across Geographies

AMER: Focus on high-liquidity equities and consider incorporating earnings-related signals, as the stocks in these markets are highly responsive to earnings announcements.
APAC: Pay attention to market microstructure data, as price-volume patterns in APAC markets often differ due to shorter market hours and unique market regulations.
EMEA: Explore macroeconomic indicators, as EMEA stocks are often influenced by geopolitical events and currency fluctuations.
GLB Alphas also include a breakdown of global PnL by geography in their PnL chart, making it easy to see how much each geography is contributing. This helps you identify imbalances and determine areas for improvement.
Picture1.png
Japan Robustness Sharpe Test for ASI Alphas Submission
Criteria: Japan Robustness Sharpe ≥ 1

ASI Alphas are subject to an additional country-specific robustness check focused on Japan. This criterion ensures that your Alpha delivers consistent, scalable performance within Japan, one of most liquid markets in ASI. Japan market provides and enhance executable capacity for live trading. If an ASI alpha is weak in Japan and derives most of its PnL outside JPN, it becomes difficult to realize due to lower liquidity, higher slippage, and limited capacity in other markets. Ensuring each ASI alpha achieves a minimum 1 Sharpe performance in Japan increases the realizability and scalability of PnL across ASI.

Note on Japan Sharpe shown in Visualization Tool versus this Test

The Japan Robustness Sharpe Test and the Visualization Tool use different Japan universes. Consequently, the test result may differ from the Japan Sharpe displayed in the Visualization Tool.
The Visualization Tool remains highly useful for diagnosing Japan-specific PnL, turnover dynamics, sector/industry and capitalization breakdowns, and coverage trends, which can guide improvements to Japan robustness.
Picture1.png
Tips to Improve Japan Sharpe

Strengthen economic rationale: Favor signals with clear intuition that plausibly hold in Japan (e.g., earnings revision persistence, conservative accruals, quality/low-risk tilts, liquidity-aware momentum). For example, you can improve your Alpha in JPN Region and re-simulate it to finally submit it in ASI region if alpha initially has <1 sharpe in JPN. Nonetheless, pass the Japan test with margin signals an economically grounded mechanism rather than country-specific overfitting.
Liquidity-aware construction: Emphasize large- and mid-cap breadth; avoid over-reliance on micro-caps where slippage/impact erode realized performance. Keep single-instrument weights well below 10%.
Avoid excessive size-only tilts: Unbounded cap or illiquidity multipliers can degrade robustness. If using cap/volume scalers, keep them bounded and balanced to prevent over-concentration.
Control sector/industry exposures: Use neutralization sensibly to avoid dominance by one industry. Inspect industry/sector-level PnL and Sharpe in the Visualization Tool to detect imbalances.
Stabilize turnover: Choose decay and smoothing that reduce churn without killing responsiveness. Very high turnover increases fragility under realistic costs; very low turnover may reduce adaptability.
Stress-test via Visualization Tool: Review Japan breakdowns for Coverage, Size, PnL, and Sharpe by Capitalization/Industry/Sector; analyze rolling performance, and seasonality. Even with universe differences, these diagnostics remain informative for improving Japan performance.
Interpreting Status Messages in Simulation Results
When “Check Submission” or “Submit Alpha” button is pressed, tests are performed in the order described below. In case Alpha fails any of the tests, respective Test Message is displayed.

1
Alpha fails Weight test
Maximum weight on an instrument is greater than 10% OR Weight is too strongly concentrated or too few instruments are assigned weight.
2
Alpha fails Correlation test
Reduce max correlation
3
Alpha fails fitness test
Improve fitness
4
Delay 0 Alpha fails checkDelay1Sharpe
Alpha better suited for Delay 1
5
Alpha fails SubUniverse test
Improve Sharpe in SubUniverse
Example: if an Alpha clears criteria 1, 2 and 3 but fails at criteria 4, recommendation would be “Improve Sharpe or reduce turnover”.
Selecting Alphas For Submission
Do not submit Alphas as soon they clear the performance cutoff. Improve the idea until you have the best version: in terms of both performance and correlation.
However, do not spend extraordinary amount of time improving a single idea either:
It is generally better to try out new ideas with low correlation to previous ones than to improve performance of Alphas with high correlation.
Generally, low correlation is more important than minor increase in performance. Example: An Alpha with slightly better performance but high correlation is worse that an Alpha with slightly lower performance but much lower correlation
Next: Parameters in the Simulation results
