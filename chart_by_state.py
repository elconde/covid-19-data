"""View NYTimes Covid-19 data"""
import matplotlib.pyplot
import pandas
import c19

STATES = ['Massachusetts', 'Pennsylvania', 'New York', 'New Jersey']
MULTIPLIER = 1e6


def get_state_population(statistics, state):
    """Get the population of the state"""
    state_abbr = c19.parse_state_name(state)
    return (
        statistics[
            statistics['State'] == state_abbr
        ]['Population (2010)'].sum()
    )


def main():
    """View NYTimes Covid-19 data"""
    data_frame = pandas.read_csv(c19.CSV_STATES)
    statistics = c19.get_county_statistics()
    data_frame_chart = data_frame[data_frame['state'].isin(STATES)]
    pivot_table = data_frame_chart.pivot_table(
        values='cases', index='date', columns=['state'], aggfunc=sum
    )
    for state in STATES:
        population = get_state_population(statistics, state)
        pivot_table[state] = pivot_table[state] / population * MULTIPLIER
    print(pivot_table)
    pivot_table.plot(logy=True)
    matplotlib.pyplot.show()


if __name__ == '__main__':
    main()
