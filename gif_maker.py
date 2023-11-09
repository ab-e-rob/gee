from PIL import Image
import os

wetland_name = 'Askoviken'
gif_type = 'ndwi'

# Input folder containing PNG images
input_folder = r"C:\Users\abro3569\Documents\PhD\Year_1\paper_1_imgs\\" + wetland_name + "_" + gif_type + "_gif"

# Output GIF file
output_gif = r"C:\Users\abro3569\Documents\PhD\Year_1\paper_1_imgs\\" + wetland_name + "_" + gif_type + ".gif"

# List all PNG files in the input folder
png_files = [f for f in os.listdir(input_folder) if f.endswith(".png")]

# Sort the PNG files by date
def extract_date_from_filename(filename):
    parts = filename.split('-')
    if len(parts) == 2:
        try:
            month = int(parts[0])
            year = int(parts[1].split('.')[0])
            return (year, month)
        except ValueError:
            return (0, 0)
    else:
        return (0, 0)

sorted_png_files = sorted(png_files, key=extract_date_from_filename)

# Create a list to hold the image objects
images = []

# Loop through the sorted PNG files and open them
for png_file in sorted_png_files:
    image = Image.open(os.path.join(input_folder, png_file))
    images.append(image)

# Save the list of images as a GIF
images[0].save(output_gif, save_all=True, append_images=images[1:], duration=400, loop=0)

print(f"GIF created and saved as {output_gif}")
