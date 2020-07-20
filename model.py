import sqlalchemy as sa
from config import Config

database_host = Config.DATABASE_HOST
database_name = Config.DATBASE_NAME
database_user = Config.DATABASE_USER
database_password = Config.DATABASE_PASSWORD


connection = 'postgres://{0}:{1}@{2}/{3}'.format(
    database_user, database_password, database_host, database_name)

metadata = sa.MetaData()
tb_orderbook = sa.Table('tb_orderbook', metadata,
                        sa.Column('id', sa.Integer, primary_key=True),
                        sa.Column('customer_id', sa.Integer),
                        sa.Column('datetime', sa.TIMESTAMP)
                        )

tb_order_details = sa.Table('tb_order_details', metadata,
                            sa.Column('order_details_id', sa.Integer, primary_key=True),
                            sa.Column('order_id', None, sa.ForeignKey('orderbook.id')),
                            sa.Column('details', sa.Text)
                            )

tb_order_status = sa.Table('tb_order_status', metadata,
                           sa.Column('status_id', sa.Integer, primary_key=True),
                           sa.Column('order_id2', None, sa.ForeignKey('orderbook.id')),
                           sa.Column('date', sa.Date),
                           sa.Column('time', sa.Time),
                           sa.Column('status', sa.Text)
                           )

quantity_available_uri = 'http://0.0.0.0:8000/quantity_available'