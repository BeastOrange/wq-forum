Data Fundamentals  
Data Field  
A named collection of data, which has constant type and business meaning. For example, 'open price' is of constant type (numeric), and it consistently means the price of a security at the starting time of the trading period. 'Close price' has the same type as 'open price', but it’s a different field as it differs in business meaning.  

A Dataset is a collection of Data Fields. Dataset can be identified by its name (text format, longer and explanatory) or its dataset ID (short alphanumeric format, only relevant for advanced scripting).  

Matrix  
Basic type of field which has just one value of every date and instrument. There is no special syntax for using this in simulation. Some examples of matrix fields are close, returns, cap.  

Vector  
Type of field which has more than one value for every date and instrument. Vector data fields have to be converted into matrix data fields using vector operators before using with other operators and matrix data fields. Otherwise, an error message will be returned.  

You can learn more about it here: Vector data fields  

vector desc.png
Dataset  
A source of information on one or more variables of interest for the WorldQuant investment process. A collection of data fields. For example: “price volume data for US equities” or “analyst target price predictions for US equities". See Datasets.  

Tips on working with new data  
WorldQuant BRAIN has thousands of data fields for you to create Alphas. But how do you quickly understand a new data field? Here are 6 ways. Simulate the below expressions in “None” neutralization and decay 0 setting. And obtains insights of specific parameters using the Long Count and Short Count in the IS Summary section of the results.  

  
  
  
1
datafield  
% coverage, would approximately be ratio of (Long Count + Short Count in the IS Summary )/ (Universe Size in the settings)  
2
datafield != 0 ? 1 : 0  
Coverage. Long Count indicates average non-zero values on a daily basis  
3
ts_std_dev(datafield,N) != 0 ? 1 : 0  
Frequency of unique data (daily, weekly, monthly etc.). Some datasets have data backfilled for missing values, while some do not. The given expression can be used to find the frequency of unique data field updates by varying N (no. of days). Data fields with a quarterly unique data frequency tend to see a Long Count + Short Count value close to its actual coverage when N = 66 (quarter). When N = 22 (month) Long Count + Short Count tend to be lower (approx. 1/3rd of coverage) and when N = 5 (week), Long Count + Short Count tend to be even lower.  
4
abs(datafield) > X  
Bounds of the data field. Vary the values of X and see the Long Count. For example, X=1 will indicate if the field is normalized to values between -1 and +1?  
5
ts_median(datafield, 1000) > X  
Median of the data field over 5 years. Vary the values of X and see the Long Count. Similar process can be applied to check the mean of the data field.  
6
X < scale_down(datafield) && scale_down(datafield) < Y  
Distribution of the data field. scale_down acts as a MinMaxScaler that can preserve the original distribution of the data. X and Y are values that vary between 0 and 1 that allow us to check how the data field distribute across its range.  
For example, if you simulate [close <= 0], You will see Long and Short Counts as 0. This implies that closing price always has a positive value (as expected!)  

Dataset Value Score (available for Consultants only)  
Dataset Value Score is a measure which signifies underutilization of a dataset. Consultants are advised to research and make Alphas using datasets with a higher value score. Don't confuse this with Value Factor.  

Data Coverage  
Coverage refers to the fraction of the total instruments present in the universe for which the given data field has a defined value. Low coverage fields can be handled by making use of backfill operators like ts_backfill, kth element, group_backfill, etc. Make use of the visualization feature to analyze the coverage of the data fields. Read this BRAIN Forum Post to know more about coverage handling.  

Further Resources  
Building Technical Indicators with Data Fields  
Finite Differences  
Statistics in Alpha Research  
