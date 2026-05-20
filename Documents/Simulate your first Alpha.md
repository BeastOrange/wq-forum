Alpha可以在“Alphas”下拉菜单中的“Simulate”页面上创建和回测。要运行第一个回测，请单击右上角的齿轮图标。这将打开设置面板。在这里，选择“US: TOP3000”作为地区和股票池，“Subindustry”作为中性化选项，并应用您的设置。确保通过单击它们来勾选Code和Result。在Alpha表达式文本框中，现在输入-Delta(close, 5)，然后单击“回测”。回测结果页面将显示累积净值的图表。此图表可以缩放以绘制较短时间段（1个月或1年）的区间。

first_alpha
显示结果包括2个图表，一个用于PnL vs. 时间，另一个用于Sharpe Ratio vs. 时间。

在统计选项卡中，一个好的Alpha应该具有持续增长的PnL和高的年度回报率、夏普比率、盈利日百分比和交易每美元利润。它应该具有低的回撤和换手率。更重要的是，它不应该在累积利润图表中有高波动性。如果标准偏差较低，图表中的波动性将较小。如果图表显示高波动性/波动，尽管年化回报率高，Alpha仍将不被视为足够好。

Alpha被认为是“好”的条件是：
• 其换手率低，但不低于1％
• 其百分比回撤小于10％
• 其delay 0 Alpha的Sharpe大于2.0，delay1 Alpha的Sharpe大于1.25

上面的Alpha表达式-Delta(close, 5)显示了几个显著的回撤，以及2017年回报的不足。下面的表格将此Alpha标记为劣质（需要改进）。2017年的PnL和Sharpe下降，2014年和2015年的回撤很大。由于波动性高且回报低，此Alpha质量不高（需要改进）。

1
-delta(close, 5)
Simulation Settings
Region	Universe	Language	Decay	Delay	Truncation	Neutralization	Pasteurization	NaN Handling	Unit Handling	Max Trade
USA	TOP3000	Fast Expression	2	1	0	Market	On	Off	Verify	Off
stats
在相关性模块中使用绿色刷新按钮，以获取当前回测Alpha与自己的样本外（Out-of-Sample）池中的Alpha之间的相关性信息。这将在回测结果页面中进一步解释。


下面的图像显示了Alpha的属性。您可以为Alpha命名，分配类别和颜色代码，并为其添加用户定义的标签。您可以为您的Alpha添加简要说明以供参考。建议-将用户定义的标签数量保持较少，以便它们不会堆积，并在“我的Alphas”页面中易于搜索。

properties
要将Alpha提交进行OS测试，请单击结果面板的提交选项卡中的“提交Alpha”按钮。这将在提交之前检查Alpha是否符合相关性和Sharpe标准。