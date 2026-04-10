import pytest
import csv
import os

# Fixture to read the CSV file
@pytest.fixture(scope="session")
def csv_data():
    base_dir = os.path.dirname(os.path.dirname(__file__))

    file_path = os.path.join(base_dir, "src", "data", "data.csv")
    with open(file_path, mode = 'r') as f:
        reader = csv.DictReader(f)
        data =  list(reader)
        return data







# Fixture to validate the schema of the file
@pytest.fixture(scope = "session")
def schema_validate():
    def _validate(expected_schema, actual_schema):
        return set(expected_schema) == set(actual_schema)
    return _validate


# Pytest hook to mark unmarked tests with a custom mark
def pytest_collection_modifyitems(config, items):
    for item in items:
        if not item.own_markers:
            item.add_marker("unmarked")

