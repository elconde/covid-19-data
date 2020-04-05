import c19


def get_data_frame_nyc():
    data_frame = c19.get_data_frame_counties()
    return (
        data_frame[data_frame['county'] == 'New York City'][['date', 'cases', 'deaths']]
    ).set_index('date')


__all__ = ['get_data_frame_nyc']
