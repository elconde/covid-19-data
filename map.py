"""Draw a map of Covid-19 cases in New York counties
> conda install --name covid-19-data python=3.7 pandas matplotlib Pillow basemap
"""
import sys
import logging
import os

LOGGER = logging.getLogger()
logging.basicConfig(level=logging.NOTSET, format="%(asctime)s %(name)s %(message)s")


def set_proj_lib_env_variable():
    """Set the PROJ_LIB environment variable or mpl_toolkts.basemap
    won't load.
    https://groups.google.com/forum/#!topic/pyart-users/Q2Zj7AFTv_w
    https://stackoverflow.com/questions/52295117/basemap-import-error-in-pycharm-keyerror-proj-lib
    https://github.com/matplotlib/basemap/issues/419
    """
    pkgs_dir = os.path.normpath(os.path.join(os.path.dirname(sys.executable), os.pardir, os.pardir, 'pkgs'))
    for entry in os.listdir(pkgs_dir):
        if not entry.startswith('proj4'):
            continue
        candidate = os.path.join(pkgs_dir, entry, 'Library', 'share')
        if not os.path.isdir(candidate):
            continue
        if os.path.isfile(os.path.join(candidate, 'epsg')):
            LOGGER.debug('Setting PROJ_LIB to %s', candidate)
            os.environ['PROJ_LIB'] = candidate
            return

from PIL import Image
import glob
import csv
set_proj_lib_env_variable()
import mpl_toolkits.basemap
import matplotlib.pyplot
import pandas
import datetime


START_DATE = datetime.date(2020, 3, 1)
CENTER_OF_NY = [-76, 42]
ZOOM_SCALE = 1
WIDTH = 1e6
HEIGHT = 1e6
CSV_FILE_NAME = os.path.join(os.path.dirname(__file__), 'us-counties.csv')


def get_county_coordinates():
    """What are the coordinates of the counties?"""
    with open('coordinates.csv') as coord_file:
        return [row for row in csv.DictReader(coord_file)]


def get_number_of_cases(fips, data_frame, date):
    """How many cases are in this county on this date?"""
    if not fips:
        # New York
        data_frame_fips = data_frame[data_frame['county'] == 'New York City']
    else:
        data_frame_fips = data_frame[data_frame['fips'] == fips]
    data_frame_fips_date = data_frame_fips[
        data_frame_fips['date'] == date.strftime('%Y-%m-%d')
    ]
    if data_frame_fips_date.empty:
        return 0
    return data_frame_fips_date['cases'].values[0]


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
    data_frame = get_data_frame()
    old_scatter = None
    old_text = None
    max_date = data_frame['date'].max()
    date = START_DATE
    while date <= max_date:
        lons = []
        lats = []
        cases = []
        file_name = 'ny{}.png'.format(date.strftime('%Y%m%d'))
        print('Generating map '+file_name)
        for coord in get_county_coordinates():
            lons.append(float(coord['lon']))
            lats.append(float(coord['lat']))
            fips = int(coord['fips'])
            cases.append(
                get_number_of_cases(fips, data_frame, date)
            )
        if old_text:
            old_text.remove()
        old_text = matplotlib.pyplot.text(
            0, 0, date, horizontalalignment='center',
            verticalalignment='center'
        )
        base_map.drawmapboundary()
        if old_scatter:
            old_scatter.remove()
        old_scatter = base_map.scatter(
            lons, lats, marker='o', color='r', latlon=True, s=cases, alpha=.4,
        )
        matplotlib.pyplot.savefig(file_name)
        date += datetime.timedelta(days=1)


def get_data_frame():
    """Get the data frame from the csv file"""
    data_frame = pandas.read_csv(CSV_FILE_NAME)
    data_frame['date'] = pandas.to_datetime(
        data_frame['date'], format='%Y-%m-%d'
    )
    return data_frame


def create_gif():
    """Convert the PNG files to a GIF"""
    # Create the frames
    frames = []
    images = sorted(glob.glob("*.png"))
    for image in images:
        new_frame = Image.open(image)
        frames.append(new_frame)

    # Save into a GIF file that loops forever
    frames[0].save(
        'png_to_gif.gif', format='GIF', append_images=frames[1:],
        save_all=True, duration=300, loop=0
    )


def main():
    draw_map()
    create_gif()


if __name__ == '__main__':
    main()
