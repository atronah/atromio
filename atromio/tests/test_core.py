def test_account_add(init_data):
    tm_session = init_data
    from ..core import account
    from ..models import Account

    count = len(tm_session.query(Account.name).all())
    assert account.add_account(tm_session, 'test') > 0
    assert len(tm_session.query(Account.name).all()) == count + 1


def test_account_list(init_data):
    tm_session = init_data
    from ..core import account
    accounts = account.accounts(tm_session)
    assert len(accounts) == 3
    names = [name for _, name in accounts]
    assert 'cash' in names
    assert 'bank' in names
    assert 'transport' in names


