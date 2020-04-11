"""Line chart of user-supplied states"""
import matplotlib.pyplot
import pandas
import c19

STATES = ['Massachusetts', 'Pennsylvania', 'New York', 'New Jersey']
MULTIPLIER = 1e6


def main():
    """Line chart of user-supplied states"""
    data_frame = pandas.read_csv(c19.CSV_STATES)
    statistics = c19.get_county_statistics()
    data_frame_chart = data_frame[data_frame['state'].isin(STATES)]
    pivot_table = data_frame_chart.pivot_table(
        values='cases', index='date', columns=['state'], aggfunc=sum
    ).dropna()
    for state in STATES:
        population = c19.get_state_population(statistics, state)
        pivot_table[state] = pivot_table[state] / population * MULTIPLIER
    print(pivot_table)
    pivot_table.plot(logy=True)
    matplotlib.pyplot.show()


if __name__ == '__main__':
    main()
