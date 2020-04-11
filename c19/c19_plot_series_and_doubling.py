import math
import matplotlib.pyplot


def plot_series_and_doubling(data_frame, series_name, avg_window, logy=True):
    """Plot the series and the doubling rate"""
    assert series_name in ('cases', 'deaths', 'diff')
    column_name = 'doubling rate ({} day avg.)'.format(avg_window)
    data_frame[column_name] = math.nan
    to_drop = ['cases', 'deaths']
    if series_name == 'diff':
        to_drop.append('diff')
        data_frame['diff'] = data_frame['cases'] - data_frame['deaths']
    series = data_frame[series_name]
    len_ = len(data_frame)
    for i in range(avg_window, len_):
        denominator = math.log2(series.iat[i] / series[i - avg_window])
        if denominator in (0, math.inf):
            continue
        doubling_rate = avg_window / denominator
        data_frame[column_name].iat[i] = doubling_rate
    print(data_frame)
    to_drop.remove(series_name)
    data_frame.drop(labels=to_drop, axis=1, inplace=True)
    print(data_frame)
    data_frame.plot(logy=logy)
    matplotlib.pyplot.show()


__all__ = ['plot_series_and_doubling']
