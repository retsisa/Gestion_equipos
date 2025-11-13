from models import db
from datetime import datetime

class Equipos(db.Model):
    __tablename__ = 'equipos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(20), nullable=False, default='disponible')
    ubicacion = db.Column(db.Text, nullable=False)
    laboratorio_id = db.Column(db.Integer, db.ForeignKey('laboratorios.id'), nullable=False)
    
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)

    usuario = db.relationship('Usuarios', backref='equipos_asignados', lazy=True) 
    
    # Estados permitidos: disponible, usado, dañado
    VALID_STATUSES = ['disponible', 'usado', 'dañado']

'''from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db=SQLAlchemy()

class Equipo(db.Model):
    """Modelo de Equipo"""
    __tablename__ = 'equipos'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)  # PC-1, PC-2, etc.
    tipo = db.Column(db.String(50), nullable=False)  # Computadora, Monitor, Impresora, etc.
    marca = db.Column(db.String(50))
    modelo = db.Column(db.String(100))
    
    # Estados: Disponible, En Uso, Dañado, Mantenimiento
    estado = db.Column(db.String(20), nullable=False, default='Disponible')
    
    # Ubicación específica dentro del lab
    ubicacion_especifica = db.Column(db.String(100))  # Ej: "Fila 1 - Posición 3"
    
    observaciones = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación con laboratorio
    lab_id = db.Column(db.Integer, db.ForeignKey('labs.id'), nullable=False)
    
    def get_estado_badge(self):
        """Retorna clase CSS según el estado"""
        estados = {
            'Disponible': 'success',
            'En Uso': 'warning',
            'Dañado': 'danger',
            'Mantenimiento': 'info'
        }
        return estados.get(self.estado, 'secondary')
    
    def __repr__(self):
        return f'<Equipo {self.codigo} - {self.estado}>'
'''