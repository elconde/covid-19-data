import pandas
import c19


def get_data_frame_usa():
    return pandas.read_csv(c19.CSV_USA, parse_dates=[0]).set_index('date')


__all__ = ['get_data_frame_usa']
