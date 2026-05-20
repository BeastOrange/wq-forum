Selection expression
Selection_expression_pic1.png
The selection expression chooses which Alphas to include in your SuperAlpha. You can select from all of your submitted Alphas with 'ACTIVE' status. Alpha selection is binary – each Alpha is either selected or excluded.

How it Works
The selection expression works by ranking all of your Alphas and choosing the highest ranked Alphas, according to the SuperAlpha settings.

The syntax for the selection expression is designed to be similar to that of Alpha expressions, and uses many of the same operators. Similar to how an Alpha expression is evaluated for each instrument in a selected universe, the Selection expression is evaluated for each of your submitted Alphas. The value of the selection expression is called "selection weight", and your Alphas are ordered by this value with the largest values first. This order, combined with some SuperAlpha settings, is used to determine which Alphas are selected.

SuperAlpha Settings
Some SuperAlpha settings constrain the selection expression. These include Language, Instrument Type, Region, Delay, Selection Handling, and Selection Limit. You may only have one option for some of these settings. Only Alphas matching the Language, Instrument Type, Region, and Delay settings will be selected. Selection Handling and Selection Limit are discussed in more detail below.

Superalpha_settings_pic2.png
Selection Handling

The selection handling setting determines what types of selection weight values are included. The "Positive" setting means that only positive values are included. For example, an Alpha which evaluates to zero would be excluded from the ordered set of Alphas if selection handling is set to "Positive". The "Non-Zero" setting means that only non-zero values are included; zero and NaN values are excluded. The "Non-NaN" setting means that real numbers and +/- infinity are included; only NaN values are excluded. Using the "Positive" or "Non-Zero" settings makes it simpler to use equalities and inequalities to select Alphas. The "Non-NaN" setting allows for the greatest flexibility, but may be more difficult to use. Refer to the Example Selection Expressions below for the details.

Selection Limit

The selection limit setting determines the maximum number of Alphas to select. From the ordered set of Alphas, only the top n are selected, where n is the selection limit. The required min value for the selection limit is 10.

As a rule of thumb, the more Alphas, the better the performance, but it also means longer simulation times. So you can first start with a smaller number of Alphas to test an idea then scale the number of Alphas.

Booleans

Comparisons evaluate to either 1 or 0. In the selection expression, True is interpreted as 1, and False is interpreted as 0. If using the "Positive" or "Non-Zero" selection handling settings, False values will be excluded since 0.0 is not a positive or non-zero value. If using the "Non-NaN" selection handling setting, False values will not be excluded but may impact the order of your Alphas.

Operator Limit Constraint

A SuperAlpha is a combination of Alphas thus naturally it consumes more resources to maintain. Thus in order to handle the memory & resource constraint of the SuperAlpha we place a threshold on the number of operators which can be used inside the SuperAlpha. Current limit is 8000 operators. What this means is that let’s say you simulate a SuperAlpha with selection_limit=50, but the total number of operators these underlying Alphas use exceeds 8000. Then the SuperAlpha simulation will automatically truncate the number of Alphas to meet this limit. In the aforementioned example, the final simulation may only have 45 Alphas.

Operator limit constraint violation will not lead to simulation error but a warning will be displayed.

How should you avoid violating this constraint?

One simple way is to use less number of Alphas. Another more clean approach is to use operator_count field in your selection. This way you can control the number of operators.

Operator limit constraint violation will not lead to simulation error but a warning will be displayed:

1. A warning above the Selected Alphas list on the simulate page:

selection_limit_warning_pic14.png
2. A warning above the Selected Alphas on the Alphas page:

selection_limit_warning_pic15.png
3. A warning at the bottom of the code editor after the simulation is complete:

selection_limit_warning_pic16.png
4. A warning in the alphas IS Testing Status:

selection_limit_warning_pic17.png
Available Data Fields
These Alpha properties are available to use in selection expressions. Some Alphas may not have data for all of these properties.

Example:

Available_data_fields_pic3.png
Alpha Properties are listed in the Table:
category
User-selected category
String: "NONE", "PRICE_REVERSION", "PRICE_MOMENTUM", "VOLUME", "FUNDAMENTAL", "ANALYST", "PRICE_VOLUME", "RELATION", "SENTIMENT"
category == "NONE"
color
User-selected color
String: "NONE", "RED", "YELLOW", "GREEN", "BLUE", "PURPLE"
color == "GREEN"
dataset
Datasets used in Alpha
String: "fundamental6", "analyst4", “model26”
in(datasets, "fundamental6")
decay
Decay setting
Numeric
decay <= 2
favorite
Favorite status
1 or 0 (true or false)
not(favorite)
long_count
IS average count of long instruments
Numeric
long_count > 600
name
Custom, user-created Alpha name. Must be an exact match.
String
name == "good_alpha"
neutralization
Neutralization setting
String: "NONE", "MARKET", "SECTOR", "INDUSTRY", "SUBINDUSTRY"
neutralization == "MARKET"
operator_count
Number of operators in Alpha expression
Numeric
operator_count < 10
short_count
IS average count of short instruments
Numeric
short_count > 600
tags
Custom, user-created tags
String
in(tags, "my_example_tag")
truncation
Truncation setting
Numeric
truncation <= 0.06
turnover
IS turnover
Numeric
turnover < 0.30
universe
Universe setting
String: "TOP200", "TOP500", "TOP1000", "TOP2000", "TOP3000"
universe == "TOP1000"
universe_size(universe)
This is an operator that interprets the universe string as a numeric value
Numeric
universe_size(universe) >= 2000
datafields
Datafields used in Alpha
String: "returns", "assets", “debt”
in(datafields, "returns")
dataset_count
Number of unique datasets in an Alpha
Numeric
dataset_count == 1
self_correlation
Self Correlation of Alphas
Numeric
self_correlation <= 0.6
prod_correlation
Prod Correlation of Alphas
Numeric
prod_correlation < 0.5
os_start_date
Out-of-Sample date of Alphas
String: date in YYYY-MM-DD format
os_start_date > "2020-01-01"
datacategories
Data Categories used in the alpha
analyst, broker, earnings, fundamental, imbalance, insiders, institutions, macro, model, news, option, other, pv, risk, sentiment, shortinterest, socialmedia
not(in(datacategories, "fundamental"))
datacategory_count
number of unique data categories in an alpha
Numeric
datacategory_count<5
datafield_count
number of unique data fields in an alpha
Numeric
datafield_count <2
classifications
Alpha classification
"POWER_POOL", "ATOM"
in(classifications, "POWER_POOL")
competitions
Competition associated with the alpha
"HCAC2025", "ACE2023"
in(competitions, "HCAC2025")
Additional SuperAlpha selection features
Overall Alphas Yield Rate
author_yield_rate
number of submissions / number of simulations * 10,000
Numeric
author_yield_rate > 1000
Alphas Yield Rate per quarter
author_quarter_yield_rate
number of submissions / number of simulations * 10,000 for the proceeding 90 days
Numeric
author_quarter_yield_rate < 1
Age of author
author_tenure
number of days difference from submission date to conditional start date
Numeric
author_tenure > 600
Days Active
author_activity
number of distinct submission days / number of days difference from submission date to conditional start date
Numeric
author_activity > 0.7 && author_activity < 0.9
Regions Count
author_distinct_count_regions
number of distinct regions
Numeric
author_distinct_count_regions >= 3
Author Dataset Categories Count
author_distinct_count_datasetcategory
number of distinct dataset categories
Numeric
author_distinct_count_datasetcategory > 10
Author Dataset Count
author_distinct_count_dataset
number of distinct dataset
author_distinct_count_dataset < 3
Datafield Count
author_distinct_count_datafield
number of distinct datafield
Numeric
author_distinct_count_datafield > 5000
Operator Count
author_distinct_count_operator
number of distinct operator
Numeric
author_distinct_count_operator > 150
Dataset Categories Quarter Count
author_distinct_quarter_count_datasetcategory
number of distinct dataset categories for the proceeding 90 days
Numeric
author_distinct_quarter_count_datasetcategory <= 10
Dataset Quarter Count
author_distinct_ quarter_count_dataset
number of distinct dataset for the proceeding 90 days
Numeric
author_distinct_quarter_count_dataset > 20
Datafield Quarter Count
author_distinct_ quarter_count_datafield
number of distinct datafield for the proceeding 90 days
Numeric
author_distinct_quarter_count_datafield < 100
Operator Quarter Count
author_distinct_ quarter_count_operator
number of distinct ts operator for the proceeding 90 days
Numeric
author_distinct_quarter_count_operator <= 20
Author ProdCorr
author_prod_correlation
mean of prod correlation
Numeric
author_prod_correlation < 0.5
Author SelfCorr
author_self_correlation
mean of self correlation
Numeric
author_self_correlation <= 0.6
Author Sharpe
author_sharpe
mean of Sharpe
Numeric
author_sharpe >= 2 && author_sharpe <= 4
Author TurnOver
author_turnover
mean of turnover
Numeric
author_turnover >= 0.2 && author_turnover <= 0.4
Author Fitness
author_fitness
mean of fitness
Numeric
author_fitness < 2
Author Returns to Drawdown Ratio
author_returns_to_drawdown
mean of returns/drawdown ratio
Numeric
author_returns_to_drawdown > 1 && author_returns_to_drawdown < 4
Dataset names are listed in the Table:
analyst11
ESG scores
analyst14
Estimations of Key Fundamentals
analyst15
Earnings forecasts
analyst16
Real Time Estimates
analyst17
A-shares Estimates
analyst2
Analysts Estimates of Key Fundamentals
analyst20
Decision Machine Data
analyst21
Indicators of Interest Data
analyst25
Analyst Estimates Data for Equity
analyst27
Analyst Estimate Daily Data
analyst34
Dividend forecasts model
analyst35
ESG Model
analyst4
Analyst Estimate Data for Equity
analyst40
Information on board of director
analyst44
Broker Estimates
analyst6
Model Rating Data
analyst7
Broker Estimates
analyst8
Analyst Estimate Daily Data
analyst9
Analyst Estimate Daily Data
earnings1
Actuals and Estimates Earnings Data
earnings3
Earnings Date Data
earnings4
Effect of earnings announcement model
earnings5
Earnings Date Breaks
earnings7
Horizon Earnings and Calendar North America
fundamental1
Management and Executive Data
fundamental11
International Fundamental Data
fundamental12
Model Data
fundamental13
Comprehensive Fundamentals Dataset
fundamental14
Audit Analytics Directors Data
fundamental17
Direct Fundamental Data
fundamental2
Report Footnotes
fundamental21
ESG Scores Data
fundamental22
Environmental and Social Governance Data
fundamental23
Fundamental Point in Time Data
fundamental25
Company Operating Metrics
fundamental27
A-shares Fundamental Data
fundamental28
Global Fundamental Data
fundamental3
Fundamentals Data for US Equities
fundamental30
Japan fundamenta data by sectors
fundamental31
Additional Factor Model
fundamental44
Accounting Quality Models
fundamental45
Systematic mining of earnings calls data
fundamental5
China Fundamentals
fundamental6
Company Fundamental Data for Equity
fundamental65
Factor Ratios and its Rank Model
fundamental7
Comprehensive Fundamentals Data
insiders1
Global Insider Trading Data
institutions1
Insider Trading for Europe
institutions4
Institutional Ownership Data
institutions5
Insiders Model
institutions6
Institutions and Beneficial Stake Ownership
institutions7
Ownership Model
institutions8
Insider Model Data
macro27
Job records from job posting
macro38
Technical Ratings Model
model10
Research Indicators
model106
Analysts rating model
model109
Fundamentals and Technical Indicators Model
model11
Revenue Forecast Data
model110
Big data and machine learning based model
model113
ML/AI-Estimates for Research Indicators
model115
ML/AI-Estimates for Earnings Quality
model116
ML/AI-Estimates for Equity Factor Model
model117
NLP on 10K and 10Q Filings Data
model119
Factor Score Data
model12
Stock Selection Model
model122
Factors for A-shares
model133
Risk Parity Method Model
model135
Alternative technical factror models
model136
ETF Based Equity Factors
model139
Inflation based stock selection model
model14
Quant Model Data
model140
Sensitivity to the Inflation Change
model141
Interest Rate Sensitivity Measures
model15
AI Driven Predictive Model
model16
Fundamental Scores
model162
Return prediction from conference call
model163
ML/AI-Estimates for Analysts' Factor Model
model165
Time-series prediction of alpha models
model169
Technical and Fundamental ranking model
model17
Research Analyst Estimate Factors
model170
Technical and Fundamental ranking model
model175
China Fundamentals and Technicals Model
model176
Non-Financial Metric Models
model182
Geographic network based model
model194
North America CDS Factor Model
model2
Brand Popularity Data
model20
Fundamental & Technical Rank Model
model21
Equity Focus Rank Model
model210
NLP Model on Textual Data
model211
Analyst estimate prediction data
model22
Fundamental Focus Rank Model
model23
Scorings Data
model25
Earnings Quality
model26
Analyst Revisions
model27
Credit Risk Model
model28
Structural Credit Risk Model
model29
EBITDA Estimate Model
model30
EPS Estimate Model
model31
Earnings Quality Model
model32
Price Momentum Model
model33
Revenue Estimate Model
model36
SmartRatios Model
model37
Text Mining Data
model38
Growth Valuation Model
model39
Valuation Momentum Data
model4
Fundamentals and Technical Indicators Model
model40
Ranking & Recommendation Data
model42
Equity Ranking Model
model43
Insider Model for the US
model44
Insider Model V2 for the US
model46
Insider Data for the US
model47
Ranking Model
model5
Country-Specific Expectational Model
model50
International Scorings Data
model51
Systematic Risk Metrics
model52
Creditworthiness model
model53
Creditworthiness Risk Measure Model
model54
Technical Indicators
model55
Fundamental Indicators
model56
Stock Reports Plus
model57
Quantitative Stock Valuation Model
model58
Implied Volatility Data
model7
Value & Growth Alpha Model
model77
Analysts' Factor Model
model8
Fundamental Analysis Model
model9
Sell Side Expectational Model
news12
US News Data
news17
PR Edition Data
news18
Ravenpack News Data
news20
Web Sources News Sentiment Data
news21
Macro Economic Event Data
news22
News Direct-feed Data
news23
MnA Deals Data
news29
Significant Developments Data
news3
Dow Jones News Analytics Data
news31
News Analytics on Equities
news42
US/AMR news data
news5
News Feed Analytics Data
news52
Conference call data
news54
Newa analystic data
news7
Real Time News Feed Data
news8
Dow Jones Press Release Data
news87
Smart Conference call transcript data
news92
Standardized Financial News Categorization
option1
Options Volatility Surfaces Data
option11
Equity Option Ratings Data
option14
Implied Volatility Data for Europe
option4
Implied Volatility and Pricing for Equity Options
option6
Forecasted Volatility for Equity Options
option8
Volatility Data
option9
Options Analytics
other1
Estimates for China A-Shares
other127
Equity Ranking Model
other131
Conviction based hedge funds selections
other137
Systematic Insider Alpha Strategy
other143
Transaction Volume Data for Equity
other15
ETF Constituents
other160
NLP on media data
other17
Flow into Equities Data
other176
Nonlinear adaptive model
other193
Systematic Hedging for Investors to Evade Large Drawdowns
other238
Event based sentiment and behavioral factors model
other32
Europe Stock Pick Data
other326
Intermediate Data from Events
other327
Sensitivity to Interest Rates Model
other33
Qualitative Alpha Model Data
other349
Patent Indicators
other351
International sentiment analysis NLP model
other376
Aggregated Transaction Data
other378
Accounting governance indicator models
other384
NLP on conference conversation
other401
Governance, Accounting, Management, and Equality
other407
Factors Dislocations Data
other41
A-Share Alpha Model
other411
Linear, nonlinear, and region-specific models
other416
Quantitative Filings Data
other419
Analyst Estimate Daily Data
other42
A-Share Index Research Data
other423
Fundamental Income and Dividend Model
other424
Dividend prediction model
other425
Supply Chain Data
other427
Quantify text part in financial reports data
other429
Sentiment Data by NLP
other432
DNN prediction of fundamentals
other434
Credit Risk Factors
other455
Relationship enhanced with AI/ML
other461
Models for A-shares
other47
Web Intelligence Data
other479
China Classification data
other486
Earnings Predictions Data
other492
Stock Events Data
other510
8-K based NLP model
other54
Quantitative Stock Selection Data
other62
Job postings Data
other65
Talent Risk Data
other7
Archive News Data
other72
Combined Alpha Model
other74
AI/ML Web Based Mention Data
other76
Employee Benefit Plan Data
other78
Earnings and conference call data
other83
Insider Transaction Analytics
other84
Upcoming Earnings Data
other85
China Flow Data
pv1
Price Volume Data for Equity
pv103
Interval and MOO&MOC statistics
pv113
Economic MacroIndicator Data
pv13
Relationship Data for Equity
pv24
A-shares EDM Data
pv25
A-shares Index Data
pv27
A-shares Trade Data
pv28
Price Volatility Predictions Data
pv29
Derived Industry Classification
pv3
Global Daily Pricing Data
pv30
Alternate Industry Classification
pv7
Relation data from Form 10-K and 20-F
risk64
Fundamentals related Risk Factors
risk69
Classification based on Business description
sentiment1
Research Sentiment Data
shortinterest2
Short Interest Model
shortinterest3
Securities Lending Files Data
shortinterest6
SmartHoldings Model
shortinterest7
Short Selling Model
socialmedia12
Sentiment Data for Equity
socialmedia15
Sentiment Indicators
socialmedia3
Twitter based sentiment data
socialmedia4
Brands and Social Media Data
socialmedia5
Lexical Breakdown Data
socialmedia7
Activity Feed Data
socialmedia8
Social Media Data for Equity
Available Operators
Selection expressions can use many of the same operators as Alpha expressions. A full list of available operators is available at Appendix: SuperAlpha Operators.

Example Selection Expressions
Selection Handling = "Positive", Selection Limit = 30
turnover
This expression will return the 30 Alphas with the highest turnover. If there are fewer than 30 Alphas, then all Alphas will be selected.
Selection Handling = "Positive", Selection Limit = 20
long_count / sqrt(universe_size(universe)) * (turnover < 0.2)
This expression will exclude all Alphas with turnover >= 0.2. Of those remaining Alphas with turnover < 0.2, the expression will select the 20 Alphas with the highest selection weight. If there are fewer than 20 Alphas with turnover < 0.2, then all of those Alphas will be selected.
Selection Handling = "Non-Zero", Selection Limit = 20
-turnover * (neutralization == "SUBINDUSTRY")
This expression will only select alphas with Subindustry neutralization. Of those alphas with Subindustry neutralization, the expression will select the 20 alphas with the lowest turnover. Note that the Selection Handling must be set to "Non-Zero" for this expression to select the desired alphas. Selection Handling = "Positive" would not select any alphas, since all selection weight values are zero or negative. Selection Handling = "Non-NaN" will include alphas with all neutralization types because the selection weight for these alphas will be zero, which is included.
Selection Handling = "Non-Zero", Selection Limit = 10
(in(datasets, "analyst6") || color == "RED") * (long_count-short_count)
This expression will only select alphas that use the analyst6 dataset, or which are designated with the color red. Of those alphas, the expression will select 10 alphas for which long_count-short_count) evaluates to the largest values. Note that this expression will include alphas for which (long_count-short_count) evaluates to a negative number. To exclude negative numbers, use Selection Handling = "Positive".
Selection Handling = "Non-NaN", Selection Limit = 20
x = if_else(category == "PRICE_MOMENTUM", 2, 1); y = if_else(category == "PRICE_REVERSION", 0.5, 1); z = (long_count * x * y - short_count); if_else(turnover > 0.2, nan, z)
This expression will only select Alphas with turnover <= 0.2. Of those Alphas with turnover <= 0.2, the expression will select the 20 Alphas for which (long_count - short_count) evaluates to the largest values, where the long_count value of Price Momentum Alphas is multiplied by 2 and the long_count value of Price Reversion Alphas is multiplied by 0.5. Note that Selection Handling is set to "Non-NaN", which means it will include Alphas for which (long_count * x * y <= short_count).
