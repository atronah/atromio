import logging
from datetime import datetime

from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError

from atromio.core.transfer import make_transfer
from ..core.account import add_account, get_accounts, add_real_balance

log = logging.getLogger(__name__)


@view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
def accounts_view(request):
    try:
        s = request.dbsession
        accounts = get_accounts(s)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'accounts': accounts, 'project': 'atromio'}


@view_config(route_name='add_account', request_method='POST')
def add_account_view(request):
    account_name = request.POST.get('account_name')
    add_account(request.dbsession, account_name)
    url = request.route_url('home')
    return HTTPFound(location=url)


@view_config(route_name='add_transfer', request_method='POST')
def add_transfer_view(request):
    source_account_id = request.POST.get('source_account_id')
    target_account_id = request.POST.get('target_account_id')
    committed_date = datetime.strptime(request.POST.get('committed_date'), '%Y-%m-%d').date()
    committed_time = datetime.strptime(request.POST.get('committed_time'), '%H:%M:%S').time()
    committed_at = datetime.combine(committed_date, committed_time)
    amount = int(request.POST.get('amount'))
    if amount:
        make_transfer(request.dbsession,
                      amount,
                      committed_at,
                      source_account_id,
                      target_account_id if target_account_id else None)
    url = request.route_url('home')
    return HTTPFound(location=url)


@view_config(route_name='add_real_balance', request_method='POST')
def add_real_balance_view(request):
    account_id = request.POST.get('account_id')
    amount = int(request.POST.get('amount'))
    confirmed_date = datetime.strptime(request.POST.get('confirmed_date'), '%Y-%m-%d').date()
    confirmed_time = datetime.strptime(request.POST.get('confirmed_time'), '%H:%M:%S').time()
    confirmed_at = datetime.combine(confirmed_date, confirmed_time)
    add_real_balance(request.dbsession, account_id, amount, confirmed_at)
    url = request.route_url('home')
    return HTTPFound(location=url)


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_atromio_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
