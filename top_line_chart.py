"""Generate a line chart of the top states"""
import matplotlib.pyplot
import c19

N = 5
SCALE_BY_POPULATION = True


def main():
    """View NYTimes Covid-19 data"""
    pivot_table_top = c19.get_pivot_table_top_n_states(N, SCALE_BY_POPULATION)
    print(pivot_table_top)
    pivot_table_top.plot(logy=True)
    matplotlib.pyplot.show()


if __name__ == '__main__':
    main()
