"""Draw a map of Covid-19 cases in New York counties"""
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


CENTER_OF_NY = [-76, 42]
ZOOM_SCALE = 1
WIDTH=1e6
HEIGHT=1e6


def draw_map():
    """Draw the map!"""
    # Define the projection, scale, the corners of the map, and the resolution.
    base_map = Basemap(
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
    base_map.drawmapboundary()
    plt.show()


def main():
    draw_map()


if __name__ == '__main__':
    main()
