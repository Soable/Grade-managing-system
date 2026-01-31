from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

teachers_classrooms = db.Table('teachers_classrooms',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('classroom_id', db.Integer, db.ForeignKey('classroom.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False) 
    full_name = db.Column(db.String(100), nullable=True)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(20), nullable=True)

    student_profile = db.relationship('Student', backref='user_account', uselist=False)
    teaching_classes = db.relationship('Classroom', secondary=teachers_classrooms, backref='teachers')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Classroom(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(50), nullable=False)
    class_code = db.Column(db.String(4), unique=True, nullable=False)
    gv_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    
    students = db.relationship('Student', backref='classroom', lazy=True)
    teacher = db.relationship('User', foreign_keys=[gv_id], backref='homeroom_classes')

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

    math_tx1 = db.Column(db.Float, default=None)
    math_tx2 = db.Column(db.Float, default=None)
    math_tx3 = db.Column(db.Float, default=None)
    math_tx4 = db.Column(db.Float, default=None)
    math_gk  = db.Column(db.Float, default=None)
    math_ck  = db.Column(db.Float, default=None)
    math_avg = db.Column(db.Float, default=None)

    lit_tx1 = db.Column(db.Float, default=None)
    lit_tx2 = db.Column(db.Float, default=None)
    lit_tx3 = db.Column(db.Float, default=None)
    lit_tx4 = db.Column(db.Float, default=None)
    lit_gk  = db.Column(db.Float, default=None)
    lit_ck  = db.Column(db.Float, default=None)
    lit_avg = db.Column(db.Float, default=None)

    eng_tx1 = db.Column(db.Float, default=None)
    eng_tx2 = db.Column(db.Float, default=None)
    eng_tx3 = db.Column(db.Float, default=None)
    eng_tx4 = db.Column(db.Float, default=None)
    eng_gk  = db.Column(db.Float, default=None)
    eng_ck  = db.Column(db.Float, default=None)
    eng_avg = db.Column(db.Float, default=None)

    phy_tx1 = db.Column(db.Float, default=None)
    phy_tx2 = db.Column(db.Float, default=None)
    phy_tx3 = db.Column(db.Float, default=None)
    phy_tx4 = db.Column(db.Float, default=None)
    phy_gk  = db.Column(db.Float, default=None)
    phy_ck  = db.Column(db.Float, default=None)
    phy_avg = db.Column(db.Float, default=None)

    chem_tx1 = db.Column(db.Float, default=None)
    chem_tx2 = db.Column(db.Float, default=None)
    chem_tx3 = db.Column(db.Float, default=None)
    chem_tx4 = db.Column(db.Float, default=None)
    chem_gk  = db.Column(db.Float, default=None)
    chem_ck  = db.Column(db.Float, default=None)
    chem_avg = db.Column(db.Float, default=None)

    bio_tx1 = db.Column(db.Float, default=None)
    bio_tx2 = db.Column(db.Float, default=None)
    bio_tx3 = db.Column(db.Float, default=None)
    bio_tx4 = db.Column(db.Float, default=None)
    bio_gk  = db.Column(db.Float, default=None)
    bio_ck  = db.Column(db.Float, default=None)
    bio_avg = db.Column(db.Float, default=None)

    inf_tx1 = db.Column(db.Float, default=None)
    inf_tx2 = db.Column(db.Float, default=None)
    inf_tx3 = db.Column(db.Float, default=None)
    inf_tx4 = db.Column(db.Float, default=None)
    inf_gk  = db.Column(db.Float, default=None)
    inf_ck  = db.Column(db.Float, default=None)
    inf_avg = db.Column(db.Float, default=None)

    hist_tx1 = db.Column(db.Float, default=None)
    hist_tx2 = db.Column(db.Float, default=None)
    hist_tx3 = db.Column(db.Float, default=None)
    hist_tx4 = db.Column(db.Float, default=None)
    hist_gk  = db.Column(db.Float, default=None)
    hist_ck  = db.Column(db.Float, default=None)
    hist_avg = db.Column(db.Float, default=None)

    geo_tx1 = db.Column(db.Float, default=None)
    geo_tx2 = db.Column(db.Float, default=None)
    geo_tx3 = db.Column(db.Float, default=None)
    geo_tx4 = db.Column(db.Float, default=None)
    geo_gk  = db.Column(db.Float, default=None)
    geo_ck  = db.Column(db.Float, default=None)
    geo_avg = db.Column(db.Float, default=None)

    civic_tx1 = db.Column(db.Float, default=None)
    civic_tx2 = db.Column(db.Float, default=None)
    civic_tx3 = db.Column(db.Float, default=None)
    civic_tx4 = db.Column(db.Float, default=None)
    civic_gk  = db.Column(db.Float, default=None)
    civic_ck  = db.Column(db.Float, default=None)
    civic_avg = db.Column(db.Float, default=None)

    tech_tx1 = db.Column(db.Float, default=None)
    tech_tx2 = db.Column(db.Float, default=None)
    tech_tx3 = db.Column(db.Float, default=None)
    tech_tx4 = db.Column(db.Float, default=None)
    tech_gk  = db.Column(db.Float, default=None)
    tech_ck  = db.Column(db.Float, default=None)
    tech_avg = db.Column(db.Float, default=None)

    @property
    def gpa(self):
        subjects = [
            self.math_avg, self.lit_avg, self.eng_avg, 
            self.phy_avg, self.chem_avg, self.bio_avg,
            self.hist_avg, self.geo_avg, self.civic_avg,
            self.inf_avg, self.tech_avg
        ]
        
        valid_scores = [s for s in subjects if s is not None]

        if not valid_scores:
            return "Chưa có"
            
        avg = sum(valid_scores) / len(valid_scores)
        return round(avg, 1)