import os


class Config(object):
    DEBUG = False
    CONFIG_PATH = os.path.dirname(os.path.abspath(__file__))
    USERS_PATH = os.path.join(CONFIG_PATH, 'users.ini')


class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = "development"
    ASSETS_DEBUG = True
    SECRET_KEY = 'IU43IUN34+34-34F34VDsdfkj456'


class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = "production"
    SECRET_KEY = 'fdglkjsnYG780+fsdsJ-ffffds123gcvd94+dds'

