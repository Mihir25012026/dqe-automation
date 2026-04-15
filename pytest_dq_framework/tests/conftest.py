import pytest

from pytest_dq_framework.src.connectors.postgres.postgres_connector import PostgresConnectorContextManager
from pytest_dq_framework.src.connectors.file_system.parquet_reader import ParquetReader

def pytest_addoption(parser):
    parser.addoption("--db_host", action="store", default="localhost")
    parser.addoption("--db_name", action="store", default="mydb")
    parser.addoption("--db_port", action="store", default="5432")
    parser.addoption("--db_user", action="store")
    parser.addoption("--db_password", action="store")

def pytest_configure(config):
    """
    Validates that all required command-line options are provided.
    """
    required_options = [
        "--db_user", "--db_password"
    ]
    for option in required_options:
        if not config.getoption(option):
            pytest.fail(f"Missing required option: {option}")

@pytest.fixture(scope='session')
def parquet_reader(request):
    try:
        reader = ParquetReader()
        yield reader
    except Exception as e:
        pytest.fail(f"Failed to initialize ParquetReader: {e}")
    finally:
        del reader



@pytest.fixture(scope='session')
def db_connection(request):
    db_host = request.config.getoption("--db_host")
    db_name = request.config.getoption("--db_name")
    db_port = request.config.getoption("--db_port")
    db_user = request.config.getoption("--db_user")
    db_password = request.config.getoption("--db_password")
    try:
        with PostgresConnectorContextManager(
                db_host=db_host,
                db_name=db_name,
                db_port=db_port,
                db_user=db_user,
                db_password=db_password
        ) as db_connector:

            yield db_connector

    except Exception as e:
        pytest.fail(f"Failed to initialize DB connection: {e}")
