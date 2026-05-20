Creating Global (GLB) SuperAlphas requires careful consideration, including neutralization, component Alpha selection, and simulation settings.

Neutralization

Neutralize your SuperAlpha to COUNTRY to account for differences across countries in the global region.
This ensures fair comparisons and avoids biases caused by regional disparities.
Neutralization to country helps align signals across diverse regions.
Universe selection

The MINVOL1M GLB universe contains over 9,000 instruments, which can make simulations slower.
To speed up simulations, test your SuperAlpha on the TOP3000 universe.
Once optimized, simulate and submit your SuperAlpha on the MINVOL1M universe.
Selection Expression

Select Alphas that are neutralized to country using the following methods:
Select Alphas neutralized in expression: in(datafields, 'country')
Select Alphas neutralized in settings: neutralization == 'COUNTRY'
Choose Alphas with 1-2 years of OS data to ensure reliability:
Use the selection expression: os_start_date <= '2022-01-23'
Combine multiple selections using the OR operator to diversify your component Alphas and improve overall performance.
This allows you to include a broader range of signals in your SuperAlpha.
Combo Expression

Use the combo_a operator to combine Alphas effectively.
This operator performs better when the selected Alphas are different.
Avoid selecting overly similar Alphas to maximize the effectiveness of the combo.
Simulation settings

Enable the Max Trade setting during simulation, especially on the MINVOL1M universe.
This ensures your SuperAlpha meets liquidity and scalability requirements.
It validates that your SuperAlpha can handle real-world constraints.
Tips for Success

Diversify selection: Use multiple selection expressions to ensure a broad range of Alphas in your SuperAlpha.
Focus on liquidity: Simulating on the TOP3000 universe speeds up testing, while submitting on MINVOL1M ensures scalability. Additionally, check Investability constrained metrics of your SuperAlpha.
Test OS performance: Prioritize Alphas with sufficient OS data to avoid overfitting and ensure robust performance.
More concepts that you can explore

What is a SuperAlpha?
SuperAlpha Selection Expression
SuperAlpha Combo Expression
SuperAlpha Helpful Tips
Getting Started: Global Alphas
