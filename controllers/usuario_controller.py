from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from models import db
from models.Usuario import Usuarios
from utils.decorators import role_required

usuarios_bp = Blueprint('usuarios', __name__, template_folder='../views/templates')

@usuarios_bp.route('/usuarios')
@login_required
@role_required('admin')
def dashboard_usuarios():
    users = Usuarios.query.all()
    return render_template('usuarios.html', users=users)

@usuarios_bp.route('/usuarios/create', methods=['POST'])
@login_required
@role_required('admin')
def crear_usuario():
    username = request.form.get('username')
    password = request.form.get('password')
    rol = request.form.get('rol')

    if Usuarios.query.filter_by(username=username).first():
        flash('El usuario ya existe', 'danger')
        return redirect(url_for('usuarios.dashboard_usuarios'))

    nuevo_usuario = Usuarios(username=username, rol=rol)
    nuevo_usuario.set_password(password)
    db.session.add(nuevo_usuario)
    db.session.commit()
    flash('Usuario creado correctamente', 'success')
    return redirect(url_for('usuarios.dashboard_usuarios'))

@usuarios_bp.route('/usuarios/<int:user_id>/delete', methods=['POST'])
@login_required
@role_required('admin')
def eliminar_usuario(user_id):
    user = Usuarios.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Usuario eliminado correctamente', 'success')
    return redirect(url_for('usuarios.dashboard_usuarios'))

@usuarios_bp.route('/usuarios/<int:user_id>/edit', methods=['POST'])
@login_required
@role_required('admin')
def edit_user(user_id):
    usu = Usuarios.query.get_or_404(user_id)
    
    usu.username = request.form.get('username')
    password = request.form.get('password')
    usu.rol=request.form.get('rol')
    if password and password.strip() != "":
        usu.set_password(password)
    db.session.commit()
    
    flash('Usuario actualizado exitosamente', 'success')
    return redirect(url_for('usuarios.dashboard_usuarios'))

@usuarios_bp.route('/usuarios/<int:user_id>')
@login_required
@role_required('admin')
def get_user(user_id):
    users = Usuarios.query.get_or_404(user_id)
    return jsonify({
        'id': users.id,
        'username': users.username,
        'rol': users.rol
    })