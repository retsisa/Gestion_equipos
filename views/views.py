from flask import Blueprint, render_template, redirect, url_for

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index():
    return redirect(url_for('auth.login'))