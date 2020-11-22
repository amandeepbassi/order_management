from sanic import Sanic
from order_book import bp_order_book
from order_history import bp_order_history
from sanic_jwt import Initialize

app= Sanic('order_management_mircoservices')
Initialize(bp_order_book, app=app, auth_mode=False)
Initialize(bp_order_history, app=app, auth_mode=False)
app.blueprint(bp_order_book)
app.blueprint(bp_order_history)
app.config.from_object('config.Config')

if __name__ == '__main__':
    app.run(host=app.config.HOST_URL, port=app.config.HOST_PORT, debug=False)