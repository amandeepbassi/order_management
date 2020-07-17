import sqlalchemy as sa

metadata = sa.MetaData()
orderbook = sa.Table('orderbook', metadata,
               sa.Column('id', sa.Integer, primary_key=True),
               sa.Column('customer_id', sa.Integer),
               sa.Column('datetime', sa.TIMESTAMP)
                         )

order_datails = sa.Table('order_details', metadata,
               sa.Column('order_details_id', sa.Integer, primary_key=True),
               sa.Column('order_id', None, sa.ForeignKey('orderbook.id')),
               sa.Column('details', sa.Text)
                         )

status = sa.Table('status', metadata,
               sa.Column('status_id', sa.Integer, primary_key=True),
               sa.Column('order_id2', None, sa.ForeignKey('orderbook.id')),
               sa.Column('date', sa.Date),
               sa.Column('time', sa.Time),
               sa.Column('status', sa.Text)
                         )
