from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quanly.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#
# BENNGO TEST PUSH
# Model cơ sở dữ liệu
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)

# --- ROUTE ĐĂNG NHẬP ---
@app.route('/login', methods=['GET', 'POST'])
def login():

    error = None

    if request.method == 'POST':
        user_name = request.form.get('username')
        pass_word = request.form.get('password')
        role = request.form.get('role')

        user = User.query.filter_by(
            username=user_name,
            password=pass_word,
            role=role
        ).first()

        if user:
            return f"Đăng nhập thành công! ({user.role})"
        else:
            error = "Sai tên đăng nhập, mật khẩu!"

    return render_template('login.html', error=error)

# --- ROUTE ĐĂNG KÝ ---
@app.route('/register', methods=['GET', 'POST'])
def register():

    error = None

    if request.method == 'POST':
        user_name = request.form.get('username')
        pass_word = request.form.get('password')
        pass_word_verify = request.form.get('password_verify')

        if not user_name or not pass_word:
            error = "Vui lòng nhập đủ thông tin!"
            return render_template('register.html', error=error)
        existing_user = User.query.filter_by(username=user_name).first()

        if existing_user:
            error = "Tài khoản đã tồn tại!"
            return render_template('register.html', error=error)
        
        if len(pass_word) < 8:
            error = "Mật khẩu phải ít nhất 8 kí tự"
            return render_template('register.html', error=error)

        if not pass_word_verify == pass_word:
            error = "Xác nhận lại mật khẩu!"
            return render_template('register.html', error=error)

        new_user = User(username=user_name, password=pass_word, role='teacher')
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    
    return render_template('register.html', error=error)

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(host='127.0.0.1', port=5005, debug=True)