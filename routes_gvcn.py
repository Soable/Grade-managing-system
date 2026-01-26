from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from models import db, User, Student, Classroom, Grade
import random, string, csv, io

gvcn_bp = Blueprint('gvcn', __name__)

# 4-DIGIT CLASS CODE 
def generate_class_code():
    return ''.join(random.choices(string.digits, k=4))


@gvcn_bp.route('/gvcn/dashboard')
def dashboard():
    # logged in?
    if 'user_id' not in session or session.get('role') != 'gvcn':
        return redirect(url_for('login'))
    
    # get teacher's classes
    teacher_id = session['user_id']
    my_classes = Classroom.query.filter_by(gvcn_id=teacher_id).all()
    
    class_ids = [c.id for c in my_classes]
    if class_ids:
        all_students = Student.query.filter(Student.class_id.in_(class_ids)).all()
    else:
        all_students = []
    
    return render_template('gvcn/dashboard.html', classes=my_classes, all_students=all_students)

@gvcn_bp.route('/gvcn/create_class', methods=['POST'])
def create_class():
    if 'user_id' not in session or session.get('role') != 'gvcn':
        return redirect(url_for('login'))

    class_name = request.form.get('class_name')
    new_code = generate_class_code() # create class code

    # save to db
    new_class = Classroom(
        class_name=class_name,
        class_code=new_code,
        gvcn_id=session['user_id']
    )
    db.session.add(new_class)
    db.session.commit()

    return redirect(url_for('gvcn.class_detail', class_id=new_class.id))

@gvcn_bp.route('/gvcn/class/<int:class_id>', methods=['GET', 'POST'])
def class_detail(class_id):
    if 'user_id' not in session or session.get('role') != 'gvcn':
        return redirect(url_for('login'))

    current_class = Classroom.query.get_or_404(class_id)
    
    if request.method == 'POST':
        # csv add
        if 'upload_csv' in request.form:
            file = request.files.get('file')
            format_type = request.form.get('format_type') 
            #format: mshs - name || mshs - middle name - name

            if file and file.filename.endswith('.csv'):
                stream = io.TextIOWrapper(file.stream, encoding="utf-8")
                csv_reader = csv.reader(stream)
                
                next(csv_reader, None)
                
                for row in csv_reader:
                    if not row: continue 
                    h_mshs = row[0].strip()
                    
                    if h_mshs.lower() == 'mshs': continue

                    h_ten = ""

                    if format_type == '1':
                        if len(row) >= 2:
                            h_ten = row[1].strip()
                    elif format_type == '2':
                        if len(row) >= 3:
                            ho_lot = row[1].strip()
                            ten_that = row[2].strip()
                            h_ten = f"{ho_lot} {ten_that}" # Ghép lại
                    
                    if not h_ten: continue
                    existed_student = Student.query.filter_by(mshs=h_mshs).first()
                    
                    if not existed_student:
                        # new user
                        u = User(username=h_mshs, role='student')
                        
                        u.set_password('123456') 
                        
                        db.session.add(u)
                        db.session.flush()

                        # new student
                        s = Student(mshs=h_mshs, name=h_ten, user_id=u.id, class_id=current_class.id)
                        db.session.add(s)
                        db.session.flush()

                        g = Grade(student_id=s.id)
                        db.session.add(g)
                
                db.session.commit()
                flash("Đã nhập danh sách từ CSV thành công!")

        # manual add
        elif 'manual_add' in request.form:
            mshs = request.form.get('mshs')
            name = request.form.get('name')

            # check replication
            if Student.query.filter_by(mshs=mshs).first():
                flash(f"Lỗi: Mã số {mshs} đã tồn tại!")
            else:
                # new student ACCOUNT
                u = User(username=mshs, role='student')
                
                # set password
                u.set_password('123456')
                
                db.session.add(u)
                db.session.flush()

                # new student
                s = Student(mshs=mshs, name=name, user_id=u.id, class_id=current_class.id)
                db.session.add(s)
                db.session.flush()

                g = Grade(student_id=s.id)
                db.session.add(g)
                
                db.session.commit()
                flash("Đã thêm học sinh thành công!")

        return redirect(url_for('gvcn.class_detail', class_id=class_id))
    
    students = Student.query.filter_by(class_id=class_id).all()
    return render_template('gvcn/class_detail.html', classroom=current_class, students=students)


@gvcn_bp.route('/gvcn/change_password/<int:student_id>', methods=['GET', 'POST'])
def change_password(student_id):
    if 'user_id' not in session or session.get('role') != 'gvcn':
        return redirect(url_for('login'))

    student = Student.query.get_or_404(student_id)
    
    # check if the student is in the class
    teacher_id = session['user_id']
    classroom = Classroom.query.filter_by(gvcn_id=teacher_id, id=student.class_id).first()
    
    if not classroom:
        flash("Không có quyền truy cập!")
        return redirect(url_for('gvcn.dashboard'))
    
    if request.method == 'POST':
        if student.user:
            student.user.set_password('123456')
            db.session.commit()
            flash("Đã reset mật khẩu thành công!")
        else:
            flash("Lỗi: Học sinh chưa có user!")
            
        return redirect(url_for('gvcn.class_detail', class_id=student.class_id))
    
    return render_template('gvcn/change_password.html', student=student)