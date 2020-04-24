"""Plot the cases or deaths of a given county"""
import c19
import argparse
import sys


def parse_args():
    """Parse the command line arguments"""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        allow_abbrev=False
    )
    parser.add_argument('--county', default='New York City', help='County')
    parser.add_argument('--state', default='New York', help='State')
    parser.add_argument('--window', default=7, help='Avg. Window', type=int)
    parser.add_argument(
        '--series', default='cases', choices=['cases', 'deaths'],
        help='Which series to plot'
    )
    argv = sys.argv[1:]
    state_in_argv = False
    county_in_argv = False
    for arg in argv:
        if not state_in_argv and arg.startswith('--state'):
            state_in_argv = True
        if not county_in_argv and arg.startswith('--county'):
            county_in_argv = True
        if state_in_argv and county_in_argv:
            break
    args = parser.parse_args()
    if state_in_argv and not county_in_argv:
        args.county = ''
    if not state_in_argv and county_in_argv:
        print('--state is mandatory when --county is supplied!')
        sys.exit(1)
    return args


def main():
    """Plot the cases or deaths of a given county"""
    args = parse_args()
    if not args.county:
        data_frame = c19.get_data_frame_state(args.state)
        print(args.state, 'State')
    else:
        data_frame = c19.get_data_frame_county(args.county, args.state)
        print('{}, {}'.format(args.county, args.state))
    c19.plot_series_and_doubling(data_frame, 'cases', args.window)


if __name__ == '__main__':
    main()
