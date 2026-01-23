from flask import Blueprint, render_template

gvcn_bp = Blueprint('gvcn', __name__)

@gvcn_bp.route('/gvcn/dashboard')
def dashboard():
    return render_template('gvcn/dashboard.html')