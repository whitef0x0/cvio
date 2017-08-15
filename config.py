import os

from setup import basedir

class BaseConfig(object):
    SECRET_KEY = "SO_SECURE"
    DEBUG = True
    if os.environ.get('DOCKER_MACHINE') and os.environ['DOCKER_MACHINE'] == 'true':
        SQLALCHEMY_DATABASE_URI = "postgres://postgres:postgres@db/cvIO_dev"
    else:
        SQLALCHEMY_DATABASE_URI = "postgresql://0.0.0.0/cvIO_dev"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(object):
    """Development configuration."""
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    if os.environ.get('DOCKER_MACHINE') and os.environ['DOCKER_MACHINE'] == 'true':
        SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@db/cvIO_test"
    else:
        SQLALCHEMY_DATABASE_URI = "postgresql://0.0.0.0/cvIO_test"
    DEBUG_TB_ENABLED = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
