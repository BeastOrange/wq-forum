SuperAlpha is a new feature in BRAIN designed to help consultants realize the power of combining many, diverse signals. SuperAlpha gives you the power and flexibility to creatively manipulate and combine the Alphas you have already created and produce even stronger, more robust signals.

SuperAlphas have two main parts – a selection expression, and a combo expression. The selection expression chooses which Alphas to include in the SuperAlpha. The combo expression determines how to combine the selected Alphas. The values in the SuperAlpha settings menu constrain how the selection and combo expressions work.

Super alpha intro jigsaw
To simulate a SuperAlpha, on Simulation page use the '+' button and choose 'New SuperAlpha Simulation':

simulation_pic13.png
Your SuperAlphas will be listed on the Alphas page with type = Super (while Alphas have type = regular).

SuperAlpha Simulation Modes
SuperAlpha simulations in BRAIN allow you to combine multiple Alphas into a single, more robust signal. To evaluate the performance of a SuperAlpha, it is essential to understand the In-Sample (IS) and Out-of-Sample (OS) periods of the component Alphas.

What is the In-Sample (IS) Period?
The IS period is a rolling 10-year simulation window.
It starts approximately 12 years ago and ends around 2 years ago.
The IS period shifts forward 2-3 times a year, meaning the start and end dates are updated periodically.
This period is used to simulate and evaluate Alphas based on historical data.
What is the Out-of-Sample (OS) Period?
The OS period begins after the IS end date.
It includes the period where the Alphas are evaluated on unseen data, providing a more realistic measure of their live performance.
image-2025-6-2_21-54-51-1.png
What does OS Start Date (os_start_date) mean?
The OS start date is the next date after the IS end date at the time the Alpha was submitted.
You can find the os_start_date for submitted Alphas:
Go to the Alphas page, switch to the Submitted tab, open the Alpha, and scroll to OS Summary.
What is a SuperAlpha OS Start Date.png
response_json = session.get("https://api.worldquantbrain.com/alphas/{alpha_id}").json()
response_json["os"]["startDate"]

What happens when the IS Period rolls forward?
If you select component Alphas created using the current IS period, the SuperAlpha performance will depend only on the IS performance of the component Alphas.
After the IS period rolls forward, the same SuperAlpha simulation will include the OS performance of the component Alphas.
Getting started with Component Activation modes
What is Component Activation?
The Component Activation setting gives you greater control when combining Alphas in a SuperAlpha by allowing you to manage their activation period:

IS - Alphas contribute to the SuperAlpha from the start of their In-Sample (IS) period.
OS - Alphas contribute to the SuperAlpha starting from their Out-of-Sample (OS) period.
Why is Component Activation important?
When combining Alphas in a SuperAlpha:

Once an Alpha is selected, the same combination logic applies in both IS and OS periods of that Alpha.
At any point in the SuperAlpha's history:
Some Alphas are in IS: Their performance can inflate SuperAlpha performance due to overfitting at both the Alpha and SuperAlpha levels. The SuperAlpha overweights IS signals because they appear stronger, creating a feedback loop that further amplifies IS performance.
Some Alphas are in OS: Their performance is likely lower, causing the SuperAlpha to underweight these signals and concentrate on IS signals.
As a result, the back-test may look good, but OS performance can drop sharply.

How does Activation Mode differ from filtering by os_start_date?
What happens when you filter by os_start_date?
Filtering requires you to manually filter component Alphas based on their os_start_date.
You need to match the exact os_start_date to evaluate SuperAlpha performance during the OS period.
If component Alphas have different OS start dates, their OS performance cannot be evaluated collectively, as it gets mixed with their IS performance.
Why is OS Component Activation mode better for SuperAlpha evaluation?
Automatically uses the OS start date of each component Alpha during simulation.
This allows you to evaluate SuperAlpha performance on unseen data, even if component Alphas have varying OS start dates.
The period where component Alphas were not fitted can be a strong predictor of your SuperAlpha's OS performance.
Advantages and Disadvantages of IS and OS Component Activation
IS Activation:

Advantages:
IS activation uses a longer history (10y), providing more data for research and refinement.
Useful for identifying promising signals during initial research.
Disadvantages:
IS activation can inflate performance due to overfitting at both the Alpha and SuperAlpha levels.
OS Activation:

Advantages:
Helps to avoid overfitting on IS period.
Provides a clearer picture of the true performance of the SuperAlpha.
Disadvantages:
OS activation relies on a smaller history (<5y), which may limit the scope of analysis.
Getting started with Component Activation setting
image-2025-07-11-223502.png
To make the most of this feature, consider following this workflow:

Initial research: Start with IS Activation. Focus on IS Sharpe - performance on a longer history.
Reality check: After finalizing any major change, switch to OS Activation. Check if the OS-only performance of your SuperAlpha improves. Improvements that don’t translate to better OS-only performance are likely overfitted to IS and may reduce the OS performance of the SuperAlpha.
Summary
The Component Activation helps you:

Avoid overfitting by activating Alphas only from the start of their OS period.
Gain a clearer understanding of your SuperAlpha's true performance.
Ensure your SuperAlpha is robust, reliable, and optimized on component’s OS period.