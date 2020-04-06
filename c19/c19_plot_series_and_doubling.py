import math
import matplotlib.pyplot


def plot_series_and_doubling(data_frame, series_name, avg_window):
    """Plot the series and the doubling rate"""
    assert series_name in ('cases', 'deaths')
    column_name = 'doubling rate ({} day avg.)'.format(avg_window)
    data_frame[column_name] = math.nan
    series = data_frame[series_name]
    len_ = len(data_frame)
    for i in range(avg_window, len_):
        denominator = math.log2(series.iat[i] / series[i - avg_window])
        if denominator in (0, math.inf):
            continue
        doubling_rate = avg_window / denominator
        data_frame[column_name].iat[i] = doubling_rate
    if series_name == 'cases':
        to_drop = 'deaths'
    else:
        to_drop = 'cases'
    data_frame.drop(labels=[to_drop], axis=1, inplace=True)
    print(data_frame)
    data_frame.plot(logy=True)
    matplotlib.pyplot.show()


__all__ = ['plot_series_and_doubling']
