from sanic import Sanic
app= Sanic("__name__")

from order_book import ob
app.blueprint(ob)
app.run(host='0.0.0.0', port=8080, debug=True)