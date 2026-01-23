from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User
import os

# --- IMPORT CÁC BLUEPRINT ---
from routes_hs import hs_bp
from routes_gvcn import gvcn_bp
from routes_gvbm import gvbm_bp

# Khởi tạo Flask với cấu hình instance_relative_config để trỏ vào thư mục instance
app = Flask(__name__, instance_relative_config=True)

# --- CẤU HÌNH ỨNG DỤNG ---
# Sử dụng sqlite:///quanly.db kết hợp với instance_relative_config=True 
# sẽ giúp Flask tự tìm database trong folder /instance/
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quanly.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'du-an-quan-ly-diem-2026' # Dùng để bảo mật session/flash

# --- KHỞI TẠO DATABASE ---
db.init_app(app)

# --- ĐĂNG KÝ CÁC BLUEPRINT ---
# Lưu ý: tên blueprint phải khớp với file lẻ (vd: hs, gvcn, gvbm)
app.register_blueprint(hs_bp)
app.register_blueprint(gvcn_bp)
app.register_blueprint(gvbm_bp)

# --- ROUTES HỆ THỐNG ---

@app.route('/')
def index():
    return redirect(url_for('login'))
db = SQLAlchemy(app)
#
# BENNGO TEST PUSH
# Model cơ sở dữ liệu
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user_name = request.form.get('username')
        pass_word = request.form.get('password')
        role = request.form.get('role')

        # Tìm người dùng khớp cả username, password và role
        user = User.query.filter_by(
            username=user_name,
            password=pass_word,
            role=role
        ).first()

        if user:
            # Điều hướng dựa trên role của User
            if user.role == 'student':
                return redirect(url_for('hs.dashboard'))
            elif user.role == 'gvcn':
                return redirect(url_for('gvcn.dashboard'))
            elif user.role == 'gvbm':
                return redirect(url_for('gvbm.input_grades'))
        else:
            error = "Sai tên đăng nhập, mật khẩu hoặc vai trò!"

    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        user_name = request.form.get('username')
        pass_word = request.form.get('password')
        pass_word_verify = request.form.get('password_verify')
        role = request.form.get('role') # Lấy từ thẻ <select> trong HTML

        # Các bước kiểm tra logic
        if not user_name or not pass_word or not role:
            error = "Vui lòng nhập đủ thông tin và chọn vai trò!"
        elif User.query.filter_by(username=user_name).first():
            error = "Tài khoản đã tồn tại!"
        elif len(pass_word) < 6:
            error = "Mật khẩu phải có ít nhất 6 ký tự!"
        elif pass_word != pass_word_verify:
            error = "Mật khẩu xác nhận không khớp!"
        else:
            try:
                # Tạo user mới và lưu vào DB
                new_user = User(username=user_name, password=pass_word, role=role)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                error = f"Lỗi cơ sở dữ liệu: {str(e)}"

    return render_template('register.html', error=error)

# --- KHỞI CHẠY ---
if __name__ == '__main__':
    with app.app_context():
        # Tạo folder instance nếu chưa có để chứa database
        if not os.path.exists(app.instance_path):
            os.makedirs(app.instance_path)
        # Tạo các bảng dựa trên models.py
        db.create_all() 
        
    app.run(host='127.0.0.1', port=5005, debug=True)