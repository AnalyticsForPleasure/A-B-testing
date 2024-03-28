import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import ttest_ind

# userid - a unique number that identifies each player.
# version - whether the player was put in the control group (gate_30 - a gate at level 30) or the test group (gate_40 - a gate at level 40).
# sum_gamerounds - the number of game rounds played by the player during the first week after installation
# retention_1 - did the player come back and play 1 day after installing?
# retention_7 - did the player come back and play 7 days after installing?




if __name__ == '__main__':

    pd.set_option('display.max_rows', 5000)
    df = pd.read_csv('/home/shay_diy/PycharmProjects/A-B-testing/Data/cookie_cats.csv')
    print('*')
    column_headers = list(df.columns.values)
    print("The Column Header :", column_headers)

    # Number of Unique User-
    # In the next row, I am checking  whether the number of unique user IDs ( left side of the equation) is equal to the total number of df  rows  ( right side of the equation ).
    print(df['userid'].nunique() == df.shape[0]) # Number of unique users over the dataset is 90,189 - all unique users

    # Summary Stats: sum_gamerounds
    summary = df.describe([0.01, 0.05, 0.10, 0.20, 0.80, 0.90, 0.95, 0.99])[["sum_gamerounds"]].T
    print('*')

    # A/B Groups & Target Summary Stats - Version 1:
    result = df.groupby("version").sum_gamerounds.agg(["count", "median", "mean", "std", "max"]).T

    # A/B Groups & Target Summary Stats - Version 2:

    # List of aggregate functions
    aggregate_functions = ["count", "median", "mean", "std", "max"]

    # Iterate over unique values in the "version" column
    for version_value in df['version'].unique():
        # Filter the DataFrame for the current version
        version_df = df[df['version'] == version_value]

        # Calculate aggregates for the current version
        aggregates = version_df['sum_gamerounds'].agg(aggregate_functions)

        # Print results
        print(f"Version: {version_value}")
        for function in aggregate_functions:
            print(f"{function.capitalize()}: {aggregates[function]}")
        print('*')

    # Create subplots
    fig, axes = plt.subplots(1, 4, figsize=(18, 5))

    # Plot histograms for each group and boxplot
    for i, version in enumerate(['Overall', 'Gate 30 (A)', 'Gate 40 (B)', 'Two Groups']):
        if version == 'Overall':
            df['sum_gamerounds'].hist(ax=axes[i], color="steelblue")
        elif version == 'Gate 30 (A)':
            df[df['version'] == 'gate_30']['sum_gamerounds'].hist(ax=axes[i], color="steelblue")
        elif version == 'Gate 40 (B)':
            df[df['version'] == 'gate_40']['sum_gamerounds'].hist(ax=axes[i], color="steelblue")
        else:
            sns.boxplot(x='version', y='sum_gamerounds', data=df, ax=axes[i])

        # Set titles for each subplot
        axes[i].set_title(f"Distribution of {version}", fontsize=15)

    # Set common title and adjust layout
    plt.suptitle("After Removing The Extreme Value", fontsize=20)
    plt.tight_layout(pad=4)
    plt.show()