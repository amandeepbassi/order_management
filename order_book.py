from sanic import Blueprint
from sanic.response import json
from aiopg.sa import create_engine
from config import Config
from model import tb_order_book, connection
from sanic.exceptions import NotFound, ServerError
from sqlalchemy import select, func, desc
import json as regularjson
from sanic_jwt.decorators import protected
import requests
import sys
import asyncio
import requests
import os
if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

bp_order_book = Blueprint("order_book_blueprint")

@bp_order_book.route('/orderbook', methods=['POST'])
@protected(initialized_on=bp_order_book)
async def order_book_value(request):
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            results = {}
            if request.method == 'POST':
                url_prefix = []
                order_data = request.json['order']
                for order in order_data:
                    insert_query = tb_order_book.insert(inline=True,returning=[tb_order_book.c.ob_id]).values(order)
                    try:
                        result_id = await(await conn.execute(insert_query)).fetchone()
                        url_prefix.append(str(Config.HOST_URL) + ":" + str(Config.HOST_PORT) + "/orderbook/" + str(result_id[0]))
                        payload = {
                            "net_stock_product_id": order['ob_product_id'],
                            "net_stock_vendor_id": order['ob_vendor_id'],
                            "transaction_type": "SUB",
                            "product_update": order['ob_product_quantity']
                        }
                        # Stock minus code
                        #r = requests.post(Config.NET_STOCK_URL, data = regularjson.dumps(payload))
                        #print(r.headers)
                    except Exception as e_x:
                        print(e_x)
                        results = {"Inserted Values": "Values have been not successfully inserted",
                                    "Error": str(e_x)}
                        return json(results, headers={'URL': url_prefix}, status=500)
                    else:
                        results = {"Inserted Values": "Values have been successfully inserted"}
                return json(results, headers={'URL': url_prefix}, status=201)
                

@bp_order_book.route('/customerorder/<ob_customer_id:string>', methods=['GET'])
@protected(initialized_on=bp_order_book)
async def get_order_customer_id(request, ob_customer_id):
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            results = {}
            if request.method == 'GET':
                select_query = tb_order_book.select().where(tb_order_book.c.ob_customer_id == ob_customer_id).order_by(desc(tb_order_book.c.ob_timestamp))
                async for row in conn.execute(select_query):
                    product_service_url = "http://" + Config.HOST_URL + ":" + \
                        str(Config.PRODUCT_SERVICE_PORT) + \
                        Config.PRODUCT_SERVICE_ENPOINT+str(row.ob_product_id)                   
                    headers = {'username': Config.SERVICE_PASSWORD,
                               'password': Config.SERVICE_USERNAME}            
                    response_val = requests.get(url=product_service_url, headers=headers)
                    if response_val.status_code ==200:
                        result = {}
                        result = {"ob_id": str(row.ob_id), 
                                "ob_timestamp": str(row.ob_timestamp),
                                "ob_customer_id": str(row.ob_customer_id),
                                "ob_product_id": str(row.ob_product_id),
                                "ob_vendor_id": str(row.ob_vendor_id),
                                "ob_product_quantity": row.ob_product_quantity,
                                "ob_product_price": row.ob_product_price,
                                "ob_status": row.ob_status,
                                "ob_choice_id": str(row.ob_choice_id),
                                "ob_start_date": str(row.ob_start_date),
                                "ob_end_date": str(row.ob_end_date),
                                "ob_choice_days":str(row.ob_choice_days),
                                "ob_customers_name": row.ob_customers_name,
                                "ob_customers_address": row.ob_customers_address,
                                "ob_customers_phone_number":row.ob_customers_phone_number,
                                "ob_customers_email_id":row.ob_customers_email_id,
                                "product_attributes": str(regularjson.loads(response_val.text)['product_attributes']),
                                "product_image":str(regularjson.loads(response_val.text)['product_image'])}
                        results[str(row.ob_id)] = result
                    else:
                        return json(results, status=500)
                return json(results, status=200)


@bp_order_book.route('/orderbook/<ob_id:string>', methods=['PUT', 'PATCH', 'GET'])
@protected(initialized_on=bp_order_book)
async def update_order_book(request, ob_id):
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            results = {}
            if request.method == 'PUT' or request.method == 'PATCH':
                update_query = tb_order_book.update().values(request.json).where(tb_order_book.c.ob_id == ob_id)       
                result_value = await(await conn.execute(select([func.count(tb_order_book.c.ob_id)]).where(tb_order_book.c.ob_id == ob_id))).fetchone()
                if str(result_value[0]) == "1":
                    update_query = tb_order_book.update().where(tb_order_book.c.ob_id == ob_id).values(request.json)
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
                select_query = tb_order_book.select().where(tb_order_book.c.ob_id == ob_id)
                async for row in conn.execute(select_query):
                    results.update(row)
                    results.__setitem__('ob_id', str(results['ob_id']))
                    results.__setitem__('ob_timestamp', str(results['ob_timestamp']))
                    results.__setitem__('ob_customer_id', str(results['ob_customer_id']))
                    results.__setitem__('ob_product_id', str(results['ob_product_id']))
                    results.__setitem__('ob_vendor_id', str(results['ob_vendor_id']))
                return json(results, status=200)


@bp_order_book.exception(NotFound)
@protected(initialized_on=bp_order_book)
async def ignore_404(request, exception):
    return json({"Not Found": "Page Not Found"}, status=404)


@bp_order_book.exception(ServerError)
@protected(initialized_on=bp_order_book)
async def ignore_503(request, exception):
    return json({"Server Error": "503 internal server error"}, status=503)


