import pandas as pd



from utils import read_model_results

wetland_names = ['Aloppkolen', 'Annsjon', 'Askoviken', 'Asnen', 'Eman', 'Farnebofjarden',
                 'Fyllean', 'Gammelstadsviken', 'Getapulien', 'Hjalstaviken', 'Kallgate',
                 'Komosse', 'Koppangen','Laidaure', 'Mellerston','Maanavuoma', 'Nittalven', 'Oldflan', 'Osten',
                 'Persofjarden','Skalderviken', 'Storremosse', 'Takern', 'Tarnsjon', 'Tavvovouma', 'Tysoarna','Vasikkavouma']


def calc_range(df, model_name, wetland_name):
    # Create a new dataframe to store the results
    range_df = pd.DataFrame(columns=['Dataset', 'Name', 'Year', 'Range'])

    # Loop through each year
    for year in range(2020, 2024):
        # Extract the year from the date column which is in YYYY-MM-DD format and convert to integer
        year_df = df[df['Date'].dt.year == year]  # Assuming 'Date' is the column containing the date information

        # Check if there is data for the current year
        if not year_df.empty:
            # Calculate the range of the area (metres squared) column
            area_range = year_df['Area (metres squared)'].max() - year_df['Area (metres squared)'].min()

            # Store the results in the dataframe
            range_df = pd.concat([range_df, pd.DataFrame(
                {'Dataset': [model_name], 'Name': [wetland_name], 'Year': [year], 'Range': [area_range]})],
                                 ignore_index=True)

    return range_df

def calc_max_min_month(df, model_name, wetland_name):
    # Create a new dataframe to store the results
    month_range_df = pd.DataFrame(columns=['Dataset', 'Name', 'Year', 'Max_Month', 'Min_Month'])

    # Loop through each year
    for year in range(2020, 2024):
        # Extract the year from the date column which is in YYYY-MM-DD format and convert to integer
        year_df = df[df['Date'].dt.year == year]  # Assuming 'Date' is the column containing the date information

        # Check if there is data for the current year
        if not year_df.empty:
            # Find the maximum and minimum month based on the 'Area' column
            max_month = year_df.loc[year_df['Area (metres squared)'].idxmax()]['Date'].month
            min_month = year_df.loc[year_df['Area (metres squared)'].idxmin()]['Date'].month

            # Store the results in the dataframe
            month_range_df = pd.concat([month_range_df, pd.DataFrame({
                'Dataset': [model_name],
                'Name': [wetland_name],
                'Year': [year],
                'Max_Month': [max_month],
                'Min_Month': [min_month]
            })], ignore_index=True)

    return month_range_df


def calc_mean_monthly_area(df, model_name, wetland_name):
    # Create a new dataframe to store the results
    mean_monthly_area_df = pd.DataFrame(columns=['Dataset', 'Name', 'Year', 'Month', 'Mean_Area'])

    # Extract data for the years 2020 to 2023
    selected_years_df = df[(df['Date'].dt.year >= 2020) & (df['Date'].dt.year <= 2023)]

    # Loop through each month
    for month in range(1, 13):
        # Extract data for the current month
        month_df = selected_years_df[selected_years_df['Date'].dt.month == month]

        # Check if there is data for the current month
        if not month_df.empty:
            # Calculate the mean area for the current month
            mean_area = month_df['Area (metres squared)'].mean()

            # Store the results in the dataframe
            mean_monthly_area_df = pd.concat([mean_monthly_area_df, pd.DataFrame({
                'Dataset': [model_name],
                'Name': [wetland_name],
                'Year': [2020],  # Using a placeholder year as the calculation is across multiple years
                'Month': [month],
                'Mean_Area': [mean_area]
            })], ignore_index=True)

    return mean_monthly_area_df

def calc_avg_area(df, model_name, wetland_name):
    # Create a new dataframe to store the results
    avg_area_df = pd.DataFrame(columns=['Dataset', 'Name', 'Avg_Area'])

    # Calculate the average area for the entire dataset
    avg_area = df['Area (metres squared)'].mean()

    # Store the results in the dataframe
    avg_area_df = pd.concat([avg_area_df, pd.DataFrame({
        'Dataset': [model_name],
        'Name': [wetland_name],
        'Avg_Area': [avg_area]
    })], ignore_index=True)

    return avg_area_df


# Initialize empty dataframes to store combined results
combined_range = pd.DataFrame(columns=['Dataset', 'Name', 'Year', 'Range'])
combined_month_range = pd.DataFrame(columns=['Dataset', 'Name', 'Year', 'Max_Month', 'Min_Month'])
combined_mean_monthly_area = pd.DataFrame(columns=['Dataset', 'Name', 'Year', 'Month', 'Mean_Area'])
combined_avg_area = pd.DataFrame(columns=['Dataset', 'Name', 'Avg_Area'])  # New dataframe for average area

for wetland_name in wetland_names:
    # Locate csv files and load as dataframes
    dynamic_world = r'C:\Users\abro3569\PycharmProjects\gee\dyn_w_area\\' + wetland_name + '.csv'
    ndwi = r'C:\Users\abro3569\PycharmProjects\gee\ndwi_area\\' + wetland_name + '.csv'
    deep_aqua = r'C:\Users\abro3569\PycharmProjects\deep-wetlands-new\data\results\big-2020_' + wetland_name + '_water_estimates_NEW_POLYGONISED.csv'

    # Read each of the datasets using code from utils
    read_model_results.read_dynamic_world(wetland_name, dynamic_world)
    read_model_results.read_ndwi(wetland_name, ndwi)
    read_model_results.read_deepaqua(wetland_name, deep_aqua)

    dw_df = read_model_results.dw_df
    ndwi_df = read_model_results.ndwi_df
    da_df = read_model_results.new_da_df

    # Convert date column to datetime for proper plotting
    dw_df['Date'] = pd.to_datetime(dw_df['Date'], format='%m/%Y')
    ndwi_df['Date'] = pd.to_datetime(ndwi_df['Date'], format='%m/%Y')
    da_df['Date'] = pd.to_datetime(da_df['Date'], format='%m/%Y')

    # Calculate the range for each dataset
    dw_range = calc_range(dw_df, 'Dynamic World', wetland_name)
    ndwi_range = calc_range(ndwi_df, 'NDWI', wetland_name)
    da_range = calc_range(da_df, 'Deep Aqua', wetland_name)

    # Combine the results
    combined_range = pd.concat([combined_range, dw_range, ndwi_range, da_range], ignore_index=True)

    # Calculate the max and min month for each dataset
    dw_month_range = calc_max_min_month(dw_df, 'Dynamic World', wetland_name)
    ndwi_month_range = calc_max_min_month(ndwi_df, 'NDWI', wetland_name)
    da_month_range = calc_max_min_month(da_df, 'Deep Aqua', wetland_name)

    # Combine the results
    combined_month_range = pd.concat([combined_month_range, dw_month_range, ndwi_month_range, da_month_range],
                                     ignore_index=True)

    # Calculate the mean monthly area for each dataset
    dw_mean_monthly_area = calc_mean_monthly_area(dw_df, 'Dynamic World', wetland_name)
    ndwi_mean_monthly_area = calc_mean_monthly_area(ndwi_df, 'NDWI', wetland_name)
    da_mean_monthly_area = calc_mean_monthly_area(da_df, 'Deep Aqua', wetland_name)

    # Combine the results
    combined_mean_monthly_area = pd.concat(
        [combined_mean_monthly_area, dw_mean_monthly_area, ndwi_mean_monthly_area, da_mean_monthly_area],
        ignore_index=True)

    # Calculate the average area for each dataset
    dw_avg_area = calc_avg_area(dw_df, 'Dynamic World', wetland_name)
    ndwi_avg_area = calc_avg_area(ndwi_df, 'NDWI', wetland_name)
    da_avg_area = calc_avg_area(da_df, 'Deep Aqua', wetland_name)

    # Combine the results
    combined_avg_area = pd.concat([combined_avg_area, dw_avg_area, ndwi_avg_area, da_avg_area], ignore_index=True)

# Save the combined results to a CSV file
combined_range.to_csv(r'C:\Users\abro3569\PycharmProjects\gee\stats\yearly_range_combined.csv', index=False)
combined_month_range.to_csv(r'C:\Users\abro3569\PycharmProjects\gee\stats\min_max_months_combined.csv', index=False)
combined_mean_monthly_area.to_csv(r'C:\Users\abro3569\PycharmProjects\gee\stats\mean_monthly_area_combined.csv', index=False)
combined_avg_area.to_csv(r'C:\Users\abro3569\PycharmProjects\gee\stats\avg_area_combined.csv', index=False)