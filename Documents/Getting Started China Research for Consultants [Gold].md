从哪里开始：尽管中国的股市具有几个独特的特征，但在您探索具体的研究想法之前，许多常见的研究想法都可以成为您开始中国研究的好起点:
技术指标（随机震荡指标、相对强弱指数、移动平均线散度等）
基本面财务指标
中国市场的交易成本很高，因此需要比其他地区更高的回报。因此，D1提交条件为Sharpe >= 1.625，Returns >= 6.3%和Fitness >= 1.0；D0提交条件为Sharpe >= 2.6，Returns >= 8.9%和Fitness >= 1.3
除了通常的鲁棒性测试（如子宇宙、换手率、适应性和权重）外，还有一个专属于中国研究区域的额外测试：鲁棒股票池测试表现：如果鲁棒宇宙组件保留了至少40%提交版本的回报和的Sharpe，则认为Alphas是好的.
由于中国市场具有涨跌停限制（即，深圳证券交易所和上海证券交易所于1996年12月26日恢复了10%的对称价格限制系统[1]），您将观察到相反的alpha不会镜像翻转alpha的PnL（即，Sharpe、Returns、Fitness）。

请参阅以下示例：

Alpha = ts_returns(close,5)，其中Delay =“1”，Neutralization =“industry”，Decay =“0”，Truncation =“0.01”，Universe =“TOP3000”的表现如下：

Sharpe = -6.10，Turnover = 63.34％，Returns = -72.73％，Margin = -229.10

然而，相反的alpha：

Alpha = -ts_returns(close,5)，其中Delay =“1”，Neutralization =“industry”，Decay =“0”，Truncation =“0.01”，Universe =“TOP3000”的表现如下：

Sharpe = 1.86，Turnover = 62.69％，Returns = 22.99％，Margin = 73.30

[1]: The impact of price limit system on the comprehensive quality of the stock market: Research on long-term and short-term effects based on submarkets