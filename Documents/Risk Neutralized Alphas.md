Introducing a new way to neutralize Alphas* on BRAIN for the USA, EUR, ASI, CHN and GLB regions.
In addition to the existing neutralizations in simulation settings (Market, Sector, Industry, Subindustry), you will see other new risk factors’ sets for neutralizations: “Slow Factors”, “Fast Factors”, “Slow + Fast Factors”, “RAM”, “Statistical” and “Crowding” . Alphas created using these settings are called “Risk-Neutralized alphas” on BRAIN.

Introduction
Often in academic studies, stock returns can be deconstructed into different risk factor drivers. Take the classical Fama-French Model for example, we can run a multi-linear regression on individual stocks, and show that stock returns (Rit) can be decomposed to market factor, size factor and value factor:

In the world of alphas*, we can apply similar methods to deconstruct an alpha’s returns. The coefficient (beta) of each risk factor shows its importance to the alpha's return. If an alpha's return can be fully explained by these well-documented risk factors, it does not bring any additional value since it can be easily replicated by these factors. On the other hand, if an alpha shows a significantly positive residual (Ɛit), it means this alpha captures some market anomalies that is not yet documented in the risk factor databases.

Here, our new risk neutralization feature will enable you to directly research on a risk-neutralized world and explore unique returns that have not been captured before.

What are risk neutralized alphas?
In the past, the most rudimentary method of risk-handling is to set the neutralization to industry classification to avoid industry level risks. More advanced users may build their own set of risk factors, for example they may neutralize their alphas against the common size factor by defining a new group based on capitalization, and manually apply a layer of group_neutralize or vector_neut on their alpha.

Now let's imagine that instead of just neutralizing against one risk factor at a time - an alpha can be simultaneously controlled for a wide range of common, but yet comprehensive risk factors, its final return will be more representative of what the alpha intends to capture, instead of bearing unwanted risk factors. These unwanted risk factors may not pose a problem in the back-testing period, but it could be harmful if they experience drawdowns in the out-sample stage.

How to use the risk neutralized feature
When opening the settings tab in the simulation stage, notice that besides the common market, and industry classifications, you will find additional new options under the neutralization setting. You may choose from these sets of risk factors. We provide you below with an overview of the feature. We cannot share granular details, due to confidentiality of the risk neutralized models and to prevent any potential overfitting of your alphas.

Risk_neutral.png
Risk factors' sets
The turnover space you intend to work on should help you decide which risk factors’ set to use. As a rule of thumb, we recommend adopting the Slow Factors for low-turnover signals and Fast Factors or Slow + Fast factors for high-turnover signals. The Slow + Fast Factors incorporates both of the above factors together. However, there is no universal rule as to which alpha should apply certain risk factors. We recommend giving them a try and finding the most suitable risk factors for your needs.

When applying neutralization, please remember the turnover of the output alpha is likely to increase versus the input one, and more so when neutralizing to the Fast Factors. Fast Factors comprises high turnover factors that would change the position weights of your alpha more so than the Slow Factors (See table below) and thus increase alpha turnover. Thus using “Fast Factors” or “Slow + Fast Factors” neutralization would be beneficial in cases where the increase in turnover comes with a corresponding increase in Sharpe. You should balance the benefits from better risk-neutralization (higher Sharpe or lower drawdown) and increased turnover by sourcing the most relevant set of factors for each alpha and leveraging the knowledge of the alpha properties : for instance, if your alpha is not susceptible to some fast factors (i.e., reversion) by design, neutralizing to Fast factors might be redundant.

All of these risk factors’ settings will also assume long-short balanced with market neutralization for the risk-neutralized alphas. Besides the style factors, all risk factors’ settings include industries and market risk as well.

Slow Factors
Includes market and industry factors as well as other common lower turnover style factors.
Fast Factors
Includes market, industry factors and higher turnover style factors, such as reversion alpha.
Slow + Fast Factors
Combines both slow and fast factors.
RAM
Includes risk factors that capture the impact of short-term mean reversion and long-term momentum trends in stock prices.
Statistical
Includes risk factors which use techniques to identify patterns in historical returns, neutralize risks, and enhance Alpha stability with diverse, data-driven insights.
Crowding
Includes risk factors of excessive investor concentration in similar positions, which can lead to reduced profitability by heightened impact during concentrated unwinding.
How should you start your risk neutralized alpha research?
We recommend first trying this new feature out on your previous submitted alphas. You may notice some of them greatly improve your original alphas while also having less correlation to the submitted alpha.
After understanding how this feature affects your alphas, we suggest setting risk-neutralized settings as default in the simulation setting, and see if you can discover new, unique alphas from here on!
We recommend you also go through the classical 5-factor FAMA French-Model to have a deeper understanding of style factors.

Summary
Risk-neutralized alphas are alphas that show orthogonal and unique returns after accounting for market, industries and style factors.
Choose "Slow Factors" or "Fast Factors" / "Slow + Fast factors" in neutralization settings depending on the signal's turnover.
Start searching for innovative ideas through risk-neutralized alphas!
Read “How to start risk neutralize research?” on the forum .
Read " Risk Neutralized Alpha: How to choose risk factors’ set?" on the forum .
*WorldQuant defines alphas as mathematical models that seek to predict the future price movements of various financial instruments

