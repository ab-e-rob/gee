import geopandas as gpd
from dotenv import load_dotenv
import rasterio
import numpy as np
import pandas as pd
from rasterio.features import geometry_mask
from rasterio.mask import mask
import os
from shapely.geometry import shape
from osgeo import gdal, osr
import pyproj

os.environ['PROJ_LIB'] =pyproj.datadir.get_data_dir()

# Load .env file
load_dotenv()

# Open the shapefile and get
shapefile_name = os.getenv('AOI')
shapefile_path = os.path.join(r'Z:\ramsar_sweden\ramsar_polygons_by_name', shapefile_name + '_shp.shp')

# Specify the folder containing NDWI rasters
ndwi_raster_folder = r'Z:\ndwi\NDWI_mask_Farnebjofarden\20220128T101301_20220128T101258_T33VWG.tif'

# Output path

output_path = r'Z:\ndwi\test_clip.tif'

gdal.Warp(output_path, ndwi_raster_folder, format='GTiff', cutlineDSName=shapefile_path)