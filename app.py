# from sanic import Sanic
# app= Sanic("__name__")

from orders import app
app.run(host='0.0.0.0', port=8080, debug=True)