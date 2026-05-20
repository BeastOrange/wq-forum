Vector类型数据集是一种不固定大小的数据字段类型。在这种类型的数据字段中，每个金融工具每天记录的事件数量不同，因此它们通常存储在vector中。这与您处理的常规矩阵数据不同，后者每天每个金融工具只有一个值。例如：如果数据集涵盖新闻数据，它可能是一个vector，因为对于每个金融工具可能会发生不同数量的新闻/事件，因此在矩阵数据中涵盖此类信息将导致缺少有用的信息。例如，一个vector字段在一天内报告单个金融工具的多个新闻事件。

现在，每当您编写一个Alpha表达式时，最终结果都是一个Alpha值矩阵，这是我们在市场上所买入的头寸。而平台上的所有运算符都是针对矩阵输入的，因此在使用矩阵运算符之前，必须使用vec_运算符将向量数据字段转换为矩阵字段。这是通过将每天和每个金融工具的向量聚合成一个类似于矩阵的单个值来完成的。下图显示了相同的情况:

vector desc.png
以下是将向量数据字段转换为矩阵的不同运算符，每个运算符在聚合特定日期和金融工具的向量以形成单个值时略有不同:

vec_avg(x)
Taking mean of the vector field x
vec_choose(x,nth=k)
Choosing kth item(indexed at 0) from each vector field x
vec_count(x)
Number of elements in vector field x
vec_ir(x)
Information Ratio (Mean / Standard Deviation) of vector field x
vec_kurtosis(x)
Kurtosis of vector field x
vec_max(x)
Maximum value form vector field x
vec_min(x)
Minimum value form vector field x
vec_norm(x)
Sum of all absolute values of vector field x
vec_percentage(x,percentage=0.5)
Percentile of vector field x
vec_powersum(x,constant=2)
Sum of power of vector field x
vec_range(x)
Difference between maximum and minimum element in vector field x
vec_skewness(x)
Skewness of vector field x
vec_stddev(x)
Standard Deviation of vector field x
vec_sum(x)
Sum of vector field x
 

Some examples:

下面是一些示例:

1, nws12_afterhsz_1_minute是一个字段，它给出了新闻发布后第一分钟内的价格变化百分比。对于不同的金融工具，每天可能有许多新闻。因此，不同的金融工具的新闻计数可能不同。假设我们想应用反转/动量的想法，即一个普遍的观察是当股票具有高新闻强度时，它遵循动量，当股票具有低新闻强度时，它遵循反转，我们需要新闻计数数据。为此，我们需要在nws12_afterhsz_1_minute（或类似字段，如nws12_afterhsz_10_min或nws12_afterhsz_120_min）字段上使用vec_count函数。这将将价格的百分比变动的向量转换为这种情况的计数。您可以使用vec_count（nws12_afterhsz_120_min）来获取新闻计数。下面是vec_count的平均值和换手率的图。您可以看到原始换手率非常高，有时会达到200％。在将其与基础数据或其他字段组合以生成Alpha之前，有必要使用衰减Decay运算符将其换手率降低.




2, 仅限有权访问顾问数据集的研究顾问阅读：scl15_d1_sentiment是一个字段，它给出了一天内各种事件的情绪得分。由于我们每个金融工具只能采取一个头寸，因此作为输入，我们只需要一个情绪值。对于AAPL的某个日期，如果有5个情绪得分，我们只需使用所有这些得分的平均值，通常可以合理地代表该整天的情绪。因此，为将此情绪向量转换为矩阵字段，我们将使用vec_avg（scl15_d1_sentiment）。如果您认为中位数可能是更好的代表，则可以使用vec_median（scl15_d1_sentiment）代替。下面再次是vec_avg字段的平均值和换手率图。平均值密集地在15,000左右，换手率在130％左右。在此处，您也需要使用ts_rank或ts_decay降低换手率，以在Alpha表达式中使用它.



