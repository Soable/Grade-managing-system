from flask import Blueprint, render_template, session, redirect, url_for 


gvbm_bp = Blueprint('gvbm', __name__)

@gvbm_bp.route('/gvbm/input')
def input_grades():
    if 'user_id' not in session or session.get('role') != 'gvbm':
        return redirect(url_for('login'))
    return render_template('gvbm/dashboad.html')