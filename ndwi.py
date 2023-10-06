# import dependencies
import os
import ee
from utils import get_aoi
from dotenv import load_dotenv

# Initialize Earth Engine
ee.Initialize()

# Load environment variables
load_dotenv()

# Get the Area of Interest (AOI)
bbox = get_aoi.get_area_of_interest(os.getenv('AOI'))

# Import the MODIS NDWI dataset
sentinel2 = ee.ImageCollection("COPERNICUS/S2_HARMONIZED") \
    .filterDate(os.getenv('START_DATE'), os.getenv('END_DATE')) \
    .filterBounds(bbox) \
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', int(os.getenv('CLOUD_PERCENTAGE'))))

def calculate_ndwi(image):
    ndwi = image.normalizedDifference(['B3', 'B8'])  # NIR and Red bands
    return ndwi

# Map the function over the image collection and calculate the median
ndwi_collection = sentinel2.map(calculate_ndwi)
ndwi_median = ndwi_collection.median()

# Clip NDWI to the AOI
ndwi_clip = ndwi_median.clip(bbox)

# Set the output directory on Google Drive
output_dir = 'ndwi_export'

# Define the export parameters
export_params = {
    'image': ndwi_clip,
    'description': 'NDWI_Export',
    'folder': output_dir,
    'scale': 10,  # Adjust the scale as needed
    'region': bbox.bounds().getInfo()['coordinates'],
    'fileFormat': 'GeoTIFF',
}

# Start the export task
task = ee.batch.Export.image.toDrive(**export_params)
task.start()
