import pandas
import c19


def get_data_frame_state(state_name):
    data_frame = get_data_frame_states()
    return (
        data_frame[data_frame['state'] == state_name]
        [['date', 'cases', 'deaths']]
    ).set_index('date')


def get_data_frame_states():
    return pandas.read_csv(c19.CSV_STATES, parse_dates=[0])


__all__ = ['get_data_frame_state', 'get_data_frame_states']
