"""Plot new cases or deaths"""
import c19
import matplotlib.pyplot


def main():
    """Plot new cases or deaths"""
    args = c19.parse_args()
    data_frame = args.data_frame
    series = args.series
    column_name = 'new {} ({} day avg.)'.format(series, args.window)
    data_frame[column_name] = (
        data_frame[series] - data_frame[series].shift(args.window)
    ) / args.window
    data_frame[column_name].dropna(inplace=True)
    print(data_frame[column_name])
    data_frame[column_name].plot()
    matplotlib.pyplot.show()


if __name__ == '__main__':
    main()
