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