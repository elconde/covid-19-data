"""Generate a line chart of the top states"""
import matplotlib.pyplot
import c19

N = 5
SCALE_BY_POPULATION = True


def main():
    """View NYTimes Covid-19 data"""
    pivot_table_top = get_pivot_table_top_n_states(N, SCALE_BY_POPULATION)
    print(pivot_table_top)
    pivot_table_top.plot(logy=True)
    matplotlib.pyplot.show()


def get_pivot_table_top_n_states(n, scale_by_population):
    """Get a pivot table with the top n states"""
    data_frame = c19.get_data_frame_states()
    pivot_table = data_frame.pivot_table(
        values='cases', index='date', columns='state'
    )
    if scale_by_population:
        stats = c19.get_county_statistics()
        for column in pivot_table:
            pivot_table[column] = (
                    pivot_table[column] / c19.get_state_population(stats,
                                                                   column)
            )
    max_date = pivot_table.index.max()
    top_n_states = pivot_table.loc[max_date].nlargest(n).index.values
    pivot_table_top = pivot_table[top_n_states].dropna(how='any')
    return pivot_table_top


if __name__ == '__main__':
    main()
