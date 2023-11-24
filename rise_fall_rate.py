import pandas as pd
import matplotlib.pyplot as plt
from utils import read_model_results
import numpy as np


wetland_names = ['Aloppkolen', 'Annsjon', 'Askoviken', 'Asnen', 'Eman', 'Farnebofjarden',
                 'Fyllean', 'Gammelstadsviken', 'Getapulien', 'Hjalstaviken', 'Kallgate',
                 'Komosse', 'Koppangen','Laidaure', 'Mellerston','Maanavuoma', 'Nittalven', 'Oldflan', 'Osten',
                 'Persofjarden','Skalderviken', 'Storremosse', 'Takern', 'Tarnsjon', 'Tavvovouma', 'Tysoarna','Vasikkavouma']

#wetland_names = ['Oldflan']

def limb_rates(df, model_name, wetland_name):
    # Create a new dataframe to store the results
    mean_monthly_area_df = pd.DataFrame(columns=['Dataset', 'Name', 'Year', 'Month', 'Mean_Area', 'Std_Area'])

    # Extract data for the years 2020 to 2023
    selected_years_df = df[(df['Date'].dt.year >= 2020) & (df['Date'].dt.year <= 2023)]

    # Loop through each month
    for month in range(1, 13):
        # Extract data for the current month
        month_df = selected_years_df[selected_years_df['Date'].dt.month == month]

        # Check if there is data for the current month
        if not month_df.empty:
            # Replace NaN values with a placeholder value (e.g., 0)
            month_df['Area (metres squared)'] = month_df['Area (metres squared)'].replace(np.nan, 0)

            # Calculate the mean and standard deviation of the area for the current month
            mean_area = month_df['Area (metres squared)'].mean()
            std_area = month_df['Area (metres squared)'].std()

            # Store the results in the dataframe
            mean_monthly_area_df = pd.concat([mean_monthly_area_df, pd.DataFrame({
                'Dataset': [model_name],
                'Name': [wetland_name],
                'Year': [month_df['Date'].dt.year.iloc[0]],  # Use the year of the first date in the current month
                'Month': [month],
                'Mean_Area': [mean_area],
                'Std_Area': [std_area]
            })], ignore_index=True)

    # Sort the dataframe by Year and Month for proper plotting
    mean_monthly_area_df.sort_values(['Year', 'Month'], inplace=True)

    # convert month to datetime
    mean_monthly_area_df['Month'] = pd.to_datetime(mean_monthly_area_df['Month'], format='%m')

    # Calculate the first derivative to identify the rate of change
    mean_monthly_area_df['Rate_of_change'] = np.gradient(mean_monthly_area_df['Mean_Area'])

    # Identify rising and falling limbs based on the rate of change
    rising_limb = mean_monthly_area_df[mean_monthly_area_df['Rate_of_change'] > 0]
    falling_limb = mean_monthly_area_df[mean_monthly_area_df['Rate_of_change'] < 0]

    # Calculate the average rate of change for the rising limb and falling limb
    avg_rising_rate = rising_limb['Rate_of_change'].mean()
    avg_falling_rate = falling_limb['Rate_of_change'].mean()

    # Create a summary dataframe
    summary_df = pd.DataFrame({
        'Dataset': [model_name],
        'Name': [wetland_name],
        'Avg_Rising_Rate': [avg_rising_rate],
        'Avg_Falling_Rate': [avg_falling_rate]
    })

    # Plot the rate of change
    plt.plot(mean_monthly_area_df['Month'], mean_monthly_area_df['Rate_of_change'])
    plt.xlabel('Month')
    plt.ylabel('Rate of Change')
    plt.title('Rate of Change in Yearly Time Series')
    plt.show()

    # Plot the mean monthly area as a buffer that is the standard deviation of the values for each month
    plt.plot(mean_monthly_area_df['Month'], mean_monthly_area_df['Mean_Area'], label='Mean Area')
    plt.fill_between(mean_monthly_area_df['Month'],
                     mean_monthly_area_df['Mean_Area'] - mean_monthly_area_df['Std_Area'],
                     mean_monthly_area_df['Mean_Area'] + mean_monthly_area_df['Std_Area'],
                     alpha=0.5, label='Standard Deviation')

    plt.xticks(mean_monthly_area_df['Month'], mean_monthly_area_df['Month'].dt.strftime('%b'))
    plt.ylabel('Mean Area (metres squared)')
    plt.title(f'Mean Monthly Area - {model_name} - {wetland_name}')
    plt.legend()
    plt.show()

    return summary_df

# Create an empty DataFrame to accumulate results
combined_results = pd.DataFrame()


# Loop through each wetland
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

    # Call function
    limb_rates_df = limb_rates(da_df, 'Deep Aqua', wetland_name)

    # Add the results to the combined DataFrame using concat
    combined_results = pd.concat([combined_results, limb_rates_df], axis=0)

# Save the combined results to a CSV file
combined_results.to_csv('stats/combined_limb_rates_results.csv', index=False)


