"""What are the fastest growing states?"""
import c19
import matplotlib.pyplot
import math

N = 5
AVG_WINDOW = 7


def main():
    """What are the fastest growing states?"""
    data_frame_states = c19.get_data_frame_states()
    pivot_table = data_frame_states.pivot_table(
        values='cases', index='date', columns='state'
    )
    growths = []
    for state in pivot_table:
        denominator = pivot_table[state].iloc[-AVG_WINDOW]
        if denominator == 0 or math.isnan(denominator):
            continue
        numerator = pivot_table[state].iloc[-1]
        if math.isnan(numerator):
            continue
        growths.append((numerator / denominator, state))
    pivot_table_top = pivot_table[
        [state for growth, state in sorted(growths)[-N:]]
    ].dropna()
    pivot_table_top.plot(logy=True)
    print(pivot_table_top)
    matplotlib.pyplot.show()


if __name__ == '__main__':
    main()
