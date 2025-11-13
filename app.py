from flask import Flask, redirect, url_for, Blueprint
from config import Config
from models import init_db, login_manager,db
from models.Usuario import Usuarios
from controllers.auth_controller import auth_bp
from controllers.lab_controller import Lab_bp
from controllers.equipo_controller import equipo_bp
from controllers.usuario_controller import usuarios_bp
from views.views import views_bp
#from flask_migrate import Migrate

app = Flask(__name__)

app.config.from_object(Config)

# Inicializar base de datos
init_db(app)
# Registrar blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(Lab_bp)
app.register_blueprint(equipo_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(views_bp)

# User loader para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return Usuarios.query.get(int(user_id))

#migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)