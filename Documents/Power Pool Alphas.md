Power Pool Alphas are simpler, smaller, higher quality Alphas that can help you do well across Genius, competitions and themes.

Eligibility Criteria for Power Pool Alphas Monthly Competition

Following are the list of criteria for an Alpha to be considered eligible for Power Pool Alphas:

Sharpe >= 1.0
Number of unique operators, including repeat operators <= 8
Number of unique data fields (excluding grouping fields) <= 3
grouping fields: country, industry, subindustry, currency, market, sector, exchange
Self-Correlation of just your Power Pool Alphas < 0.5.
Once you tag an Alpha as Power Pool, it stays in the self-correlation pool even if you untag it later
Turnover should be between 1%-70% (both inclusive)
Pass Sub-universe check
USA D0 and D1, EUR D0 and D1, ASI D1, GLB D1 and OTHER ( JPN, CHN, HKG, TWN, KOR, AMR ) D0 and D1 research regions
Risk Handled Neutralization is mandatory for (USA/EUR/ASI/GLB/CHN Delay 1 and 0)
Note: If the Alpha has Self-Correlation among Power Pool Alphas > 0.5, it should have Sharpe 10% higher than the most correlated Alpha to be considered eligible for submission.

Submission Checks Exempted for Power Pool Alphas

Following submission checks do not apply for Power Pool Alphas:

Prod Correlation
Self Correlation with own Alphas from outside Power Pool
Fitness threshold
IS Ladder
Monthly Awards Qualification

To qualify for the monthly awards in any of the 8 Power Pool leaderboards, a minimum of 10 tagged Alphas per leaderboard is required, with no minimum submissions required per month​. Those 10 Alphas could have been submitted even prior to the month
Submission Quotas After 3 Months

The below quota will apply when consultants cross 3 months since date of first submitting a Power Pool Alpha:

Each consultant can submit up to 10 pure Power Pool Alphas per calendar month, in one single leaderboard of Power Pool​. Pure Power Pool Alphas are those that do not meet submission criteria of either Atom or Regular Alphas
Each consultant can submit up to 1 pure Power Pool Alpha per day
Alpha classified as [Power Pool + ATOM] or [Power Pool + Regular] is excluded from these two limits
Example of daily submissions:
1 Pure Power Pool Alpha
1 [Power Pool + ATOM] Alpha
Total: 2 Power Pool-related submissions
For consultants who have not crossed 3 months since their first Power Pool Alpha submission, standard submission limits for BRAIN consultants apply. Max 4 alpha submissions in a day.
Description of the Power Pool Alpha

To submit a Power Pool Alpha, it is mandatory to describe the idea in at least 100 characters. In the PROPERTIES section at the bottom of the Simulation results. Using the template of Idea and Rationale. Otherwise the Alpha will not be eligible for Power Pool.

Here is an example description:

Idea: In normal market conditions, if a stock is shorted more, its likelihood of bouncing back may also increase (reversion). However, in extreme cases where the consensus in the market is high reflecting in extremely high/low level of short interest, it may potentially be better to follow that trend
Rationale for data used: shrt3_bar field is a vector data field representing the demand to borrow stock, with higher values indicating higher demand
Rationale for operators used:
vec_avg(): Calculates the average value of shrt3_bar for a given day
Conditional operator: Separates normal cases from extreme ones
ts_backfill: Handles NaN values in the data field, detected by checking the coverage with a visualization tool
How do I add or remove Alphas from the Power Pool?

You can view the list of your Power Pool Alphas on the Alphas Page under the Submitted tab. To remove a submitted Alpha from the Power Pool, go to the Submitted tab, open the Alpha description, and click the cross next to the "PowerPoolSelected" tag in the Properties section.

Please note that even after removing the tag, this Alpha will still be part of the self-correlation pool, so new Power Pool Alphas will still be checked for correlation against it.

To retag a submitted Alpha later to the Power Pool, in the Properties section of the Alpha, click on the Tags dropdown and retag the alpha as "PowerPoolSelected"

Tips to create Power Pool Alphas

Review Merged Performance before tagging the Alpha
Explore Low turnover Alphas and liquid (small) universes, which can help improve After Cost performance
Explore your existing Alpha pool for eligible signals
Make use of the newly released Investability Constrained PNL
Your pool should have diverse signals to ensure robust performance of your pool in OS. Diversify your pool across datasets, ideas, operators, universes and even turnover (to some extent)
After creating a sizable pool of Power Pool Alphas, consider removing Alphas which have high correlation with other Alphas in your Power Pool. This may potentially improve combo performance while reducing the Alpha count penalty
Reach out to your research advisor for specific tips on creating good Power Pool Alphas