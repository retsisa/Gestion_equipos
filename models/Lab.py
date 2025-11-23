from models import db

class Laboratorios(db.Model):
    __tablename__ = 'laboratorios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
    ubicacion = db.Column(db.Text, nullable=False)
    
    equipos = db.relationship('Equipos', backref='laboratorio', lazy=True, cascade='all, delete-orphan')

'''from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db=SQLAlchemy()

class Lab(db.Model):
    """Modelo de Laboratorio"""
    __tablename__ = 'labs'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    ubicacion = db.Column(db.String(200), nullable=False)
    capacidad = db.Column(db.Integer, nullable=False)
    descripcion = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con equipos
    equipos = db.relationship('Equipo', backref='lab', lazy=True, cascade='all, delete-orphan')
    
    def get_estadisticas(self):
        """Obtener estadísticas del laboratorio"""
        total = len(self.equipos)
        disponibles = len([e for e in self.equipos if e.estado == 'Disponible'])
        en_uso = len([e for e in self.equipos if e.estado == 'En Uso'])
        danados = len([e for e in self.equipos if e.estado == 'Dañado'])
        mantenimiento = len([e for e in self.equipos if e.estado == 'Mantenimiento'])
        
        return {
            'total': total,
            'disponibles': disponibles,
            'en_uso': en_uso,
            'danados': danados,
            'mantenimiento': mantenimiento
        }
    
    def __repr__(self):
        return f'<Lab {self.nombre}>'
'''