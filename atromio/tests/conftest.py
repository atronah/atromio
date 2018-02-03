import pytest
import transaction
from pyramid import testing


@pytest.fixture(scope='module')
def setup_database():
    config = testing.setUp(settings={'sqlalchemy.url': 'sqlite:///:memory:'})
    config.include('..models')
    settings = config.get_settings()

    from ..models import get_engine, get_session_factory
    engine = get_engine(settings)
    tm_session_factory = get_session_factory(engine, transaction.manager)

    yield engine, tm_session_factory

    testing.tearDown()
    transaction.abort()


@pytest.fixture(scope='module')
def init_structure(setup_database):
    engine, _ = setup_database
    from ..models.meta import Base
    Base.metadata.create_all(engine)

    yield setup_database

    Base.metadata.drop_all(engine)


@pytest.fixture(scope='module')
def setup_tm_session(init_structure):
    _, tm_session_factory = init_structure
    session = tm_session_factory()

    yield session


@pytest.fixture(scope='module')
def init_data(setup_tm_session):
    session = setup_tm_session
    from ..core import account
    account.add_account(session, 'cash')
    account.add_account(session, 'bank')
    account.add_account(session, 'transport')

    yield session