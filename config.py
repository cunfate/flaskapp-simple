import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY_FLASK')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.qq.com'
    MAIl_PORT = 25
    MAIL_UES_TLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'null'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'null'
    FLASKY_MAIL_SUBJECT_PREFIX = '[FLASKY]'
    FLASKY_MAIL_SENDER = '%s <%s>' % (MAIL_USERNAME, MAIL_USERNAME)
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    mysql_username = os.getenv('MYSQL_USERNAME')
    mysql_pwd = os.getenv('MYSQL_PWD_FLASK')
    develop_database = os.getenv('MYSQL_DEVELOP_DATABASE')
    SQLALCHEMY_DATABASE_URI = \
        'mysql+pymysql://%s:%s@127.0.0.1/%s?charset=utf8'\
        % (mysql_username, mysql_pwd, develop_database)


class TestingConfig(Config):
    TESTING = True
    mysql_username = os.getenv('MYSQL_USERNAME')
    mysql_pwd = os.getenv('MYSQL_PWD_FLASK')
    test_database = os.getenv('MYSQL_TEST_DATABASE')
    SQLALCHEMY_DATABASE_URI = \
        'mysql+pymysql://%s:%s@127.0.0.1/%s?charset=utf8'\
        % (mysql_username, mysql_pwd, test_database)


class ProductionConfig(Config):
    mysql_username = os.getenv('MYSQL_USERNAME')
    mysql_pwd = os.getenv('MYSQL_PWD_FLASK')
    product_database = os.getenv('MYSQL_PRODUCT_DATABASE')
    SQLALCHEMY_DATABASE_URI = \
        'mysql+pymysql://%s:%s@127.0.0.1/%s?charset=utf8'\
        % (mysql_username, mysql_pwd, product_database)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
