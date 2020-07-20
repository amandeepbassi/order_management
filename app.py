from sanic import Sanic
app= Sanic("__name__")

from order_book import bp_order_book
from order_history import bp_order_history
app.blueprint(bp_order_book)
app.blueprint(bp_order_history)
app.config.from_object('config.Config')

if __name__ == '__main__':
    app.run(host=app.config.HOST_URL, port=app.config.HOST_PORT, debug=False)