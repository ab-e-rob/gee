import os
import ee
from utils import get_aoi
from dotenv import load_dotenv

# Initialize Earth Engine
ee.Initialize()

# Load environment variables
load_dotenv()

roi = get_aoi.get_area_of_interest(os.getenv('AOI'))

# Define a date range for the entire year.
startYear = 2022
endYear = 2022

# Create an empty image collection to store the monthly NDWI masks.
ndwiMaskCollection = ee.ImageCollection([])

# Loop through each month.
for month in range(1, 13):
    # Define the start and end dates for the current month.
    startDate = ee.Date.fromYMD(startYear, month, 1)
    endDate = ee.Date.fromYMD(startYear, month, 28)  # Adjust end date as needed.

    # Filter the Sentinel-2 data by date, cloud cover, and location.
    collection = (ee.ImageCollection('COPERNICUS/S2')
                  .filterBounds(roi)
                  .filterDate(startDate, endDate)
                  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10)))  # Adjust cloud cover threshold as needed.

    # Check if there are composites available for the current month.
    compositeCount = collection.size().getInfo()
    if compositeCount == 0:
        print('No composites available for Month', month)
        continue  # Skip this month and move to the next.

    # Create a composite by reducing the collection to the median value.
    composite = collection.median()

    # Calculate NDWI for the composite image.
    ndwi = composite.normalizedDifference(['B3', 'B8'])

    # Define a threshold for NDWI to identify open water.
    ndwiThreshold = 0  # You can adjust this threshold as needed.

    # Create a binary mask where 1 represents open water and 0 represents background.
    waterMask = ndwi.gt(ndwiThreshold)

    # Clip the water mask to the ROI (polygon).
    waterMaskClipped = waterMask.clip(roi)

    # Add the water mask to the collection only if it has bands.
    if waterMask.bandNames().size().getInfo() > 0:
        ndwiMaskCollection = ndwiMaskCollection.merge(ee.ImageCollection([waterMaskClipped.set('month', month)]))

    # Export the water mask to Google Drive for the current month.
    exportWaterMask = waterMaskClipped.unmask(0).byte()  # Convert to byte type
    task = ee.batch.Export.image.toDrive(exportWaterMask,
        description='water_mask_month_' + str(month),  # Name for the exported file
        scale=10,
        folder='test_ndwi_mask',
        region=roi.getInfo()['coordinates'],
        maxPixels=1e10
    )
    task.start()
