import os
import ee
from dotenv import load_dotenv
from utils import get_aoi

# Initialize Earth Engine
ee.Initialize()

aoi_list = get_aoi.get_all_aois()

# Define the years for which you want to obtain composites.
startYear = 2020
endYear = 2023

# Loop through each AOI.
for aoi_name, roi in aoi_list.items():  # Iterate through dictionary items.
    # Create an empty image collection to store the monthly dynamic world images
    dw_collection = ee.ImageCollection([])

    # Loop through each month.
    for month in range(1, 13):
        # Define the start and end dates for the current month.
        startDate = ee.Date.fromYMD(startYear, month, 1)
        endDate = startDate.advance(1, 'month')

        # Filter the Sentinel-2 data by date, cloud cover, and location.
        collection = (ee.ImageCollection('GOOGLE/DYNAMICWORLD/V1')
                      .filterDate(startDate, endDate)
                      .filterBounds(roi))

        # Select the 'label' band from the collection.
        classification = collection.select('label')

        # Create a composite by reducing the collection to the mode (most frequent) value.
        dwComposite = classification.reduce(ee.Reducer.mode())




        export_dwComposite = dwComposite.byte().unmask(-9999)  # Convert to byte type

        task = ee.batch.Export.image.toDrive(export_dwComposite,
                                             description=aoi_name + '_' + str(startYear) + '_' + str(month),
                                             # Name for the exported file
                                             scale=10,
                                             folder='dynamic_world_' + aoi_name,  # Use the AOI name for the folder
                                             region=roi.getInfo()['coordinates'],
                                             maxPixels=1e10
                                             )
        task.start()

        print(f'Exporting Dynamic World image to Google Drive: {aoi_name}, month {month}')
