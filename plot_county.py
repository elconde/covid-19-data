"""Plot the cases or deaths of a given county"""
import c19
import argparse


def parse_args():
    """Parse the command line arguments"""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--county', default='New York City', help='County')
    parser.add_argument('--state', default='New York', help='State')
    parser.add_argument('--window', default=7, help='Avg. Window', type=int)
    parser.add_argument(
        '--series', default='cases', choices=['cases', 'deaths'],
        help='Which series to plot'
    )
    return parser.parse_args()


def main():
    """Plot the cases or deaths of a given county"""
    args = parse_args()
    c19.plot_series_and_doubling(
        c19.get_data_frame_county(args.county, args.state),
        'cases', args.window
    )


if __name__ == '__main__':
    main()
