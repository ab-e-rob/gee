import os
import ee
from dotenv import load_dotenv
from utils import get_aoi

# Initialize Earth Engine
ee.Initialize()

#aoi_list = get_aoi.get_all_aois()

aoi_list = {
     'Maanavuoma': ee.Geometry.Polygon(
            [[[22.20897406328696, 68.41693085944348], [22.398160571515426, 68.41693085944348],
              [22.398160571515426, 68.50106477410417], [22.20897406328696, 68.50106477410417]]]),
        'Mellanljusnan': ee.Geometry.Polygon(
            [[[15.468519997463957, 61.75168007734304], [16.20860993934602, 61.75168007734304],
              [16.20860993934602, 61.96056547706965], [15.468519997463957, 61.96056547706965]]]),
        'Mellerston': ee.Geometry.Polygon(
            [[[21.781205188109173, 65.17173709091354], [21.921919835971224, 65.17173709091354],
              [21.921919835971224, 65.23416339156074], [21.781205188109173, 65.23416339156074]]]),
        'Morrumsan': ee.Geometry.Polygon(
            [[[14.62982327684704, 56.03524665605006], [14.831228741105539, 56.03524665605006],
              [14.831228741105539, 56.420789786617036], [14.62982327684704, 56.420789786617036]]]),
        'Mossatrask': ee.Geometry.Polygon(
            [[[17.215041047404657, 63.7977338364231], [17.395123624587956, 63.7977338364231],
              [17.395123624587956, 63.87273660100153], [17.215041047404657, 63.87273660100153]]]),
        'Nittalven': ee.Geometry.Polygon(
            [[[14.672378203321315, 59.82246119902609], [14.96380377831855, 59.82246119902609],
              [14.96380377831855, 60.05994133577251], [14.672378203321315, 60.05994133577251]]]),
        'Nordealvs': ee.Geometry.Polygon(
            [[[11.679294201510082, 57.72251730676328], [11.948147999334621, 57.72251730676328],
              [11.948147999334621, 57.86755328518364], [11.679294201510082, 57.86755328518364]]]),
        'Olands': ee.Geometry.Polygon(
            [[[16.490349808551436, 56.29956663173564], [16.995779229001588, 56.29956663173564],
              [16.995779229001588, 57.07155536645641], [16.490349808551436, 57.07155536645641]]]),
        'Oldflan': ee.Geometry.Polygon(
            [[[13.588140435045093, 63.71539796849901], [13.987336047044089, 63.71539796849901],
              [13.987336047044089, 63.89388031721747], [13.588140435045093, 63.89388031721747]]]),
        'Oset': ee.Geometry.Polygon(
            [[[15.210548749205131, 59.24553175480199], [15.322310199427893, 59.24553175480199],
              [15.322310199427893, 59.32112103529444], [15.210548749205131, 59.32112103529444]]]),
        'Osten': ee.Geometry.Polygon(
            [[[13.839131178700226, 58.51617960588248], [13.999130906213852, 58.51617960588248],
              [13.999130906213852, 58.6151697004769], [13.839131178700226, 58.6151697004769]]]),
        'Ottenby': ee.Geometry.Polygon(
            [[[16.35749907055198, 56.17662832667295], [16.497563435623967, 56.17662832667295],
              [16.497563435623967, 56.25515378849109], [16.35749907055198, 56.25515378849109]]]),
        'Ovresulan': ee.Geometry.Polygon(
            [[[16.755244118979956, 62.557370939262725], [16.904671810626056, 62.557370939262725],
              [16.904671810626056, 62.63374787070935], [16.755244118979956, 62.63374787070935]]]),
        'Paivavouma': ee.Geometry.Polygon(
            [[[21.039356873492494, 66.58241391855049], [21.391778663784844, 66.58241391855049],
              [21.391778663784844, 66.70483991740039], [21.039356873492494, 66.70483991740039]]]),
        'Persofjarden': ee.Geometry.Polygon(
            [[[21.899292496873013, 65.7009273521774], [22.21491475628821, 65.7009273521774],
              [22.21491475628821, 65.85146482198189], [21.899292496873013, 65.85146482198189]]]),
        'Pirttimysvuoma': ee.Geometry.Polygon(
            [[[20.60030392991728, 68.19963683298894], [20.883210152912365, 68.19963683298894],
              [20.883210152912365, 68.3269846970409], [20.60030392991728, 68.3269846970409]]]),
        'Rappomyran': ee.Geometry.Polygon(
            [[[20.800505096909944, 66.2970408810874], [21.11550238065602, 66.2970408810874],
              [21.11550238065602, 66.45434335763757], [20.800505096909944, 66.45434335763757]]]),
        'Sikavagarna': ee.Geometry.Polygon(
            [[[15.14680709543518, 63.588417766786975], [15.39663757925339, 63.588417766786975],
              [15.39663757925339, 63.68004819228282], [15.14680709543518, 63.68004819228282]]])
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
