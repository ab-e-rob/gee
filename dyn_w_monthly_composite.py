import os
import ee
from dotenv import load_dotenv
from utils import get_aoi

# Initialize Earth Engine
ee.Initialize()

#aoi_list = get_aoi.get_all_aois()

aoi_list = {
    'Farnebjofarden': ee.Geometry.Polygon(
        [[[16.610364777863907, 60.01583532594324], [17.054983864348788, 60.01583532594324],
          [17.054983864348788, 60.35754096685158], [16.610364777863907, 60.35754096685158]]]),
    'Fyllean': ee.Geometry.Polygon(
        [[[12.862095085746729, 56.58527836887409], [13.146199273474716, 56.58527836887409],
          [13.146199273474716, 56.73351485277274], [12.862095085746729, 56.73351485277274]]]),
    'Gammelstadsviken': ee.Geometry.Polygon(
        [[[22.00353441892008, 65.59577260617353], [22.15837095870042, 65.59577260617353],
          [22.15837095870042, 65.6683594683777], [22.00353441892008, 65.6683594683777]]]),
    'Getapulien': ee.Geometry.Polygon(
        [[[15.388032007097472, 59.59300910906786], [15.556494080759048, 59.59300910906786],
          [15.556494080759048, 59.738763603612774], [15.388032007097472, 59.738763603612774]]]),
    'Getteron': ee.Geometry.Polygon(
        [[[12.177869017856528, 57.10439396744924], [12.292823230310525, 57.10439396744924],
          [12.292823230310525, 57.16406093553091], [12.177869017856528, 57.16406093553091]]]),
    'Gotlands': ee.Geometry.Polygon(
        [[[18.298578702539643, 56.96256492899876], [19.09910506944924, 56.96256492899876],
          [19.09910506944924, 57.82593074525376], [18.298578702539643, 57.82593074525376]]]),
    'Gullhog': ee.Geometry.Polygon(
        [[[14.065673331805273, 62.12081464002947], [14.212732842024394, 62.12081464002947],
          [14.212732842024394, 62.24663190688309], [14.065673331805273, 62.24663190688309]]]),
    'Gustavmurane': ee.Geometry.Polygon(
        [[[17.257830333013985, 60.56003386854193], [17.392546190961355, 60.56003386854193],
          [17.392546190961355, 60.66617719445942], [17.257830333013985, 60.66617719445942]]]),
    'Helge': ee.Geometry.Polygon(
        [[[14.035947215902297, 55.83765788327101], [14.29788571822225, 55.83765788327101],
          [14.29788571822225, 56.11806462683611], [14.035947215902297, 56.11806462683611]]]),
    'Hjalstaviken': ee.Geometry.Polygon(
        [[[17.318272439862497, 59.63089398664613], [17.44367306416101, 59.63089398664613],
          [17.44367306416101, 59.70646365725113], [17.318272439862497, 59.70646365725113]]]),
    'Hornborgasjon': ee.Geometry.Polygon(
        [[[13.398628103605674, 58.21110805658671], [13.679356394128149, 58.21110805658671],
          [13.679356394128149, 58.387833917261496], [13.398628103605674, 58.387833917261496]]]),
    'Hovramomradet': ee.Geometry.Polygon(
        [[[15.889411244851837, 60.21652466829843], [16.2062005381951, 60.21652466829843],
          [16.2062005381951, 60.44801504872225], [15.889411244851837, 60.44801504872225]]]),
    'Kallgate': ee.Geometry.Polygon(
        [[[18.63314562183302, 57.62942648112829], [18.77344884119503, 57.62942648112829],
          [18.77344884119503, 57.724681422791534], [18.63314562183302, 57.724681422791534]]]),
    'Kilsviken': ee.Geometry.Polygon(
        [[[13.904338809271447, 58.96854297301332], [14.189817281351974, 58.96854297301332],
          [14.189817281351974, 59.14033254384489], [13.904338809271447, 59.14033254384489]]]),
    'Klingavalsan': ee.Geometry.Polygon(
        [[[13.404232400107736, 55.54317296217624], [13.716905177072379, 55.54317296217624],
          [13.716905177072379, 55.728934183127016], [13.404232400107736, 55.728934183127016]]]),
    'Komosse': ee.Geometry.Polygon(
        [[[13.601057171087156, 57.611274109266446], [13.800744323444126, 57.611274109266446],
          [13.800744323444126, 57.7588938038336], [13.601057171087156, 57.7588938038336]]]),
    'Koppangen': ee.Geometry.Polygon(
        [[[14.706166250128238, 61.271140130601715], [14.883354940881325, 61.271140130601715],
          [14.883354940881325, 61.436229126810794], [14.706166250128238, 61.436229126810794]]]),
    'Kvismaren': ee.Geometry.Polygon(
        [[[15.290481705057626, 59.1391737926136], [15.462789354679959, 59.1391737926136],
          [15.462789354679959, 59.20992899200545], [15.290481705057626, 59.20992899200545]]]),
    'Laidaure': ee.Geometry.Polygon(
        [[[18.038711868890296, 67.07853147893837], [18.519723432734143, 67.07853147893837],
          [18.519723432734143, 67.184543817285], [18.038711868890296, 67.184543817285]]]),
    'Lundakrabukten': ee.Geometry.Polygon(
        [[[12.84444931529691, 55.75374652536043], [12.969377309758286, 55.75374652536043],
          [12.969377309758286, 55.880633150511194], [12.84444931529691, 55.880633150511194]]])
}

# Define the years for which you want to obtain composites.
startYear = 2020
endYear = 2023

# Loop through each AOI.
for aoi_name, roi in aoi_list.items():  # Iterate through dictionary items.

    # Create an empty image collection to store the monthly dynamic world images
    dw_collection = ee.ImageCollection([])

    for year in range(startYear, endYear + 1):
        # Loop through each month.
        for month in range(1, 13):
            # Define the start and end dates for the current month.
            startDate = ee.Date.fromYMD(year, month, 1)
            endDate = ee.Date.fromYMD(year, month, 28)

            # Filter the Sentinel-2 data by date, cloud cover, and location.
            collection = (ee.ImageCollection('GOOGLE/DYNAMICWORLD/V1')
                          .filterDate(startDate, endDate)
                          .filterBounds(roi))

            # Select the 'label' band from the collection.
            classification = collection.select('label')

            # Create a composite by reducing the collection to the mode (most frequent) value.
            dwComposite = classification.reduce(ee.Reducer.mode())

            # Export as byte type and give no data values -9999
            export_dwComposite = dwComposite.byte().unmask(-9999)

            task = ee.batch.Export.image.toDrive(export_dwComposite,
                                                 description=aoi_name + '_' + str(year) + '_' + str(month),
                                                 # Name for the exported file
                                                 scale=10,
                                                 folder='dynamic_world_' + aoi_name,  # Use the AOI name for the folder
                                                 region=roi.getInfo()['coordinates'],
                                                 maxPixels=1e10
                                                 )
            task.start()

            print(f'Exporting Dynamic World image to Google Drive: {aoi_name}, month {month}, year {year}')
