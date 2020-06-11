from sanic import Sanic
app = Sanic(__name__)

database_name = 'ordermgt'
database_host = 'localhost'
database_user = 'postgres'
database_password = '1234'
connection = 'postgres://{0}:{1}@{2}/{3}'.format(database_user,
                                                 database_password,
                                                 database_host,
                                                 database_name)




from orders.orderbook.order_book import ob
app.blueprint(ob)
