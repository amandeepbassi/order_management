from sanic import Blueprint
from sanic.response import json, json_dumps
from aiopg.sa import create_engine
from config import connection
import sqlalchemy as sa
from models import orderbook, order_datails, status
import json as dict_json
import requests


oh = Blueprint("order_history")


@oh.route('/all_orders', methods=['GET', 'POST'])
async def allorders(request):
    if request.method == 'GET':
        result = []
        data = request.json
        if 'customer_id' in data.keys():
            customer_id = data['customer_id']
            check_id = []
            async with create_engine(connection) as engine:
                async with engine.acquire() as conn:
                    c1 = await conn.scalar(orderbook.count().where(orderbook.c.customer_id == customer_id))
                    if c1 == 0:
                        return json({"Message": "No Data Found"})
                    else:
                        join = sa.join(orderbook, order_datails,
                                       order_datails.c.order_id == orderbook.c.id)
                        query = (sa.select([orderbook, order_datails])
                                .select_from(join).where(orderbook.c.customer_id == customer_id))
                        async for row in conn.execute(query):
                            order_id = row.id
                            orderDetails = row.details
                            customer_id = row.customer_id
                            date_time = str(row.datetime)
                            result.append({order_id: {"customer_id": customer_id, "datetime": date_time,
                                                      "order_details": orderDetails}})

                        return json(result)

@oh.route('/status-details/<order_id:int>', methods=['GET', 'POST'])
async def status_details(request, order_id):
    result= []
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            if request.method == 'GET':
                async for row in conn.execute(status.select().where(status.c.order_id2 == order_id).order_by(status.c.status_id.desc())):
                    date = str(row.date)
                    time = str(row.time)
                    status_details = row.status
                    result.append({"date": date, "time" : time, "status": status_details})




                return json({order_id: result})
