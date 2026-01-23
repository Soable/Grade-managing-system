from flask import Blueprint, render_template

hs_bp = Blueprint('hs', __name__)

@hs_bp.route('/student/dashboard')
def dashboard():
    return render_template('hs/dashboard.html')