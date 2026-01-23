from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User, Student
import os

# import blueprints
from routes_hs import hs_bp
from routes_gvcn import gvcn_bp
from routes_gvbm import gvbm_bp

app = Flask(__name__, instance_relative_config=True)

# --- CẤU HÌNH ---
# Database nằm trong thư mục /instance/quanly.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quanly.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'khoa-bi-mat-cho-session-2026' 

# initialise db
db.init_app(app)

app.register_blueprint(hs_bp)
app.register_blueprint(gvcn_bp)
app.register_blueprint(gvbm_bp)

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    role = session.get('role')
    if role == 'student':
        return redirect(url_for('hs.dashboard'))
    elif role == 'gvcn':
        return redirect(url_for('gvcn.dashboard'))
    elif role == 'gvbm':
        return redirect(url_for('gvbm.input_grades'))
    
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user_name = request.form.get('username')
        pass_word = request.form.get('password')
        role = request.form.get('role') 

        # find user
        user = User.query.filter_by(username=user_name, role=role).first()

        if user and user.check_password(pass_word):
            session['user_id'] = user.id
            session['role'] = user.role
            session['username'] = user.username
            
            #redirecting
            if user.role == 'student':
                return redirect(url_for('hs.dashboard'))
            elif user.role == 'gvcn':
                return redirect(url_for('gvcn.dashboard'))
            elif user.role == 'gvbm':
                return redirect(url_for('gvbm.input_grades'))
        else:
            error = "Sai tên đăng nhập, mật khẩu hoặc vai trò!"

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        user_name = request.form.get('username')
        pass_word = request.form.get('password')
        role = request.form.get('role')

        if User.query.filter_by(username=user_name).first():
            error = "Tài khoản đã tồn tại!"
        else:
            new_user = User(username=user_name, role=role)
            new_user.set_password(pass_word) # encoding password
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    
    return render_template('register.html', error=error)

if __name__ == '__main__':
    with app.app_context():
        # create instance if not created
        if not os.path.exists(app.instance_path):
            os.makedirs(app.instance_path)
        db.create_all()
        
    app.run(host='127.0.0.1', port=5005, debug=True)