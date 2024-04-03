from scipy import stats
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

# **************************************************************************************************************
# Function  name: bootstrapping - Bootstrapping function for retention
# input:
# return value:
# ***************************************************************************************************************
def bootstrapping(data, iterations=1):
    boot_retention = []
    for i in range(iterations):
        boot_data = np.random.choice(data, int(len(data)))
        boot_retention.append(boot_data.mean())
    return boot_retention

# **************************************************************************************************************
# Function  name: print_summary
# input:
# return value:
# ***************************************************************************************************************
# Function that summarises test result based on the test used and p value and threshold
def print_summary(stat_test, p_val, threshold):
    # Data frame to store the results
    temp = pd.DataFrame(data={"Test": stat_test, "Test threshold": threshold, "p value": "{:.2g}".format(p_val)},
                        index=[0])

    # Determining if test rejected initial hypothesis
    if p_val < threshold:
        temp["Result"] = "Reject H0"
        temp["Comment"] = "Control and test groups are not from the same distribution"
    else:
        temp["Result"] = "Can't reject H0"
        temp["Comment"] = "Control and test groups may come from the same distribion"

    temp = temp[["Test", "Result", "p value", "Test threshold", "Comment"]]

    # Print tested hypothesis
    print("Test hypothesis")
    print("H0: A == B")
    print("H1: A != B", "\n")

    return temp


if __name__ == '__main__':

    pd.set_option('display.max_rows', 5000)
    df = pd.read_csv('/home/shay_diy/PycharmProjects/A-B-testing/Data/cookie_cats.csv')
    print('*')
    column_headers = list(df.columns.values)
    print("The Column Header :", column_headers)

    # Removing the outlier with 49854 rounds played
    df = df[df['sum_gamerounds'] != 49854]

    # Splitting the data ( After removing the outlier )
    control_group_7 = df[df['version'] == 'gate_30']['retention_7']
    test_group_7 = df[df['version'] == 'gate_40']['retention_7']

    control_group_rounds = df[df['version'] == 'gate_30']['sum_gamerounds']
    test_group_rounds = df[df['version'] == 'gate_40']['sum_gamerounds']


    # Creating a list with bootstrapped means for 7 day retention each A/B-group
    # Bootstrapping for control group & test group
    Bootstrap_control_group_7 = bootstrapping(control_group_7, iterations=5000)
    Bootstrap_test_group_7 = bootstrapping(test_group_7, iterations=5000)

    Bootstrap_7 = pd.DataFrame(data={'gate_30': Bootstrap_control_group_7,
                                     'gate_40': Bootstrap_test_group_7},
                                      index=range(5000))

    # Adding a column with the % difference between the two AB-groups
    Bootstrap_7['diff'] = Bootstrap_7['gate_30'] - Bootstrap_7['gate_40']

    # Plotting the bootstrap % difference
    sns.set(font='serif')  # Set font to serif
    sns.displot(Bootstrap_7['diff'], kind="kde",lw=4.0 ,color='#DAA520').set(
        title="Difference in retention between bootstrapped samples",
        xlabel="Difference in 1 day retention")
    plt.axvline(Bootstrap_7['diff'].mean(), c='gray', ls='--', lw=4.0)  # Change line color to red
    plt.savefig('difference_between_the_two_AB_groups_retantion_7.jpg', dpi=250, bbox_inches='tight')

    # Display the plot
    plt.show()

    # Calculate the probability of control group having a higher 1-day retention than test group
    prob = (Bootstrap_7['diff'] < 0).sum() / len(Bootstrap_7)


    #
    # Showing the probability
    print('The chance of the control group (gate at level 30) having higher 7-day retention than the test group (gate at level 40) is about {}%.\n '
          'Also, the difference in average 7-day retention between the control and test groups is {}%'.format(
            round(prob * 100, 1), round(Bootstrap_7['diff'].mean(), 3)))

    # Testing if changing the gate affects the number of rounds played by users
    test = stats.mannwhitneyu(control_group_rounds, test_group_rounds)
    print_summary("MannWhitneyu", test[1], 0.05)

    # Output print:
    # **************************************************************************************************************
    # The chance of the control group (gate at level 30) having higher 7-day retention than the test group (gate at level 40) is about 3.7%.
    #  Also, the difference in average 7-day retention between the control and test groups is 0.006%
    # Test hypothesis
    # H0: A == B
    # H1: A != B
    # ***************************************************************************************************************