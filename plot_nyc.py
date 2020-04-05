"""Plot New York City cases"""
import matplotlib.pyplot
import math
import c19

AVG_WINDOW = 7
SERIES = 'cases'


def main():
    """View NYTimes Covid-19 data"""
    data_frame_ny = c19.get_data_frame_nyc()
    column_name = 'doubling rate ({} day avg.)'.format(AVG_WINDOW)
    data_frame_ny[column_name] = math.nan
    series = data_frame_ny[SERIES]
    len_ = len(data_frame_ny)
    for i in range(AVG_WINDOW, len_):
        denominator = math.log2(series.iat[i]/series[i-AVG_WINDOW])
        if denominator == 0:
            continue
        doubling_rate = AVG_WINDOW / denominator
        data_frame_ny[column_name].iat[i] = doubling_rate
    if SERIES == 'cases':
        to_drop = 'deaths'
    else:
        to_drop = 'cases'
    data_frame_ny.drop(labels=[to_drop], axis=1, inplace=True)
    print(data_frame_ny)
    data_frame_ny.plot(logy=True)
    matplotlib.pyplot.show()


if __name__ == '__main__':
    main()
