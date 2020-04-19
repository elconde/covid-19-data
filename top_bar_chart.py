"""Generate a line chart of the top states"""
import matplotlib.pyplot
import c19

SCALE_BY_POPULATION = True


def main():
    """View NYTimes Covid-19 data"""
    pivot_table_top = (
        c19.get_pivot_table_states(
            SCALE_BY_POPULATION
        ).iloc[-1].sort_values(ascending=False)
    )
    print(pivot_table_top)
    pivot_table_top.plot.bar()
    matplotlib.pyplot.show()


if __name__ == '__main__':
    main()
