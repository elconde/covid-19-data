"""Read the county statistics file"""

import pandas


def get_county_statistics():
    """Read the county statistics into a data frame."""
    return pandas.read_csv('statistics.csv', thousands=',')


__all__ = ['get_county_statistics']
