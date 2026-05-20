Single Dataset Alphas* use data fields from only one dataset to build the entire Alpha expression, excluding 6 permitted grouping fields that can be a part of the expression – country, exchange, market, sector, industry and subindustry. Single Dataset Alphas also have a slightly relaxed submission criteria. For such Alphas, rather than clearing IS Ladder Sharpe test, Alphas need to only clear certain limits for Last 2Y IS Sharpe.

Further details on the importance of Single Dataset Alphas and the relaxed IS testing details are discussed below:

Introduction

BRAIN offers a wide array of datasets spanning various categories, including fundamental, price-volume, analyst, and options data. While an alpha can incorporate data fields from multiple datasets, this approach if not implemented correctly, may potentially lead to overfitting due to the mixing of conflicting signals between datasets.

In contrast, single dataset Alphas maintain homogeneity by using data from only one dataset, making them less prone to overfitting and more robust in their predictions.

Single Dataset Alpha Expression Properties

Single Dataset Alphas must utilize data fields from only one dataset, with exceptions for the following 5 permitted grouping fields – country, exchange, market, sector, industry and subindustry.
The use of inst_pnl() and convert() operators is considered as utilizing the pv1 dataset since these operators rely on pv1 data for calculations.
Submission Tests for Single Dataset Alphas

Single Dataset Alphas have slightly relaxed submission criteria as compared to regular Alphas. These Alphas don’t need to pass the IS Ladder Sharpe Test. Instead, only the last two year Avg IS Sharpe of the Alpha must clear the following thresholds:

Last 2Y Sharpe limit	Threshold
Delay-1	2.38
Delay-0	3.96
Note: If the turnover of Alpha is less than 30%, the IS Sharpe Ladder PASS_THRESHOLDS are multiplied by a factor of 0.85.

For more information, refer to Check-IS-Sharpe or IS-Ladder test

All Alpha simulations with properties of Single Dataset Alphas shall display the message “2 year Sharpe of <value> is below cutoff of <limit>” or “

2 year Sharpe of <value> is above cutoff of <limit>.” in the IS Testing Status tab of Alpha simulation results instead of the IS Ladder Sharpe Pass/Fail criteria.