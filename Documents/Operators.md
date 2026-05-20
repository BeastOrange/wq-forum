Unlock more complex operators at Expert, Master and Grandmaster Genius levels.
Arithmetic
abs(x)
base
Combo, Regular, Selection
Absolute value of x
add(x, y, filter = false), x + y
base
Combo, Regular, Selection
Add all inputs (at least 2 inputs required). If filter = true, filter all input NaN to 0 before adding
densify(x)
base
Combo, Regular
Converts a grouping field of many buckets into lesser number of only available buckets so as to make working with grouping fields computationally efficient
Show more
divide(x, y), x / y
base
Combo, Regular, Selection
x / y
inverse(x)
base
Combo, Regular, Selection
1 / x
log(x)
base
Combo, Regular, Selection
Natural logarithm. For example: Log(high/low) uses natural logarithm of high/low ratio as stock weights.
max(x, y, ..)
base
Combo, Regular, Selection
Maximum value of all inputs. At least 2 inputs are required
Show more
min(x, y ..)
base
Combo, Regular, Selection
Minimum value of all inputs. At least 2 inputs are required
Show more
multiply(x ,y, ... , filter=false), x * y
base
Combo, Regular, Selection
Multiply all inputs. At least 2 inputs are required. Filter sets the NaN values to 1
Show more
power(x, y)
base
Combo, Regular, Selection
x ^ y
Show more
reverse(x)
base
Combo, Regular, Selection
 - x
sigmoid(x)
genius
Combo, Regular, Selection
Returns 1 / (1 + exp(-x))
sign(x)
base
Combo, Regular, Selection
if input > 0, return 1; if input < 0, return -1; if input = 0, return 0; if input = NaN, return NaN; Input: Value of 7 instruments at day t: (2, -3, 5, 6, 3, NaN, -10) Output: (1, -1, 1, 1, 1, NaN, -1)
signed_power(x, y)
base
Combo, Regular, Selection
x raised to the power of y such that final result preserves sign of x
Show more
sqrt(x)
base
Combo, Regular, Selection
Square root of x
subtract(x, y, filter=false), x - y
base
Combo, Regular, Selection
x-y. If filter = true, filter all input NaN to 0 before subtracting
tanh(x)
genius
Combo, Regular, Selection
Hyperbolic tangent of x
Show more
Logical
and(input1, input2)
base
Combo, Regular, Selection
Logical AND operator, returns true if both operands are true and returns false otherwise
if_else(input1, input2, input 3)
base
Combo, Regular, Selection
If input1 is true then return input2 else return input3.
Show more
input1 < input2
base
Combo, Regular, Selection
If input1 < input2 return true, else return false
input1 <= input2
base
Combo, Regular, Selection
Returns true if input1 <= input2, return false otherwise
input1 == input2
base
Combo, Regular, Selection
Returns true if both inputs are same and returns false otherwise
input1 > input2
base
Combo, Regular, Selection
Logic comparison operators to compares two inputs
input1 >= input2
base
Combo, Regular, Selection
Returns true if input1 >= input2, return false otherwise
input1!= input2
base
Combo, Regular, Selection
Returns true if both inputs are NOT the same and returns false otherwise
is_nan(input)
base
Combo, Regular, Selection
If (input == NaN) return 1 else return 0
Show more
not(x)
base
Combo, Regular, Selection
Returns the logical negation of x. If x is true (1), it returns false (0), and if input is false (0), it returns true (1).
or(input1, input2)
base
Combo, Regular, Selection
Logical OR operator returns true if either or both inputs are true and returns false otherwise
Time Series
days_from_last_change(x)
base
Combo, Regular
Amount of days since last change of x Input: Value of 1 instrument in past 7 days where first element is the latest: (2, 2, 2, 7, 5, 16, 1) Output: 3
hump(x, hump = 0.01)
base
Combo, Regular
Limits amount and magnitude of changes in input (thus reducing turnover)
Show more
kth_element(x, d, k)
base
Combo, Regular
Returns K-th valid value of input by looking through lookback days. This operator can be used to backfill missing data if k=1
Show more
last_diff_value(x, d)
base
Combo, Regular
Returns last x value not equal to current x value from last d days
ts_arg_max(x, d)
base
Combo, Regular
Returns the relative index of the max value in the time series for the past d days. If the current day has the max value for the past d days, it returns 0. If previous day has the max value for the past d days, it returns 1
Show more
ts_arg_min(x, d)
base
Combo, Regular
Returns the relative index of the min value in the time series for the past d days; If the current day has the min value for the past d days, it returns 0; If previous day has the min value for the past d days, it returns 1.
Show more
ts_av_diff(x, d)
base
Combo, Regular
Returns x - tsmean(x, d), but deals with NaNs carefully. That is NaNs are ignored during mean computation
Show more
ts_backfill(x, d)
base
Combo, Regular
Returns the first valid value of the input x by looking through lookback days (d). This operator can be used to backfill missing data.
Show more
ts_corr(x, y, d)
base
Combo, Regular
Returns correlation of x and y for the past d days
Show more
ts_count_nans(x ,d)
base
Combo, Regular
Returns the number of NaN values in x for the past d days Input: Value of 1 instrument in past 4 days where first element is the latest: (100, NaN, NaN, 200), d: 4 Output: Number of NaN in 4 days = 2
ts_covariance(y, x, d)
base
Combo, Regular
Returns covariance of y and x for the past d days
ts_decay_linear(x, d, dense = false)
base
Combo, Regular
Returns the linear decay on x for the past d days. Dense parameter=false means operator works in sparse mode and we treat NaN as 0. In dense mode we do not.
Show more
ts_delay(x, d)
base
Combo, Regular
Returns x value d days ago Input: Value of 1 instrument in past 7 days where first element is the latest: (2, 3, 5, 6, 3, 8, 10), d: 6 Output: Value 6 days ago = 10
ts_delta(x, d)
base
Combo, Regular
Returns x - ts_delay(x, d) Input: Value of 1 instrument in past 7 days where first element is the latest: (2, 3, 5, 6, 3, 8, 10), d: 6 Output: Value today – value 6 days ago = 2 - 10 = -8
ts_entropy(x,d)
genius
Combo, Regular
For each instrument, we collect values of input in the past d days and calculate the probability distribution then the information entropy via a histogram as a result
Show more
ts_mean(x, d)
base
Combo, Regular
Returns average value of x for the past d days.
ts_min_diff(x, d)
genius
Combo, Regular
Returns x - ts_min(x, d)
ts_min_max_cps(x, d, f = 2)
genius
Combo, Regular
Returns (ts_min(x, d) + ts_max(x, d)) - f * x. If not specified, by default f = 2
ts_min_max_diff(x, d, f = 0.5)
genius
Combo, Regular
Returns x - f * (ts_min(x, d) + ts_max(x, d)). If not specified, by default f = 0.5
ts_product(x, d)
base
Combo, Regular
Returns product of x for the past d days
Show more
ts_quantile(x,d, driver="gaussian" )
base
Combo, Regular
It calculates ts_rank and apply to its value an inverse cumulative density function from driver distribution. Possible values of driver (optional ) are "gaussian", "uniform", "cauchy" distribution where "gaussian" is the default. Input: Value of 1 instrument in past 7 days where first element is the latest: (8, 10, 4, 6, 5, 3, 2), d: 7, driver: ’gaussian’ Output: quantile = 0.82 from SD = 2.82, mean = 5.43, zscore = 0.911
ts_rank(x, d, constant = 0)
base
Combo, Regular
Rank the values of x for each instrument over the past d days, then return the rank of the current value + constant. If not specified, by default, constant = 0. Input: Value of 1 instrument in past 3 days where first element is the latest: (100, 0, 200), d: 3 Output: 0.5
ts_regression(y, x, d, lag = 0, rettype = 0)
base
Combo, Regular
Returns various parameters related to regression function
Show more
ts_scale(x, d, constant = 0)
base
Combo, Regular
Returns (x - ts_min(x, d)) / (ts_max(x, d) - ts_min(x, d)) + constant. This operator is similar to scale down operator but acts in time series space
Show more
ts_skewness(x, d)
genius
Combo, Regular
Return skewness of x for the past d days
Show more
ts_std_dev(x, d)
base
Combo, Regular
Returns standard deviation of x for the past d days
ts_step(1)
base
Combo, Regular
Returns days' counter
ts_sum(x, d)
base
Combo, Regular
Sum values of x for the past d days.
ts_target_tvr_decay(x, lambda_min=0, lambda_max=1, target_tvr=0.1)
genius
Combo, Regular
Tune "ts_decay" to have a turnover equal to a certain target, with optimization weight range between lambda_min, lambda_max
ts_zscore(x, d)
base
Combo, Regular
Z-score is a numerical measurement that describes a value's relationship to the mean of a group of values. Z-score is measured in terms of standard deviations from the mean: (x - tsmean(x,d)) / tsstddev(x,d). This operator may help reduce outliers and drawdown. Input: Value of 1 instrument in past 5 days where first element is the latest: (100, 0, 50, 60, 25), d: 5 Output: (100-47)/33.7 = 1.57 from SD: 33.7, mean = 47
Cross Sectional
normalize(x, useStd = false, limit = 0.0)
base
Combo, Regular
Calculates the mean value of all valid alpha values for a certain date, then subtracts that mean from each element
Show more
quantile(x, driver = gaussian, sigma = 1.0)
base
Combo, Regular
Rank the raw vector, shift the ranked Alpha vector, apply distribution (gaussian, cauchy, uniform). If driver is uniform, it simply subtract each Alpha value with the mean of all Alpha values in the Alpha vector
Show more
rank(x, rate=2)
base
Combo, Regular
Ranks the input among all the instruments and returns an equally distributed number between 0.0 and 1.0. For precise sort, use the rate as 0
Show more
regression_proj(y, x)
genius
Combo, Regular
Conducts the cross-sectional regression on the stocks with Y as target and X as the independent variable
Show more
scale(x, scale=1, longscale=1, shortscale=1)
base
Combo, Regular
Scales input to booksize. We can also scale the long positions and short positions to separate scales by mentioning additional parameters to the operator
Show more
vector_proj(x, y)
genius
Combo, Regular
Returns vector projection of x onto y.
winsorize(x, std=4)
base
Combo, Regular
Winsorizes x to make sure that all values in x are between the lower and upper limits, which are specified as multiple of std. Input: Value of 7 instruments at day t: (2, 4, 5, 6, 3, 8, 10), std: 1 Output: (2.81, 4, 5, 6, 3, 8, 8.03) from SD. = 2.61, mean = 5.42
zscore(x)
base
Combo, Regular
Z-score is a numerical measurement that describes a value's relationship to the mean of a group of values. Z-score is measured in terms of standard deviations from the mean
Show more
Vector
vec_avg(x)
base
Combo, Regular
Taking mean of the vector field x Input: Vector of value of 1 instrument in a day: (2, 3, 5, 6, 3, 8, 10) Output: 37 / 7 = 5.29
vec_sum(x)
base
Combo, Regular
Sum of vector field x Input: Vector of value of 1 instrument in a day: (2, 3, 5, 6, 3, 8, 10) Output: 2 + 3 + 5 + 6 + 3 + 8 + 10 = 37
Transformational
bucket(rank(x), range="0, 1, 0.1" or buckets = "2,5,6,7,10")
base
Combo, Regular
Convert float values into indexes for user-specified buckets. Bucket is useful for creating group values, which can be passed to GROUP as input
Show more
generate_stats(alpha)
base
Combo
The generate_stats() operator calculates Alpha statistics for each day in the IS period. It takes an input of selected Alphas with shape = (A x D x I). It outputs daily statistics for each Alpha with shape = (S x D x A), where S is the number of statistics calculated.
trade_when(x, y, z)
base
Combo, Regular
Used in order to change Alpha values only under a specified condition and to hold Alpha values in other cases. It also allows to close Alpha positions (assign NaN values) under a specified condition
Show more
Group
combo_a(alpha, nlength = 250, mode = 'algo1')
base
Combo
Combines multiple alpha signals into a single weighted output by balancing each alpha's historical return with its variability over the most recent nlength days. The parameter mode selects one of the several weighted approaches (algo1, algo2, algo3), each of which handles the tradeoff between performance and stability differently.
group_backfill(x, group, d, std = 4.0)
base
Combo, Regular
If a certain value for a certain date and instrument is NaN, from the set of same group instruments, calculate winsorized mean of all non-NaN values over last d days
Show more
group_cartesian_product(g1, g2)
genius
Combo, Regular
Merge two groups into one group. If originally there are len_1 and len_2 group indices in g1 and g2, there will be len_1 * len_2 indices in the new group.
group_extra(x, weight, group)
genius
Combo, Regular
Replaces NaN values by their corresponding group means.
group_mean(x, weight, group)
base
Combo, Regular
All elements in group equals to the mean
Show more
group_neutralize(x, group)
base
Combo, Regular
Neutralizes Alpha against groups. These groups can be subindustry, industry, sector, country or a constant
Show more
group_rank(x, group)
base
Combo, Regular
Each elements in a group is assigned the corresponding rank in this group
Show more
group_scale(x, group)
base
Combo, Regular
Normalizes the values in a group to be between 0 and 1. (x - groupmin) / (groupmax - groupmin)
group_zscore(x, group)
base
Combo, Regular
Calculates group Z-score - numerical measurement that describes a value's relationship to the mean of a group of values. Z-score is measured in terms of standard deviations from the mean. zscore = (data - mean) / stddev of x for each instrument within its group. Input: Value of 5 instruments of Group A: (100, 0, 50, 60, 25) Output: (1.57, -1.39, 0.09, 0.39, -0.65)
Special
in
base
Selection
in
inst_pnl(x)
genius
Combo, Regular
Generate pnl per instruments. Please note that the use of the inst_pnl() operator in an Alpha Expression is considered as utilizing the pv1 dataset (Price Volume Data for Equity) since it relies on pv1 data for calculations.
self_corr(input)
base
Combo
Taking an input matrix of (D x N) with lookback="K", producing an output matrix of (D x N x N), where each output(di, j, k) refers to correlation of input(di-K:di, j) and input(di-K:di, k). Outputs (D x N x N) from the input of (D x N)
universe_size
base
Selection
universe_size
Reduce
reduce_avg(input, threshold=0)
base
Combo
Average of non-NAN elements of d(..., :). Threshold: Minimum required number of valid (non-nan) values. If there is not enough valid values, then the output is nan. 0 means no limit.threshold (Default: 0) *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)).
reduce_choose(input, nth, ignoreNan=true)
base
Combo
Choose the 'nth' element in the array, return NAN if not found. Threshold: nth="" (Required) ignoreNan="true|false" (Default: true) *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)).
reduce_count(input, threshold)
base
Combo
Count the number of element of d(..., :) > threshold. threshold= *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)).
reduce_ir(input)
base
Combo
IR of values in the array *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)).
reduce_kurtosis(input)
base
Combo
Kurtosis of values in the array ***Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. If input matrix is (D x N), output matrix (D x 1) If input matrix is (D x N X N), output matrix (D x N X 1) The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)).
reduce_max(input)
base
Combo
Maximum of elements of d(..., :) *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)).
reduce_min(input)
base
Combo
Minimum of elements of d(..., :) ***Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. If input matrix is (D x N), output matrix (D x 1) If input matrix is (D x N X N), output matrix (D x N X 1) The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)).
reduce_norm(input)
base
Combo
Absolute sum of number of element of d(..., :) *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)).
reduce_percentage(input, percentage=0.5)
base
Combo
Return the value of percentage in the sorted array: e.g., median value when percentage=0.5. Threshold: percentage="" (Default: 0.5) *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)).
reduce_powersum(input, constant=2, precise=false)
base
Combo
Sum of power, sum(power(x, constant)). Threshold: precise, whether calculate power precise if constant greater than 4, default false constant=, default:2 *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)).
reduce_range(input)
base
Combo
Return the range of values in the array, return NAN if no valid value *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)).
reduce_skewness(input)
base
Combo
Skewness of values in the array *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)).
reduce_stddev(input, threshold=0)
base
Combo
Standard deviation of values in the array. Threshold: Minimum required percentage of valid (non-nan) values. If there is not enough valid values, then the output is NAN. 0 means no limit.threshold (Default: 0) *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)).
reduce_sum(input)
base
Combo
Sum the number of element of d(..., :) *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)).