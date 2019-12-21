def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('add_account', '/add_account')
    config.add_route('add_transfer', '/add_transfer')
