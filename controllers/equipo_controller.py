from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, send_file
from flask_login import login_required
from models import db
from models.equipos import Equipos
from models.Usuario import Usuarios
from utils.decorators import role_required
import qrcode
from io import BytesIO
import base64
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
from reportlab.pdfbase.pdfmetrics import stringWidth
from weasyprint import HTML

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
    
def generar_qr_base64(texto):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=6,
        border=2,
    )
    qr.add_data(texto)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return base64.b64encode(buffer.getvalue()).decode('utf-8')

def wrap_text(text, max_width, font_name="Helvetica", font_size=11):
    palabras = text.split(" ")
    lineas = []
    linea_actual = ""

    for palabra in palabras:
        prueba = linea_actual + " " + palabra if linea_actual else palabra
        if stringWidth(prueba, font_name, font_size) <= max_width:
            linea_actual = prueba
        else:
            lineas.append(linea_actual)
            linea_actual = palabra

    if linea_actual:
        lineas.append(linea_actual)

    return lineas


@equipo_bp.route('/equipo/reporte/pdf')
@login_required
@role_required('admin', 'profesor', 'tecnico')
def generar_reporte_pdf():
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    y = 720

    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(50, 770, "Reporte de Equipos")
    pdf.setFont("Helvetica", 11)
    from models.Lab import Laboratorios
    labs=Laboratorios.query.all()
    for lab in labs:
        y += 50
        equipos = Equipos.query.filter_by(laboratorio_id=lab.id).all()
        if not equipos:
            pdf.drawString(70, y, "No hay equipos registrados.")
            y -= 30
            continue
        y -= 30
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(210, y, f"{lab.nombre}")
        pdf.setFont("Helvetica", 11)
        y -= 20
        for eq in equipos:
            usuario = "Sin usuario"
            if eq.usuario_id:
                usuario_data = Usuarios.query.get(eq.usuario_id)
                usuario = usuario_data.username if usuario_data else "Sin usuario"

            '''qr_base64 = generar_qr_base64(
                f"ID: {eq.id}\nNombre: {eq.nombre}\nUbicación: {eq.ubicacion}\nUsuario: {usuario}"
            )

            img_data = base64.b64decode(qr_base64)
            qr_file = BytesIO(img_data)

            img = Image.open(qr_file)'''

            pdf.drawString(50, y, f"ID: {eq.id}")
            nombre_text = f"Nombre: {eq.nombre}"
            lineas_nombre = wrap_text(nombre_text, max_width=120)

            for linea in lineas_nombre:
                pdf.drawString(90, y, linea)
                y -= 12

            pdf.drawString(190, y, f"Estado: {eq.estado}")
            ubicacion_text = f"Ubicación: {eq.ubicacion}"
            lineas_ubicacion = wrap_text(ubicacion_text, max_width=250)

            for linea in lineas_ubicacion:
                pdf.drawString(290, y, linea)
                y -= 12

            pdf.drawString(50, y-15, f"Usuario: {usuario}")
            #pdf.drawInlineImage(img, 500, y - 40, 50, 50)

            y -= 70
            if y < 80:
                pdf.showPage()
                pdf.setFont("Helvetica", 11)
                y = 760

    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="reporte_equipos.pdf",
        mimetype="application/pdf"
    )
    
@equipo_bp.route('/equipo/<int:equipment_id>/mover', methods=['POST'])
@login_required
@role_required('admin', 'profesor', 'tecnico')
def mover_equipo(equipment_id):
    equipment = Equipos.query.get_or_404(equipment_id)

    nuevo_lab = request.form.get('nuevo_lab')

    if not nuevo_lab:
        flash("Debes seleccionar un laboratorio destino.", "warning")
        return redirect(url_for('laboratorio.view_panel', panel_id=equipment.laboratorio_id))

    try:
        nuevo_lab = int(nuevo_lab)
    except:
        flash("ID de laboratorio inválido", "danger")
        return redirect(url_for('laboratorio.view_panel', panel_id=equipment.laboratorio_id))

    from models.Lab import Laboratorios
    if not Laboratorios.query.get(nuevo_lab):
        flash("El laboratorio de destino no existe.", "danger")
        return redirect(url_for('laboratorio.view_panel', panel_id=equipment.laboratorio_id))

    laboratorio_anterior = Laboratorios.query.get_or_404(equipment.laboratorio_id)
    n_lab=Laboratorios.query.get_or_404(nuevo_lab)
    equipment.laboratorio_id = nuevo_lab
    if equipment.estado == "disponible":
        equipment.ubicacion=n_lab.nombre
    db.session.commit()

    flash(f"Equipo movido del laboratorio {laboratorio_anterior.nombre} al {n_lab.nombre}", "success")
    return redirect(url_for('laboratorio.view_panel', panel_id=nuevo_lab))

@equipo_bp.route('/equipo/reporte/generar_pdf', methods=['POST'])
@login_required
def generar_pdf():
    data = request.get_json()
    contenido_html = data.get('contenido', '')

    # Generar PDF
    pdf_file = BytesIO()
    HTML(string=contenido_html).write_pdf(pdf_file)
    pdf_file.seek(0)

    return send_file(pdf_file, as_attachment=True, download_name="reporte.pdf", mimetype='application/pdf')
    
@equipo_bp.route('/equipo/editor')
@login_required
@role_required('admin', 'profesor', 'tecnico')
def editor_reporte():
    return render_template("editor_reporte.html")