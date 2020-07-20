from sanic import Blueprint
from sanic.response import json, json_dumps
from aiopg.sa import create_engine
from config import Config
from model import tb_orderbook, tb_order_details, connection
from sanic.exceptions import NotFound, ServerError
import json as dict_json
import requests
from stock_management import StockManagement

# app=Sanic('__main__')
bp_order_book = Blueprint("order_book")

@bp_order_book.route('/order-book', methods=['GET', "POST"])
async def order_book(request):
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            last_row = await (await conn.execute(
                tb_orderbook.select().order_by(tb_orderbook.select().columns['id'].desc()))).fetchone()
            last_id = last_row.id

            if request.method == "POST":
                result = {}
                data = request.json
                order_id = last_id+1
                customer_id = data['customer_id']
                status = 'pending'
                details = data['details']
                # print(details)
                # print(details.values())
                products_available = []
                products_unavailable = []
                for order, value in details.items():
                    order_no = order
                    product_id = value['product']
                    price = value['price']
                    quantity_ordered = value['quantity']
                    productavailable = StockManagement(product_id)
                    quantity_available = int(productavailable.availablility())
                    if quantity_available > quantity_ordered:
                        products_available.append({product_id : "available"})
                    else:
                        products_unavailable.append({product_id: "unavailable"})
                if len(products_unavailable) > 0:
                    return json({"message": "Some products from you cart are not available","Products_available": products_available, "Products_unavailable": products_unavailable})
                else:
                    for order, value in details.items():
                        order_no = order
                        product_id = value['product']
                        price = value['price']
                        quantity_ordered = value['quantity']
                        productavailable = StockManagement(product_id)
                        quantity_available = int(productavailable.availablility())
                        stock_left = quantity_available - quantity_ordered
                        payload = {"stock_left": stock_left, "product_id": product_id, "quantity": quantity_ordered}
                        rpost = requests.post('http://0.0.0.0:8000/update_inventory', data=json_dumps(payload))
                        print(rpost.ok)
                        if rpost.ok:
                        # print(dict_json.dumps(details))
                            result.update({order_no: {"product": product_id, "quantity": quantity_ordered, "status": 'confirmed'}})
                            await conn.execute(
                                tb_orderbook.insert().values(id=order_id, customer_id=customer_id, status="confirmed"))
                            await conn.execute(
                                tb_order_details.insert().values(order_id=order_id, details=json_dumps(
                                    {"product": product_id, "price":price, "quantity": quantity_ordered})))
                            order_id+=1
                        else:
                            return json({"message": "error in communicating microservices"})
                return json(result)

            else:
                return json({"message": "I am get method"})

@bp_order_book.exception(NotFound)
async def ignore_404(request, exception):
    return json({"Not Found": "Page Not Found"}, status=404)


@bp_order_book.exception(ServerError)
async def ignore_503(request, exception):
    return json({"Server Error": "503 internal server error"}, status=503)


