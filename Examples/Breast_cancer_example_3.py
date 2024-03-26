import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import ttest_ind



if __name__ == '__main__':

    pd.set_option('display.max_rows', 5000)
    df = pd.read_csv('/home/shay_diy/PycharmProjects/A-B-testing/Data/Breast_Cancer.csv')
    print('*')
    column_headers = list(df.columns.values)
    print("The Column Header :", column_headers)


    # Define the groups based on the 'Race' column
    white_group = df[df['Race'] == 'White']['Survival Months']
    black_group = df[df['Race'] == 'Black']['Survival Months']

    # Perform independent two-sample t-test
    t_statistic, p_value = ttest_ind(white_group, black_group, equal_var=False)

    # Print the results
    print("T-statistic:", t_statistic)
    print("P-value:", p_value)

    # Visualize the data using box plots
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Race', y='Survival Months', data=df)
    plt.title('Survival Months by Race')
    plt.xlabel('Race')
    plt.ylabel('Survival Months')
    plt.show()

    # Interpret the results
    alpha = 0.05
    if p_value < alpha:
        print(
            "Reject null hypothesis: There is a significant difference in survival outcomes between White and Black patients.")
    else:
        print(
            "Fail to reject null hypothesis: There is no significant difference in survival outcomes between White and Black patients.")