from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def role_required(*roles):
    """Permite acceso solo a los usuarios con alguno de los roles dados"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Debes iniciar sesión para acceder.", "warning")
                return redirect(url_for("auth.login"))
            if current_user.rol not in roles:
                flash("No tienes permiso para acceder a esta sección.", "danger")
                return redirect(url_for("laboratorio.dashboard"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
