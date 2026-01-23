from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False) # 'student', 'gvcn', 'gvbm'

class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_code = db.Column(db.String(4), unique=True, nullable=False)
    gvcn_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classroom.id'))

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    math = db.Column(db.Float, default=0.0)
    literature = db.Column(db.Float, default=0.0)
    english = db.Column(db.Float, default=0.0)