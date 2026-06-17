def generate_report(analysis):

    correlation = analysis["correlation"]
    p_value = analysis["p_value"]
    significance = analysis["significance"]

    if correlation > 0.7:
        strength = "very strong positive relationship"
    elif correlation > 0.4:
        strength = "moderate positive relationship"
    elif correlation > 0:
        strength = "weak positive relationship"
    elif correlation < -0.7:
        strength = "very strong negative relationship"
    elif correlation < -0.4:
        strength = "moderate negative relationship"
    else:
        strength = "weak relationship"

    report = f"""
Research Report

Independent Variable:
{analysis['independent_variable']}

Dependent Variable:
{analysis['dependent_variable']}

Number of Observations:
{analysis['rows']}

Correlation:
{correlation}

P-Value:
{p_value}

Interpretation:
The analysis indicates a {strength} between the variables.

Statistical Significance:
{significance}

Conclusion:
The dataset suggests that changes in
{analysis['independent_variable']}
are associated with changes in
{analysis['dependent_variable']}.
"""

    return report