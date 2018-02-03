from pyramid import testing


def dummy_request(dbsession):
    return testing.DummyRequest(dbsession=dbsession)

def test_failing_view(setup_database):
    _, session_factory = setup_database
    from ..views.default import accounts_view
    info = accounts_view(dummy_request(session_factory()))
    assert info.status_int == 500


def test_passing_view(init_data):
    session = init_data
    from ..views.default import accounts_view
    info = accounts_view(dummy_request(session))
    assert info['project'] == 'atromio'
    assert len(info['accounts']) == 3
    assert 'cash' in info['accounts']





