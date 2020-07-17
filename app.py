from sanic import Sanic
app= Sanic("__name__")

from order_book import ob
from order_history import oh
app.blueprint(ob)
app.blueprint(oh)
app.run(host='0.0.0.0', port=8080, debug=True)