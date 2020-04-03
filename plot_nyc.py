"""Plot New York City cases"""
import matplotlib.pyplot
import math
import c19

AVG_WINDOW = 7


def main():
    """View NYTimes Covid-19 data"""
    data_frame_ny = c19.get_data_frame_nyc()
    column_name = 'doubling rate ({} day avg.)'.format(AVG_WINDOW)
    data_frame_ny[column_name] = math.nan
    cases = data_frame_ny['cases']
    for i in range(AVG_WINDOW, len(data_frame_ny)):
        denominator = math.log2(cases.iat[i]/cases[i-AVG_WINDOW])
        if denominator == 0:
            continue
        data_frame_ny[column_name].iat[i] = AVG_WINDOW/denominator
    print(data_frame_ny)
    data_frame_ny.plot(logy=True)
    matplotlib.pyplot.show()


if __name__ == '__main__':
    main()
