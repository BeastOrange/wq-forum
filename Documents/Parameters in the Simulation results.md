在回测结果页面中，您会发现一个评级面板，位于结果的统计选项卡中，标明了卓越、优秀、良好、一般或需要改进等评级，取决于您的Alpha的Fitness分数，具体如下所示：

Spectacular
> 2.5
> 3.25
Excellent
> 2
> 2.6
Good
> 1.5
> 1.95
Average
> 1
> 1.3
Needs Improvement
<= 1
<= 1.3
年化收益率
年化收益率是特定期间内一种证券或组合的收益或损失。收益率包括，相对于投资金额而言，收到的收入加上资本收益。在BRAIN平台中，收益率=年化PnL/账户本金大小的一半.

夏普比率和信息比率
信息比率（IR）衡量模型的预测能力。在BRAIN平台中，定义为组合每日平均收益与这些收益的波动率之比:

 
其中PnL是每日盈亏，以美元计算

Sharpe是IR统计量的年化版本，即Sharpe=sqrt(252)IR ≈ 15.8IR，其中252是一年中美国交易日（市场开放日）的平均数量。
Sharpe或IR衡量Alpha的回报，同时尝试识别其一致性。IR越高，Alpha的回报就越一致，一致性是理想的特征。高Sharpe（或IR）比仅仅高回报更为理想.

注意：Sharpe和IR在BRAIN平台以外的其他地方可能会被定义得略有不同.

适应性
Alpha的适应性是收益、换手率和Sharpe的函数:

 
良好的Alpha具有高适应度。您可以通过增加Sharpe（或收益）并降低换手率来优化Alpha的表现。改善一个因素通常会对另一个因素产生不利影响。当您努力优化Alpha时，其适应度的提高表明您的更改产生了积极影响.

累积PnL图表
累计PnL图表：Alpha在整个回测期间的表现（PnL）的图表（如下所示）。该图表可以通过在绘图区域下方单击并拖动来放大。在此处可以更改PnL绘制的起始和结束日期。在PnL图表上方的下拉菜单中单击Sharpe比率可显示Sharpe比率图表（随时间变化的Sharpe Ratio）。确保PnL图表呈上升趋势，Sharpe高且回撤（Drawdown）最小

Cumulative PnL
样本内表现摘要
样本内表现摘要: 向下滚动到回测结果的统计信息模块（如下所示），会显示有关Alpha表现的各种指标.

IS_Result.PNG
年份: 回测数据所在的年份。最后一行显示的是Alpha在所有年份上的表现.

做多/做空数量: 分别为做多或做空头寸的金融工具数量。

夏普比率: Sharpe = IR * Sqrt(252), 其中IR=观察时间段内PnL平均值/ PnL标准差。

稳健Fitness性 在Alpha Performance帮助页面中定义为：Fitness = Sharpe*sqrt(abs(Returns) / max(Turnover, 0.125))。

年化收益率: 交易资本的回报率：年回报率=年化PnL/账本大小的一半。它表示观察期间您获得或损失的金额，以%表示。Booksize指的是在回测期间用于交易的资本（资金）的金额。Booksize是恒定的，并且每天都设置为2000万美元。利润不会再投资，损失会用现金注入到组合中补充。BRAIN平台假设您有1000万美元，并将投资于高达2000万美元的资产。这被称为杠杆。表现（如收益率、Sharpe）是在1000万美元的基础上计算的.

换手率: 换手率表示交易的频率。它可以定义为交易价值与账本大小之比。Daily Turnover = Dollar trading volume/Booksize。良好的Alpha换手率低，因为低换手率意味着较低的交易成本。

单位收益: 每交易一美元的利润；计算方法是PnL除以一定时间段内总交易额。

PnL: 盈亏（PnL）是头寸和交易产生的资金（这意味着您在该年赚或赔的金额，以美元表示）。

daily_PnL = sum of (size of position * daily_return) for all instruments, 其中 daily return per instrument = (today’s close / yesterday’s close) – 1.0。

回撤：一段时间内PnL最大的降低，以百分比表示。计算方法如下：找到PnL中最大的峰值到谷值回撤，并将其美元金额除以账本大小的一半（$1,000,000）来计算

自相关性
开始自相关性检查：单击自相关性行中的向下箭头按钮将生成一个表格，其中最多包含5个与您已提交的符合OS测试资格的Alpha的性能统计数据。此信息旨在帮助用户确保他们拥有多样化的Alpha。也可以通过单击Alphas页面中的Alpha来访问此信息。

Correlation
样本内（IS），半样本外（Semi-OS）和样本外（OS）
与固定的开始和结束日期相比 ，In Sample(IS) 是一个5年的滚动窗口，每天都会改变。In Sample (IS)回测从当前日期的7年前开始，到2年前结束。最近一年的数据被隐藏并用于评分和测试。在“我的Alpha页面”的“OS”选项卡中显示的统计数据将随着数据变得可用而逐渐补全。

完全隐藏最后两年的数据会提高Alpha在OS表现和评分方面的置信程度。

rolling_semi_os.PNG
Alpha状态
在成功模拟Alpha之后，Alpha会被标记为“UNSUBMITTED ”。
成功提交之后，Alpha会显示“ACTIVE”状态。
研究顾问的状态为“ACTIVE”的Alpha可以积累weight并对季度薪酬产生贡献，如同在顾问条款中描述的那样。"ACTIVE"状态会一直保持直到该Alpha所用到的数据集退役或者WorldQuant根据自己的裁量退役这个Alpha。
如果该Alpha所用的数据集不再可用或者该Alpha在OS阶段一直表现不佳，这个Alpha的状态会变为"DECOMMISSIONED”。
退役后的Alpha不再积累weight, 也不在对顾问季度薪酬产生贡献。
Alpha Lifecycle
注意：在我们升级以上Alpha状态的过程中，平台有可能出现暂时的数据不一致现象，我们希望并感谢您的理解。