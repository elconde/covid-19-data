"""Plot New York  cases"""
import c19

AVG_WINDOW = 7


def main():
    """View NYTimes Covid-19 data"""
    data_frame = c19.get_data_frame_county('Suffolk', 'New York')
    c19.plot_series_and_doubling(
        data_frame, 'cases', AVG_WINDOW
    )


if __name__ == '__main__':
    main()
