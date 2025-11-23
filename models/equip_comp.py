from models import db

class Equip_comp(db.Model):
    __tablename__ = 'equip_comp'
    
    cod_eq=db.Column(db.Integer, primary_key=True)
    ram=db.Column(db.String(80), nullable=False)
    hd=db.Column(db.String(50), nullable=False)
    modelo=db.Column(db.String(100), nullable=False)
    equipo_id=db.Column(db.Integer, db.ForeignKey('equipos.id'), nullable=False)
    
    equipos = db.relationship('Equipos', backref='equipo_comp', lazy=True)