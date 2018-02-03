# noinspection PyAttributeOutsideInit
import transaction


class TestAccount(object):
    def test_account_add(self, init_data):
        tm_session = init_data
        from ..core import account
        from ..models import Account

        count = len(tm_session.query(Account.name).all())
        assert account.add_account(tm_session, 'test') > 0
        assert len(tm_session.query(Account.name).all()) == count + 1





