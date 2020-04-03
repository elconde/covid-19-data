import c19


def get_population(fips, statistics):
    """What is the population of this row? Include the entire dataframe
    in case we need access to other counties"""
    assert fips not in c19.FIPS_OUTER_BOROUGHS, (
        'Outer boroughs are merged into Manhattan!'
    )
    population = (
        statistics[statistics['FIPS'] == fips]['Population (2010)'].sum()
    )
    if fips != c19.FIPS_MANHATTAN:
        return population
    return population + (
        statistics[
            statistics['FIPS'].isin(c19.FIPS_OUTER_BOROUGHS)
        ]['Population (2010)'].sum()
    )


__all__ = ['get_population']