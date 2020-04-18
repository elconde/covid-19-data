"""Generate a line chart of all the states"""
import matplotlib.pyplot
import c19
import argparse


def parse_args():
    """Parse the command line arguments"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scale-by-population', action='store_true')
    return parser.parse_args()


def main():
    """View NYTimes Covid-19 data"""
    data_frame = c19.get_data_frame_states()
    pivot_table = data_frame.pivot_table(
        values='cases', index='date', columns='state'
    )
    if parse_args().scale_by_population:
        stats = c19.get_county_statistics()
        ny_population = c19.get_state_population(stats, 'New York')
        for column in pivot_table:
            if column == 'New York':
                population = ny_population
            else:
                population = c19.get_state_population(stats, column)
            pivot_table[column] = (
                pivot_table[column] / population * ny_population
            )
    pivot_table.plot(
        logy=True, subplots=True, layout=(8, 8), ylim=(1, 215000)
    )
    matplotlib.pyplot.show()


if __name__ == '__main__':
    main()
