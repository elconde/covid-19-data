"""Generate a line chart of the top counties"""
import matplotlib.pyplot
import c19

N = 5
SCALE_BY_POPULATION = True


def main():
    """View NYTimes Covid-19 data"""
    data_frame = c19.get_data_frame_counties()
    pivot_table = data_frame.pivot_table(
        values='cases', index='date', columns=('state', 'county', 'fips')
    )
    if SCALE_BY_POPULATION:
        stats = c19.get_county_statistics()
        for state, county, fips in pivot_table:
            if fips in c19.FIPS_OUTER_BOROUGHS:
                continue
            population = c19.get_population(fips, stats)
            pivot_table[(state, county, fips)] = (
                pivot_table[(state, county, fips)] / population * 1e6
            )
    max_date = pivot_table.index.max()
    top_n_counties = pivot_table.loc[max_date].nlargest(N).index.values
    pivot_table_top = pivot_table[top_n_counties].dropna(how='any')
    print(pivot_table_top)
    pivot_table_top.plot(logy=True)
    matplotlib.pyplot.show()


if __name__ == '__main__':
    main()
