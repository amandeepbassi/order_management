import sqlalchemy as sa
from config import Config

database_host = Config.DATABASE_HOST
database_name = Config.DATBASE_NAME
database_user = Config.DATABASE_USER
database_password = Config.DATABASE_PASSWORD


connection = 'postgres://{0}:{1}@{2}/{3}'.format(
    database_user, database_password, database_host, database_name)


order_book = sa.Table('tb_order_book', sa.MetaData(),
                    sa.Column('ob_id', sa.String, primary_key=True),
                    sa.Column('ob_timestamp', sa.TIMESTAMP, nullable=False),
                    sa.Column('ob_customer_id', sa.String, nullable=False),
                    sa.Column('ob_product_id', sa.String, nullable=False),
                    sa.Column('ob_vendor_id', sa.String, nullable=False),
                    sa.Column('ob_product_quantity', sa.Integer, nullable=False),
                    sa.Column('ob_product_price', sa.Float, nullable=False),
                    sa.Column('ob_status', sa.VARCHAR(50), nullable=False))


order_status = sa.Table('tb_order_status', sa.MetaData(),
                        sa.Column('os_id', sa.String, primary_key=True),
                        sa.Column('os_timestamp', sa.TIMESTAMP, nullable=False),
                        sa.Column('os_order_book_id', sa.String, nullable=False),
                        sa.Column('os_order_status', sa.VARCHAR(50), nullable=False))

                           

