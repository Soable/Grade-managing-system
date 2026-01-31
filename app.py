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
        role = session.get('role')
        if role == 'teacher':
            return redirect(url_for('gv.dashboard'))
        elif role == 'student':
            return redirect(url_for('hs.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            flash("Sai tên đăng nhập hoặc mật khẩu!")
            return redirect(url_for('login'))

        session['user_id'] = user.id
        session['role'] = user.role
        session['username'] = user.username
        
        return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        role = session.get('role')
        if role == 'teacher':
            return redirect(url_for('gv.dashboard'))
        elif role == 'student':
            return redirect(url_for('hs.dashboard'))
        
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        username = request.form.get('username')
        password = request.form.get('password')
        role = 'teacher'
        
        subject = request.form.get('subject')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Tài khoản đã tồn tại!')
            return redirect(url_for('register'))

        new_user = User(
            username=username, 
            full_name=full_name,
            role=role,
            subject=subject if role == 'teacher' else None
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Đăng ký thành công! Vui lòng đăng nhập.')
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
