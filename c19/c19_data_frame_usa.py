import pandas
import c19


def get_data_frame_usa(scale_by_population):
    data_frame = pandas.read_csv(c19.CSV_USA, parse_dates=[0]).set_index('date')
    if not scale_by_population:
        return data_frame
    data_frame['Population (2010)'] /= c19.get_usa_population(
        c19.get_county_statistics()
    )
    return data_frame


__all__ = ['get_data_frame_usa']
