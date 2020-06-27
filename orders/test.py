dict1 = {"order1": {'product': 20, 'quantity': 30, 'price':99},
        "order2": {'product': 20, 'quantity': 30, 'price':99}}

# print(dict1.items())
print(dict1.values())
for order, value in dict1.items():
    print(order)
    print(value['product'])
    print(value['quantity'])
    print(value['price'])
