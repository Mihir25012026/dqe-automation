"""
Description: Data Quality checks ...
Requirement(s): TICKET-1234
Author(s): Name Surname
"""

import pytest
from pytest_dq_framework.src.data_quality.data_quality_validation_library import DataQualityLibrary

@pytest.fixture(scope='module')
def source_data(db_connection):
    source_query = """
    SELECT 
        f.facility_type,
        DATE(v.visit_timestamp) as visit_date,
        ROUND(AVG(v.duration_minutes), 2) as avg_time_spent
    FROM visits v
    JOIN facilities f ON v.facility_id = f.id
    GROUP BY f.facility_type, DATE(v.visit_timestamp)
    """
    source_data = db_connection.get_data_sql(source_query)
    return source_data


@pytest.fixture(scope='module')
def target_data(parquet_reader):
    target_path = "/parquet_data/facility_type_avg_time_spent_per_visit_date"
    target_data = parquet_reader.process(target_path)
    return target_data

@pytest.fixture(scope="module")
def data_quality_library():
    return DataQualityLibrary()

@pytest.mark.example
def test_check_dataset_is_not_empty(target_data, data_quality_library):
    data_quality_library.check_dataset_is_not_empty(target_data)


@pytest.mark.example
def test_check_count(source_data, target_data, data_quality_library):
    data_quality_library.check_count(source_data, target_data)
