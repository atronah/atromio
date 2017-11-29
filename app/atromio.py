from contextlib import contextmanager
from datetime import datetime

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy.sql import functions as func

from db.account import Account, Transfer, AccountBalance
from db.meta.base import Base

Session = sessionmaker()


@contextmanager
def start_session(session_class):
    session = session_class()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class Atromio(object):
    """Creates instance of app for working with specified db
    
    All arguments will be passed to create_engine() method from sqlalchemy
    """
    def __init__(self, *args, **kwargs):
        self._engine = create_engine(*args, **kwargs)
        self._Session = sessionmaker(bind=self._engine)

    def init_database(self):
        Base.metadata.create_all(self._engine)

    def create_account(self, name, description=None):
        with start_session(self._Session) as s:
            account = Account(name=name, description=description)
            s.add(account)
            return account
        return None


    def get_balance(self, account, at_datetime=None):
        at_datetime = at_datetime or datetime.now()

        with start_session(self._Session) as s:
            if isinstance(account, int):
                account = s.query(Account).get(account)
            incomes = aliased(Transfer)
            expenses = aliased(Transfer)
            balance, total_income, total_expense = \
                s.query(AccountBalance.amount,
                        func.sum(incomes.amount),
                        func.sum(expenses.amount))\
                    .join(incomes,
                          incomes.destination_id == AccountBalance.account_id,
                          isouter=True) \
                    .join(expenses,
                          expenses.source_id == AccountBalance.account_id,
                          isouter=True)\
                    .filter(AccountBalance.account == account)\
                    .filter(AccountBalance.confirmed_at <= at_datetime)\
                    .filter(incomes.committed_at >= AccountBalance.confirmed_at)\
                    .filter(incomes.committed_at <= at_datetime) \
                    .filter(expenses.committed_at >= AccountBalance.confirmed_at)\
                    .filter(expenses.committed_at <= at_datetime)\
                    .group_by(AccountBalance.id)\
                    .order_by(desc(AccountBalance.confirmed_at))\
                    .first() or (None, None, None)
            if balance is None: balance = 0
            if total_income is None: total_income = 0
            if total_expense is None: total_expense = 0
            return balance + total_income - total_expense
        return None


def main():
    app = Atromio('sqlite:///data.db', echo=True)
    app.init_database()

    print('balance:', app.get_balance(1))


if __name__ == '__main__':
    main()