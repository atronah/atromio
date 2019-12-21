import transaction

from atromio.models import Account


def add_account(session, name):
    account = Account(name=name)
    session.add(account)
    session.flush()
    return account


def get_accounts(session):
    return session.query(Account).all()