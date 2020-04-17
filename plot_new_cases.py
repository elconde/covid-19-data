"""Plot new cases for a given county"""
import c19
import matplotlib.pyplot

AVG_WINDOW = 7


def main():
    """Plot new cases for a given county"""
    data_frame = c19.get_data_frame_county('New York City', 'New York')
    column_name = 'new cases ({} day avg.)'.format(AVG_WINDOW)
    data_frame[column_name] = (
        data_frame['cases'] - data_frame['cases'].shift(AVG_WINDOW)
    ) / AVG_WINDOW
    data_frame[column_name].dropna().plot()
    print(data_frame[column_name])
    matplotlib.pyplot.show()


if __name__ == '__main__':
    main()
