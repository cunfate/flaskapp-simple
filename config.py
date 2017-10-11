import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY_FLASK')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIl_PORT = 587
    MAIL_UES_TLS = True
    MAIL_USER_NAME = os.environ.get('MAIL_USERNAME') or 'null'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'null'
    FLASKY_MAIL_SUBJECT_PREFIX = '[FLASKY]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    mysql_username = os.getenv('MYSQL_USERNAME')
    mysql_pwd = os.getenv('MYSQL_PWD_FLASK')
    SQLALCHEMY_DATABASE_URI = \
        'mysql+pymysql://%s:%s@127.0.0.1/flaskapp?charset=utf8'\
        % (mysql_username, mysql_pwd)


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
