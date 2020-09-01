class Config(object):
    HOST_URL = "0.0.0.0"
    HOST_PORT = 8028
    ACCESS_LOG = False
    DATABASE_HOST = 'localhost'
    DATBASE_NAME = 'db_order_management'
    DATABASE_USER = 'test'
    DATABASE_PASSWORD = 'test'
    NET_STOCK_URL = 'http://0.0.0.0:8001/updatenetstock'
    TESTING = False


class ProductionConfig(Config):
    TESTING = True


class DevelopmentConfig(Config):
    TESTING = True


class TestingConfig(Config):
    TESTING = True







