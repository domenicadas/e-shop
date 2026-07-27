from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.config import obtener_config

db = SQLAlchemy()
migrate = Migrate()
login_manager=LoginManager()

# Imágenes fijas por nombre de producto: viven en el repo (persisten en Railway),
# a diferencia de las que se suben desde el panel de admin en producción.
IMAGENES_FIJAS = {
    'Vela de Vainilla': 'vainilla.png',
    'Vela de Chocolate': 'chocolate.png',
    'Vela de Frutos Rojos': 'Frutosrojos.png',
    'Vela de Lavanda': 'lavanda_vela.png',
    'Vela de Canela': 'canela.png',
    'Kit de Cuidado de Velas': 'Kit.png',
}

def create_app():
    app = Flask(__name__)
    app.config.from_object(obtener_config())

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @app.context_processor
    def utilidades_imagenes():
        def imagen_producto(producto):
            return IMAGENES_FIJAS.get(producto.nombre, producto.imagen)
        return dict(imagen_producto=imagen_producto)

    #Configuración de login manager
    login_manager.login_view='auth.login'
    login_manager.login_message= 'Inicia sesión para continuar'
    login_manager.login_message_category='warning'

    #Modelos
    from app.models import Usuario
    from app.models import Categoria
    from app.models import Pedido, DetallePedido
    from app.models import Producto

    #User loader: Flask-login necesita saber como cargar un usuario (es para seleccionar especificamente creo)
    @login_manager.user_loader
    def load_user (user_id):
        return Usuario.query.get(int(user_id))

    # Blueprints
    from app.blueprints.public import public_bp
    from app.blueprints.auth import auth_bp
    from app.blueprints.admin import admin_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app