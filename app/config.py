import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '7980e6df8d5d61eb167532ad39d28ee8')

    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
    DB_NAME = os.getenv('DB_NAME', 'ecommerce_db')

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_por_entorno = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}


def obtener_config():
    entorno = os.getenv('FLASK_ENV', 'production')
    return config_por_entorno.get(entorno, ProductionConfig)
