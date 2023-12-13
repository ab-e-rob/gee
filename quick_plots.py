import pandas as pd
import matplotlib.pyplot as plt

# Replace 'your_file_path.csv' with the path to your CSV file
csv_file_path = r'D:\GIS_practical\depth_processing\table.csv'

# Read CSV into a Pandas DataFrame
df = pd.read_csv(csv_file_path)

# Plot NDWI against lake depth
plt.scatter(df.iloc[:, 0], df.iloc[:, 1], s=10)
plt.xlabel(df.columns[0])  # Set X-axis label
plt.ylabel(df.columns[1])  # Set Y-axis label
plt.title('NDWI vs Lake Depth')
plt.show()

# Group by lake depth (x-axis) and calculate mean for NDWI (y-axis)
grouped_data = df.groupby(df.columns[0]).agg({df.columns[1]: 'mean'}).reset_index()

# Plot mean values
# change size of dot

plt.plot(grouped_data[df.columns[0]], grouped_data[df.columns[1]], 'o-', label='Mean NDWI', s=10)
plt.xlabel(df.columns[0])  # Set X-axis label
plt.ylabel(f'Mean of {df.columns[1]}')  # Set Y-axis label
plt.title(f'Mean NDWI Plot for {df.columns[1]}')
plt.legend()
plt.show()
