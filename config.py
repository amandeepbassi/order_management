class Config(object):
    HOST_URL = "0.0.0.0"
    HOST_PORT = 8028
    ACCESS_LOG = False
    DATABASE_HOST = 'localhost'
    DATBASE_NAME = 'db_ordermanagement'
    DATABASE_USER = 'postgres'
    DATABASE_PASSWORD = '1234'
    TESTING = False

class ProductionConfig(Config):
    TESTING = True

class DevelopmentConfig(Config):
    TESTING = True

class TestingConfig(Config):
    TESTING = True







