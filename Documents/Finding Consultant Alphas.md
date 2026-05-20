Welcome to the WorldQuant BRAIN Research Consultant Community!

To kickstart your journey as a BRAIN Research Consultant, this article provides a step-by-step guide in navigating the new submission tests and platform features in the consultant environment, so that you can work towards finding your first consultant Alpha. At the start, the consultant environment may seem more challenging than the user environment you were used to, but treat this as the initial learning phase. Just like how you managed to find Alphas in the user environment, you’ll get the hang of the consultant environment eventually.

Understand the new submission tests
finding_consultant_alphas_new_submission_tests.png
Passing the new consultant submissions tests is one main source of challenge in the consultant environment. In addition to higher thresholds for passing the Sharpe and fitness tests, there will be two new submissions tests: Production Correlation and IS Ladder Sharpe.

Production Correlation

Your Alpha’s correlation will be tested against all existing Alphas in the consultant pool and not just your own. An Alpha passes the production correlation test if its maximum correlation with any BRAIN consultant Alpha is less than 0.7 or its Sharpe is at least 10% greater than the Sharpe of each Alpha with which it has a correlation greater than 0.7.

Tip: By default, this test is not run immediately when you simulate an Alpha. When you test out a new Alpha idea, you may choose to run this test once first, by clicking the refresh button at the Production Correlation section in the Results panel. You can then assess whether this idea is unique enough from the rest of the consultant pool, before deciding whether to continue working on the idea. Try not to run this test too often though, as consultants may be limited to a certain number of correlation requests per hour.

ConsultantProductionCorrelation.png
IS Ladder Sharpe

The IS Ladder Sharpe test checks whether your Alpha is robust throughout the simulation period, with more emphasis placed on recent years’ performance. It is an iterative test, where it assesses your Alpha’s Sharpe in the most recent 2 years in the first iteration, then the most recent 3 years in the next iteration, and so on, until we reach 10 years in the last iteration.

In each iteration, there are two benchmarks that the Alpha’s Sharpe will be compared against. The FAIL_THRESHOLD is the same as the usual overall Sharpe test you’re familiar with, which is 1.58 for Delay 1. The PASS_THRESHOLD is stricter and can differ for each year of iteration. For example, the PASS_THRESHOLD is 2.38 for years 2 to 5, 2.22 for year 6, 2.06 for year 7, etc.

In the first iteration, if the Alpha’s Sharpe for the most recent 2 years is below the FAIL_THRESHOLD of 1.58, the Alpha will fail the IS Ladder Sharpe test immediately. If it is above the relevant PASS_THRESHOLD of 2.38, the Alpha will pass the IS Ladder Sharpe test immediately. Otherwise, if it is above the FAIL_THRESHOLD but lower than the PASS_THRESHOLD, we will enter the next iteration where the Alpha’s Sharpe for the most recent 3 years will be compared to the two benchmarks.

Tip: Some Alphas may have performed well in the past but deteriorated in recent years. Before you choose to double down on a particular Alpha idea, you may wish to check the Alpha’s performance in recent years. For example, is there a downward trend in its more recent PnL? Is the Alpha already failing the IS Ladder Sharpe test in the first iteration, which looks at the most recent two years?

ISLadderSharpe.png
Other consultant submission tests

Here’s the full list of consultant submission tests and their details: Consultant Submission Tests.

Start with what you’re familiar with
When you become a Research Consultant, you gain access to many new features: more datasets, a different simulation period, more regions, more simulation settings and so on. You may be wondering where to start from.

As consultants, your simulation period is now 10 years instead of 5 years. One way to begin would be to simulate your past Alpha ideas with this new simulation period, to see how they work over a longer period of historical data. You can also see how each Alpha performs in the new submission tests to earn a better understanding of how these tests work.

Thereafter, you can move on to other datasets in dataset categories you’re more familiar with. Swap out existing data fields you used in your past Alphas with similar data fields from these other datasets. Try new Alpha ideas using these datasets that you can understand well. You may also wish to explore model datasets, which usually has data fields with values that may already be treated and may be more easily used to create Alphas.

As you explore simulating Alphas in the consultant environment, you may wish to refer to tips on how to improve your Alphas here: A list of must-read posts on how to improve your Alphas that are submitted.

Try new regions
finding_consultant_alphas_region_characteristics.png
When trying out Alpha ideas, you may choose to try the same idea out in all the available regions to potentially increase the likelihood of finding an Alpha that works. Here are some notes on the regions available on BRAIN.

USA

As users, you would have mostly worked with the USA region. This region remains popular among consultants and quite a number of Alphas have already been found in this region. This means that it may be hard to beat production correlation in USA.

HKG, KOR, TWN, CHN, IND

Look out for the high turnover in these regions. There may also be some region-specific considerations for KOR and TWN too. More tips here: Getting started on HKG/KOR/TWN, Getting Started: China Research for Consultants, India Alphas

GLB, EUR, ASI

For these regions, each region may contain stocks from different countries, which may cause the data field values to contain currency differences. It might be more meaningful to instead neutralize by country first before neutralizing by any other grouping. Refer to this guide on applying: Double Neutralization.

Explore new datasets
As you become more comfortable with the consultant environment, it may be time to try new dataset categories that you haven’t tried before! Trying new dataset categories can improve the diversity of your alpha pool too.

When trying new datasets, here are some things to take note:

For vector data fields, you’ll need to convert the vector data field into a matrix data field first: Vector Datafields.
Evaluate new datasets using these tips: [BRAIN TIPS] 6 ways to quickly evaluate a new dataset.
How to handle datafields with low coverage: [BRAIN TIPS] Weight Coverage common issues and advice.
Choosing datasets that are included in multiplier themes would increase your likelihood of having higher base payments: Overview of Themes.
Build Alphas using research papers
The first and foremost step of building an alpha is coming up with an alpha idea. While there are multiple sources for finding ideas, research papers stand out as one of the most useful. In the beginning, the learn section of the platform is a good resource for sourcing ideas. For instance, the “Example” tab and Alpha concepts page are very useful. Although, for building low correlation alphas, it is important to use some unique or lesser utilized ideas. Research papers can assist you in finding different ideas.

Here are some general guidelines to build alphas using research papers:

Know your Operators: The second step of the research process is to implement your alpha idea using operator. Hence, it is important to understand the concept of operators well. We recommend you go through the detailed operator descriptions before reading the research papers.

Reading the paper: Visit any online journal and go through a few abstracts of the research papers. Choose a paper with an interesting idea to work with amongst all of the options. You can read the introduction, abstract, and main body. The aim is to gain a decent understanding of the research paper so that you know the methodology and data used by the authors.

Formulating your alpha: The final step is to formulate your alpha. This is where your understanding of the operators comes in. Try to replicate the idea suggested in the paper and assess its performance, then think of any improvements that can be made on this version using any additional operators / data.

We will take you through an example research paper to show you how you can come up with an idea and refine it to create an alpha. This research paper talks about meeting or beating earnings estimate. Stocks that are better or equal to their earnings estimate are likely to show an outperformance as compared to other firms.

Iteration 1

Since the research paper is talking about an event (earnings release), we can use trade_when operator. A simple implementation of this idea could be to enter your positions when earnings estimate are beaten and amongst those stocks take positions according to the rank of ratio of actual earnings and estimated earnings and maintainyour position for the remainder of the quarter.

We have used the days_from_last_change operator to check if the earnings announcement was recent or not. The alpha below is in the US region, decay 4 and on subindustry neutralization, you can feel free to play around with the settings.

12
event=days_from_last_change(eps)<=5 && ts_delay(est_eps,10) <eps ;
trade_when(event,rank(eps/est_eps),-1)
Simulation Settings
Region	Universe	Language	Decay	Delay	Truncation	Neutralization	Pasteurization	NaN Handling	Unit Handling	Max Trade
USA	TOP3000	Fast Expression	3	1	5	Industry	On	Off	Verify	Off
Here are the results

is_summary.png
Finding Consultant Alphas: Iteration 1 Graph
The alpha isn’t submittable but the results aren’t too bad either. This is a good sign for us and increases our confidence in the idea since our first implementation has shown decent results. Performance metrics give us a direction that we need to focus on increasing the turnover.

Iteration 2

In our first iteration, we only focused on stocks that were meeting or beating the earnings estimate and hence we took positions in a small subset of stocks. We can try another implementation of our idea where we take positions in all stocks but take positive weight in those stocks that beat expectations.

12
event = days_from_last_change(eps)<=5 && ts_delay(est_eps,10) < eps ;
if_else(event, 0.5 + rank(sales/assets), rank(sales/assets) )
Simulation Settings
Region	Universe	Language	Decay	Delay	Truncation	Neutralization	Pasteurization	NaN Handling	Unit Handling	Max Trade
USA	TOP3000	Fast Expression	3	1	4	Industry	On	Off	Verify	Off
The 0.5 + rank(sales/assets) ensures that we up weight stocks that meet or beat earnings estimate. The asset turnover ratio was used to get an idea of how efficiently the firm uses its resources, you can obviously try out different ratios or data fields as a proxy for financial health of the firm /as a default fundamental signal.

5.png
6.png
Our turnover has increased since we have now moved from trade_when to if_else operator and take positions in all the stocks. We have taken a hit on our fitness due to this.

Iteration 3

Working on a new idea doesn’t mean you can’t use your previous knowledge or ideas to aid your research. In fact, a responsible use of your past knowledge with your new ideas can help you build a great number of alphas from a single research paper.

Our paper here talks about the outperformance of stocks that beat earnings estimate. So, deciding to go long on these stocks for the complete quarter sounds plausible. For the other stocks, it would make sense to use an idea which is irrespective of meeting or beating the earnings estimate. This will make sure we are not taking positions solely on the basis of information added at an interval of 3 months. From our past knowledge, we can bet on the mean reverting nature for these other stocks in our portfolio.

7.png
Alpha =1 makes sure we are long on the stocks that beat earnings estimate since 1 is the max possible value of our alt_alpha hence even after neutralization it is likely that these stocks will have positive weight.

8.png
9.png
We see a significant improvement in all of our performance metrics. You may notice we have used the same event across all three implementations and despite that, achieved very different results. This shows how we can use a single framework and a responsible combination of different ideas to build multiple alphas.

Iteration 4

Similar to the previous iteration here we have scaled the alpha by sales_ps in order to adjust for different eps scales of different firms

10.png
11.png
12.png
You can use different implementations for the same idea on the brain platform or use any of the numerous data fields at your disposal to improve an idea or come up with an alpha that is not correlated to our existing production pool. So, reading new ideas/papers will not only help you build high-sharpe alphas but also in bringing down your correlation, which should be an equally important goal of your research. Further, the target is never to make an alpha “just good enough to be submittable” you may carry forward improvements even after passing all tests and submit the best version that you deem fit since the OS results hold the highest importance.

Some Additional Tips

Reading helps. Almost none of the ideas given in the research papers would work as they are presented (in some cases, opposite works). They are helpful in guiding you to think in a certain direction which you might otherwise miss completely.

Before reading, also make sure that the dataset given in the research paper exists in Brain. This will save you a lot of time in case you read a research paper only to realize the dataset isn’t available.

finding_consultant_alphas_best_practices.png
