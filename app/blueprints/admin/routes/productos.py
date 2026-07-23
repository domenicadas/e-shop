import os
import uuid
from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
from app import db
from app.models import Producto, Categoria
from .. import admin_bp
from ..decorators import admin_requerido

EXTENSIONES_PERMITIDAS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}


def _extension_valida(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSIONES_PERMITIDAS


def _guardar_imagen(archivo):
    if not archivo or archivo.filename == '':
        return None
    if not _extension_valida(archivo.filename):
        flash('Formato de imagen no permitido.', 'warning')
        return None

    nombre_final = f'{uuid.uuid4().hex}_{secure_filename(archivo.filename)}'
    carpeta = os.path.join(current_app.static_folder, 'img')
    os.makedirs(carpeta, exist_ok=True)
    archivo.save(os.path.join(carpeta, nombre_final))
    return nombre_final


@admin_bp.route('/productos')
@login_required
@admin_requerido
def productos():
    productos = Producto.query.order_by(Producto.nombre).all()
    return render_template('admin/productos.html', productos=productos)


@admin_bp.route('/productos/crear', methods=['GET', 'POST'])
@login_required
@admin_requerido
def crear_producto():
    categorias = Categoria.query.filter_by(activa=True).all()

    if request.method == 'POST':
        nombre       = request.form.get('nombre', '').strip()
        descripcion  = request.form.get('descripcion', '').strip()
        precio       = request.form.get('precio', type=float)
        stock        = request.form.get('stock', type=int)
        categoria_id = request.form.get('categoria_id', type=int)

        if not nombre or precio is None or stock is None or not categoria_id:
            flash('Completa todos los campos obligatorios.', 'danger')
            return redirect(url_for('admin.crear_producto'))

        producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            categoria_id=categoria_id,
            imagen=_guardar_imagen(request.files.get('imagen'))
        )
        db.session.add(producto)
        db.session.commit()
        flash(f'Producto "{nombre}" creado correctamente.', 'success')
        return redirect(url_for('admin.productos'))

    return render_template('admin/producto_form.html', producto=None, categorias=categorias)


@admin_bp.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_requerido
def editar_producto(id):
    producto   = Producto.query.get_or_404(id)
    categorias = Categoria.query.filter_by(activa=True).all()

    if request.method == 'POST':
        nombre       = request.form.get('nombre', '').strip()
        precio       = request.form.get('precio', type=float)
        stock        = request.form.get('stock', type=int)
        categoria_id = request.form.get('categoria_id', type=int)

        if not nombre or precio is None or stock is None or not categoria_id:
            flash('Completa todos los campos obligatorios.', 'danger')
            return redirect(url_for('admin.editar_producto', id=id))

        producto.nombre       = nombre
        producto.descripcion  = request.form.get('descripcion', '').strip()
        producto.precio       = precio
        producto.stock        = stock
        producto.categoria_id = categoria_id

        nueva_imagen = _guardar_imagen(request.files.get('imagen'))
        if nueva_imagen:
            producto.imagen = nueva_imagen

        db.session.commit()
        flash(f'Producto "{producto.nombre}" actualizado.', 'success')
        return redirect(url_for('admin.productos'))

    return render_template('admin/producto_form.html', producto=producto, categorias=categorias)


@admin_bp.route('/productos/toggle/<int:id>', methods=['POST'])
@login_required
@admin_requerido
def toggle_producto(id):
    producto = Producto.query.get_or_404(id)
    producto.activo = not producto.activo
    db.session.commit()
    estado = 'activado' if producto.activo else 'eliminado'
    flash(f'Producto "{producto.nombre}" {estado}.', 'info')
    return redirect(url_for('admin.productos'))
