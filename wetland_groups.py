import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a pandas DataFrame
file_path = 'stats\min_max_months_combined.csv'
df = pd.read_csv(file_path)

# Group by wetland and calculate the mode of the min and max months
grouped_df = df.groupby(['Name']).agg({
    'Min_Month': lambda x: x.mode().iloc[0] if not x.mode().empty else None,
    'Max_Month': lambda x: x.mode().iloc[0] if not x.mode().empty else None
})

# save as csv
grouped_df.to_csv('stats\min_max_months_combined_grouped.csv')


print(grouped_df)

# Assuming 'Max_Month' is the column containing mode values in grouped_df
grouped_df_sorted = grouped_df.sort_values(by='Max_Month')

plt.figure(figsize=(30, 20))
plt.bar(x=grouped_df_sorted.index, height=grouped_df_sorted['Max_Month'], color='skyblue')
plt.xlabel('Wetland', fontsize=25)
plt.xticks(rotation=90, fontsize=25)
plt.yticks(fontsize=25)
# plot all ticks and name them as months
plt.gca().yaxis.set_major_locator(plt.MultipleLocator(1))
plt.ylabel('Mode of Max Month')
plt.title('Mode of Max Month for Each Wetland', fontsize=25)
plt.show()

# Assuming 'Max_Month' is the column containing mode values in grouped_df
grouped_df_sorted = grouped_df.sort_values(by='Min_Month')

plt.figure(figsize=(30, 20))
plt.bar(x=grouped_df_sorted.index, height=grouped_df_sorted['Min_Month'], color='skyblue')
plt.xlabel('Wetland', fontsize=25)
plt.xticks(rotation=90, fontsize=25)
plt.gca().yaxis.set_major_locator(plt.MultipleLocator(1))
plt.ylabel('Mode of Min Month')
plt.yticks(fontsize=25)
plt.title('Mode of Min Month for Each Wetland', fontsize=25)
plt.show()

# Show historgam of frequency of max months
plt.hist(grouped_df['Max_Month'], bins=12)
plt.xticks(range(1, 13))
plt.xlabel('Month')
plt.ylabel('Frequency')
plt.title('Timing Frequency of Peak Wetland Area')
plt.show()

# Show histogram of rising limb rates from csv combined_limb_rates_results.csv
file_path = 'stats\combined_limb_rates_results.csv'
df = pd.read_csv(file_path)

# plot the average falling limb rate on the same plot
plt.hist(df['Avg_Falling_Rate'], bins=20)
plt.xlabel('Falling Limb Rate')
plt.ylabel('Frequency')
plt.title('Frequency of Falling Limb Rates')
plt.show()


df['Avg_Rising_Rate'] = df['Avg_Rising_Rate'] / 10000

plt.hist(df['Avg_Rising_Rate'], bins=10)
plt.xlabel('Rising Limb Rate')
plt.ylabel('Frequency (No. of wetlands)')
plt.title('Rising Limb Rates (ha/month)')
plt.show()

# Show histogram of peak frequency from csv combined_peak_frequency_results.csv
file_path = 'stats\combined_peak_frequency_results.csv'
df = pd.read_csv(file_path)

# plot histogram of the yearly range for each wetland in yearly_range_combined.csv
file_path = 'stats\yearly_range_combined.csv'

# Use a raw string (r-prefix) or double backslashes in the file path to avoid escape characters
df = pd.read_csv(file_path)

# Only select rows where the Dataset is 'Deep Aqua'
df = df[df['Dataset'] == 'Deep Aqua']

# Take a yearly average of the range for each wetland
df = df.groupby(['Name']).agg({
    'Range': 'mean'
}).reset_index()  # Resetting index to have 'Name' as a column for later merging

# Normalize to the average area by using the average area for each wetland from avg_area_combined.csv
file_path_avg_area = r'stats\avg_area_combined.csv'
avg_area_df = pd.read_csv(file_path_avg_area)

# Merge the two dataframes
df = pd.merge(df, avg_area_df, on='Name')



# Normalize the range by dividing by the average area
df['Range'] = df['Range'] / df['Avg_Area']

# group by wetland
grouped_df = df.groupby(['Name']).agg({
    'Range': 'mean'
}).reset_index()

print(df)

# Plot the histogram
plt.hist(grouped_df['Range'], bins=5)
plt.xlabel('m2')
plt.ylabel('Frequency (No. of wetlands)')
plt.title('Annual Range (2020-2023 average) of Wetland Area')
plt.show()









