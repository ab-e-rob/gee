import os
import rasterio.features
from shapely.geometry import shape, MultiPolygon
import geopandas as gpd
import csv

raster_path = (r'C:\Users\abro3569\PycharmProjects\deep-wetlands-new\data\results\big-2020_Askoviken_exported_images\20200513_S1A_IW_GRDH_1SDV_20200513T051518_20200513T051543_032542_03C4E0_7498.tif_pred.tif')

utm_crs = "EPSG:32633"

# Use a context manager to open the raster file
with rasterio.open(raster_path) as src:
    # Read the first band
    binary_array = src.read(1)

    # Make sure you read the transform inside the context manager
    transform = src.transform

    # Get shapes (polygons)
    shapes = list(rasterio.features.shapes(binary_array, transform=transform))

    # Extract polygons with values 0 and 3 using a list comprehension
    polygons = [shape(geom) for geom, value in shapes if value in [1]]

    # Dissolve the polygons into a single polygon and buffer it by 0 (no buffer)
    dissolved_polygon = MultiPolygon(polygons).buffer(0)

    # Create a GeoDataFrame with the dissolved polygon
    dissolved_gdf = gpd.GeoDataFrame(geometry=[dissolved_polygon])

    # Set the CRS of the GeoDataFrame to WGS84 (EPSG:4326)
    dissolved_gdf.crs = "EPSG:4326"

    # Reproject the GeoDataFrame to UTM (or your desired projected CRS)
    dissolved_gdf = dissolved_gdf.to_crs(utm_crs)

    # Calculate the area in square meters (m²) in the projected CRS
    area_utm = dissolved_gdf.geometry.area.iloc[0]

    # Test save as shapefile
    dissolved_gdf.to_file(f'20200513_S1A_IW_GRDH_1SDV_20200513T051518_20200513T051543_032542_03C4E0_7498.shp')

    # Optionally, you can print the area for each raster
    print(f" Area (UTM): {area_utm} m²")

