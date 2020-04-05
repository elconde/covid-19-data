"""Plot New York City cases"""
import c19

AVG_WINDOW = 7


def main():
    """View NYTimes Covid-19 data"""
    c19.plot_series_and_doubling(
        c19.get_data_frame_state('New York'), 'cases', AVG_WINDOW
    )


if __name__ == '__main__':
    main()
