import c19


def get_usa_population(statistics):
    """USA population"""
    return statistics['Population (2010)'].sum()

def get_state_population(statistics, state_name):
    """What is the population of this state"""
    return (
        statistics[statistics['State'] == c19.parse_state_name(state_name)]
        ['Population (2010)'].sum()
    )


def get_county_population(statistics, state_name, county_name):
    """What is the population of this county?"""
    return (
        statistics[
            (statistics['State'] == c19.parse_state_name(state_name)) &
            (statistics['County'] == county_name)
        ]['Population (2010)'].sum()
    )


__all__ = [
    'get_county_population', 'get_state_population', 'get_usa_population'
]