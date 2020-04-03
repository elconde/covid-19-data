"""View NYTimes Covid-19 data"""
import matplotlib.pyplot
import pandas
import c19

COUNTIES = [
    ('New York City', 'New York'),
    ('Middlesex', 'Massachusetts'),
    ('Centre', 'Pennsylvania'),
    ('Lehigh', 'Pennsylvania')
]
FIPS = [36061, 25017, 42027, 42077]

def main():
    """View NYTimes Covid-19 data"""
    data_frame = pandas.read_csv(c19.CSV_COUNTIES)
    pivot_table = data_frame.pivot_table(
        values='cases', index='date', columns=['county', 'state'], aggfunc=sum
    )[COUNTIES]
    statistics = c19.get_county_statistics()
    for county, fips in zip(COUNTIES, FIPS):
        pivot_table[county] = pivot_table[county] / c19.get_population(fips, statistics)*10000
    print(pivot_table.iloc[-1].sort_values())
    pivot_table.plot(logy=True)
    matplotlib.pyplot.show()


if __name__ == '__main__':
    main()
