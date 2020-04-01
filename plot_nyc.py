"""Plot New York City cases"""
import matplotlib.pyplot
import math
import c19


def main():
    """View NYTimes Covid-19 data"""
    data_frame_ny = c19.get_data_frame_nyc()
    data_frame_ny['doubling rate (days)'] = math.nan
    cases = data_frame_ny['cases']
    for i in range(1, len(data_frame_ny)):
        denominator = math.log2(cases.iat[i]/cases[i-1])
        if denominator == 0:
            continue
        data_frame_ny['doubling rate (days)'].iat[i] = 1/denominator
    print(data_frame_ny)
    data_frame_ny.plot(logy=True)
    matplotlib.pyplot.show()


if __name__ == '__main__':
    main()
