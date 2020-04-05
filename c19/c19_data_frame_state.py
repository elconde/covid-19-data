import pandas
import c19


def get_data_frame_state(state_name):
    data_frame = pandas.read_csv(c19.CSV_STATES, parse_dates=[0])
    return (
        data_frame[data_frame['state'] == state_name]
        [['date', 'cases', 'deaths']]
    ).set_index('date')


__all__ = ['get_data_frame_state']
