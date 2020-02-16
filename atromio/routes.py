import logging
from datetime import datetime

from pyramid.traversal import find_root
from sqlalchemy import inspect

from atromio.models import Account, Transfer

logger = logging.getLogger('atromio')


class LocatedAwareResource(object):
    def __init__(self, name, parent):
        self.__name__ = name
        self.__parent__ = parent


class Resource(LocatedAwareResource):
    data_class = None

    def retrieve(self, request):
        logger.debug(f'retrieving resource {self.__name__}')
        session = request.dbsession
        resource_data = session.query(self.data_class).get(self.__name__)
        return resource_data

    def __json__(self, request):
        json = {}
        resource_data = self.retrieve(request)
        logger.debug(f'format resource {self.__name__} to json')
        for column in inspect(self.data_class).columns:
            key = column.name
            value = getattr(resource_data, key)
            if isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            json[key] = value

        return json


class ResourcesCollection(LocatedAwareResource):
    resource_class = None

    def __init__(self, name, parent, collection_data=None):
        self.collection_data = collection_data
        super().__init__(name, parent)

    def __getitem__(self, name):
        return self.resource_class(name, self)

    def retrieve(self, request):
        if self.collection_data is not None:
            logger.debug(f'{self.collection_data}')
            return self.collection_data
        logger.debug('loading')
        session = request.dbsession
        collection_data = session.query(self.resource_class.data_class)
        return collection_data

    def create(self, request):
        session = request.dbsession
        params = request.json_body
        resource_data = self.resource_class.data_class(**params)
        session.add(resource_data)
        session.flush()
        return self.resource_class(inspect(resource_data).identity, self)

    def __json__(self, request):
        return [self.resource_class(inspect(resource_data).identity, self).__json__(request)
                for resource_data in self.retrieve(request)]


class TransferResource(Resource):
    data_class = Transfer


class TransferCollection(ResourcesCollection):
    resource_class = TransferResource


class AccountResource(Resource):
    data_class = Account

    def __getitem__(self, name):
        logger.debug(name)
        if name == 'transfers':
            return TransferCollection(name, self, getattr(self.retrieve(find_root(self).request), name))
        raise KeyError


class AccountsCollection(ResourcesCollection):
    resource_class = AccountResource


class Root(LocatedAwareResource):
    def __init__(self, request):
        self.request = request
        super().__init__('', None)

    def __getitem__(self, name):
        return {
            'accounts': AccountsCollection
        }.get(name)(name, self)


def get_root(request):
    return Root(request)


'''
    /accounts 
        GET - returns list of accounts
        POST - adds new account
    /accounts/:id
        GET - returns info about account (name, balance, owner)
        PUT - update info
    /accounts/:id/transfers[?after=:after_time&before=:before_time]
        GET - returns incomes (deposits) to specified account and outcomes (withdrawals) from it
        POST - adds transfer from specified account to another or backward
    /accounts/:id/real_balances
        GET - returns list of real balances (real amounts after checking)
        POST - adds new real balance for the account
'''


def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.set_root_factory(get_root)
    config.add_route('add_account', '/add_account')
    config.add_route('add_transfer', '/add_transfer')
    config.add_route('add_real_balance', '/add_real_balance')
