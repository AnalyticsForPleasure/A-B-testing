import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
import seaborn as sns



if __name__ == '__main__':

    pd.set_option('display.max_rows', 5000)
    df = pd.read_csv('/Data/Breast_Cancer.csv')
    print('*')
    column_headers = list(df.columns.values)
    print("The Column Header :", column_headers)


    # Assuming 'Age' and 'Marital Status' are the variables of interest
    # Separate data into two groups based on marital status
    married_age = df[df['Marital Status'] == 'Married']['Age']
    not_married_age = df[df['Marital Status'] != 'Married']['Age']

    # Perform two-sample t-test
    t_statistic, p_value = ttest_ind(married_age, not_married_age)

    # Print results
    print("T-statistic:", t_statistic)
    print("P-value:", p_value)

    # Check for statistical significance
    alpha = 0.05
    if p_value < alpha:
        print(
            "Reject null hypothesis. There is a significant difference in age between married and not married individuals.")
    else:
        print(
            "Fail to reject null hypothesis. There is no significant difference in age between married and not married individuals.")

    # Plotting the age distributions for each group using Kernel Density Estimation (KDE) line chart
    plt.figure(figsize=(10, 6))
    sns.kdeplot(married_age, label='Married', color='blue')
    sns.kdeplot(not_married_age, label='Not Married', color='orange')
    plt.xlabel('Age')
    plt.ylabel('Density')
    plt.title('Kernel Density Estimation of Age by Marital Status')
    plt.legend()
    plt.grid(True)
    plt.show()