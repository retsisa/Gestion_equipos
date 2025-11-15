from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required
from models import db
from models.Lab import Laboratorios
from models.Usuario import Usuarios
from utils.decorators import role_required

Lab_bp = Blueprint('laboratorio', __name__,template_folder='../views/templates')

@Lab_bp.route('/dashboard')
@login_required
def dashboard():
    panels = Laboratorios.query.all()
    return render_template('dashboard.html', panels=panels)

@Lab_bp.route('/laboratorio/<int:panel_id>')
@login_required
def view_panel(panel_id):
    panel = Laboratorios.query.get_or_404(panel_id)
    panels = Laboratorios.query.all()
    usuarios=Usuarios.query.all()
    return render_template('panel.html', panel=panel, usuarios=usuarios, panels=panels)

@Lab_bp.route('/laboratorio/create', methods=['POST'])
@login_required
@role_required('admin', 'profesor')
def create_panel():
    name = request.form.get('name')
    description = request.form.get('description')
    
    panel = Laboratorios(nombre=name, descripcion=description)
    db.session.add(panel)
    db.session.commit()
    
    flash('Panel creado exitosamente', 'success')
    return redirect(url_for('laboratorio.dashboard'))

@Lab_bp.route('/laboratorio/<int:panel_id>/delete', methods=['POST'])
@login_required
@role_required('admin')
def delete_panel(panel_id):
    panel = Laboratorios.query.get_or_404(panel_id)
    db.session.delete(panel)
    db.session.commit()
    
    flash('Laboratorio eliminado exitosamente', 'success')
    return redirect(url_for('laboratorio.dashboard'))

@Lab_bp.route('/laboratorio/<int:lab_id>/edit', methods=['POST'])
@login_required
@role_required('admin', 'profesor', 'tecnico')
def edit_panel(lab_id):
    labs = Laboratorios.query.get_or_404(lab_id)
    
    labs.nombre = request.form.get('nombre')
    labs.descripcion = request.form.get('descripcion')
    
    db.session.commit()
    
    flash('Panel actualizado exitosamente', 'success')
    return redirect(url_for('laboratorio.dashboard'))

@Lab_bp.route('/laboratorio/<int:lab_id>/data')
@login_required
@role_required('admin', 'profesor', 'tecnico')
def get_lab(lab_id):
    labs = Laboratorios.query.get_or_404(lab_id)
    return jsonify({
        'id': labs.id,
        'nombre': labs.nombre,
        'descripcion': labs.descripcion
    })