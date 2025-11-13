from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, send_file
from flask_login import login_required
from models import db
from models.equipos import Equipos
from models.Usuario import Usuarios
from utils.decorators import role_required
import qrcode
from io import BytesIO
import base64

equipo_bp = Blueprint('equipo', __name__,template_folder='../views/templates')

@equipo_bp.route('/laboratorio/<int:panel_id>/equipo/create', methods=['POST'])
@login_required
@role_required('admin', 'profesor', 'tecnico')
def create_equipment(panel_id):
    name = request.form.get('name')
    status = request.form.get('status', 'disponible')
    location = request.form.get('location')
    user_id=request.form.get('user_id')
    
    if status not in Equipos.VALID_STATUSES:
        flash('Estado inválido', 'danger')
        return redirect(url_for('laboratorio.view_panel', panel_id=panel_id))
    
    if status == 'disponible':
        user_id=None
    
    equipment = Equipos(
        nombre=name,
        estado=status,
        ubicacion=location,
        laboratorio_id=panel_id,
        usuario_id=user_id
    )
    
    db.session.add(equipment)
    db.session.commit()
    
    flash('Equipo creado exitosamente', 'success')
    return redirect(url_for('laboratorio.view_panel', panel_id=panel_id))

@equipo_bp.route('/equipo/<int:equipment_id>/edit', methods=['POST'])
@login_required
@role_required('admin', 'profesor', 'tecnico')
def edit_equipment(equipment_id):
    equipment = Equipos.query.get_or_404(equipment_id)
    
    equipment.nombre = request.form.get('name')
    equipment.estado = request.form.get('status')
    equipment.ubicacion = request.form.get('location')
    
    if equipment.estado not in Equipos.VALID_STATUSES:
        flash('Estado inválido', 'danger')
        return redirect(url_for('laboratorio.view_panel', panel_id=equipment.laboratorio_id))
    
    if equipment.estado in ['usado','dañado']:
        equipment.usuario_id=request.form.get('user_id')
    else:
        equipment.usuario_id=None
    
    db.session.commit()
    
    flash('Equipo actualizado exitosamente', 'success')
    return redirect(url_for('laboratorio.view_panel', panel_id=equipment.laboratorio_id))

@equipo_bp.route('/equipo/<int:equipment_id>/delete', methods=['POST'])
@login_required
@role_required('admin', 'profesor', 'tecnico')
def delete_equipment(equipment_id):
    equipment = Equipos.query.get_or_404(equipment_id)
    panel_id = equipment.laboratorio_id
    
    db.session.delete(equipment)
    db.session.commit()
    
    flash('Equipo eliminado exitosamente', 'success')
    return redirect(url_for('laboratorio.view_panel', panel_id=panel_id))

@equipo_bp.route('/equipo/<int:equipment_id>')
@login_required
@role_required('admin', 'profesor', 'tecnico')
def get_equipment(equipment_id):
    equipment = Equipos.query.get_or_404(equipment_id)
    usu = None
    if equipment.usuario_id:
        usu = Usuarios.query.get(equipment.usuario_id)
        
    return jsonify({
        'id': equipment.id,
        'name': equipment.nombre,
        'status': equipment.estado,
        'location': equipment.ubicacion,
        'user_id': usu.username if usu else None
    })
    
@equipo_bp.route('/equipo/<int:equipment_id>/qr')
@login_required
@role_required('admin', 'profesor', 'tecnico')
def get_qr(equipment_id):
    equipment = Equipos.query.get_or_404(equipment_id)
    usu = None
    if equipment.usuario_id:
        usu = Usuarios.query.get(equipment.usuario_id)
    
    datos = f"""
    Nombre: {equipment.nombre}
    Estado: {equipment.estado}
    Ubicación: {equipment.ubicacion}
    Usuario: {usu.username if usu != None else 'Sin Usuario'}
    """
    
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
        'nombre_archivo': f"qr_{equipment.nombre}.png"
    })

'''def generar_qr():
    nombre = request.form.get('nombre')
    estado = request.form.get('estado')
    ubicacion = request.form.get('ubicacion')
    usuario = request.form.get('usuario')

    datos = f"""
    Nombre: {nombre}
    Estado: {estado}
    Ubicación: {ubicacion}
    Usuario: {usuario}
    """

    filename = f"qr_image_{nombre}.png"
    ruta_qr = os.path.join(TEMP_FOLDER, filename)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(datos)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(ruta_qr)

    return render_template(
        "Panel.html",
        qr_image=url_for('static', filename=f"temp/{filename}"),
        nombre_archivo=filename,
        mensaje="QR generado con éxito"
    )
'''

# Ruta para "guardar" el QR (descarga al usuario)
@equipo_bp.route('/equipo/guardar_qr/<int:equipment_id>')
@login_required
@role_required('admin', 'profesor', 'tecnico')
def guardar_qr(equipment_id):
    equipment = Equipos.query.get_or_404(equipment_id)
    usu = Usuarios.query.get(equipment.usuario_id) if equipment.usuario_id else None

    datos = f"""
    Nombre: {equipment.nombre}
    Estado: {equipment.estado}
    Ubicación: {equipment.ubicacion}
    Usuario: {usu.username if usu else 'Sin Usuario'}
    """

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
        download_name=f"qr_{equipment.nombre}.png"
    )