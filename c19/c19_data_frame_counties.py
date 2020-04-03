import c19
import pandas


def get_data_frame_counties():
    return pandas.read_csv(c19.CSV_COUNTIES)


__all__ = ['get_data_frame_counties']