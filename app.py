from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User
import os

from routes_hs import hs_bp
from routes_gv import gv_bp

app = Flask(__name__, instance_relative_config=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'khoa-bi-mat-cho-session-2026' 

db.init_app(app)

app.register_blueprint(hs_bp)
app.register_blueprint(gv_bp)

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    role = session.get('role')
    if role == 'student':
        return redirect(url_for('hs.dashboard'))
    elif role == 'teacher':
        return redirect(url_for('gv.dashboard'))
    
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role_from_form = request.form.get('role') 
        
        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            flash("Sai tên đăng nhập hoặc mật khẩu!")
            return redirect(url_for('login'))

        elif user.role != role_from_form:
            flash(f"Tài khoản này không phải là { 'Học sinh' if role_from_form == 'student' else 'Giáo viên' }!")
            return redirect(url_for('login'))

        session['user_id'] = user.id
        session['role'] = user.role
        session['username'] = user.username
        
        return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        subject = request.form.get('subject') # teacher's in-charge subject

        if User.query.filter_by(username=username).first():
            flash("Tài khoản đã tồn tại!")
            return redirect(url_for('register'))

        new_user = User(username=username, role='teacher', subject=subject)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash("Đăng ký thành công! Hãy đăng nhập.")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists(app.instance_path):
            os.makedirs(app.instance_path)
        db.create_all()
    
    app.run(host='127.0.0.1', port=5005, debug=True)
    logout() 
    