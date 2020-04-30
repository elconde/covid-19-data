"""Plot the cases or deaths of a given state, county, or countrywide."""
import c19


def main():
    """Plot the cases or deaths of a given state, county, or countrywide."""
    args = c19.parse_args()
    c19.plot_series_and_doubling(args.data_frame, args.series, args.window)


if __name__ == '__main__':
    main()
