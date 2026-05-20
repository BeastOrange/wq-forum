欢迎来到WorldQuant BRAIN

本指南的目的是提供BRAIN顾问项目的基本概述和简单的量化金融概念，以帮助您开始创建Alpha。在完成本指南的学习后，你将获得足够的知识来尝试回测你的策略。这是一个学习的过程，许多人以前有同样的经历，所以无论你的背景如何，你也可以做到。祝您好运!

本课程有以下章节供您学习

研究顾问—与WorldQuant一起合作的机会

金融基础知识--股票市场和它的运作模式

量化分析--及其与BRAIN平台的关系

如何使用BRAIN平台--快速表达式、操作符和数据集

常见的金融分析方法及实例--技术和基本面分析

研究顾问
成为我们的顾问

WorldQuant是一家全球量化资产管理公司。由Igor Tulchinsky创立于2007年，我们的团队在全球拥有超过850名员工，在全球市场上开发和部署各种资产类别的投资策略。我们为全球人才提供机会，让他们在我们项目开展的国家成为研究顾问，并参与到WorldQuant的研究工作中。

全球社区

通过我们专有的研究平台产生高质量的预测信号（Alphas），回测金融市场策略，利用市场低效率以盈利，WorldQuant BRAIN通过由数据集和工具、业绩仪表板和价值增强组成的回测平台，以互动方式向用户介绍量化金融世界。

18,000多名用户， 700多名顾问， 65,000多个数据集

成为顾问的好处

作为一名研究顾问，你将有以下机会：

- 获得基于择优选拔的补助。每天赚取高达120美元（基于用户产出），每季度赚取25.000美元（基于绩效）。

- 符合条件的BRAIN顾问有机会被考虑提供全职职位

- 各种潜在的实习机会

- 成为全球量化分析师精英社区的成员

- 还有更多。

谁有资格？

不存在特定的背景要求！在科学、技术、工程、数学（STEM）或任何其他与分析和量化高度的相关领域的经验将会是有用的。

用户仅需在WorldQuant模拟练习中获得10,000分以上，就有资格申请成为顾问。目前，我们只向以下居民提供这个机会：

- 中国大陆

- 香港

- 台湾

- 肯尼亚

- 韩国

- 印度尼西亚

- 印度

- 马来西亚

- 新加坡

- 英国

- 越南

- 泰国

阅读我们顾问的故事 :

Azmi-Fauzi-Hero-Image-QA-scaled.jpg
Azmi Fauzi – Indonesia印尼

consultant 2.jpg
Aradhana Singh – India印度

consultant 3.jpg
Zhuangzhuang Meng - China中国

金融基础知识
我们的许多顾问都是从非金融专业开始的，所以如果你之前没有金融知识，也不必担心。本节将向你介绍一些基本的知识。

股票市场如何运作

股票市场是指为发行、购买和出售在证券交易所或场外交易的股票而存在的公共市场。股票，也被称为股权，代表着对一家公司的部分所有权，而股市是一个投资者可以购买和出售这种可投资资产所有权的地方[1]。

寻求回报

投资者寻求从购买股票中获利，如果股票价格比他们的购买价格上涨，他们就会卖出自己的股票以获得利润。例如，如果投资者以每股10美元的价格购买一家公司的股票，随后股票价格上涨到每股15美元，那么投资者就可以通过出售他们的股票实现50%的投资利润[1]。回报被WorldQuant定义为交易资本的回报：

它表示在这段时间内赚取或损失的金额，以%表示。

做多一只股票

持有一只股票的多头头寸意味着买入它，如果股票升值，你就会赚钱。

做空一只股票

另一方面，持有股票空头头寸意味着借入你不拥有的股票，通常是从你的经纪人那里借入，然后卖出，并希望其价值下降。当这种情况发生时，你可以以低于你所支付的价格买回它，并把借来的股票还给你的经纪人。

交易量的定义

交易量是指在一段时间内，通常在一天内，一种资产或证券的换手率。例如，股票交易量可以指在每天开盘和收盘之间交易的股票数量。交易量，以及交易量在一段时间内的变化，是技术交易者的重要信息。[2].

什么是收盘价/开盘价

开盘价是指证券在一个交易日开盘时首次交易的价格。收盘价是交易时段结束前的最后一笔交易的价格。这些价格很重要，因为它们被用来创建传统的线型股票图表，以及在计算移动平均线和其他技术指标时使用。 [3, 4].

进一步阅读和参考资料:

[1] Corporate Finance Institute. (2022, October 28). Stock market. https://corporatefinanceinstitute.com/resources/wealth-management/stock-market/

[2] What is volume of a stock, and why does it matter to investors? (2003, November 23). Investopedia. https://www.investopedia.com/terms/v/volume.asp#:~:text=Volume%20is%20the%20amount%20of,its%20daily%20open%20and%20close

[3] Close. (2003, November 18). Investopedia. https://www.investopedia.com/terms/c/close.asp

[4] Opening price: Definition, example, trading strategies. (2005, July 3). Investopedia. https://www.investopedia.com/terms/o/openingprice.asp#:~:text=The%20opening%20price%20is%20the,is%20its%20daily%20opening%20price

量化分析
有许多方法可以确定是做多（买入）一只股票还是做空它。金融学中的定量分析（QA）是一种强调数学和统计分析的方法，以帮助确定一只股票的价值。量化交易分析师（也被称为 "quants"）使用各种数据--包括历史投资和股票市场数据--来开发交易算法和计算机模型。这些计算机模型产生的信息有助于投资者分析投资机会，并制定他们认为将是成功的交易策略 [5].

关于BRAIN平台

利用定量分析方法，BRAIN平台是一个全球金融市场回测模拟器，是为探索Alpha研究而创建的。它接受Alpha表达式作为输入，并绘制其盈亏（PnL）作为输出.

graph3 (1).jpg
每天根据历史日期对每个金融工具的输入表达进行评估，并据此构建投资组合。BRAIN平台根据表达式的值对每种金融工具进行投资。它进行交易（买入或卖空），并为每种工具分配权重。

什么是Alpha？

Alpha是一种算法，它将输入数据（价格-成交量、新闻、基本面等）转化为一个向量，其中的数值与我们每天要持有的每种金融工具的头寸和权重成正比。

权重

想象一下，市场数据是一个矩阵，每一行代表一个日期，每一列代表一只股票。例如，收盘价数据的矩阵可以是这样的:

graph4 (1).jpg
表格: A、B和C公司各自3天的股票收盘价.

Alpha表达式的作用是将输入矩阵转化为权重输出向量，每个权重对应于一只股票。Alpha输出向量，其权重是对应于股票池中每个工具的值，它看起来可能是这样的:

graph5 (1).jpg
表格:输出向量，表明交易方向以及对公司A、B和C的权重

累积盈亏（PnL）

我们从Alpha表达式中得到了股票的权重，下一步就是要得到每一天的利润和损失（PnL）。

从上表中，我的权重_A = 0.2，权重_B = -0.5，权重_C = 0.3。现在，我的投资金额被称为 "账面规模"。假设我的账面金额是100美元。所以我计算我想投资于每只股票的资金：

money_A = 0.2 * 100 USD = 20 USD 多头

money_B = -0.5 * 100 USD = 50 USD 空头

money_C = 0.3 * 100 USD = 30 USD 多头

现在，我买入价值20美元的A，卖出价值50美元的B，买入价值30美元的C。

我持有这个投资组合一整天，并在模拟期的第二天把它卖掉。现在在一天之内，股票A、B、C的价格都发生了变化。因此，我的投资组合的总价值也发生了变化，例如从100美元到105美元。因此，我在这一天赚了5美元。

现在我再次计算股票的Alpha值，再次计算权重，再次交易价值100美元的投资组合。[注：在BRAIN平台上，我们对所有的日子都使用恒定的账面大小，无论你的投资组合是赚钱还是亏钱。］

在回测期的每一天都要重复这样的操作，以计算和绘制累积的PnL

graph1 (2).png
降低风险和波动性

一个好的阿尔法最好是有持续增长的净值，高的年回报率，更重要的是，在累积利润图中的波动很小。如果标准差较低，图表中的波动就会较小。如果图表中显示出高波动/波幅，尽管回报率很高，那么阿尔法就不会被认为是足够好。

WorldQuant旨在开发具有低波动性和低风险的股票多空市场中性阿尔法指数。这种投资具有吸引力，因为它们有望产生比只做多头的投资组合更好的风险调整后的回报。股票多空市场中性策略被对冲基金普遍使用，其目标是最大限度地减少市场风险，并从两只股票的价差变化中获利。

进一步阅读和参考:

[5] What to know about quantitative analysis. (2014, April 11). Investopedia. https://www.investopedia.com/articles/investing/041114/simple-overview-quantitative-analysis.asp

如何使用BRAIN平台
理论够了，让我们深入了解如何在BRAIN平台上编写第一个Alpha。

不需要编程经验

对所有没有编程背景的人员来说，使用BRAIN的好消息是，不需要事先有编程经验。

BRAIN的编码方式

BRAIN使用快速表达语言，由两个主要元素组成： 数据字段和运算符。

能否使用Python/R/MATLAB等进行字母运算？

我们的一位用户曾问我们： 是否有计划允许用户利用Python/MATLAB/R与BRAIN API互动，分析数据集并提交Alpha向量？

我们的答复是：BRAIN平台目前只能使用快速表达式语言。关于API，当API通信以低强度进行时，我们目前不禁止对BRAIN平台进行程序化访问。

数据字段、数据集

数据字段指的是一个命名的数据集合，例如 "开盘价 "或 "收盘价"。

数据集是数据字段的集合（点击这里查看）.大多数用户通常从价格、成交量和基本面数据集开始研究。

运算符

运算符是实现您Alpha策略所需的一组数学或统计技术，例如数学运算符：+ - / * 或横截面运算符，如“排名”（rank）。阅读 Learn/Operators 获取更多详细内容.

以下是使用数据字段和运算符构建Alpha策略的常见示例:

graph2.png
您可以通过在回测模拟器页面的左下角点击“示例”按钮来尝试一些样本Alpha策略。利用提示并测试几个模拟！点击此处立即尝试: Simulate Page

股市分析方法
您可能会问, 如何想出新Alpha策略的想法？本节将带您了解两个Alpha策略的想法和解释它们背后的思路，分别是技术分析和基本面分析。

技术分析

技术分析是一种交易纪律，通过分析交易活动中收集的统计趋势（如价格变动和成交量）来评估投资和识别交易机会。技术分析师相信，一个证券的过去交易活动和价格变化可以是该证券未来价格变动的有价值指标。

在整个行业中，已经有数百种模式和信号被研究人员开发出来用于支持技术分析交易。这些包括趋势线、通道、移动平均线和动量指标等[6].

以成交量作为指标

如果一家公司的股票成交量很高，意味着许多人在买卖该股票。假设我们的假设是，具有更多交易量的公司比交易量较低的另一家公司更有吸引力。然后我们将更多的权重分配给交易量更高的公司。

表达这个想法的一种方法是通过以下Alpha表达式:

1
volume
Simulation Settings
Region	Universe	Language	Decay	Delay	Truncation	Neutralization	Pasteurization	NaN Handling	Unit Handling	Max Trade
USA	TOP3000	Fast Expression	1	1	5	Market	On	Off	Verify	Off
graph26.png
基本面分析

基本面分析是通过检查相关的经济和财务因素来衡量证券的内在价值的一种方法。基本面分析师研究任何可能影响证券价值的因素，从宏观经济因素，如经济状况和行业条件，到微观经济因素，如公司管理的有效性。

分析师可以将公司的增长率与其所在的行业和部门进行比较，以及提供的其他信息，以确定该公司是否被正确地估值[7].

存货周转率

财务比率是基本面数据的比率，可以深入了解公司的健康状况和投资决策。一种常见的财务比率是存货周转率。它是一种活动比率，用于衡量公司销售和替换存货的速度。计算公式为:

销售额除以平均存货.

通常，较高的存货水平与更高的存储成本、保险费用和损耗有关。假设是具有较高存货周转率的股票将具有较差的股票表现，因此将被分配负权重。

其Alpha表达式如下:

1
inventory_turnover
Simulation Settings
Region	Universe	Language	Decay	Delay	Truncation	Neutralization	Pasteurization	NaN Handling	Unit Handling	Max Trade
USA	TOP3000	Fast Expression	3	1	5	Market	On	Off	Verify	Off
invemtory_turnuverupdated.png
时间序列和横截面

此外，还有两种经常使用的运算符类别：时间序列和横截面。

时间序列分析可以用于观察给定变量随时间的变化情况。假设您想分析一家给定股票在一年期间的每日收盘价格时间序列。您可以获取过去一年内该股票每天的所有收盘价格列表，并使用技术分析工具分析时间序列数据，以确定该股票的时间序列是否显示任何季节性。这将帮助您确定该股票是否每年定期经历峰值和谷值[8].

或者，您可以使用横截面分析，将特定公司与其同行业竞争对手进行比较。横截面分析可以针对单个公司进行头对头分析，也可以从行业整体的视角来考虑，以确定具有特定优势的公司。基本上，横截面分析可以向投资者展示，基于您所关心的指标，哪家公司是最好的[9].

希望您喜欢本指南！要开始使用，请单击Simulate页面左下角的示例按钮。在那里，您将找到一些示例Alpha策略，并得到改进提示。

如果您有任何研究相关的问题，可以访问我们的社区论坛并在那里发布您的问题。

进一步阅读和参考资料:

[6] Technical analysis: What it is and how to use it in investing. (2003, November 24). Investopedia. https://www.investopedia.com/terms/t/technicalanalysis.asp

[7] Fundamental analysis: Principles, types, and how to use it. (2003, November 23). Investopedia. https://www.investopedia.com/terms/f/fundamentalanalysis.asp

[8] Time series definition. (2006, March 12). Investopedia. https://www.investopedia.com/terms/t/timeseries.asp

[9] What is cross sectional analysis and how does it work? (2007, May 21). Investopedia. https://www.investopedia.com/terms/c/cross_sectional_analysis.asp

