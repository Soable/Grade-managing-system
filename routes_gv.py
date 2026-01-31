from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from models import db, User, Student, Classroom, Grade
import random, string, csv, io

gv_bp = Blueprint('gv', __name__)

def generate_class_code():
    return ''.join(random.choices(string.digits, k=4))

@gv_bp.route('/gv/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('role') != 'teacher':
        return redirect(url_for('login'))
    
    teacher_id = session['user_id']
    user = User.query.get(teacher_id)
    my_homeroom_classes = Classroom.query.filter_by(gv_id=teacher_id).all()
    my_teaching_classes = user.teaching_classes

    return render_template('gv/dashboard.html', 
                           classes=my_homeroom_classes, 
                           teaching_classes=my_teaching_classes, 
                           user=user)

# HOMEROOM classes
@gv_bp.route('/gv/create_class', methods=['POST'])
def create_class():
    if 'user_id' not in session or session.get('role') != 'teacher':
        return redirect(url_for('login'))

    class_name = request.form.get('class_name')
    new_code = generate_class_code() 

    new_class = Classroom(
        class_name=class_name,
        class_code=new_code,
        gv_id=session['user_id']
    )
    db.session.add(new_class)
    db.session.commit()
    return redirect(url_for('gv.dashboard'))

@gv_bp.route('/gv/class/<int:class_id>', methods=['GET', 'POST'])
def class_detail(class_id):
    if 'user_id' not in session or session.get('role') != 'teacher':
        return redirect(url_for('login'))

    current_class = Classroom.query.get_or_404(class_id)
    if current_class.gv_id != session['user_id']:
        flash("Bạn không phải gv của lớp này!")
        return redirect(url_for('gv.dashboard'))
    
    # create class list by uploading a .csv
    if request.method == 'POST':
        if 'upload_csv' in request.form:
            file = request.files.get('file')
            format_type = request.form.get('format_type') 
            if file and file.filename.endswith('.csv'):
                stream = io.TextIOWrapper(file.stream, encoding="utf-8")
                csv_reader = csv.reader(stream)
                for row in csv_reader:
                    if not row: continue 
                    h_mshs = row[0].strip()
                    if h_mshs.lower() == 'mshs': continue
                    
                    h_ten = ""
                    # 2 format type: full name | last name - first name
                    if format_type == '1' and len(row) >= 2: h_ten = row[1].strip()
                    elif format_type == '2' and len(row) >= 3: h_ten = f"{row[1].strip()} {row[2].strip()}"
                    
                    if not h_ten: continue
                    
                    if not Student.query.filter_by(mshs=h_mshs).first():
                        u = User(username=h_mshs, role='student'); u.set_password('123456')
                        db.session.add(u); db.session.flush()
                        s = Student(mshs=h_mshs, name=h_ten, user_id=u.id, class_id=current_class.id)
                        db.session.add(s); db.session.flush()
                        db.session.add(Grade(student_id=s.id))
                db.session.commit()
                flash("Đã nhập danh sách CSV!")

        elif 'manual_add' in request.form:
            mshs = request.form.get('mshs')
            name = request.form.get('name')
            if Student.query.filter_by(mshs=mshs).first():
                flash(f"Mã số {mshs} đã tồn tại!")
            else:
                u = User(username=mshs, role='student'); u.set_password('123456')
                db.session.add(u); db.session.flush()
                s = Student(mshs=mshs, name=name, user_id=u.id, class_id=current_class.id)
                db.session.add(s); db.session.flush()
                db.session.add(Grade(student_id=s.id))
                db.session.commit()
                flash("Đã thêm học sinh!")

        return redirect(url_for('gv.class_detail', class_id=class_id))
    
    students = Student.query.filter_by(class_id=class_id).order_by(Student.mshs.asc()).all()
    return render_template('gv/class_detail.html', classroom=current_class, students=students)

# teachers have ability to reset passwords
@gv_bp.route('/gv/change_password/<int:student_id>', methods=['GET', 'POST'])
def change_password(student_id):
    if 'user_id' not in session or session.get('role') != 'teacher': return redirect(url_for('login'))
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        if student.user_account: 
            student.user_account.set_password('123456')
            db.session.commit()
            flash("Đã reset mật khẩu!")
        return redirect(url_for('gv.class_detail', class_id=student.class_id))
    return render_template('gv/change_password.html', student=student)

# TEACHING classes
@gv_bp.route('/gv/join_class', methods=['POST'])
def join_class():
    if 'user_id' not in session: return redirect(url_for('login'))
    
    code = request.form.get('class_code')
    user = User.query.get(session['user_id'])
    target_class = Classroom.query.filter_by(class_code=code).first()
    
    if not target_class:
        flash("Mã lớp không tồn tại!")
    elif target_class in user.teaching_classes:
        flash("Bạn đã tham gia lớp này rồi!")
    else:
        user.teaching_classes.append(target_class)
        db.session.commit()
        flash(f"Đã tham gia dạy lớp {target_class.class_name}!")
        
    return redirect(url_for('gv.dashboard'))

@gv_bp.route('/gv/grading/<int:class_id>', methods=['GET', 'POST'])
def grading(class_id):
    if 'user_id' not in session: return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    classroom = Classroom.query.get_or_404(class_id)
    
    subject_map = {
        'Toan': 'math', 'Toán': 'math', 'math': 'math',
        'Van': 'lit',   'Văn': 'lit',   'lit': 'lit', 'Literature': 'lit',
        'Anh': 'eng',   'eng': 'eng',   'English': 'eng',
        'Ly': 'phy',    'Lý': 'phy',    'phy': 'phy', 'Physics': 'phy',
        'Hoa': 'chem',  'Hóa': 'chem',  'chem': 'chem', 'Chemistry': 'chem',
        'Sinh': 'bio',  'bio': 'bio',   'Biology': 'bio',
        'Tin': 'inf',   'inf': 'inf',   'Informatics': 'inf',
        'Su': 'hist',   'Sử': 'hist',   'hist': 'hist', 'History': 'hist',
        'Dia': 'geo',   'Địa': 'geo',   'geo': 'geo',   'Geography': 'geo',
        'GDCD': 'civic', 'civic': 'civic', 'ktpl': 'civic',
        'CongNghe': 'tech', 'CN': 'tech', 'tech': 'tech', 'Technology': 'tech'
    }

    display_name_map = {
        'math': 'Toán học', 'lit': 'Ngữ văn', 'eng': 'Tiếng Anh',
        'phy': 'Vật lý', 'chem': 'Hóa học', 'bio': 'Sinh học',
        'inf': 'Tin học', 'hist': 'Lịch sử', 'geo': 'Địa lý',
        'civic': 'GDCD/KTPL', 'tech': 'Công nghệ'
    }
    
    prefix = subject_map.get(user.subject)
    
    if not prefix:
        flash(f"Lỗi: Tài khoản của bạn (môn '{user.subject}') chưa được cấu hình để nhập điểm.", "error")
        return redirect(url_for('gv.dashboard'))

    subj_name = display_name_map.get(prefix, user.subject)
    students = Student.query.filter_by(class_id=class_id).order_by(Student.mshs).all()

    if request.method == 'POST':
        count_updated = 0
        for s in students:
            if not s.grade:
                s.grade = Grade(student_id=s.id)
                db.session.add(s.grade)
            
            score_cols = ['tx1', 'tx2', 'tx3', 'tx4', 'gk', 'ck']
            
            for col in score_cols:
                input_name = f"{col}_{s.id}"
                raw_val = request.form.get(input_name)
                
                db_field = f"{prefix}_{col}"
                
                if raw_val and raw_val.strip() != '':
                    try:
                        val = float(raw_val)
                        if 0 <= val <= 10:
                            setattr(s.grade, db_field, val)
                    except ValueError:
                        continue
                else:
                    setattr(s.grade, db_field, None)
            try:
                tx_values = []
                for i in range(1, 5):
                    val = getattr(s.grade, f"{prefix}_tx{i}")
                    if val is not None: tx_values.append(val)
                
                gk_val = getattr(s.grade, f"{prefix}_gk")
                ck_val = getattr(s.grade, f"{prefix}_ck")
                
                total_point = sum(tx_values)
                total_coeff = len(tx_values)
                
                if gk_val is not None:
                    total_point += gk_val * 2
                    total_coeff += 2
                    
                if ck_val is not None:
                    total_point += ck_val * 3
                    total_coeff += 3
                
                avg_field = f"{prefix}_avg"
                if total_coeff > 0:
                    avg_val = round(total_point / total_coeff, 1)
                    setattr(s.grade, avg_field, avg_val)
                else:
                    setattr(s.grade, avg_field, None)
                    
                count_updated += 1
                
            except Exception as e:
                print(f"Error calculating avg for student {s.id}: {e}")

        db.session.commit()
        flash(f"Đã lưu điểm thành công cho {count_updated} học sinh!", "success")
        return redirect(url_for('gv.grading', class_id=class_id))

    def get_score(grade_obj, col):
        if not grade_obj: return ''
        val = getattr(grade_obj, f"{prefix}_{col}", None)
        return val if val is not None else ''

    return render_template('gv/grading.html', 
                           classroom=classroom, 
                           students=students, 
                           subject=subj_name, 
                           get_score=get_score)