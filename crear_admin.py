from app import create_app, db
from app.models import Usuario

EMAIL    = 'admin12@gmail.com'
PASSWORD = '122345'

app = create_app()

with app.app_context():
    usuario = Usuario.query.filter_by(email=EMAIL).first()

    if usuario:
        usuario.rol = 'admin'
        usuario.set_password(PASSWORD)
        db.session.commit()
        print(f'Usuario existente actualizado a admin: {usuario.email}')
    else:
        usuario = Usuario(nombre='Administrador', email=EMAIL, rol='admin')
        usuario.set_password(PASSWORD)
        db.session.add(usuario)
        db.session.commit()
        print(f'Usuario admin creado: {usuario.email}')