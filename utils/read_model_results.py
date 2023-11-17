import pandas as pd

def read_dynamic_world(wetland_name, dynamic_world):
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
    print(f'Dynamic world:\n{dw_df.head()}')

    return

def read_ndwi(wetland_name, ndwi):
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
    print(f'NDWI:\n{ndwi_df.head()}')

    return

def read_deepaqua(wetland_name, deep_aqua):
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

    print(f'Deep Aqua:\n{new_da_df.head()}')

    return new_da_df