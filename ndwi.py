# import dependencies
import os
import ee
from utils import get_aoi
from dotenv import load_dotenv
import geetools

# Initialize Earth Engine
ee.Initialize()

# Load environment variables
load_dotenv()

def export_ndwi(area_name):
    roi = get_aoi.get_area_of_interest(area_name)

    def clip_image(image):
        return image.clip(roi)

    def create_ndwi(image):
        ndwi = image.normalizedDifference(['B3', 'B8']).rename('NDWI')

        return image

    collection = ee.ImageCollection('COPERNICUS/S2')\
        .filterDate(os.getenv('START_DATE'), os.getenv('END_DATE'))\
        .filterBounds(roi)\
        .filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE', int(os.getenv('CLOUD_PERCENTAGE'))))\
        .map(clip_image)\
        .map(create_ndwi)

    print('NDWI collection size:', collection.size().getInfo())

    # batch export to Google Drive
    geetools.batch.Export.imagecollection.toDrive(
        collection,
        f'export_{area_name}_ndwi',
        namePattern='{id}',
        scale=10,
        dataType="float",
        region=roi,
        crs='EPSG:4326',
        datePattern=None,
        extra=None,
        verbose=False
    )

export_ndwi(os.getenv('AOI'))