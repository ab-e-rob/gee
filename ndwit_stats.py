# read csv file
import pandas as pd
import os
from dotenv import load_dotenv
import calendar
import matplotlib.pyplot as plt

# Load environment variables
load_dotenv()

# Specify the folder where your CSV files are located
folder_path = r'Z:\ndwi\water_percent_results'

# Get a list of CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Create empty DataFrames
result_df = pd.DataFrame()
data_dict = {'File Name': [], 'Mean percentage open water': []}

for file in csv_files:

    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path, delimiter=',', header=0)

    # Skip over empty CSV files
    if df.empty:
        print(f"Skipping empty file: {file}")
        continue

    replacement_conditions = [
        (f"clip_water_mask_month_1_{file[:-4]}_", "January"),
        (f"clip_water_mask_month_2_{file[:-4]}_", "February"),
        (f"clip_water_mask_month_3_{file[:-4]}_", "March"),
        (f"clip_water_mask_month_4_{file[:-4]}_", "April"),
        (f"clip_water_mask_month_5_{file[:-4]}_", "May"),
        (f"clip_water_mask_month_6_{file[:-4]}_", "June"),
        (f"clip_water_mask_month_7_{file[:-4]}_", "July"),
        (f"clip_water_mask_month_8_{file[:-4]}_", "August"),
        (f"clip_water_mask_month_9_{file[:-4]}_", "September"),
        (f"clip_water_mask_month_10_{file[:-4]}_", "October"),
        (f"clip_water_mask_month_11_{file[:-4]}_", "November"),
        (f"clip_water_mask_month_12_{file[:-4]}_", "December")]

    def replace_heading(column_name):
        for old, new in replacement_conditions:
            if old in column_name:
                column_name = column_name.replace(old, new)
        return column_name

    # Iterate through the columns and rename them
    new_column_names = {}
    for column_name in df.columns:
        new_name = replace_heading(column_name)
        new_column_names[column_name] = new_name

    # Rename the columns
    df.rename(columns=new_column_names, inplace=True)
    df = df.drop(df.columns[0], axis=1)

    # Define a function to get the month order for sorting
    def get_month_order(column_name):
        for month_num, month_name in enumerate(calendar.month_name[1:]):
            if month_name.lower() in column_name.lower():
                return month_num
        return len(calendar.month_name)

    # Sort the columns based on the month order
    sorted_columns = sorted(df.columns, key=get_month_order)

    # Reorganize the DataFrame with the sorted columns
    df = df[sorted_columns]
    df = df.transpose()

    def plot_ndwi():
        # Assuming the second column name is 'February' (change it to the actual column name)
        column_name = 0

        # Plot the specified column
        plt.figure(figsize=(10, 6))
        plt.plot(df[column_name])
        plt.title(f'Monthly open water as a percentage of the Ramsar site area ({file[-4]})')
        plt.xlabel('Year')
        plt.ylabel('%')
        plt.show()
        return plot_ndwi

    plot_ndwi()

    print(df)

    # Calculate the mean of column 1
    mean_value = df[1].mean()

    # Append the data to the dictionary
    data_dict['File Name'].append(file[:-4])
    data_dict['Mean percentage open water'].append(mean_value)

    # Rename and append the data to the result_df DataFrame
    df.columns = [f'0-{file[:-4]}', f'1-{file[:-4]}']
    result_df = pd.concat([result_df, df], axis=1)


result_df.to_csv('combined_results.csv', index=True)
mean_df = pd.DataFrame(data_dict)
mean_df.to_csv('mean_values.csv', index=True)
