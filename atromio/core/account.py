import transaction

from atromio.models import Account, RealBalance


def add_account(session, name):
    account = Account(name=name)
    session.add(account)
    session.flush()
    return account


def get_accounts(session):
    return session.query(Account).all()


def add_real_balance(session, account_id, amount, confirmed_at):
    real_balance = RealBalance(account_id=account_id, amount=amount, confirmed_at=confirmed_at)
    session.add(real_balance)
    session.flush()
    return real_balance
