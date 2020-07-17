from sanic import Blueprint
from sanic.response import json, json_dumps
from aiopg.sa import create_engine
from config import connection
from models import orderbook, order_datails
import json as dict_json
import requests
from stock_management import StockManagement

# app=Sanic('__main__')
ob = Blueprint("order_book")

@ob.route('/order_book', methods=['GET', "POST"])
async def order_book(request):
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            last_row = await (await conn.execute(
                orderbook.select().order_by(orderbook.select().columns['id'].desc()))).fetchone()
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
                                orderbook.insert().values(id=order_id, customer_id=customer_id, status="confirmed"))
                            await conn.execute(
                                order_datails.insert().values(order_id=order_id, details=json_dumps(
                                    {"product": product_id, "price":price, "quantity": quantity_ordered})))
                            order_id+=1
                        else:
                            return json({"message": "error in communicating microservices"})
                return json(result)

            else:
                return json({"message": "I am get method"})




