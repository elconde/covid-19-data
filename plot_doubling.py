"""Plot doubling rates"""
import matplotlib.pyplot
import math
import c19

AVG_WINDOW = 7
COUNTIES = [
    ('Camden', 'New Jersey'),
    ('New York City', 'New York'),
    ('Middlesex', 'Massachusetts')
]


def get_county_pivot_table():
    data_frame = c19.get_data_frame_counties()
    pivot_table = data_frame.pivot_table(
        values='cases', index='date', columns=['county', 'state'], aggfunc=sum
    )
    return pivot_table


def main():
    """View NYTimes Covid-19 data"""
    pivot_table = get_county_pivot_table()[COUNTIES]
    dr_column_names = []
    for county, state in COUNTIES:
        dr_column_name = county + ' doubling rate'
        dr_column_names += [dr_column_name]
        pivot_table[dr_column_name] = math.nan
        for i in range(AVG_WINDOW, len(pivot_table)):
            cases = pivot_table[(county, state)]
            denominator = math.log2(cases.iat[i]/cases.iat[i - AVG_WINDOW])
            if denominator == 0:
                continue
            pivot_table[(dr_column_name, '')].iat[i] = AVG_WINDOW / denominator
    pivot_table_plot = pivot_table[dr_column_names]
    print(pivot_table_plot)
    pivot_table_plot.plot(logy=False)
    matplotlib.pyplot.show()


if __name__ == '__main__':
    main()
