from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


CENTER_OF_NY = [-76, 42]
ZOOM_SCALE = 1

bbox = [
    CENTER_OF_NY[0]-ZOOM_SCALE, CENTER_OF_NY[0]+ZOOM_SCALE,
    CENTER_OF_NY[1]-ZOOM_SCALE, CENTER_OF_NY[1]+ZOOM_SCALE
]

# Define the projection, scale, the corners of the map, and the resolution.
MAP = Basemap(
    lon_0=CENTER_OF_NY[0], lat_0=CENTER_OF_NY[1], width=1000000,
    height=1000000, projection='tmerc'
)

# https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html
MAP.readshapefile(
    'cb_2018/cb_2018_us_county_500k', 'states', drawbounds=True, linewidth=0.45,
    color='gray'
)
MAP.readshapefile(
    'cb_2018/cb_2018_us_state_500k', 'states', drawbounds=True, linewidth=0.9,
    color='gray'
)

# Then add element: draw coast line, map boundary, and fill continents:
# m.drawcoastlines()
MAP.drawmapboundary()
# m.fillcontinents()

# You can add rivers as well
# m.drawrivers(color='#0000ff')

plt.show()
