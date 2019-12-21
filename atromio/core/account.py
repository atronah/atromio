import transaction

from atromio.models import Account


def add_account(session, name):
    account = Account(name=name)
    session.add(account)
    session.flush()
    return account.id


def get_accounts(session):
    return [(a.id, a.name) for a in session.query(Account).all()]