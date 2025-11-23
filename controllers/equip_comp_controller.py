from flask import Blueprint, redirect, url_for, jsonify, render_template,request, flash
from flask_login import login_user, logout_user, login_required
from utils.decorators import role_required
from models import db
from models.equip_comp import Equip_comp
from models.equipos import Equipos

eq_comp_bp = Blueprint('eq_comp', __name__,template_folder='../views/templates')

@eq_comp_bp.route('/eq_comp')
@login_required
def dashboard():
    comps = Equip_comp.query.all()
    equipos = Equipos.query.all()
    return render_template('componentes_dashboard.html', comps=comps, equipos=equipos)

@eq_comp_bp.route('/eq_comp/create', methods=['POST'])
@login_required
@role_required('admin', 'profesor')
def create_comp():
    cod_eq = request.form.get('cod_eq')
    ram = request.form.get('ram')
    hd=request.form.get('hd')
    modelo=request.form.get('modelo')
    eq_id=request.form.get('eq_id')
    
    otro_comp = Equip_comp.query.filter(
        Equip_comp.equipo_id == eq_id,
        Equip_comp.cod_eq != cod_eq
    ).first()

    if otro_comp:
        flash('Error: Este equipo ya tiene un componente asignado.', 'danger')
        return redirect(url_for('eq_comp.dashboard'))
    
    comp=Equip_comp(cod_eq=cod_eq, ram=ram, hd=hd, modelo=modelo, equipo_id=eq_id)
    db.session.add(comp)
    db.session.commit()
    
    flash('Componentes creados exitosamente', 'success')
    return redirect(url_for('eq_comp.dashboard'))

@eq_comp_bp.route('/eq_comp/<int:cod_eq>/delete', methods=['POST'])
@login_required
@role_required('admin')
def delete_comp(cod_eq):
    comp = Equip_comp.query.get_or_404(cod_eq)
    db.session.delete(comp)
    db.session.commit()
    
    flash('Componentes eliminados exitosamente', 'success')
    return redirect(url_for('eq_comp.dashboard'))

@eq_comp_bp.route('/eq_comp/<int:cod_eq>/edit', methods=['POST'])
@login_required
@role_required('admin', 'profesor', 'tecnico')
def edit_comp(cod_eq):
    eq_comp = Equip_comp.query.get_or_404(cod_eq)
    eq_id=request.form.get('eq_id')
    
    otro_comp = Equip_comp.query.filter(
        Equip_comp.equipo_id == eq_id,
        Equip_comp.cod_eq != cod_eq
    ).first()

    if otro_comp:
        flash('Error: Este equipo ya tiene un componente asignado.', 'danger')
        return redirect(url_for('eq_comp.dashboard'))
    
    eq_comp.ram = request.form.get('ram')
    eq_comp.hd=request.form.get('hd')
    eq_comp.modelo=request.form.get('modelo')
    
    eq_comp.equipo_id=eq_id
    
    db.session.commit()
    
    flash('Componentes actualizados exitosamente', 'success')
    return redirect(url_for('eq_comp.dashboard'))

@eq_comp_bp.route('/eq_comp/<int:cod_eq>')
@login_required
@role_required('admin', 'profesor', 'tecnico')
def get_comp(cod_eq):
    eq_comp = Equip_comp.query.get_or_404(cod_eq)
    return jsonify({
        'id':eq_comp.cod_eq,
        'ram':eq_comp.ram,
        'hd':eq_comp.hd,
        'modelo':eq_comp.modelo,
        'equipo_id':eq_comp.equipo_id
    })
    
@eq_comp_bp.route('/eq_comp/<int:cod_eq>')
@login_required
@role_required('admin', 'profesor', 'tecnico')
def get_eq(cod_eq):
    equipment = Equipos.query.get_or_404(cod_eq)
    return jsonify({
        'id': equipment.id,
        'name': equipment.nombre,
        'status': equipment.estado
    })