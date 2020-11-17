from sanic import Blueprint
from sanic.response import json
from aiopg.sa import create_engine
import sqlalchemy as sa
from model import order_status, connection
from sanic.exceptions import NotFound, ServerError
import json as dict_json
import requests


bp_order_history = Blueprint("order_history_blueprint")


@bp_order_history.route('/orderhistory/<os_order_book_id:string>', methods=['GET'])
async def order_history(request, os_order_book_id):
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            if request.method == 'GET':
                results = {}
                select_query = order_status.select().where(order_status.c.os_order_book_id == os_order_book_id)          
                async for row in conn.execute(select_query):
                    result = []
                    result.append({"os_timestamp": str(row.os_timestamp), "os_order_status": str(row.os_order_status)})
                    results.__setitem__(row['os_id'], result)
        return json(results, status=200)


@bp_order_history.exception(NotFound)
async def ignore_404(request, exception):
    return json({"Not Found": "Page Not Found"}, status=404)


@bp_order_history.exception(ServerError)
async def ignore_503(request, exception):
    return json({"Server Error": "503 internal server error"}, status=503)