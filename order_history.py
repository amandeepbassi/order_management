from sanic import Blueprint
from sanic.response import json, json_dumps
from aiopg.sa import create_engine
import sqlalchemy as sa
from model import tb_orderbook, tb_order_details, tb_order_status, connection
from sanic.exceptions import NotFound, ServerError
import json as dict_json
import requests


bp_order_history = Blueprint("order_history")


@bp_order_history.route('/all-orders', methods=['GET', 'POST'])
async def allorders(request):
    if request.method == 'GET':
        result = []
        data = request.json
        if 'customer_id' in data.keys():
            customer_id = data['customer_id']
            check_id = []
            async with create_engine(connection) as engine:
                async with engine.acquire() as conn:
                    c1 = await conn.scalar(tb_orderbook.count().where(tb_orderbook.c.customer_id == customer_id))
                    if c1 == 0:
                        return json({"Message": "No Data Found"})
                    else:
                        join = sa.join(tb_orderbook, tb_order_details,
                                       tb_order_details.c.order_id == tb_orderbook.c.id)
                        query = (sa.select([tb_orderbook, tb_order_details])
                                 .select_from(join).where(tb_orderbook.c.customer_id == customer_id))
                        async for row in conn.execute(query):
                            order_id = row.id
                            orderDetails = row.details
                            customer_id = row.customer_id
                            date_time = str(row.datetime)
                            result.append({order_id: {"customer_id": customer_id, "datetime": date_time,
                                                      "order_details": orderDetails}})

                        return json(result)
        else:
            async with create_engine(connection) as engine:
                async with engine.acquire() as conn:
                    join = sa.join(tb_orderbook, tb_order_details,
                                   tb_order_details.c.order_id == tb_orderbook.c.id)
                    query = (sa.select([tb_orderbook, tb_order_details])
                             .select_from(join))
                    async for row in conn.execute(query):
                        order_id = row.id
                        orderDetails = row.details
                        customer_id = row.customer_id
                        date_time = str(row.datetime)
                        result.append({order_id: {"customer_id": customer_id, "datetime": date_time,
                                                  "order_details": orderDetails}})

                    return json(result)

@bp_order_history.route('/order-status/<order_id:int>', methods=['GET', 'POST'])
async def status_details(request, order_id):
    result= []
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            if request.method == 'GET':
                async for row in conn.execute(tb_order_status.select().where(tb_order_status.c.order_id2 == order_id).order_by(tb_order_status.c.status_id.desc())):
                    date = str(row.date)
                    time = str(row.time)
                    status_details = row.tb_order_status
                    result.append({"date": date, "time" : time, "status": status_details})




                return json({order_id: result})
@bp_order_history.exception(NotFound)
async def ignore_404(request, exception):
    return json({"Not Found": "Page Not Found"}, status=404)


@bp_order_history.exception(ServerError)
async def ignore_503(request, exception):
    return json({"Server Error": "503 internal server error"}, status=503)