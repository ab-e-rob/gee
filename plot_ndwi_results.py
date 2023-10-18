import pandas as pd
import matplotlib.pyplot as plt
import calendar

def plot_open_water_percent():
    # Read the CSV file into a DataFrame
    df = pd.read_csv('combined_results_edited.csv', delimiter=',', header=0)

    # Set first row as index
    df = df.set_index(df.columns[0])

    # reorder the columns
    def get_month_order(column_name):
        for month_num, month_name in enumerate(calendar.month_name[1:]):
            if month_name.lower() in column_name.lower():
                return month_num
        return len(calendar.month_name)


    # Sort the columns based on the month order
    sorted_columns = sorted(df.columns, key=get_month_order)

    # now plot
    # Create a scatter plot for each column
    for column in df.columns:
        plt.plot(df.index, df[column], label=column)

    # Set labels and a legend
    plt.xlabel('Months')
    plt.ylabel('Values')
    plt.legend()

    # Show the plot
    plt.show()

    return()

def plot_mean():
    df = pd.read_csv('mean_values.csv', delimiter=',', header=0)
    # Set first row as index
    df = df.set_index(df.columns[1])
    df = df.drop('Unnamed: 0', axis=1)

    # Create a bar chart
    plt.figure(figsize=(10, 20))
    ax = df.plot(kind='bar')

    # Set labels and a title
    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title('Bar Chart of Data')

    ax.set_xticklabels(ax.get_xticklabels(), fontsize=7)

    # Show the plot
    plt.show()

