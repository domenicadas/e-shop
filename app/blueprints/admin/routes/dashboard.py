from flask import render_template
from flask_login import login_required
from app import db
from app.models import Pedido, Producto
from .. import admin_bp
from ..decorators import admin_requerido

LOW_STOCK_THRESHOLD = 5


@admin_bp.route('/admin')
def admin():
    return render_template('admin/home.html')


@admin_bp.route('/dashboard')
@login_required
@admin_requerido
def dashboard():
    ventas_total = db.session.query(
        db.func.coalesce(db.func.sum(Pedido.total), 0)
    ).filter(Pedido.estado != 'cancelado').scalar()

    total_pedidos      = Pedido.query.count()
    pedidos_pendientes = Pedido.query.filter_by(estado='pendiente').count()

    productos_bajo_stock = Producto.query.filter(
        Producto.activo == True,
        Producto.stock <= LOW_STOCK_THRESHOLD
    ).order_by(Producto.stock.asc()).all()

    return render_template('admin/index.html',
                           ventas_total=ventas_total,
                           total_pedidos=total_pedidos,
                           pedidos_pendientes=pedidos_pendientes,
                           productos_bajo_stock=productos_bajo_stock,
                           low_stock_threshold=LOW_STOCK_THRESHOLD)
