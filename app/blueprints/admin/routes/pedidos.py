from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import Pedido
from .. import admin_bp
from ..decorators import admin_requerido

ESTADOS = ['pendiente', 'pagado', 'enviado', 'entregado', 'cancelado']


@admin_bp.route('/pedidos')
@login_required
@admin_requerido
def pedidos():
    pedidos = Pedido.query.order_by(Pedido.fecha.desc()).all()
    return render_template('admin/pedidos.html', pedidos=pedidos, estados=ESTADOS)


@admin_bp.route('/pedidos/estado/<int:id>', methods=['POST'])
@login_required
@admin_requerido
def cambiar_estado_pedido(id):
    pedido       = Pedido.query.get_or_404(id)
    nuevo_estado = request.form.get('estado')

    if nuevo_estado not in ESTADOS:
        flash('Estado no válido.', 'danger')
        return redirect(url_for('admin.pedidos'))

    pedido.estado = nuevo_estado
    db.session.commit()
    flash(f'Pedido #{pedido.id} actualizado a "{nuevo_estado}".', 'success')
    return redirect(url_for('admin.pedidos'))
