from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import Account


@view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
def accounts_view(request):
    try:
        query = request.dbsession.query(Account.name)
        name_list = [a.name for a in query.all()]
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'accounts': name_list, 'project': 'atromio'}


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