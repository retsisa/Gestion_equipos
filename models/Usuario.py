from models import db
from flask_login import UserMixin
from sqlalchemy import CheckConstraint
from werkzeug.security import generate_password_hash, check_password_hash

class Usuarios(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    rol = db.Column(db.String(20), nullable=False, default='estudiante')
    
    def set_password(self, password_e):
        self.password = generate_password_hash(password_e)
    
    def check_password(self, password_e):
        return check_password_hash(self.password, password_e)
    
    __table_args__ = (
        CheckConstraint("rol IN ('admin', 'profesor', 'estudiante', 'tecnico')", name='check_rol'),
    )