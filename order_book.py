from sanic import Blueprint
from sanic.response import json
from aiopg.sa import create_engine
from config import Config
from model import order_book, connection
from sanic.exceptions import NotFound, ServerError
from sqlalchemy import select, func
import json as regularjson

import requests



bp_order_book = Blueprint("order_book_blueprint")

@bp_order_book.route('/orderbook', methods=['POST'])
async def order_book_value(request):
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            if request.method == 'POST':
                results = {}
                url_prefix = []
                order_data = request.json['order']
                for order in order_data:
                    insert_query = order_book.insert(inline=True,returning=[order_book.c.ob_id]).values(order)
                    try:
                        result_id = await(await conn.execute(insert_query)).fetchone()
                        url_prefix.append(str(Config.HOST_URL) + ":" + str(Config.HOST_PORT) + "/orderbook/" + str(result_id[0]))
                        payload = {
                            "net_stock_product_id": order['ob_product_id'],
                            "net_stock_vendor_id": order['ob_vendor_id'],
                            "transaction_type": "SUB",
                            "product_update": order['ob_product_quantity']
                        }
                        r = requests.post(Config.NET_STOCK_URL, data = regularjson.dumps(payload))
                        print(r.headers)
                    except Exception as e_x:
                        print(e_x)
                        results = {"Inserted Values": "Values have been not successfully inserted",
                                    "Error": str(e_x)}
                    else:
                        results = {"Inserted Values": "Values have been successfully inserted"}
               
                return json(results, headers={'URL': url_prefix}, status=201)
         

@bp_order_book.route('/orderbook/<ob_id:string>', methods=['PUT', 'PATCH', 'GET'])
async def update_order_book(request, ob_id):
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            results = {}
            if request.method == 'PUT' or request.method == 'PATCH':
                update_query = order_book.update().values(request.json).where(order_book.c.ob_id == ob_id)       
                result_value = await(await conn.execute(select([func.count(order_book.c.ob_id)]).where(order_book.c.ob_id == ob_id))).fetchone()
                if str(result_value[0]) == "1":
                    update_query = order_book.update().where(order_book.c.ob_id == ob_id).values(request.json)
                    try:
                        await conn.execute(update_query)
                    except Exception as e_x:
                        print(e_x)
                        results = {"Updated Values": "Values have not been successfully updated",
                        "exception": str(e_x)}
                    else:
                        results = {"Updated Values": "values have been successfully updated"}
                else:
                    results = {"Updated Values": "Values not found"}
                return json(results, status=200)
            elif request.method == 'GET':
                select_query = order_book.select().where(order_book.c.ob_id == ob_id)
                async for row in conn.execute(select_query):
                    results.update(row)
                    results.__setitem__('ob_id', str(results['ob_id']))
                    results.__setitem__('ob_timestamp', str(results['ob_timestamp']))
                    results.__setitem__('ob_customer_id', str(results['ob_customer_id']))
                    results.__setitem__('ob_product_id', str(results['ob_product_id']))
                    results.__setitem__('ob_vendor_id', str(results['ob_vendor_id']))
                return json(results, status=200)


@bp_order_book.exception(NotFound)
async def ignore_404(request, exception):
    return json({"Not Found": "Page Not Found"}, status=404)


@bp_order_book.exception(ServerError)
async def ignore_503(request, exception):
    return json({"Server Error": "503 internal server error"}, status=503)


