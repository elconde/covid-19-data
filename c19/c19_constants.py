import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
CSV_COUNTIES = os.path.join(ROOT_DIR, 'us-counties.csv')
CSV_STATES = os.path.join(ROOT_DIR, 'us-states.csv')
CSV_STATISTICS = os.path.join(ROOT_DIR, 'statistics.csv')
FIPS_OUTER_BOROUGHS = (36085, 36081, 36047, 36005)
FIPS_MANHATTAN = 36061

__all__ = [
    'ROOT_DIR', 'CSV_COUNTIES', 'CSV_STATES', 'FIPS_OUTER_BOROUGHS',
    'FIPS_MANHATTAN', 'CSV_STATISTICS'
]