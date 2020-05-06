"""Plot new cases or deaths"""
import c19
import matplotlib.pyplot
import pandas

STATES = ['New York']


def main():
    """Plot new cases or deaths"""
    pivot_table = c19.get_pivot_table_states(False)
    data_frames = []
    for state in STATES:
        data_frame_state = pivot_table[state]
        data_frames.append(data_frame_state)
        pivot_table.drop(state, axis=1, inplace=True)
    data_frames.append(pivot_table.sum(axis=1))
    data_frame = pandas.concat(data_frames, axis=1)
    data_frame = (data_frame - data_frame.shift(7))/7
    data_frame = data_frame.rename(columns={0: 'Remainder'}).dropna()
    print(data_frame)
    data_frame.plot()
    matplotlib.pyplot.show()


if __name__ == '__main__':
    main()
