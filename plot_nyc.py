"""Plot New York City cases"""
import matplotlib.pyplot
import pandas
import os

CSV_FILE_NAME = os.path.join(os.path.dirname(__file__), 'us-counties.csv')


def main():
    """View NYTimes Covid-19 data"""
    data_frame = pandas.read_csv(CSV_FILE_NAME)
    data_frame_ny = (
        data_frame[data_frame['county'] == 'New York City'][['date', 'cases']]
    ).set_index('date')
    print(data_frame_ny)
    data_frame_ny.plot(logy=True)
    matplotlib.pyplot.show()


if __name__ == '__main__':
    main()
