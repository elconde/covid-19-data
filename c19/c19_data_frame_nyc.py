import pandas
import os

CSV_COUNTIES = os.path.join(
    os.path.dirname(__file__), os.pardir, 'us-counties.csv'
)


def get_data_frame_nyc():
    data_frame = pandas.read_csv(CSV_COUNTIES)
    return (
        data_frame[data_frame['county'] == 'New York City'][['date', 'cases']]
    ).set_index('date')


__all__ = ['get_data_frame_nyc', 'CSV_COUNTIES']
