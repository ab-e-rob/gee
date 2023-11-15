import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

wetland_name = 'Komosse'

# Locate csv file and load as a dataframe
dynamic_world = r'C:\Users\abro3569\PycharmProjects\gee\dyn_w_area\\' + wetland_name + '.csv'
ndwi = r'C:\Users\abro3569\PycharmProjects\gee\ndwi_area\\' + wetland_name + '.csv'
deep_aqua = r'C:\Users\abro3569\PycharmProjects\deep-wetlands-new\data\results\big-2020_' + wetland_name + '_water_estimates_NEW_POLYGONISED.csv'
precip = r'C:\Users\abro3569\Documents\ArcGIS\Projects\seasonal_var\monthly_precip_all_wetlands.csv'

def read_precip():
    global precip_df

    precip_df = pd.read_csv(precip, delimiter=',', header=0)

    # Rename StdTime column to 'Date'
    precip_df = precip_df.rename(columns={'StdTime': 'Date'})

    # Convert Date column (format MM/DD/YYYY) to datetime format (YYYY-MM-DD)
    precip_df['Date'] = pd.to_datetime(precip_df['Date'], format='%m/%d/%Y')

    # Reset the time so that it is the first of every month
    precip_df['Date'] = precip_df['Date'].dt.strftime('%Y-%m-01')

    # Convert Date column back to datetime format
    precip_df['Date'] = pd.to_datetime(precip_df['Date'], format='%Y-%m-%d')

    # Extract column name based on which wetland is being plotted
    precip_df = precip_df[['Date', wetland_name]]

    # Display the DataFrame
    print(precip_df)

    return


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
    print(dw_df)

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
    # Create a figure with a size of 12x8 inches
    fig, ax1 = plt.subplots(figsize=(12, 8))

    # Scatter plots for Dynamic World, NDWI, and Deep Aqua
    ax1.scatter(dw_df['Date'], dw_df['Area (metres squared)'], s=20, c='red', label='Dynamic World')
    ax1.scatter(ndwi_df['Date'], ndwi_df['Area (metres squared)'], s=20, c='black', label='NDWI')
    ax1.scatter(new_da_df['Date'], new_da_df['Area (metres squared)'], s=20, c='blue', label='Deep Aqua')

    # Create a secondary y-axis for precipitation
    ax2 = ax1.twinx()
    ax2.plot(precip_df['Date'], precip_df[wetland_name], color='green', label='Precipitation (mm)')
    ax2.set_ylabel('Precipitation (mm)')
    ax2.tick_params(axis='y')
    ax2.legend(loc='upper left')

    # Set x-axis ticks and labels
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=90, fontsize=9)

    # Set axis labels and plot title
    ax1.set_xlabel('Date')
    ax1.set_ylabel(r'Area ($m^2$)')
    ax1.legend()
    plt.title(f'{wetland_name} Area (2020-2023)')

    # Save and show the plot
    plt.tight_layout()
    plt.savefig(f'C:\\Users\\abro3569\\PycharmProjects\\gee\\precip_plots\\{wetland_name}_combined_precip.png')
    plt.show()


read_precip()
read_dynamic_world()
read_ndwi()
read_deepaqua()
plot()


