import pandas as pd
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt


if __name__ == '__main__':

    pd.set_option('display.max_rows', 5000)
    df = pd.read_csv('/Data/Breast_Cancer.csv')
    print('*')
    column_headers = list(df.columns.values)
    print("The Column Header :", column_headers)

    # Very important :
    # comparing survival months between two groups based on marital status,
    # we used a chi-square test of independence, not a two-sample t-test, because the variables
    # being compared were categorical rather than continuous.

    # Assuming 'Marital Status' and 'Status' are the variables of interest
    # Create a contingency table
    contingency_table = pd.crosstab(df['Marital Status'], df['Status'])


    # Perform chi-square test of independence
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)

    # Print results
    print("Chi-square statistic:", chi2)
    print("P-value:", p_value)

    # Check for statistical significance
    alpha = 0.05
    if p_value < alpha:
        print("Reject null hypothesis. There is a significant relationship between marital status and survival status.")
    else:
        print(
            "Fail to reject null hypothesis. There is no significant relationship between marital status and survival status.")

    # Plotting the contingency table
    contingency_table.plot(kind='bar', stacked=True, figsize=(10, 6))
    plt.title('Marital Status vs. Survival Status')
    plt.xlabel('Marital Status')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.legend(title='Survival Status')
    plt.grid(True)
    plt.tight_layout()
    plt.show()