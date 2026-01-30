from flask import Blueprint, render_template, session, redirect, url_for
from models import Student

hs_bp = Blueprint('hs', __name__)

@hs_bp.route('/student/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('role') != 'student':
        return redirect(url_for('login'))
    
    student = Student.query.filter_by(user_id=session['user_id']).first()
    if student:
        grade = student.grade
    else:
        grade = 0

    return render_template(
        'hs/dashboard.html',
        student=student,
        grade=grade
    )

@hs_bp.route('/hs/change_password', methods=['POST'])
def change_password():
    if 'user_id' not in session or session.get('role') != 'student':
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    old_pass = request.form.get('old_password')
    new_pass = request.form.get('new_password')
    confirm_pass = request.form.get('confirm_password')

    if not user.check_password(old_pass):
        flash("Mật khẩu cũ không chính xác!")
        return redirect(url_for('hs.dashboard'))
    
    if new_pass != confirm_pass:
        flash("Mật khẩu mới và xác nhận không khớp!")
        return redirect(url_for('hs.dashboard'))

    user.set_password(new_pass)
    db.session.commit()
    flash("Đổi mật khẩu thành công!")
    return redirect(url_for('hs.dashboard'))
