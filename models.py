from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash #for hashing passwords

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False) 
    password_hash = db.Column(db.String(200), nullable=False) #hashing password
    role = db.Column(db.String(20), nullable=False)
    
    student_profile = db.relationship('Student', backref='user_account', uselist=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Classroom(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(50), nullable=False)
    class_code = db.Column(db.String(4), unique=True, nullable=False) #each class has 1 4-digit code
    gvcn_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    students = db.relationship('Student', backref='classroom', lazy=True)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mshs = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True) 
    class_id = db.Column(db.Integer, db.ForeignKey('classroom.id'))
    grade = db.relationship('Grade', backref='student', uselist=False)

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    math = db.Column(db.Float, default=None)
    literature = db.Column(db.Float, default=None)
    english = db.Column(db.Float, default=None)