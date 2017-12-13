import pytest

from db import setup_from_file
from db.meta.base import DatabaseModel


@pytest.fixture(scope="session")
def setup_engine():
    engine = setup_from_file('../atromio.ini', 'test.')
    DatabaseModel.metadata.create_all(engine)
    return engine