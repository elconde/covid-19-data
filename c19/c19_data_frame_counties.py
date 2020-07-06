import c19
import pandas


def get_data_frame_counties():
    data_frame = pandas.read_csv(
        c19.CSV_COUNTIES, parse_dates=[0]
    ).fillna({'fips': 0}).astype({'fips': int})
    nyc_loc = (
        data_frame[(data_frame['county'] == 'New York City')].index.tolist()
    )
    data_frame.at[nyc_loc, 'fips'] = 36061
    return data_frame


def get_data_frame_county(county_name, state_name, scale_by_population):
    counties = get_data_frame_counties()
    data_frame = counties[
        (counties['county'] == county_name) &
        (counties['state'] == state_name)
    ][['date', 'cases', 'deaths']].set_index('date')
    if not scale_by_population:
        return data_frame
    population = c19.get_county_population(
        c19.get_county_statistics(), state_name, county_name
    )
    for series in ('cases', 'deaths'):
        data_frame[series] = data_frame[series] / population
    return data_frame


__all__ = ['get_data_frame_counties', 'get_data_frame_county']
