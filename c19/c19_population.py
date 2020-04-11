import c19


def get_state_population(statistics, state_name):
    """What is the population of this state"""
    return (
        statistics[statistics['State'] == c19.parse_state_name(state_name)]
        ['Population (2010)'].sum()
    )


def get_county_population(statistics, fips):
    """What is the population of this county?"""
    return (
        statistics[(statistics['FIPS'] == fips)]['Population (2010)'].sum()
    )


__all__ = ['get_county_population', 'get_state_population']