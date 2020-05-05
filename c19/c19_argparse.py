"""Common command line argument parser"""
import c19
import sys
import argparse
import ast
import inspect


def parse_args(argv=sys.argv[1:]):
    """Parse the command line arguments"""
    parser = argparse.ArgumentParser(
        description=get_description(),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        allow_abbrev=False
    )
    parser.add_argument('--county', default='New York City', help='County')
    parser.add_argument('--state', default='New York', help='State')
    parser.add_argument('--window', default=7, help='Avg. Window', type=int)
    parser.add_argument(
        '--usa', action='store_true', help='Show countrywide statistics'
    )
    parser.add_argument(
        '--series', default='cases', choices=['cases', 'deaths'],
        help='Which series to plot'
    )
    state_in_argv = False
    county_in_argv = False
    for arg in argv:
        if not state_in_argv and arg.startswith('--state'):
            state_in_argv = True
        if not county_in_argv and arg.startswith('--county'):
            county_in_argv = True
        if state_in_argv and county_in_argv:
            break
    args = parser.parse_args(argv)
    if state_in_argv and not county_in_argv:
        args.county = ''
    if not state_in_argv and county_in_argv:
        print('--state is mandatory when --county is supplied!')
        sys.exit(1)
    if args.usa:
        args.data_frame = c19.get_data_frame_usa()
    elif not args.county:
        args.data_frame = c19.get_data_frame_state(args.state)
    else:
        args.data_frame = c19.get_data_frame_county(args.county, args.state)
    return args


def get_description():
    """What should the description be?"""
    file_name = inspect.stack()[2].filename
    with open(file_name, 'r') as f:
        tree = ast.parse(f.read())
    doc_string = ast.get_docstring(tree)
    return doc_string


__all__ = ['parse_args']