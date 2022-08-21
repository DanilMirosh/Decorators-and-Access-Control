import base64


class Config(object):
    DEBUG = True
    SECRET_HERE = '249y823r9v8238r9u'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./movies.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PWD_HASH_SALT = base64.b16decode('salt')
    PWD_HASH_ITERATIONS = 100000
    TOKEN_EXPIRE_MINUTES = 15
    TOKEN_EXPIRE_DAY = 130
