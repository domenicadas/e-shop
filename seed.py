from app import create_app, db
from app.models.categoria import Categoria
from app.models.producto import Producto
from app.models.usuario import Usuario
from app.models.pedido import Pedido, DetallePedido

app = create_app()

with app.app_context():
    # 1. Limpiar la base de datos previa para evitar errores de duplicados
    # (los pedidos dependen de productos y usuarios, deben borrarse primero)
    db.session.query(DetallePedido).delete()
    db.session.query(Pedido).delete()
    db.session.query(Producto).delete()
    db.session.query(Categoria).delete()
    db.session.query(Usuario).delete()
    db.session.commit()

    # 2. Crear Categorías
    cat1 = Categoria(nombre='Velas', descripcion='Velas aromáticas')
    cat2 = Categoria(nombre='Complementos', descripcion='Todo lo necesario para tus velas')
    db.session.add_all([cat1, cat2])
    db.session.commit()

    # 3. Crear Productos
    p1 = Producto(nombre='Vela de Vainilla', precio=14, stock=20, categoria_id=cat1.id, imagen='vainilla.png')
    p2 = Producto(nombre='Vela de Chocolate', precio=14, stock=50, categoria_id=cat1.id, imagen='chocolate.png')
    p3 = Producto(nombre='Vela de Frutos Rojos', precio=14, stock=20, categoria_id=cat1.id, imagen='Frutosrojos.png')
    p4 = Producto(nombre='Vela de Lavanda', precio=14, stock=50, categoria_id=cat1.id, imagen='lavanda_vela.png')
    p5 = Producto(nombre='Vela de Canela', precio=14, stock=50, categoria_id=cat1.id, imagen='canela.png')
    p6 = Producto(nombre='Kit de Cuidado de Velas', precio=25, stock=50, categoria_id=cat2.id, imagen='Kit.png')
    db.session.add_all([p1, p2, p3, p4, p5, p6])

    # 4. Crear Usuarios
    admin = Usuario(nombre='Administrador', email='admin@tienda.com', rol='admin')
    admin.set_password('admin123')

    cliente = Usuario(nombre='Juan Pérez', email='juan@email.com', rol='cliente')
    cliente.set_password('cliente123')

    db.session.add_all([admin, cliente])
    db.session.commit()

    print("Datos de prueba insertados correctamente")