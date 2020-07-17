database_name = 'ordermgt'
database_host = 'localhost'
database_user = 'postgres'
database_password = '1234'
connection = 'postgres://{0}:{1}@{2}/{3}'.format(database_user,
                                                 database_password,
                                                 database_host,
                                                 database_name)

quantity_available_uri = 'http://0.0.0.0:8000/quantity_available'