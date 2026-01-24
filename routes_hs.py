from flask import Blueprint, render_template, session, redirect, url_for
from models import Student

hs_bp = Blueprint('hs', __name__)

@hs_bp.route('/student/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('role') != 'student':
        return redirect(url_for('login'))
    
    student = Student.query.filter_by(user_id=session['user_id']).first()
    
    grade = student.grade  # có thể là None

    return render_template(
        'hs/dashboard.html',
        student=student,
        grade=grade
    )
