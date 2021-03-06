atromio
=======

**atromio** is an abbreviation of "ATROnah's Money is In Order".

It is a program for budget accounting: receipts and expenditure, borrowing, expired dates of goods, billings, price developments, exchange rates.

The idea came in about 2013.


end goal
========

Finally I want to get the accounting core with telegram-bot interface, to

- manage accounts (create/delete/modify, get balance, made transfers between, etc)
- useful and fast registration expenses (shopping, services, etc) and incomes (salary, sponsoring, etc)
    - templates (including support rules for flexible amounts)
    - suggestions
    - auto-payments
- build reports in different slice
- monitoring best prices
- monitoring expiration dates and goods lifespan (pharmacy, appliances, etc)


stack of technologies
=====================

- Python for core logic (because I like it)
    - [sqlalchemy][] for interaction with database, because it powerful and flexible
    - [alembic] for database migration, because it is made by [sqlalchemy] author and looks good
    - [pytest] for testing, because it easy to write tests
- SQLite as main dbms (but not the only one in the feature), because it very lightweight.


Getting Started
===============

- `python3 -m venv env` - create a Python virtual environment.
- `env/bin/activate` - activate virtual enviroment.
- `env/bin/pip install --upgrade pip setuptools` - upgrade packaging tools.
- i`env/bin/pip install -e ".[testing]"` - install the project in editable mode with its testing requirements.
- `env/bin/initialize_atromio_db development.ini` - configure the database.
- `env/bin/pytest` - run your project's tests.
- `env/bin/pserve development.ini` - run your project.
 
 
[sqlalchemy]: http://www.sqlalchemy.org/
[alembic]: http://alembic.zzzcomputing.com/en/latest/
[pytest]: https://docs.pytest.org/en/latest/