"""Plot new cases for a given county"""
import argparse

import c19
import matplotlib.pyplot


def parse_args():
    """Parse the command line arguments"""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--county', default='New York City', help='County')
    parser.add_argument('--state', default='New York', help='State')
    parser.add_argument('--window', default=7, help='Avg. Window', type=int)
    return parser.parse_args()


def main():
    """Plot new cases for a given county"""
    args = parse_args()
    data_frame = c19.get_data_frame_county(args.county, args.state)
    column_name = 'new cases ({} day avg.)'.format(args.window)
    data_frame[column_name] = (
        data_frame['cases'] - data_frame['cases'].shift(args.window)
    ) / args.window
    data_frame[column_name].dropna().plot()
    print(data_frame[column_name])
    matplotlib.pyplot.show()


if __name__ == '__main__':
    main()
