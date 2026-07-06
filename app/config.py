import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '7980e6df8d5d61eb167532ad39d28ee8')
    
    # Cambia los valores por defecto para que coincidan con tu XAMPP local:
    DB_USER = os.getenv('DB_USER', 'root')          # <-- Cambiado a 'root'
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')      # <-- Dejado vacío ''
    DB_HOST = os.getenv('DB_HOST', '127.0.0.1')  
    DB_NAME = os.getenv('DB_NAME', 'ecommerce_db') # <-- Pon aquí el nombre real de tu BDD

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False