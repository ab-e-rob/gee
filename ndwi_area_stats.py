import pandas as pd
import os
import calendar
import matplotlib.pyplot as plt

wetland_names = ['Aloppkolen']

# Locate csv file and load as a dataframe
file_path = r'Z:\ndwi\area\Aloppkolen.csv'
df = pd.read_csv(file_path, delimiter=',', header=0)

# Extract year and month
df['year'] = df['Polygon Name'].str.extract(r'year_(\d+)').astype(int)
df['month'] = df['Polygon Name'].str.extract(r'month_(\d+)').astype(int)

# Create a new column with the desired format
df['Date'] = df['month'].apply(lambda x: f'{x:02d}') + '/' + df['year'].astype(str)

# Give df a new name
df['Name'] = wetland_names * len(df)

# Remove the old columns
df = df.drop('Polygon Name', axis=1)
df = df.drop('year', axis=1)
df = df.drop('month', axis=1)

# Rearrange the old columns
df = df[['Name', 'Date', 'Area (square meters)']]

# Display the DataFrame
print(df)

# now plot
# Convert 'new_column' to datetime for proper plotting
df['Date'] = pd.to_datetime(df['Date'], format='%m/%Y')

# Create the scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(df['Date'], df['Area (square meters)'], s=70)
plt.xlabel('Date')
plt.ylabel('Area (m^2)')
plt.title('Wetland Area from NDWI (2020-2023)')

# Disable scientific notation for the y-axis
#plt.gca().get_yaxis().get_major_formatter().set_scientific(False)

plt.savefig(f'{wetland_names}.png')

plt.show()



