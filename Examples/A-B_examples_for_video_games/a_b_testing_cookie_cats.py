# https://www.kaggle.com/code/ekrembayar/a-b-testing-step-by-step-hypothesis-testing
from scipy import stats
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from scipy.stats import ttest_ind

# userid - a unique number that identifies each player.
# version - whether the player was put in the control group (gate_30 - a gate at level 30) or the test group (gate_40 - a gate at level 40).
# sum_gamerounds - the number of game rounds played by the player during the first week after installation
# retention_1 - did the player come back and play 1 day after installing?
# retention_7 - did the player come back and play 7 days after installing?

# **************************************************************************************************************
# Function  name: number_of_games_rounds_played_by_a_user_first_week
# input: adding a chart line which illustrate the number of games rounds played by a user first week
# return value:
# ***************************************************************************************************************
def number_of_games_rounds_played_by_a_user_first_week(df):
    fig = plt.figure(figsize=(10, 6), facecolor='#f6f5f5')
    # Grouping data and plotting
    plot_df = df.groupby(by='sum_gamerounds')['userid'].count()
    ax = plot_df.head(150).plot(x='sum_gamerounds', y='userid', color='white', linewidth=4)
    # Set logarithmic scale on Y-axis
    ax.set_yscale('log')
    # Set labels and title
    ax.set_xlabel("Total Game Rounds", {'font': 'serif', 'size': 13, 'color': 'black'})
    ax.set_ylabel("Number of Players\n(Log Scale)", {'font': 'serif', 'size': 13, 'color': 'black'})
    ax.set_title("How many game rounds did players participate\nduring the initial week?",
                 {'font': 'serif', 'size': 20, 'color': 'black'})
    # Remove borders
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    # Set background color
    ax.set_facecolor('lightgray')
    plt.savefig('number_if_games_rounds_played_after_first_week_1.jpg', dpi=250, bbox_inches='tight')
    # Display the plot
    plt.show()

# **************************************************************************************************************
# Function  name: first_day_retention
# input: 
# return value:
# ***************************************************************************************************************
def first_day_retention(df):
    # the row below show us that a little less than half of the players come back one day after installing the game.
    # Let’s look at how 1-day retention differs between the two AB-groups
    result_info = df.groupby('version')['retention_1'].mean() # gate 30 - the retention is 0.44818,gate 30 - the retention is 0.44228

    boot_1d = []
    iterations = 1000
    for i in range(iterations):
        boot_mean = df.sample(frac=1, replace=True).groupby(by='version')['retention_1'].mean()
        boot_1d.append(boot_mean)
    fig = plt.figure(figsize=(10, 6), facecolor='#f6f5f5')
    boot_1d = pd.DataFrame(boot_1d)
    colors = ['white', 'lightgreen']
    ax = boot_1d.plot.kde(color=colors, linewidth=4)
    # Set labels and title
    ax.set_xlabel("The Average of 1-Day Retention", {'font': 'serif', 'size': 13, 'color': 'black'})
    ax.set_ylabel("Density", {'font': 'serif', 'size': 13, 'color': 'black'})
    ax.set_title("The Average of 1-Day Retention for each AB group", {'font': 'serif', 'size': 22, 'color': 'black'})
    # Remove borders
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    # Legend
    ax.legend(loc='upper left', bbox_to_anchor=(1.01, 1))
    # Set background color
    ax.set_facecolor('lightgray')
    plt.savefig('Avg_of_first_day_Retention.jpg', dpi=250, bbox_inches='tight')
    # Display the plot
    plt.show()


if __name__ == '__main__':

    pd.set_option('display.max_rows', 5000)
    df = pd.read_csv('/home/shay_diy/PycharmProjects/A-B-testing/Data/cookie_cats.csv')
    print('*')
    column_headers = list(df.columns.values)
    print("The Column Header :",
          column_headers)  # ['userid', 'version', 'sum_gamerounds', 'retention_1', 'retention_7']

    unique_version = df['version'].value_counts()

    print('*')
    # Number of Unique User-
    # In the next row, I am checking  whether the number of unique user IDs ( left side of the equation) is equal to the total number of df  rows  ( right side of the equation ).
    print(df['userid'].nunique() == df.shape[0])  # Number of unique users over the dataset is 90,189 - all unique users

    # Summary Stats: sum_gamerounds
    summary = df.describe([0.01, 0.05, 0.10, 0.20, 0.80, 0.90, 0.95, 0.99])[["sum_gamerounds"]].T
    print('*')

    df.sort_values(by='sum_gamerounds', inplace=True, ascending=False)
    print('*')
    # A/B Groups & Target Summary Stats - Version 1:
    result = df.groupby("version").sum_gamerounds.agg(["count", "median", "mean", "std", "max"]).T

    # A/B Groups & Target Summary Stats - Version 2:
    # List of aggregate functions
    aggregate_functions = ["count", "median", "mean", "std", "max"]

    #number_of_games_rounds_played_by_a_user_first_week(df)

    first_day_retention(df)

    #
    # # Iterate over unique values in the "version" column
    # for version_value in df['version'].unique():
    #     # Filter the DataFrame for the current version
    #     version_df = df[df['version'] == version_value]
    #
    #     # Calculate aggregates for the current version
    #     aggregates = version_df['sum_gamerounds'].agg(aggregate_functions)
    #
    #     # Print results
    #     print(f"Version: {version_value}")
    #     for function in aggregate_functions:
    #         print(f"{function.capitalize()}: {aggregates[function]}")
    #     print('*')
    #
    # # Create subplots
    # fig, axes = plt.subplots(2, 4, figsize=(18, 5))
    #
    # # Histogram for Gate 30
    # df[df['version'] == 'gate_30']['sum_gamerounds'].plot(kind='hist', ax=axes[0], color='lightgray')
    # axes[0].set_title('Distribution of Gate 30 (A)', fontsize=15)
    #
    # # Histogram for Gate 40
    # df[df['version'] == 'gate_40']['sum_gamerounds'].plot(kind='hist', ax=axes[1], color='darkgray')
    # axes[1].set_title('Distribution of Gate 40 (B)', fontsize=15)
    #
    # # Set common title
    # fig.suptitle('Before Removing The Extreme Value', fontsize=20)
    #
    # # Adjust layout
    # plt.tight_layout(pad=4)
    #
    # print('*')
    #
    # # After Removing The Extreme Value
    # df_after_removing_extreme_value = df[df.sum_gamerounds < df.sum_gamerounds.max()]
    # print('*')
    #
    # #
    # # # Create subplots
    # # fig, axes = plt.subplots(1, 2, figsize=(18, 5))
    #
    # # Plot histograms for each group and boxplot
    # for i, version in enumerate(['Gate 30 (A)', 'Gate 40 (B)']):
    #     if version == 'Gate 30 (A)':
    #         df[df['version'] == 'gate_30']['sum_gamerounds'].hist(ax=axes[i], color="lightgray")
    #     elif version == 'Gate 40 (B)':
    #         df[df['version'] == 'gate_40']['sum_gamerounds'].hist(ax=axes[i], color="darkgray")
    #     else:
    #         sns.boxplot(x='version', y='sum_gamerounds', data=df, ax=axes[i])
    #
    #     # Set titles for each subplot
    #     axes[i + 2].set_title(f"Distribution of {version}", fontsize=15)
    #
    # # Set common title and adjust layout
    # plt.suptitle("After Removing The Extreme Value", fontsize=20)
    # plt.tight_layout(pad=4)
    # plt.show()