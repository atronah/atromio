import pytest

from db.account import Account
from db.meta.base import Session, start_session


@pytest.fixture(scope='module')
def init_test_data():
    account = Account(name='test')
    with start_session(Session) as s:
        s.add(account)
    return account


def test_dummy(setup_engine, init_test_data):
    pass

