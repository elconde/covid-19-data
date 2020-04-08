"""Read the county statistics file"""
import c19
import pandas


def get_county_statistics():
    """Read the county statistics into a data frame."""
    data_frame = pandas.read_csv(c19.CSV_STATISTICS, thousands=',')
    data_frame['County'].replace(r' \[.*', '', inplace=True, regex=True)
    return data_frame


__all__ = ['get_county_statistics']
