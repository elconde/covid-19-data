import c19
import pandas


def get_data_frame_counties():
    data_frame = pandas.read_csv(c19.CSV_COUNTIES, parse_dates=[0])
    nyc_loc = (
        data_frame[(data_frame['county'] == 'New York City')].index.tolist()
    )
    data_frame.at[nyc_loc, 'fips'] = 36061
    return data_frame



def get_data_frame_county(county_name, state_name):
    counties = get_data_frame_counties()
    return counties[
        (counties['county'] == county_name) &
        (counties['state'] == state_name)
    ][['date', 'cases', 'deaths']].set_index('date')


__all__ = ['get_data_frame_counties', 'get_data_frame_county']