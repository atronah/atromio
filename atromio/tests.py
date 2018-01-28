import transaction
import pytest

from pyramid import testing


def dummy_request(dbsession):
    return testing.DummyRequest(dbsession=dbsession)


@pytest.fixture(scope='module')
def setup_database():
    config = testing.setUp(settings={'sqlalchemy.url': 'sqlite:///:memory:'})
    config.include('.models')
    settings = config.get_settings()

    from .models import get_engine, get_session_factory
    engine = get_engine(settings)
    session_factory = get_session_factory(engine)

    yield engine, session_factory

    testing.tearDown()
    transaction.abort()


@pytest.fixture(scope='module')
def setup_session(setup_database):
    _, session_factory = setup_database
    from .models import get_tm_session
    session = get_tm_session(session_factory, transaction.manager)

    yield session


@pytest.fixture(scope='function')
def setup_structure(setup_database):
    engine, _ = setup_database
    from .models.meta import Base
    Base.metadata.create_all(engine)

    yield engine

    Base.metadata.drop_all(engine)


@pytest.fixture(scope='function')
def init_data(setup_session, setup_structure):
    session = setup_session
    from .models import Account
    account = Account(name='cash')
    session.add(account)

    yield session


def test_passing_view(init_data):
    session = init_data
    from .views.default import accounts_view
    info = accounts_view(dummy_request(session))
    assert info['project'] == 'atromio'
    assert len(info['accounts']) == 1
    assert 'cash' in info['accounts']


def test_failing_view(setup_session):
    session = setup_session
    from .views.default import accounts_view
    info = accounts_view(dummy_request(session))
    assert info.status_int == 500
