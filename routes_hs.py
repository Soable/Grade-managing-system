from flask import Blueprint, render_template, session, redirect, url_for 

hs_bp = Blueprint('hs', __name__)

@hs_bp.route('/student/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('role') != 'student':
        return redirect(url_for('login'))
    return render_template('hs/dashboard.html')