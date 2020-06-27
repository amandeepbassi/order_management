import sqlalchemy as sa
from sanic import Sanic
metadata = sa.MetaData()
orderbook = sa.Table('orderbook', metadata,
               sa.Column('id', sa.Integer, primary_key=True),
               sa.Column('customer_id', sa.Integer),
               sa.Column('datetime', sa.TIMESTAMP),
               sa.Column('status', sa.Text)
                         )

order_datails = sa.Table('order_details', metadata,
               sa.Column('id', sa.Integer, primary_key=True),
               sa.Column('order_id', None, sa.ForeignKey('orderbook.id')),
               sa.Column('details', sa.Text)
                         )

app= Sanic("__main__")