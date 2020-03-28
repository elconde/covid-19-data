from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


CENTER_OF_NY = [-76, 42]
ZOOM_SCALE = 1

bbox = [
    CENTER_OF_NY[0]-ZOOM_SCALE, CENTER_OF_NY[0]+ZOOM_SCALE,
    CENTER_OF_NY[1]-ZOOM_SCALE, CENTER_OF_NY[1]+ZOOM_SCALE
]

# Define the projection, scale, the corners of the map, and the resolution.
m = Basemap(
    lon_0=CENTER_OF_NY[0], lat_0=CENTER_OF_NY[1], width=1000000,
    height=1000000, projection='tmerc'
)


shp_info = m.readshapefile(
    'cb_2018_us_county_500k', 'states', drawbounds=True, linewidth=0.45,
    color='gray'
)

# Then add element: draw coast line, map boundary, and fill continents:
# m.drawcoastlines()
m.drawmapboundary()
# m.fillcontinents()

# You can add rivers as well
# m.drawrivers(color='#0000ff')

plt.show()
