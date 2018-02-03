import transaction

from atromio.models import Account


def add_account(session, name):
    with transaction.manager:
        account = Account(name=name)
        session.add(account)
        session.flush()
        return account.id


def accounts(session):
    with transaction.manager:
        return session.query(Account).all()