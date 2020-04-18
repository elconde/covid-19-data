"""Generate a line chart of the top counties"""
import argparse

import matplotlib.pyplot
import c19


def parse_args():
    """Parse the command line arguments"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scale-by-population', action='store_true')
    parser.add_argument('--number', default=5, type=int)
    return parser.parse_args()


def main():
    """Plot the top n counties"""
    args = parse_args()
    data_frame = c19.get_data_frame_counties()
    pivot_table = data_frame.pivot_table(
        values='cases', index='date', columns=('state', 'county', 'fips')
    )
    if args.scale_by_population:
        stats = c19.get_county_statistics()
        for state, county, fips in pivot_table:
            population = c19.get_county_population(stats, fips)
            pivot_table[(state, county, fips)] = (
                pivot_table[(state, county, fips)] / population
            )
    max_date = pivot_table.index.max()
    top_n_counties = (
        pivot_table.loc[max_date].nlargest(args.number).index.values
    )
    pivot_table_top = pivot_table[top_n_counties].dropna(how='any')
    pivot_table_top.columns = [
        '{}, {}'.format(county, state)
        for state, county, fips in pivot_table_top
    ]
    print(pivot_table_top.iloc[-1])
    pivot_table_top.plot(logy=True)
    matplotlib.pyplot.show()


if __name__ == '__main__':
    main()
