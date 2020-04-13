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
        ny_population = c19.get_state_population(stats, 'New York')
        print('NY population: ', ny_population)
        for column in pivot_table:
            if column == 'New York':
                population = ny_population
            else:
                population = c19.get_state_population(stats, column)
            pivot_table[column] = (
                pivot_table[column] / population * ny_population
            )
    max_date = pivot_table.index.max()
    top_n_states = pivot_table.loc[max_date].nlargest(N).index.values
    pivot_table_top = pivot_table[top_n_states].dropna(how='any')
    print(pivot_table_top)
    pivot_table_top.plot(logy=True)
    matplotlib.pyplot.show()


if __name__ == '__main__':
    main()
