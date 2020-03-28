"""Draw a map of Covid-19 cases in New York counties"""
import csv
import mpl_toolkits.basemap
import matplotlib.pyplot
import os
import pandas


CENTER_OF_NY = [-76, 42]
ZOOM_SCALE = 1
WIDTH = 1e6
HEIGHT = 1e6
CSV_FILE_NAME = os.path.join(os.path.dirname(__file__), 'us-counties.csv')


def get_county_coordinates():
    """What are the coordinates of the counties?"""
    with open('coordinates.csv') as coord_file:
        return [row for row in csv.DictReader(coord_file)]


def get_number_of_cases(fips, data_frame):
    """How many cases are in this county?"""
    if not fips:
        # New York
        data_frame_fips = data_frame[data_frame['county'] == 'New York City']
    else:
        data_frame_fips = data_frame[data_frame['fips'] == fips]
    if data_frame_fips.empty:
        return 0
    return data_frame_fips.loc[(data_frame_fips['date'].idxmax()), 'cases']


def draw_map():
    """Draw the map!"""
    # Define the projection, scale, the corners of the map, and the resolution.
    base_map = mpl_toolkits.basemap.Basemap(
        lon_0=CENTER_OF_NY[0], lat_0=CENTER_OF_NY[1], width=WIDTH,
        height=HEIGHT, projection='tmerc'
    )
    base_map.readshapefile(
        'cb_2018/cb_2018_us_county_500k', 'states', drawbounds=True,
        linewidth=0.45,
        color='gray'
    )
    base_map.readshapefile(
        'cb_2018/cb_2018_us_state_500k', 'states', drawbounds=True,
        linewidth=0.9,
        color='gray'
    )
    lons = []
    lats = []
    cases = []
    data_frame = get_data_frame()
    for coord in get_county_coordinates():
        lons.append(float(coord['lon']))
        lats.append(float(coord['lat']))
        fips = int(coord['fips'])
        cases.append(get_number_of_cases(fips, data_frame))
    base_map.drawmapboundary()
    base_map.scatter(
        lons, lats, marker='o', color='r', latlon=True, s=cases, alpha=.4,
    )
    matplotlib.pyplot.show()


def get_data_frame():
    """Get the data frame from the csv file"""
    data_frame = pandas.read_csv(CSV_FILE_NAME)
    data_frame['date'] = pandas.to_datetime(
        data_frame['date'], format='%Y-%m-%d'
    )
    return data_frame


def main():
    draw_map()


if __name__ == '__main__':
    main()
