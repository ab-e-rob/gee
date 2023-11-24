import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

wetland_name = 'Koppangen'

# Locate csv file and load as a dataframe
dynamic_world = r'C:\Users\abro3569\PycharmProjects\gee\dyn_w_area\\' + wetland_name + '.csv'
ndwi = r'C:\Users\abro3569\PycharmProjects\gee\ndwi_area\\' + wetland_name + '.csv'
deep_aqua = r'C:\Users\abro3569\PycharmProjects\deep-wetlands-new\data\results\big-2020_' + wetland_name + '_water_estimates_NEW_POLYGONISED.csv'

def read_dynamic_world():
    global dw_df

    dw_df = pd.read_csv(dynamic_world, delimiter=',', header=0)

    # Extract year and month correctly
    dw_df[['year', 'month']] = dw_df['Filename'].str.extract(r'_(\d{4})_(\d+)\.tif')

    # Create a new column with the desired format
    dw_df['Date'] = dw_df['month'].str.zfill(2) + '/' + dw_df['year']

    # Give the DataFrame a new name
    dw_df['Name'] = wetland_name

    # Remove the old columns
    dw_df = dw_df.drop('Filename', axis=1)
    dw_df = dw_df.drop('year', axis=1)
    dw_df = dw_df.drop('month', axis=1)

    # Rearrange the old columns
    dw_df = dw_df[['Name', 'Date', 'Area (metres squared)']]

    # Convert date column to datetime for proper plotting
    dw_df['Date'] = pd.to_datetime(dw_df['Date'], format='%m/%Y')

    # Display the DataFrame
    #print(dw_df)

    return

def read_ndwi():
    global ndwi_df

    ndwi_df = pd.read_csv(ndwi, delimiter=',', header=0)

    # Extract year and month correctly
    ndwi_df[['year', 'month']] = ndwi_df['Filename'].str.extract(r'_(\d{4})_(\d+)\.tif')

    # Create a new column with the desired format
    ndwi_df['Date'] = ndwi_df['month'].str.zfill(2) + '/' + ndwi_df['year']

    # Give the DataFrame a new name
    ndwi_df['Name'] = wetland_name

    # Remove the old columns
    ndwi_df = ndwi_df.drop('Filename', axis=1)
    ndwi_df = ndwi_df.drop('year', axis=1)
    ndwi_df = ndwi_df.drop('month', axis=1)

    # Rearrange the old columns
    ndwi_df = ndwi_df[['Name', 'Date', 'Area (metres squared)']]

    # Convert date column to datetime for proper plotting
    ndwi_df['Date'] = pd.to_datetime(ndwi_df['Date'], format='%m/%Y')

    # Display the DataFrame
    #print(ndwi_df)

    return

def read_deepaqua():
    global da_df
    global new_da_df

    da_df = pd.read_csv(deep_aqua, delimiter=',', header=0)

    # Convert the 'Date' column to a datetime object with the correct format
    da_df['Date'] = pd.to_datetime(da_df['Date'], format='%Y-%m-%d %H:%M:%S')

    # Extract the month and year information from the 'Date' column
    da_df['Year'] = da_df['Date'].dt.year
    da_df['Month'] = da_df['Date'].dt.month

    # Group by 'Year' and 'Month', and calculate the mean of 'Area' for each group
    da_df = da_df.groupby(['Year', 'Month', 'Name'])['Area (metres squared)'].mean().reset_index()

    # Create a new DataFrame with columns 'Name', 'Date', and 'Area'
    new_da_df = da_df[['Name', 'Year', 'Month', 'Area (metres squared)']]

    # Rename the 'Year' and 'Month' columns to 'Date'
    new_da_df['Date'] = pd.to_datetime(new_da_df[['Year', 'Month']].assign(day=1))
    new_da_df = new_da_df[['Name', 'Date', 'Area (metres squared)']]

    print(new_da_df)

    return new_da_df

def plot():

    dw_df['Area (metres squared)'] = dw_df['Area (metres squared)'] / 10000
    ndwi_df['Area (metres squared)'] = ndwi_df['Area (metres squared)'] / 10000
    new_da_df['Area (metres squared)'] = new_da_df['Area (metres squared)'] / 10000
    # set font to Tahoma

    plt.rcParams['font.sans-serif'] = "Tahoma"
    # add main black border around plot AND CHANGE THICKNESS
    plt.rcParams['axes.linewidth'] = 2
    plt.rcParams['axes.edgecolor'] = 'black'
    # set black border and thickness with some thinner gridlines
    plt.rcParams['grid.color'] = 'black'
    plt.rcParams['grid.linewidth'] = 0.5


    plt.figure(figsize=(26, 16))
    # move the plot up
    plt.subplots_adjust(top=0.90, bottom=0.2)

    # Use Seaborn scatterplot instead of plt.scatter
    sns.scatterplot(x='Date', y='Area (metres squared)', data=dw_df, s=300, color='#1b9e77', edgecolor='black', label='Dynamic World')
    sns.scatterplot(x='Date', y='Area (metres squared)', data=ndwi_df, s=300, color='#d95f02', edgecolor='black', label='NDWI')
    sns.scatterplot(x='Date', y='Area (metres squared)', data=new_da_df, s=300, color='#7570b3', edgecolor='black', label='Deep Aqua')

    plt.xticks(rotation=90)
    # plot as Jan-22
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b-%y'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.xticks(fontsize=40)
    plt.yticks(fontsize=40)
    #plt.xlabel('Date')
    plt.ylabel(r'Area (ha)', fontsize=40)
    #plt.ylim(-100, 7000)
    # plot legend top right
    plt.legend(loc='upper right', fontsize=40, facecolor='#E3E5E2')
    plt.gca().set_facecolor('#E3E5E2')
    #plt.title(f'{wetland_name} Area (2020-2023)')

    # Save and show the plot
    plt.savefig(r'C:\Users\abro3569\PycharmProjects\gee\combined_plots\\' + wetland_name + '_combined_plot.svg',
                facecolor='#E3E5E2')
    plt.show()
    return



read_dynamic_world()
read_ndwi()
read_deepaqua()
plot()

