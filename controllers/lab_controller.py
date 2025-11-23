from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, send_file
from flask_login import login_required
from models import db
from models.Lab import Laboratorios
from models.Usuario import Usuarios
from utils.decorators import role_required
import base64
import qrcode
from io import BytesIO

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
    ubicacion = request.form.get('ubicacion')
    
    panel = Laboratorios(nombre=name, descripcion=description, ubicacion=ubicacion)
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
    labs.ubicacion = request.form.get('ubicacion')
    
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
        'descripcion': labs.descripcion,
        'ubicacion': labs.ubicacion
    })
    
@Lab_bp.route('/laboratorio/qr')
@login_required
@role_required('admin', 'profesor', 'tecnico')
def get_qr():
    datos = "https://gestion-equipos.onrender.com/"
    
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=10, border=4)
    qr.add_data(datos)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    # Guardar en memoria y convertir a base64
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Enviar como JSON
    return jsonify({
        'qr_image': f"data:image/png;base64,{qr_base64}",
        'mensaje': "QR generado con éxito",
        'nombre_archivo': f"qr_pagina.png"
    })

@Lab_bp.route('/laboratorio/guardar_qr')
@login_required
@role_required('admin', 'profesor', 'tecnico')
def guardar_qr():
    datos = "https://gestion-equipos.onrender.com/"

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=10, border=4)
    qr.add_data(datos)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype='image/png',
        as_attachment=True,
        download_name=f"qr_pagina.png"
    )