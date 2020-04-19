"""Pivot tables"""
import c19


def get_pivot_table_states(scale_by_population):
    """Get a pivot table with all the states (including territories)"""
    data_frame = c19.get_data_frame_states()
    pivot_table = data_frame.pivot_table(
        values='cases', index='date', columns='state'
    )
    if scale_by_population:
        stats = c19.get_county_statistics()
        for column in pivot_table:
            pivot_table[column] = (
                pivot_table[column] / c19.get_state_population(stats, column)
            )
    return pivot_table


def get_pivot_table_top_n_states(n, scale_by_population):
    """Get a pivot table with the top n states"""
    pivot_table = get_pivot_table_states(scale_by_population)
    max_date = pivot_table.index.max()
    top_n_states = pivot_table.loc[max_date].nlargest(n).index.values
    pivot_table_top = pivot_table[top_n_states].dropna(how='any')
    return pivot_table_top


__all__ = ['get_pivot_table_states', 'get_pivot_table_top_n_states']
