import os
import geopandas as gpd
import contextily as cx
import matplotlib.pyplot as plt
from rasterio.crs import CRS
from PIL import Image
import concurrent.futures

wetland_name = 'Askoviken'
model_type = 'ndwi'

# Get directory names

if model_type == 'ndwi':
    shapefiles = [f for f in os.listdir(r'C:\Users\abro3569\PycharmProjects\gee\test_shps\ndwi') if
                  wetland_name in f and model_type in f and f.endswith('.shp')]

elif model_type == 'dw':
    shapefiles = [f for f in os.listdir(r'C:\Users\abro3569\PycharmProjects\gee\test_shps\dw') if
                  wetland_name in f and model_type in f and f.endswith('.shp')]

elif model_type == 'da':
    shapefiles = [f for f in os.listdir(r'C:\Users\abro3569\PycharmProjects\gee\test_shps\da') if
                  wetland_name in f and model_type in f and f.endswith('.shp')]

# Add an else statement or other handling if needed
else:
    print("Invalid model_type")

# Create a directory to save the images
output_dir = f'output_images_{wetland_name}'
os.makedirs(output_dir, exist_ok=True)

# Set a fixed size for the figures
fig_size = (10, 10)

# Set a custom configuration for the figure to suppress max open warning
plt.rcParams['figure.max_open_warning'] = 1

# Read the first shapefile to get the bounding box
first_shapefile = os.path.join(r'C:\Users\abro3569\PycharmProjects\gee\test_shps\\' + model_type + '\\' + shapefiles[0])
first_gdf = gpd.read_file(first_shapefile)

# Check and set the CRS if needed
if first_gdf.crs is None:
    first_gdf.crs = {'init': 'EPSG:32633'}

# Get the bounding box of the first shapefile
minx, miny, maxx, maxy = first_gdf.envelope.total_bounds

# Plot each shapefile onto a nice basemap and save as PNG
for i, shapefile in enumerate(shapefiles):

    # Extract year and month from the shapefile name
    parts = os.path.splitext(shapefile)[0].split('_')
    year = parts[-2]
    month = parts[-1]

    # Read the shapefile using geopandas
    gdf = gpd.read_file(r'C:\Users\abro3569\PycharmProjects\gee\test_shps\\' + model_type + '\\' + shapefile)

    # Check and set the CRS if needed
    if gdf.crs is None:
        gdf.crs = {'init': 'EPSG:32633'}

    # Plot the wetland with a fixed size and the same extent
    fig, ax = plt.subplots(figsize=fig_size)
    gdf.plot(ax=ax, alpha=0.5, edgecolor='k')

    # Set the extent of the plot to be the same as the first shapefile
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)

    # Add basemap
    basemap_crs = CRS.from_user_input('EPSG:32633')
    cx.add_basemap(ax, crs=basemap_crs.to_epsg(), zoom=15)

    # Set a title for the plot
    plt.title(f'Wetland: {wetland_name}, Model: {model_type}, Year: {year}, Month: {month}')

    # Save the plot as PNG
    plt.savefig(os.path.join(output_dir, f'plot_{i}.png'))
    plt.close()

# Input folder containing PNG images
input_folder = r'C:\Users\abro3569\PycharmProjects\gee\output_images_' + wetland_name

# Output GIF file
output_gif = r"C:\Users\abro3569\PycharmProjects\gee\gifs\\" + wetland_name + "_" + model_type + ".gif"

# List all PNG files in the input folder
png_files = [f for f in os.listdir(input_folder) if f.endswith(".png")]

sorted_png_files = sorted(png_files)

# Create a list to hold the image objects
images = []

# Loop through the sorted PNG files and open them
for png in sorted_png_files:
    image = Image.open(os.path.join(input_folder, png))
    images.append(image)

# Resize all images to the same size (use the size of the first image)
image_size = images[0].size
images = [image.resize(image_size) for image in images]

# Save the list of images as a GIF
images[0].save(output_gif, save_all=True, append_images=images[1:], duration=500, loop=0)

print(f"GIF created and saved as {output_gif}")

# Remove the temporary images directory
for file_name in os.listdir(output_dir):
    file_path = os.path.join(output_dir, file_name)
    os.remove(file_path)
os.rmdir(output_dir)
