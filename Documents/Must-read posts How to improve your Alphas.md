从使用者向顾问的转变并不是一件简单的事情，因为在制作Alphas的过程中，您将会处理许多开放式问题。在量化研究中，创造性思维和科学思维的结合，使得Alpha制作过程中没有对错之分。

通常，Alpha研究周期由以下3个阶段组成：
1.提出一个直观的Alpha理念；
2.使用可用的数据集和运算符实现它；
3.优化Alpha的参数和中性化设置，以便以最佳形式提交。

虽然Alpha理念、数据集和运算符不断变化，但实现这三个阶段所需的技术和方法论基本保持不变。因此，以下文章是您Alpha研究旅程的通用指南，将为您提供坚实的基础:

如何获得更高的Sharpe How to get a higher Sharpe

Often there is no best answer for this general question, so we would suggest you first need to understand the Sharpe or the related metric, information ratio (IR).

IR = Return / standard_deviation (Return)

Based on this formula, there are two ways to improve IR:

Increase your alpha return
Reduce your volatility
Increase your alpha return
If you think of alpha as a prediction of the return, then increasing the return often means you are predicting the return better. In other words, the more information you have, the better your prediction. You can predict short term with price–volume data or news and long term with fundamental, analyst or news data, just to name a few possibilities. A simple prediction model is often more robust, but the performance may be low, while a more complex model will often generate a higher return, but beware of overfitting

Reduce your Volatility
To reduce your volatility you may want to understand where it comes from: One way is to think about the instability of a stock and the market. Neutralization can often help reduce the exposure to the overall market or a certain group within it with high volatility.

The more you work on Brain, the more you will gain techniques to improve your signals — nothing can replace hard work. For the beginner, we suggest you spend time on the Learn section of the Brain platform and on the Community forum where you can get insights from other experienced researchers.

如何潜在地增加Alpha的回报How to potentially increase returns of an alpha
Here are five tips that may help you improve the returns of your alphas:

Increase the turnover of your alphas — higher turnover means more trading and potentially higher returns.
Use lower decay values in the alpha settings.
Work on more liquid (smaller) universes in the alpha settings.
While keeping returns and drawdown at the same level, you may get higher returns if you increase the volatility of your alphas.
Try using news and analyst datasets. They may have the potential to generate alphas with good returns.

如何降低Alpha的相关性How to reduce correlation of an alpha
This is a common problem many researchers face in their alpha research — you are not alone. First, let’s look at the good side of the problem. If the correlation between alphas is high, that means you have probably implemented similar ideas, so it is unlikely that you did something wrong. Your idea and implementation should be sound (assuming the original alpha had good performance).

So if you are new researcher, you should keep the idea around because it can be used for different alphas. Those alphas can be a variation of the current alpha using:

 Different data fields: You might try to use an equivalent data field first (such as “high,” “low” or “open” to replace “close”).
Different operator: Again start with something you find similar in practice, building your own library of similarity that could further help you reduce max correlation.
Different grouping: This is powerful approach, but don’t create an arbitrary group just for the sake of reducing correlation.
The reason to try something equivalent first is to reduce the chance that you distort the implementation of your original idea. Maintain the purity of the idea rather than complicate it unnecessarily for the sake of correlation fitting (which is considered bad practice).

Of course, the best way to reduce max correlation is to think outside of the box. That is true research.

如何降低换手率How to reduce turnover
You can use the following targeting to create event-driven alphas and low turnover alphas.

Concept:
If (event) {
Assign alpha values;
} else {
Hold alpha values;
}
Expression:

trade_when(Event_condition, Alpha_expression, -1)

Pros:

Good alpha coverage
Flexible in determining events
Can be used to enhance signals by trading at the right time
Low turnover and low cost alpha

 

Cons:

Not easy to get high Sharpe alpha
Not easy to get high return alpha

Approach:
Define events: Any spike in returns, data values and technical indicators can be used to define events.
Alpha assignment: Look for signals that are aligned with the abnormality of an event — that is, alphas that need to be executed when such events happen.

Note:
Hold alpha can be replaced by decaying alpha linearly or exponentially.
Check alpha coverage to make sure events are not so rare.

如何潜在地减少PnL波动How to potentially decrease PnL fluctuations
There can be some reasons for sudden jumps:

Because the Alpha values are frequently changing from NaN to non-NaN or vice versa. You can use backfill function to take care of this.
The other reason is that the Alpha values change rapidly from time to time. Thus decay or taking average in Alpha formula can help you in making the curve smoother.
It also may be because of too much money on one stock and if the stock value has a jump then the PNL will also have a jump in it. To tackle this you can set stock weight (Truncation) in sim settings to non-zero value between 0 and 1, preferably less than 0.1.


如何选择合适的中性化How to gain intuition for Neutralization
Neutralization 🥉
I.基础中性化:

中性化是一种操作，其中原始的Alpha值被分成组，然后在每个组内进行归一化（从每个值中减去平均值）。这些组可以是整个市场，也可以使用其他分类（如行业或子行业）进行划分。

这样做是为了关注组内股票的相对回报，并将风险敞口最小化到组的回报。由于中性化的结果，组合是半多头、半空头的，并且可以保护组合免受市场或行业冲击。

例如，在交易时，我们不希望押注市场走向，以最小化“市场风险”。这是通过等量的多头和空头头寸来实现的，即投入在多头头寸中的金额与投入在空头头寸中的金额大致相等。这被称为“市场中性化”。在BRAIN平台中，我们可以在回测设置中设置Neutralization = market（或所需的行业或子行业）来实现这一点。

假设我们有Alpha = -ts_delta（close，5），其中Alpha是一个向量。设置neutralization = market会使Alpha向量的平均值等于零，即Alpha向量将经历以下变化：Alpha = Alpha - mean(Alpha)。

然后，将对此新向量进行缩放以对应账户规模。因此形成的组合将包含等同金额的多头和空头头寸，并可用于计算当天的PnL。

在回测Alpha时，平台会自动在设置中执行一些操作。 "回测设置中的中性化"将您的Alpha作为操作的最后一步进行中性化。这确保了您的Alpha是多空中性的。

“group_neutralize(x, group)”和“回测设置中的中性化”使用相同的操作。

何时使用group_neutralize：您可以使用group_neutralize(x, group)在不同的组值上以更细化地应用中性化。

在group_neutralize中使用什么设置：如果您将group_neutralize(x, group)用作最后一个运算符，则可以在回测设置中将“None”设置为中性化，衰减设置为“0”和截断设置为“0”（值0将禁用衰减和截断运算符）。您可以在group_neutralize之前直接在Alpha表达式中插入衰减/截断运算符。

“group_neutralize(x, group)”和“回测设置中的中性化”是否可以互换使用？
是的，例如：
alpha1 = -ts_returns(close,5)，在中性化中使用行业，衰减为“0”和截断为“0”在回测设置中与
alpha1 = group_neutralize(-ts_returns(close,5),industry)，中性化为“None”，衰减为“0”和截断为“0”相同。

提示：
• 始终选择中性化；仅在Alpha中有中性化运算符时时将其保留为None。
• 尝试流动性更好的股票池，因其股票数量较少，因为我们希望每个组中有足够的股票。
• 在流动性差的股票池尝试更小的股票组。

• 对于EUR、ASI地区，请手动使用“国家”和“交易所”中性化选项。

以下是基于数据集类别的建议中性化。我们强烈建议您在研究中尝试这些中性化方法

Fundamental Datasets
✔️
Fundamentals of a company can affect stock price in a different way depending on the industry, so an industry neutralization is recommended.
Analysts Datasets
✔️
Analyst datasets provide an estimate of future fundamental data, hence an industry neutralization is recommended here as well
Model Datasets
✔️
✔️
✔️
✔️
Model datasets can be extremely variable depending on the subcategory of the dataset available. Try experimenting with different neutralization categories based on those subcategories to find the best result.
News Datasets
✔️
News could have very different impact on different companies, based on their subindustry. Impact of a CEO change can be different for Twitter and Apple Inc even though both are in the broader Tech industry. Hence, try neutralizing for subindustry.
Option Datasets
✔️
✔️
For Options datasets, we suggest neutralizing for Market or Sector, because the impact of options on a stock price is almost similar across broader industries.
Price Volume Datasets
✔️
✔️
Generic ideas work well across all instruments, using Industry or Subindustry neutralization could reduce the performance.
Social Media Datasets
✔️
✔️
Social media impact could have different impact on different companies, based on the subindustry, so try neutralizing at the subindustry level. You can also try neutralizing at the industry level as well depending on how broadly applicable the news is.
Institutions Datasets
✔️
✔️
Depends on the type of institution datasets available, who provides them, and its implications. Test out neutralizations for Sector or Industry.
Short Interest Datasets
✔️
Industry neutralization is recommended for Short Interest datasets. Try others as well!
Insider Datasets
✔️
✔️
Insider news will not necessarily affect each company in a similar way, since it is based on the industry or subindustry. Hence, neutralize for those categories with these datasets.
Sentiment Datasets
✔️
✔️
Similar to insider/social media, sentiment could have different impact on different companies, based on the industry or subindustry, so neutralize for those categories.
Earnings Datasets
✔️
For Earnings datasets, Industry neutralization recommended, similar to Fundamental datasets
Macro Datasets
✔️
✔️
✔️
Sector/Market/Industry are macro-economic activities, so neutralizing Macro datasets for those categories will be best. There is not much difference across subindustries.

如何避免过度拟合How to avoid overfitting
We have to accept the fact that fitting is a part of the alpha creation process. As a result, overfitting is also part of the game. The most important way to control for overfitting is by doing disciplined research.


Is overfitting bad? Yes, it is. However, random data mining research without ideas is even worse. Robust alphas require good ideas and rigorous testing. Here are some of the tests you can use to reduce the chance for overfitting and improve the robustness of your alphas.

Rank test (turn alpha to rank)
Binary test (turn alpha to -1, 1)
Sub/super universe test
Don’t limit yourself to what is listed here. There are tests that can be done based on your creativity and experience; the more you do the better. By the way, random backtest is often not very applicable due to changing market conditions.

Here are some other tips and tricks:

Often it is not a good idea to concentrate weight on volatile stocks.
Reduce your exposure to factors.
Don’t choose the best; the second best often has less overfitting tendency.
Don’t fit tests. No test is bad. Fitting to tests is also bad.
Don’t select. If you have to choose between using 4 or 6-day decays, you can use 5 or simply take the alpha average of 4 and 6 days.
Don’t fail in to the excellent/superior trap. What you see based on IS performance. The main question is, “Can that performance hold?”
Be courteous to other people and share ideas and good advice.
Using the test period feature in settings to prevent overfitting:

Using simulation settings, you can divide your In-Sample (IS) period into a Train and Test period. The Train period can be utilized to develop your Alphas and SuperAlphas, while the Test period is ideal for validating them. An Alpha developed based on the simulation results of Training Period and performs well in both periods is likely a strong candidate for submission and may have avoided overfitting.

这些阅读回答了在开发Alphas的过程中遇到的一些最常见的问题。采用上述建议的做法应该有助于您使用WorldQuant Brain，并可能在长期内带来显著更好的结果。