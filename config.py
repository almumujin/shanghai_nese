class Config(object):
    SECRET_KEY = '736670cb10a600b695a55839ca3a5aa54a7d7356cdef815d2ad6e19a2031182b'



class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HOSTNAME = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'nese'
    USERNAME = 'root'
    PASSWORD = 'jin26215'
    DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
    SQLALCHEMY_DATABASE_URI = DB_URI
