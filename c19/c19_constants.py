import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
CSV_COUNTIES = os.path.join(ROOT_DIR, 'us-counties.csv')
CSV_STATES = os.path.join(ROOT_DIR, 'us-states.csv')
CSV_STATISTICS = os.path.join(ROOT_DIR, 'statistics.csv')
CSV_USA = os.path.join(ROOT_DIR, 'us.csv')

__all__ = [
    'ROOT_DIR', 'CSV_COUNTIES', 'CSV_STATES', 'CSV_STATISTICS', 'CSV_USA'
]
