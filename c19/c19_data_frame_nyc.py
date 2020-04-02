import pandas
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
CSV_COUNTIES = os.path.join(ROOT_DIR, 'us-counties.csv')
CSV_STATES = os.path.join(ROOT_DIR, 'us-states.csv')


def get_data_frame_nyc():
    data_frame = pandas.read_csv(CSV_COUNTIES)
    return (
        data_frame[data_frame['county'] == 'New York City'][['date', 'cases']]
    ).set_index('date')


__all__ = ['get_data_frame_nyc', 'CSV_COUNTIES', 'CSV_STATES']
