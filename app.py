from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quanly.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#

# Model cơ sở dữ liệu
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)

# --- ROUTE ĐĂNG NHẬP ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form.get('username')
        pass_word = request.form.get('password')
    
        # Kiểm tra xem có user nào khớp cả user_name và pass_word không
        user = User.query.filter_by(username=user_name, password=pass_word).first()

        if user:
            return f"Đăng nhập thành công! Chào {user.username} (Vai trò: {user.role})"
        else:
            return "Sai tên đăng nhập hoặc mật khẩu!"

    return render_template('login.html')

# --- ROUTE ĐĂNG KÝ ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form.get('username')
        pass_word = request.form.get('password')
        pass_word_verify = request.form.get('password_verify')

        if not user_name or not pass_word:
            return "Vui lòng nhập đủ thông tin!"

        existing_user = User.query.filter_by(username=user_name).first()
        if existing_user:
            return "Tài khoản đã tồn tại!"
        if not pass_word_verify == pass_word:
            return redirect(url_for('register'))

        new_user = User(username=user_name, password=pass_word, role='teacher')
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    
    return render_template('register.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(host='0.0.0.0', port=5002, debug=True)