from sanic import Blueprint
from sanic.response import json
from aiopg.sa import create_engine
from orders import connection
from orders.config.models import orderbook, order_datails
import json as dict_json
import requests

# app=Sanic('__main__')
ob = Blueprint("order_book")

@ob.route('/order_book', methods=['GET', "POST"])
async def order_book(request):
    # payload = {}
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            last_row = await (await conn.execute(
                orderbook.select().order_by(orderbook.select().columns['id'].desc()))).fetchone()
            last_id = last_row.id

            if request.method == "POST":
                data = request.json
                order_id = last_id+1
                customer_id = data['customer_id']
                status = 'pending'
                details = data['details']
                print(details)
                print(details.values())
                result = {}
                for order, value in details.items():
                    order_no = order
                    product_id = value['product']
                    price = value['price']
                    quantity = value['quantity']
                    payload = {"product_id": product_id}
                    r = requests.get('http://0.0.0.0:8000/quantity_available', data=dict_json.dumps(payload))
                    if r.json()['quantity'] > quantity:
                        stock_left = r.json()['quantity'] - quantity
                        payload1 = {"stock_left": stock_left, "product_id": product_id, "quantity": quantity}
                        rpost = requests.post('http://0.0.0.0:8000/update_inventory', data=dict_json.dumps(payload1))
                        print(rpost.ok)
                        if rpost.ok:
                            # print(dict_json.dumps(details))
                            result.update({order_no: {"product": product_id, "quantity": quantity, "status": 'confirmed'}})
                        else:
                            return json({"message": "error in communicating microservices"})
                    else:
                        return json({"message": f'{product_id} quantity is not enough' })
                await conn.execute(orderbook.insert().values(id=order_id, customer_id=customer_id, status=status))
                await conn.execute(order_datails.insert().values(order_id=order_id, details=dict_json.dumps(details)))
                return json(result)

            else:
                return json({"message": "I am get method"})


# app.run(host='0.0.0.0', port=8080)