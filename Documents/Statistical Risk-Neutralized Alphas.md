What is the Statistical Risk Model?
Literature classifies factor models into two main categories:

Fundamental Factor Models

Fundamental factor models use attributes that explain the cross-sectional differences in stock prices. These factors often include a company's financial health, profitability, growth potential, and other fundamental characteristics. Essential metrics such as the price-to-earnings (P/E) ratio, debt-to-equity ratio, and earnings growth rate are used to evaluate the intrinsic value of stocks and inform investment decisions.

For example, a classic and seminal paper in this domain is "The Cross-Section of Expected Stock Returns" by Eugene F. Fama and Kenneth R. French, published in 1992. This paper introduced the Fama-French Three-Factor Model, which includes market risk, size (SMB, Small Minus Big), and value (HML, High Minus Low) as key factors in explaining stock returns.

Statistical Factor Models

Statistical factor models apply statistical techniques to analyze the returns of various securities. These models identify patterns and relationships in market data to develop Alphas. Statistical methods such as Principal Component Analysis (PCA) or cluster analysis can be used to explore correlations between stock returns. Statistical models rely on historical return data to seek to predict future performance or optimize portfolio risk.

A notable work in this area is "An Empirical Investigation of the Arbitrage Pricing Theory" by Richard Roll and Stephen Ross. This paper investigates the Arbitrage Pricing Theory (APT), which emphasizes the importance of using statistical methods to identify multiple factors that influence asset returns. The paper employs techniques such as Principal Component Analysis (PCA) to extract key factors from historical return data and analyze their impact on asset prices. This approach allows for the identification of complex, non-linear relationships within the data, providing a more sophisticated means of risk management and prediction.

In BRAIN Research, fundamental models such as SLOW, FAST, and SLOW_AND_FAST are already represented. Thus, we have chosen to focus on the statistical approach, which offers a distinctly different perspective. Statistical models provide opportunities to capture various factors, promoting portfolio diversification. The model allows for the creation of signals that perform well in the specific returns space, adding diversity to the pool of available Alphas.

How to Simulate Statistical Risk-Neutralized Alphas
To manage statistical risk in Alphas, BRAIN has developed a risk model incorporating various risk factors. By monitoring and controlling these factors, BRAIN consultants can mitigate statistical risks that may be overlooked by fundamental factor models and enhance the robustness of Alphas. Consultants can neutralize Alphas using statistical risk factors by configuring the settings to use STATISTICAL neutralization:

statistical_risk-neutralized.png
settings_dict = {

'instrumentType': 'EQUITY',

'region': 'USA',

'universe': 'TOP3000',

'delay': 1,

'decay': 0,

'neutralization': 'STATISTICAL',

'truncation': 0.1,

'pasteurization': 'ON',

'unitHandling': 'VERIFY',

'nanHandling': 'ON',

'language': 'FASTEXPR',

'visualization': False

}

By adjusting these settings, consultants can effectively implement statistical risk-neutralized Alphas, enhancing their stability and performance in diverse market conditions. Notably, this feature has been shown to retain performance while significantly reducing risk. The statistical risk-neutralization process ensures that Alphas maintain their profitability while mitigating potential risks, thereby providing a more stable and reliable performance over time.

Additionally, the existing page on Learn here has a useful section at the bottom on how to get started with this new feature. It is recommended to try this neutralization on your existing alphas and "An Empirical Investigation of the Arbitrage Pricing Theory" for further insights.