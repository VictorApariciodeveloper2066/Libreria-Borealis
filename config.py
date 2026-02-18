import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'borealis-secret-key-2024'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///rifas.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """Production configuration for PythonAnywhere"""
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
