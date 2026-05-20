News-driven Volatility
Hypothesis:

Stocks of companies that face high differences in their prices after any news release can be subject to varying sentiments that can lead to volatile behaviour. You can try avoiding periods of extreme volatility due to recent news releases

Implementation :

Using 'news_session_range' news datafield, employ 'ts_backfill' operator to support data coverage. Additionally, 'ts_arg_max' operator identifies the number of days from today in the past quarter when the maximum value was achieved. The lower the number of days, the lower the stock weight in the Alpha vector

Hint to improve the Alpha

The recent news event only be relevant for a limited time, can using an operator which changes Alpha weights quickly for values closer to zero rather than distant values help improve Alpha performance? Also can using trade_when operator help reduce the turnover?

1
(ts_arg_max(ts_backfill(news_session_range, 20), 60))
Simulation Settings
Region	Universe	Language	Decay	Delay	Truncation	Neutralization	Pasteurization	NaN Handling	Unit Handling	Max Trade
USA	TOP3000	Fast Expression	0	1	0.08	Sector	On	Off	Verify	Off
Implied Volatility Spread as a predictor
Hypothesis:

If the Call Open interest is higher than the Put Open interest, the stock may rise based on the intensity of the implied volatility spread or vice versa.

Implementation :

Use 'trade_when' operator, with condition on the call-put open interest ratio. If it is less than unity, go long on stock based on intensity of the (Implied Volatility) IV spread, using option data.

Hint to improve the Alpha

Can using custom neutralization on the Alpha based on self-created groups (like historical volatility) help improve sub-universe performance? Use floor or bucket operator combined with rank operator to implement custom neutralization

1
trade_when(pcr_oi_270 < 1, (implied_volatility_call_270-implied_volatility_put_270), -1)
Simulation Settings
Region	Universe	Language	Decay	Delay	Truncation	Neutralization	Pasteurization	NaN Handling	Unit Handling	Max Trade
USA	TOP3000	Fast Expression	4	1	0.08	Market	On	Off	Verify	Off
