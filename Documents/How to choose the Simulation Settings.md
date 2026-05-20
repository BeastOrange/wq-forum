设置面板可以在回测页面右上角的“设置”按钮中找到。您可以指定参数，如语言、工具类型、股票池、延迟、中性化等，这些参数将在单击“应用”按钮后应用于您的下一次回测.

语言
BRAIN 平台支持快速表达式。要了解更多信息，请参阅“可用运算符”

工具类型
目前只能使用权益工具(equity)

区域和股票池
目前所有 BRAIN 平台用户都可以使用的区域是美国和中国市场。欧洲和亚洲地区等区域目前仅适用于我们的研究顾问.

股票池是由 BRAIN 平台准备的交易工具集。例如，“美国：TOP3000”表示美国市场上最流通的前 3000 只股票（根据最高日均交易额确定）.

延迟Delay
延迟指数据可用性相对于决策时间的时间差。换句话说，延迟（Delay）是指一旦我们决定持仓，我们可以交易股票的时间假设。

假设您在今天的交易结束前看到数据，决定要买入股票。我们可以选择积极的交易策略，在剩余时间内交易股票。在这种情况下，持仓基于当天可用的数据（今天）。这称为“延迟 0 回测”。

或者，我们可以选择一种保守的交易策略，并在第二天（明天）交易股票。然后，持仓是在明天实现的，基于今天的数据。在这种情况下，有一个 1 天的滞后。这称为“延迟 1 回测”。在表达式语言中，延迟是自动应用的，您不必担心它。

衰减Decay
通过将今天的值与前 n 天的衰减值相结合，执行线性衰减函数。它执行以下函数:

 
允许输入的衰减值：整数“n”，其中 n >= 0。注意：使用负数或非整数值进行衰减将破坏回测。

提示：衰减可用于减少周转，但衰减值过大会削弱信号。

截断Truncation
整体组合中每只股票的最大权重。当它设置为 0 时，没有限制。

允许输入的截断值：0 <= x <= 1 的浮点数（注意：截断的任何值超出此范围都可能影响/破坏回测）。

提示：截断旨在防止过度暴露于个别股票的波动。推荐的设置值为 0.05 到 0.1（涵盖 5%-10%）。

中性化Neutralization
中性化是用于使我们的策略市场/行业/子行业中性的操作。当中性化 =“市场”时，它执行以下操作:

Alpha = Alpha – mean(Alpha)

其中 Alpha 是权重向量.

实际上，它使 Alpha 向量的平均值为零。因此，与市场相比没有净头寸。换句话说，多头暴露完全抵消了空头暴露，使我们的策略市场中性。

当中性化 = 行业或子行业时，Alpha 向量中的所有股票都分组到对应的行业或子行业中，并分别应用中性化。有关行业/子行业分类的说明，请参见 GICS （注意：这不一定是 BRAIN 平台使用的相同分类标准）。

要了解有关中性化的更多信息，请参阅Neutralization FAQ部分。

pic8.png
消毒Pasteurize
消毒将不在 Alpha 股票池中的输入值替换为 NaN。当 Pasteurize =“On” 时，将为未在回测设置中选择的股票池中的工具将输入转换为 NaN。当 Pasteurize =“Off” 时，不会发生此操作，并且将使用所有可用的输入.

消毒数据仅具有 Alpha 股票池中工具的非 NaN 值。虽然消毒数据包含的信息较少，但在考虑横向或组操作时可能更合适。默认的 Pasteurize 设置为“On”。研究人员可以将其切换为“Off”，并使用Pasteurize (x) 运算符进行手动消毒。

示例
假设使用以下设置：Universe TOP500，Pasteurize：“Off”。以下代码计算 Alpha 股票池中 sales_growth 所在行业排名与所有工具中 sales_growth 所在行业排名之间的差异

1
group_rank(pasteurize(sales_growth),sector) - group_rank(sales_growth,sector)
Simulation Settings
Region	Universe	Language	Decay	Delay	Truncation	Neutralization	Pasteurization	NaN Handling	Unit Handling	Max Trade
USA	TOP3000	Fast Expression	4	1	0.01	Market	On	Off	Verify	Off
第一组排名中的消毒运算符将输入消毒为 Alpha 股票池（TOP500）中的股票，而第二组等级排名将 sales_growth 在所有股票中进行排名.

NaN 处理
NaN 处理将 NaN 值替换为其他值。如果 NaNHandling：“On”，则根据运算符类型处理 NaN 值。对于时间序列运算符，如果所有输入都为 NaN，则返回 0。对于每组返回一个值的群组运算符（例如 group_median、group_count），如果一只股票的输入值为 NaN，则返回该组的值.

如果 NaNHandling：“Off”，则保留 NaN。对于时间序列运算符，如果所有输入都为 NaN，则返回 NaN。对于群组运算符，如果一只股票的输入值为 NaN，则返回 NaN。在这种情况下，研究人员应手动处理 NaN。默认设置 NaNHandling 值为“Off”。一些手动处理 NaN 值的方法可以复制 “On” 操作.

1
ts_zscore(etz_eps, 252)
Simulation Settings
Region	Universe	Language	Decay	Delay	Truncation	Neutralization	Pasteurization	NaN Handling	Unit Handling	Max Trade
USA	TOP3000	Fast Expression	4	1	0.01	Market	On	Off	Verify	Off
假设 NaNHandling = ‘On’，那么对于一个股票，其 etz_eps 在 252 天内都为 NaN，则 ts_zscore(x, d) 返回 0。然而，当 x == tsmean(x, d) 时，ts_zscore(x, d) 也返回 0，这与 x == NaN（“没有数据可用”）是不同的。这意味着 NaNHandling = ‘On’ 可以增加覆盖率，但可能会在 Alpha 中引入模糊的信息。

如果 NaNHandling = ‘Off’，NaN 可以通过其他方式处理：
is_nan(ts_zscore(etz_eps, 252)) ? ts_zscore(est_eps, 252) : ts_zscore(etz_eps, 252)

这里，当 etz_eps 在 252 天内都为 NaN 时，使用 est_eps。

Example示例

1
groupmax(sales, industry)
Simulation Settings
Region	Universe	Language	Decay	Delay	Truncation	Neutralization	Pasteurization	NaN Handling	Unit Handling	Max Trade
USA	TOP3000	Fast Expression	3	1	0.01	None	On	Off	Verify	Off
当给定股票的 sales 为 NaN 时，如果 NaNHandling = 'Off'，则运算符的输出为 NaN。如果 NaNHandling = 'On'，则运算符的输出为该股票所在行业中 sales 的最大值.

单位处理
单位处理选项允许在运算符中使用到不兼容的量纲时发出警告。如果表达式使用不兼容的数据字段，例如试图将价格加上成交量，则会显示警告.

