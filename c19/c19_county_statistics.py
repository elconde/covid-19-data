"""Read the county statistics file"""
import c19
import pandas

NYC_OUTER_BOROUGHS = ['Richmond', 'Queens', 'Kings', 'Bronx']
NYC_BOROUGHS = NYC_OUTER_BOROUGHS+['New York']


def get_county_statistics():
    """Read the county statistics into a data frame. Merge all NYC
    boroughs into one"""
    data_frame = pandas.read_csv(c19.CSV_STATISTICS, thousands=',')
    data_frame['County'].replace(r' \[.*', '', inplace=True, regex=True)
    data_frame_nyc = data_frame[
        (data_frame['State'] == 'NY') & (
            data_frame['County'].isin(NYC_BOROUGHS)
        )
    ]
    nyc_population = data_frame_nyc['Population (2010)'].sum()
    data_frame = data_frame[
        ~(
            (data_frame['State'] == 'NY') &
            (data_frame['County'].isin(NYC_OUTER_BOROUGHS))
        )
    ]
    nyc_loc = (
        data_frame[
            (data_frame['County'] == 'New York') &
            (data_frame['State'] == 'NY')
        ].index.tolist()[0]
    )
    data_frame.at[nyc_loc, 'Population (2010)'] = nyc_population
    return data_frame


__all__ = ['get_county_statistics']
