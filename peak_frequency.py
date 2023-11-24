import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np

from utils import read_model_results


wetland_names = ['Aloppkolen', 'Annsjon', 'Askoviken', 'Asnen', 'Eman', 'Farnebofjarden',
                 'Fyllean', 'Gammelstadsviken', 'Getapulien', 'Hjalstaviken', 'Kallgate',
                 'Komosse', 'Koppangen','Laidaure', 'Mellerston','Maanavuoma', 'Nittalven', 'Oldflan', 'Osten',
                 'Persofjarden','Skalderviken', 'Storremosse', 'Takern', 'Tarnsjon', 'Tavvovouma', 'Tysoarna','Vasikkavouma']


#wetland_names = ['Oldflan']

def peak_frequency(df, model_name, wetland_name):
    # Convert 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Extract year and month from 'Date' column
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month

    # Create a new column for the adjusted year
    df['Adjusted_Year'] = df['Year']
    df.loc[df['Month'] < 8, 'Adjusted_Year'] -= 1

    # Calculate the 90th percentile value for each adjusted year
    thresholds = df.groupby('Adjusted_Year')['Area (metres squared)'].quantile(0.9)

    # Find peaks in each adjusted year and store in a list
    peaks = []
    for year, threshold in thresholds.items():
        year_data = df[(df['Adjusted_Year'] == year)]['Area (metres squared)']
        year_peaks, _ = find_peaks(year_data, height=threshold)
        peaks.extend(year_data.index[year_peaks])

    # Extract the year from the index for the peaks
    peak_years = df['Year'].loc[peaks]

    # Count the number of peaks in each year
    peak_count_per_year = peak_years.value_counts().sort_index()

    # Plot the bar chart
    plt.bar(peak_count_per_year.index, peak_count_per_year)
    plt.xlabel('Year')
    plt.ylabel('Number of Peaks')
    plt.title(f'Number of Peaks per Year - {model_name} - {wetland_name}')
    plt.show()

    # Mark the identified peaks on the plot
    plt.plot(df['Date'], df['Area (metres squared)'], label='Original Data')
    plt.plot(df['Date'].loc[peaks], df['Area (metres squared)'].loc[peaks], 'r.', markersize=10, label='Prominent Peaks')
    plt.xlabel('Date')
    plt.ylabel('Area (metres squared)')
    plt.title(f'Yearly Wetland Area with Prominent Peaks - {model_name} - {wetland_name}')
    plt.legend()
    plt.show()

    return peak_count_per_year

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

    # Calculate peaks for the current wetland
    wetland_peaks = peak_frequency(da_df, 'Deep Aqua', wetland_name)

    # Add the results to the combined DataFrame
    combined_results[f'{wetland_name}'] = wetland_peaks

# Save the combined results to a CSV file
combined_results.to_csv('stats\combined_peak_frequency_results.csv')


