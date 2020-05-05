"""Generate a line chart of all the states"""
import matplotlib.pyplot
import c19
import argparse


def parse_args():
    """Parse the command line arguments"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scale-by-population', action='store_true')
    parser.add_argument('--window', default=7)
    return parser.parse_args()


def main():
    """View NYTimes Covid-19 data"""
    args = parse_args()
    pivot_table = c19.get_pivot_table_states(args.scale_by_population)
    pivot_table = (pivot_table - pivot_table.shift(args.window)) / args.window
    latest_row = pivot_table.iloc[-1]
    pivot_table.plot(
        logy=True, subplots=True, layout=(8, 8),
        ylim=(pivot_table.min().min(), pivot_table.max().max()*10)
    )
    print(latest_row)
    matplotlib.pyplot.show()


if __name__ == '__main__':
    main()
