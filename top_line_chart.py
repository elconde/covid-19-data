"""Generate a line chart of the top states"""
import matplotlib.pyplot
import c19

N = 5
SCALE_BY_POPULATION = True


def main():
    """View NYTimes Covid-19 data"""
    data_frame = c19.get_data_frame_states()
    pivot_table = data_frame.pivot_table(
        values='cases', index='date', columns='state'
    )
    if SCALE_BY_POPULATION:
        stats = c19.get_county_statistics()
        for column in pivot_table:
            population = c19.get_state_population(stats, column)
            pivot_table[column] = pivot_table[column] / population * 1e6
    max_date = pivot_table.index.max()
    top_n_states = pivot_table.loc[max_date].nlargest(N).index.values
    pivot_table_top = pivot_table[top_n_states]
    pivot_table_top.plot(logy=True)
    matplotlib.pyplot.show()


if __name__ == '__main__':
    main()
