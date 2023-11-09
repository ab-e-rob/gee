import os
import ee
from dotenv import load_dotenv
from utils import get_aoi

# Initialize Earth Engine
ee.Initialize()

#aoi_list = get_aoi.get_all_aois()

aoi_list = {
        'Sjaunja': ee.Geometry.Polygon(
            [[[18.44317813176649, 67.07603823151958], [20.18843715683951, 67.07603823151958],
              [20.18843715683951, 67.70396215343895], [18.44317813176649, 67.70396215343895]]]),
        'Skalderviken': ee.Geometry.Polygon(
            [[[12.638607796337459, 56.19836191037679], [12.821080446810944, 56.19836191037679],
              [12.821080446810944, 56.259313791907985], [12.638607796337459, 56.259313791907985]]]),
        'Stigfjorden': ee.Geometry.Polygon(
            [[[11.463328963249285, 58.024083089225186], [11.856159374775302, 58.024083089225186],
              [11.856159374775302, 58.15639851765114], [11.463328963249285, 58.15639851765114]]]),
        'Storemosse': ee.Geometry.Polygon(
            [[[13.805432657491863, 57.19800578850779], [14.093069022389214, 57.19800578850779],
              [14.093069022389214, 57.3613303782832], [13.805432657491863, 57.3613303782832]]]),
        'Storkolen': ee.Geometry.Polygon(
            [[[12.111756240047269, 61.71741205161274], [12.390755824386746, 61.71741205161274],
              [12.390755824386746, 61.85867244453625], [12.111756240047269, 61.85867244453625]]]),
        'Svartadalen': ee.Geometry.Polygon(
            [[[16.187136366776855, 59.79654271322899], [16.42447600292698, 59.79654271322899],
              [16.42447600292698, 59.980854009637284], [16.187136366776855, 59.980854009637284]]]),
        'Svenskahog': ee.Geometry.Polygon(
            [[[19.1214042583935, 59.35494734628139], [19.580235785161264, 59.35494734628139],
              [19.580235785161264, 59.51608527006222], [19.1214042583935, 59.51608527006222]]]),
        'Svenskundsviken': ee.Geometry.Polygon(
            [[[16.315441341085695, 58.563047643579345], [16.60296370953899, 58.563047643579345],
              [16.60296370953899, 58.65609629552398], [16.315441341085695, 58.65609629552398]]]),
        'Takern': ee.Geometry.Polygon(
            [[[14.67340054837837, 58.30129150350324], [14.955339865203179, 58.30129150350324],
              [14.955339865203179, 58.405939246905305], [14.67340054837837, 58.405939246905305]]]),
        'Tarnsjon': ee.Geometry.Polygon(
            [[[15.339117713983278, 65.75221637464979], [15.847946907930018, 65.75221637464979],
              [15.847946907930018, 66.1790991265736], [15.339117713983278, 66.1790991265736]]]),
        'Tavvovouma': ee.Geometry.Polygon(
            [[[20.382016136635006, 68.38986140789989], [21.09599220796833, 68.38986140789989],
              [21.09599220796833, 68.63666996585133], [20.382016136635006, 68.63666996585133]]]),
        'Tjalmejaure': ee.Geometry.Polygon(
            [[[15.88452376706067, 66.10595499579311], [16.675021260690247, 66.10595499579311],
              [16.675021260690247, 66.38265236993958], [15.88452376706067, 66.38265236993958]]]),
        'Tonnersjoheden': ee.Geometry.Polygon(
            [[[13.129846881189236, 56.61613122114145], [13.485710316324665, 56.61613122114145],
              [13.485710316324665, 56.84193572874967], [13.129846881189236, 56.84193572874967]]]),
        'Traslovslage': ee.Geometry.Polygon(
            [[[12.235204037515846, 56.89823362457907], [12.413850569465405, 56.89823362457907],
              [12.413850569465405, 57.0705074128832], [12.235204037515846, 57.0705074128832]]]),
        'Tysoarna': ee.Geometry.Polygon(
            [[[14.570377367334281, 63.20262999383208], [14.702889350360534, 63.20262999383208],
              [14.702889350360534, 63.2676225903782], [14.570377367334281, 63.2676225903782]]]),
        'Umealvens': ee.Geometry.Polygon(
            [[[20.206053229563057, 63.696965275262265], [20.427749294992495, 63.696965275262265],
              [20.427749294992495, 63.78952360877675], [20.206053229563057, 63.78952360877675]]]),
        'Vasikkavouma': ee.Geometry.Polygon(
            [[[23.11432701111463, 67.19432612267958], [23.28644369047891, 67.19432612267958],
              [23.28644369047891, 67.25682392423104], [23.11432701111463, 67.25682392423104]]]),
        'Vastraroxen': ee.Geometry.Polygon(
            [[[15.458073824479545, 58.40366578666712], [15.67374693760755, 58.40366578666712],
              [15.67374693760755, 58.552793852155936], [15.458073824479545, 58.552793852155936]]]),
        'Vattenan': ee.Geometry.Polygon(
            [[[15.18679456755876, 62.534186181617144], [15.586791537164371, 62.534186181617144],
              [15.586791537164371, 62.64227218243379], [15.18679456755876, 62.64227218243379]]])
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
