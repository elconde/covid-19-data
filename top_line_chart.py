"""Generate a line chart of the top states"""
import matplotlib.pyplot
import c19


def main():
    """View NYTimes Covid-19 data"""
    data_frame = c19.get_data_frame_states()
    max_date = data_frame['date'].max()
    top_ten_states = (
        data_frame[
            data_frame['date'] == max_date
        ].nlargest(10, 'cases')['state'].values
    )
    data_frame_plot = data_frame[data_frame['state'].isin(top_ten_states)]
    pivot_table = data_frame_plot.pivot_table(values='cases', index='date', columns='state')
    print(pivot_table)
    pivot_table.plot(logy=True)
    matplotlib.pyplot.show()


if __name__ == '__main__':
    main()
