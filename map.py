"""Draw an animated gif of COVID-19 cases throughout time in the United
States.
> conda install --name covid-19-data python=3.7 pandas matplotlib \
  Pillow basemap
"""
import c19
import sys
import logging
import os
from PIL import Image
import matplotlib.pyplot
import pandas
import datetime
import argparse

ROOT_DIR = os.path.dirname(__file__)

BUBBLE_SCALE = 100000  # Bubble area is cases per BUBBLE_SCALE

LOGGER = logging.getLogger('map')
START_DATE = datetime.date(2020, 3, 1)
CENTER = [39.828175, -98.5795]
WIDTH = 6.5e6
HEIGHT = 4e6
CSV_FILE_NAME = os.path.join(ROOT_DIR, 'us-counties.csv')
PNG_DIR = os.path.join(ROOT_DIR, 'png')
DPI = 300


def set_proj_lib_env_variable():
    """Set the PROJ_LIB environment variable or mpl_toolkts.basemap
    won't load.
    https://groups.google.com/forum/#!topic/pyart-users/Q2Zj7AFTv_w
    https://stackoverflow.com/questions/52295117/basemap-import-error-in-pycharm-keyerror-proj-lib
    https://github.com/matplotlib/basemap/issues/419
    """
    exe_dir = os.path.dirname(sys.executable)
    proj_lib = ''
    if os.name == 'posix':
        proj_lib = os.path.normpath(
            os.path.join(exe_dir, os.pardir, 'share', 'proj')
        )
    else:
        pkgs_dir = os.path.normpath(
            os.path.join(exe_dir, os.pardir, os.pardir, 'pkgs')
        )
        for entry in os.listdir(pkgs_dir):
            if not entry.startswith('proj4'):
                continue
            candidate = os.path.join(pkgs_dir, entry, 'Library', 'share')
            if not os.path.isdir(candidate):
                continue
            if os.path.isfile(os.path.join(candidate, 'epsg')):
                proj_lib = candidate
                break
    if not proj_lib:
        return
    print('Setting PROJ_LIB to', proj_lib)
    os.environ['PROJ_LIB'] = proj_lib
    return


set_proj_lib_env_variable()
import mpl_toolkits.basemap


def get_number_of_cases(fips, data_frame, date):
    """How many cases are in this county on this date?"""
    if fips in c19.FIPS_OUTER_BOROUGHS:
        # Ignore non-Manhattan boroughs
        return 0
    if fips == c19.FIPS_MANHATTAN:
        # New York City data encompasses all five boroughs. We'll put
        # the marker in Manhattan
        data_frame_fips = data_frame[data_frame['county'] == 'New York City']
    else:
        data_frame_fips = data_frame[data_frame['fips'] == fips]
    data_frame_fips_date = data_frame_fips[
        data_frame_fips['date'] == date.strftime('%Y-%m-%d')
    ]
    if data_frame_fips_date.empty:
        return 0
    return data_frame_fips_date['cases'].values[0]


def draw_map(args):
    """Draw the map!"""
    # Define the projection, scale, the corners of the map, and the resolution.
    base_map = mpl_toolkits.basemap.Basemap(
        lat_0=CENTER[0], lon_0=CENTER[1], width=WIDTH,
        height=HEIGHT, projection='tmerc'
    )
    base_map.readshapefile(
        'cb_2018/cb_2018_us_state_500k', 'states', drawbounds=True,
        linewidth=0.2,
        color='gray'
    )
    data_frame = get_data_frame()
    old_scatter = None
    old_text = None
    max_date = data_frame['date'].max()
    date = START_DATE
    base_map.drawmapboundary()
    statistics = c19.get_county_statistics()
    for png_file in get_pngs():
        os.remove(png_file)
    while date <= max_date:
        lons = []
        lats = []
        cases = []
        file_name = 'covid-19-data-{}.png'.format(date.strftime('%Y%m%d'))
        LOGGER.info('Generating map %s', file_name)
        for index, statistic in statistics.iterrows():
            fips = int(statistic['FIPS'])
            number_of_cases = get_number_of_cases(fips, data_frame, date)
            if not number_of_cases:
                continue
            lons.append(statistic['Longitude'])
            lats.append(statistic['Latitude'])
            if args.scale_by_population:
                scalar = BUBBLE_SCALE / c19.get_population(fips, statistics)
            else:
                scalar = 0.10
            cases.append(number_of_cases * scalar)
        if old_text:
            old_text.remove()
        old_text = matplotlib.pyplot.text(
            0, 0, date, horizontalalignment='center',
            verticalalignment='center'
        )
        if old_scatter:
            old_scatter.remove()
        old_scatter = base_map.scatter(
            lons, lats, marker='o', color='r', latlon=True, s=cases, alpha=.4,
        )
        matplotlib.pyplot.savefig(os.path.join(PNG_DIR, file_name), dpi=DPI)
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
    for image in get_pngs():
        new_frame = Image.open(image)
        frames.append(new_frame)

    # Save into a GIF file that loops forever
    gif_file_name = 'png_to_gif.gif'
    LOGGER.info('Creating GIF: %s', gif_file_name)
    frames[0].save(
        gif_file_name, format='GIF', append_images=frames[1:],
        save_all=True, duration=300
    )


def get_pngs():
    """Return a list of png paths"""
    return [
        os.path.join(PNG_DIR, entry) for entry
        in sorted(os.listdir(PNG_DIR)) if entry.lower().endswith('.png')
    ]


def parse_args():
    """Parse the command line arguments"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scale-by-population', action='store_true')
    parser.add_argument('--verbose', action='store_true')
    return parser.parse_args()


def setup_logger(args):
    """Set up the logger"""
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(name)s %(message)s"
    )


def main():
    args = parse_args()
    setup_logger(args)
    draw_map(args)
    create_gif()


if __name__ == '__main__':
    main()
