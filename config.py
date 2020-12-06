class Config(object):
    HOST_URL = "192.168.1.6"
    HOST_PORT = 9029
    ACCESS_LOG = False
    DATABASE_HOST = 'localhost'
    DATBASE_NAME = 'db_order_management'
    DATABASE_USER = 'test'
    DATABASE_PASSWORD = 'test'
    NET_STOCK_URL = 'http://0.0.0.0:8001/updatenetstock'
    TESTING = False
    PRODUCT_SERVICE_PORT = 9007
    PRODUCT_SERVICE_ENPOINT = "/productdetails/"
    SERVICE_PASSWORD ='test'
    SERVICE_USERNAME ='test'


class ProductionConfig(Config):
    TESTING = True


class DevelopmentConfig(Config):
    TESTING = True


class TestingConfig(Config):
    TESTING = True







