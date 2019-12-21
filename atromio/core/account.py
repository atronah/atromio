import transaction

from atromio.core.transfer import make_transfer
from atromio.models import Account, RealBalance


def add_account(session, name):
    account = Account(name=name)
    session.add(account)
    session.flush()
    return account


def get_accounts(session):
    return session.query(Account).all()


def add_real_balance(session, account_id, real_balance, confirmed_at):
    account = session.query(Account).get(account_id)
    account_balance = account.balance(confirmed_at)
    if real_balance > account_balance:
        make_transfer(session, real_balance - account_balance, confirmed_at, None, account.id)
    elif real_balance < account_balance:
        make_transfer(session, account_balance - real_balance, confirmed_at, account.id, None)
    real_balance = RealBalance(account_id=account_id, amount=real_balance, confirmed_at=confirmed_at)
    session.add(real_balance)
    session.flush()
    return real_balance
