Combo Expression
Combo_expression_pic4.png
The combo expression combines the selected Alphas together into one Alpha – a SuperAlpha. The output of the combo expression is a set of daily weights for each of the selected Alphas.

How it Works
The combo expression works by weighting each selected Alpha each day. Similar to how an Alpha expression is evaluated for each instrument each day, the combo expression is evaluated for each of your Alphas each day.

Typically, combo expressions take the set of selected Alphas as input. The data from the selected Alphas is held in a matrix with shape = (A x D x I), where:

A is the number of selected Alphas
D is the number of days
I is the number of instruments in the universe
The output of the combo expression is a set of weights for each selected Alpha each day, held in a matrix with shape = (D x A). These weights determine how the scaled output of each Alpha is combined together to yield a SuperAlpha.


Operator generate_stats()
generate_stats_operator_pic6.png
The generate_stats() operator calculates Alpha statistics for each day in the IS period. It takes an input of selected Alphas with shape = (A x D x I). It outputs daily statistics for each Alpha with shape = (S x D x A), where S is the number of statistics calculated.

generate_stats_
Alpha Statistics

The generate_stats() operator calculates the following daily statistics for each Alpha:

drawdown
% difference between current cumulative PnL and maximum PnL since beginning of simulation
hold_pnl
PnL of shares that did not trade
hold_shares
Count of shares that did not trade
hold_value
Sum of value of shares that did not trade
long_count
Number of instruments with positive weight
long_value
Sum of positive weight
pnl
Net profit or loss
returns
PnL as percent of book size
short_count
Number of instruments with negative weight
short_value
Sum of absolute value of negative weight
trade_pnl
PnL of shares that did trade
trade_shares
Count of shares that did trade
trade_value
Sum of value of shares that did trade
turnover
Value traded as percent of book size
Available operators
Combo expressions can use most of the same operators as Alpha expressions. A full list of available operators is available at Appendix: SuperAlpha Operators.

SuperAlpha Combo Settings
Superalpha_combo_settings_pic7.png
The lower section of the SuperAlpha settings menu applies to the combo expression and the resulting SuperAlpha.

Universe

The selected universe setting is applied to all selected Alphas when the SuperAlpha is simulated, regardless of the original universe of those Alphas. The resulting SuperAlpha is based upon this universe.

Neutralization

The selected neutralization is applied to the final weighted combination of selected Alphas.

Decay

The decay setting applies the ts_decay() operator to the final weighted combination of selected Alphas, where the decay value is the number of lookback days. This is useful for reducing turnover, but larger values can attenuate the signal.

Truncation

The selected truncation is applied to the final weighted combination of selected Alphas. This is useful to reducing overfitting.

Pasteurization

Replaces operator input values with NaN for instruments not in the universe. Original Alpha pasteurization settings are preserved. The combo pasteurization setting applies to operators used in the combo expression.

NaN Handling

Allows aggregation operators to output numeric values when input values are NaN for a given instrument and date. Original Alpha NaN Handling settings are preserved. The combo NaN Handling setting applies to operators used in the combo expression.

Test Period

The Test Period setting offers you the flexibility to designate a separate testing period for your SuperAlpha. This period corresponds to the final 0-6 years of the In-Sample (IS) period, providing a distinct timeframe for assessing your SuperAlpha's performance before submission.

Examples
1
This expression evaluates to 1 for every Alpha every day. It will weight each selected Alpha equally every day.
stats = generate_stats(alpha); ts_ir(stats.returns, 250)
This expression weights each Alpha by its information ratio from the previous 250 trading days (~1 year).
stats = generate_stats(alpha); innerCorr = self_corr(stats.returns, 500); ic = if_else(innerCorr == 1.0, nan, innerCorr); maxCorr = reduce_max(ic); 1 - maxCorr
This expression weights each Alpha by the maximum correlation with all other selected Alphas over a 2 year period, with more correlated Alphas receiving less weight.
