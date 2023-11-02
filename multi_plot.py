import pandas as pd
import matplotlib.pyplot as plt

wetland_name = 'Askoviken'

# Locate csv file and load as a dataframe
dynamic_world = r'C:\Users\abro3569\PycharmProjects\gee\dyn_w_area\\' + wetland_name + '.csv'
ndwi = r'C:\Users\abro3569\PycharmProjects\gee\ndwi_area\\' + wetland_name + '.csv'
deep_aqua = r'C:\Users\abro3569\PycharmProjects\deep-wetlands-new\data\results\big-2020_' + wetland_name + '_water_estimates.csv'

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
    print(ndwi_df)

    return

def read_deepaqua():
    global da_df

    da_df = pd.read_csv(deep_aqua, delimiter=',', header=0)

    # Extract the area and date and give them new names
    new_names = ['Area (metres squared)', 'Date']
    da_df = da_df.iloc[:, [2, 3]]
    da_df.columns = new_names

    # Add name column
    da_df['Name'] = wetland_name

    # Rearrange the old columns
    da_df = da_df[['Name', 'Date', 'Area (metres squared)']]

    print(da_df)

    return

def plot():
    plt.figure(figsize=(8, 6))
    plt.scatter(dw_df['Date'], dw_df['Area (metres squared)'], s=40, c='red', label='Dynamic World')
    plt.scatter(ndwi_df['Date'], ndwi_df['Area (metres squared)'], s=40, c='black', label='NDWI')
    plt.scatter(da_df['Date'], da_df['Area (metres squared)'], s=40, c='blue', label='Deep Aqua')
    plt.xlabel('Date')
    plt.ylabel('Area (m^2)')
    #plt.ylim(0, 1e8)
    plt.legend()
    plt.title(f'{wetland_name} Area (2020-2023)')

    # Save and show the plot
    plt.savefig(r'C:\Users\abro3569\PycharmProjects\gee\combined_plots\\' + wetland_name + '_combined_plot.png')
    plt.show()

    return



read_dynamic_world()
read_ndwi()
read_deepaqua()
plot()

