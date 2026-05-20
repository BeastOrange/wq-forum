Introductions
In this documentation, we will introduce a new Universe for Alpha on USA, EUR, ASI regions called ILLIQUID_MINVOL1M. It’s a unique universe consisting of illiquid equities, defined by our liquidity metrics: minimum volume of $1M.

The illiquid universe offers potential opportunities to capitalize on short term and long term price discrepancies due to its market inefficiency. However, it also implies higher trading costs, as short selling becomes more difficult and obtaining optimal order pricing is challenging due to slippage. For this reason, a new submission test for Alpha builds has been introduced in the ILLIQUID_MINVOL1M universe.

getting-started-illiquid-universes.png
New Submission test
Most Illiquid instruments after cost Sharpe test measures the proportion of after cost performance in an illiquid universe with reference to the original universe. This test ensures that the most illiquid half of the illiquid universe has a minimum required Sharpe after considering the various costs of trading these instruments