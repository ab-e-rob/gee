import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# Read stats\min_max_months_combined_grouped.csv
df_min_max_months_combined_grouped = pd.read_csv('stats\min_max_months_combined_grouped.csv')

print(df_min_max_months_combined_grouped)

data = {
    "Wetland name": [
        "Aloppkolen", "Annsjon", "Askoviken", "Asnen", "Blaikfjallet", "Blekinge",
        "Dattern", "Dummemosse", "Eman", "Falsterbo", "Farnebjofarden", "Fyllean",
        "Gammelstadsviken", "Getapulien", "Getteron", "Gotlands", "Gullhog",
        "Gustavsmurane", "Helge", "Hjalstaviken", "Hornborgasjon", "Hovranomradet",
        "Kallgate", "Kilsviken", "Klingavalsan", "Komosse", "Koppangen", "Kvismaren",
        "Laidaure", "Lundakrabukten", "Maanavuoma", "Mellanljusnan", "Mellerston",
        "Morrumsan", "Mossatrask", "Nittalven", "Nordrealvs", "Olands", "Oldflan",
        "Oset", "Osten", "Ottenby", "Ovresulan", "Paivavouma", "Persöfjärden",
        "Pirttimysvuoma", "Rappomyran", "Sikasvagarna", "Sjaunja", "Skalderviken",
        "Stigfjorden", "Storemosse", "Storkolen", "Svartadalen", "Svenskahog",
        "Svenskundsviken", "Takern", "Tarnasjon", "Tavvovouma", "Tjalmejaure",
        "Tonnersjoheden", "Traslovslage", "Tysoarna", "Umealvens", "Vasikkavouma",
        "Vastraroxen", "Vattenan"
    ],
    "Latitude": [
        62.64, 63.2736, 59.4744, 56.6317, 64.6425, 56.1236, 58.3911, 57.7758, 57.1447,
        55.4367, 60.2172, 56.6611, 65.6317, 59.662, 57.1328, 57.2717, 62.1875, 60.6069,
        55.9814, 59.6681, 58.3086, 60.335, 57.6781, 59.0456, 55.6517, 57.69, 61.3531,
        59.1739, 67.1339, 55.8233, 68.4631, 61.8422, 65.2022, 56.1536, 63.8342, 59.9039,
        57.7856, 56.7747, 63.7978, 59.2844, 58.5625, 56.2136, 62.5956, 66.6519, 65.775,
        68.2675, 66.3733, 63.6344, 67.39, 56.2325, 58.0931, 57.2853, 61.7828, 59.8778,
        59.4303, 58.6192, 58.352, 65.9367, 68.5114, 66.2467, 56.72, 56.9864, 63.2347,
        63.7367, 67.2272, 58.4839, 62.5933
    ]
}

df = pd.DataFrame(data)
print(df)

# combine df and df_min_max_months_combined_grouped based on wrtland and discard the rest
df = pd.merge(df, df_min_max_months_combined_grouped, left_on='Wetland name', right_on='Name', how='inner')
print(df)


# Set font
plt.rcParams['font.sans-serif'] = "Tahoma"

# Set border properties
plt.rcParams['axes.linewidth'] = 2
plt.rcParams['axes.edgecolor'] = 'black'
plt.rcParams['grid.color'] = 'black'
plt.rcParams['grid.linewidth'] = 0.5

# Create a figure with adjusted layout
plt.figure(figsize=(26, 25))
plt.subplots_adjust(top=0.90, bottom=0.2)

# Use Seaborn scatterplot
sns.scatterplot(x='Latitude', y='Max_Month', data=df, s=300, color='#1b9e77', edgecolor='black')


# add regression line and r2
sns.regplot(x='Latitude', y='Max_Month', data=df, scatter=False, color='black', label='Regression Line')



# Customize tick font size
plt.xticks(fontsize=40)
plt.yticks(fontsize=40)

# Set x and y axis labels
plt.xlabel('Latitude (°N)', fontsize=40)
plt.ylabel('Month', fontsize=40)

# Customize y-axis ticks to display month names
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
plt.yticks(range(1, 13), months, fontsize=40)

# Set background color
plt.gca().set_facecolor('#E3E5E2')

# Save the plot
plt.savefig(r'C:\Users\abro3569\PycharmProjects\gee\combined_plots\lat_vs_max_month.svg', facecolor='#E3E5E2')

# Show the plot
plt.show()

# plot a histogram of the max months
# change size of plot
plt.figure(figsize=(20, 16))
# centre bins over x ticks
# Calculate the bin edges to center the bars on x ticks
bin_edges = list(range(1, 14))  # 13 edges to create 12 bins
bin_centers = [0.5 * (bin_edges[i] + bin_edges[i + 1]) for i in range(len(bin_edges) - 1)]


# Plot histogram with centered bars
plt.hist(df['Max_Month'], bins=bin_edges, color='#d95f02', edgecolor='black')
plt.xticks(bin_centers, range(1, 13))
plt.xlabel('')
plt.ylabel('Frequency (No. of Wetlands)', fontsize=40)

# rotate the whole plot by 90 degrees
plt.yticks(rotation=90, fontsize=40)
plt.xticks(rotation=90, fontsize=40)

# reverse the order of the x axis 12-1 instead of 1-12
plt.gca().invert_xaxis()



# Set background color
plt.gca().set_facecolor('#E3E5E2')

# Save the plot
plt.savefig(r'C:\Users\abro3569\PycharmProjects\gee\combined_plots\max_month_histogram.svg', facecolor='#E3E5E2')

plt.show()



