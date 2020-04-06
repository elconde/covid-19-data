import c19
import pandas


def get_data_frame_counties():
    return pandas.read_csv(c19.CSV_COUNTIES, parse_dates=[0])


def get_data_frame_county(county_name, state_name):
    counties = get_data_frame_counties()
    return counties[
        (counties['county'] == county_name) &
        (counties['state'] == state_name)
    ][['date', 'cases', 'deaths']].set_index('date')


__all__ = ['get_data_frame_counties', 'get_data_frame_county']