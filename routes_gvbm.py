from flask import Blueprint, render_template

gvbm_bp = Blueprint('gvbm', __name__)

@gvbm_bp.route('/gvbm/input')
def input_grades():
    return render_template('gvbm/dashboad.html')