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
import datetime

ROOT_DIR = os.path.dirname(__file__)
AVG_WINDOW = 7
BUBBLE_SCALE = 1
LOGGER = logging.getLogger('map')
START_DATE = datetime.date(2020, 3, 1)
CENTER = [39.828175, -98.5795]
WIDTH = 6.5e6
HEIGHT = 4e6
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


def get_bubble_area(fips, pivot_table, date):
    """What should the area of the bubble be?"""
    cases = pivot_table.loc[fips]
    current = cases.loc[date.strftime('%Y-%m-%d')]
    prior = cases.loc[
        (date - datetime.timedelta(days=AVG_WINDOW)).strftime('%Y-%m-%d')
    ]
    delta = (current-prior)/AVG_WINDOW
    if delta == 0:
        return 0
    return delta * BUBBLE_SCALE


def draw_map():
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
    data_frame_counties = c19.get_data_frame_counties()
    pivot_table = data_frame_counties.pivot_table(
        index='fips', values='cases', columns=['date']
    ).fillna(0)
    old_scatter = None
    old_text = None
    max_date = data_frame_counties['date'].max()
    date = START_DATE + datetime.timedelta(days=AVG_WINDOW)
    base_map.drawmapboundary()
    statistics = c19.get_county_statistics()
    for png_file in get_pngs():
        os.remove(png_file)
    while date <= max_date:
        file_name = 'covid-19-data-{}.png'.format(date.strftime('%Y%m%d'))
        LOGGER.info('Generating map %s', file_name)
        cases, lats, lons = get_bubble_data(pivot_table, date, statistics)
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


def get_bubble_data(pivot_table, date, statistics):
    """Generate the required bubble data"""
    lons = []
    lats = []
    cases = []
    for fips in pivot_table.index:
        if fips == 0:
            # Unknown counties
            continue
        bubble_area = get_bubble_area(fips, pivot_table, date)
        if bubble_area == 0:
            continue
        statistics_fips = statistics[statistics['FIPS'] == fips]
        lons.append(statistics_fips['Longitude'].values[0])
        lats.append(statistics_fips['Latitude'].values[0])
        cases.append(bubble_area)
    return cases, lats, lons


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


def setup_logger():
    """Set up the logger"""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(name)s %(message)s"
    )


def main():
    setup_logger()
    draw_map()
    create_gif()


if __name__ == '__main__':
    main()
