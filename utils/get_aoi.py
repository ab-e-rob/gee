import ee

ee.Initialize()

def get_area_of_interest(area_name):

    areas_of_interest = {
        'laidaure': ee.Geometry.Polygon(
            [[[18.038711868890296, 67.07853147893837],
              [18.519723432734143, 67.07853147893837],
              [18.519723432734143, 67.184543817285],
              [18.038711868890296, 67.184543817285]]]),
        'farnebjofarden': ee.Geometry.Polygon(
            [[[16.610364777863907, 60.01583532594324],
              [17.054983864348788, 60.01583532594324],
              [17.054983864348788, 60.35754096685158],
              [16.610364777863907, 60.35754096685158]]]
        )
    }

    return areas_of_interest[area_name]

print(get_area_of_interest('laidaure'))