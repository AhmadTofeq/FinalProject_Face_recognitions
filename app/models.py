from app import db

class Faculty(db.Model):
    __tablename__ = 'faculty'
    id_faculty = db.Column(db.Integer, primary_key=True)
    name_faculty = db.Column(db.String(255), nullable=False)

class Department(db.Model):
    __tablename__ = 'department'
    id_department = db.Column(db.Integer, primary_key=True)
    name_department = db.Column(db.String(255), nullable=False)
    id_faculty = db.Column(db.Integer, db.ForeignKey('faculty.id_faculty'))

class Staff(db.Model):
    __tablename__ = 'staff'
    id_staff = db.Column(db.Integer, primary_key=True)
    staff_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(255))
    gender = db.Column(db.Enum('Male', 'Female', 'Other'), nullable=False)
    id_department = db.Column(db.Integer, db.ForeignKey('department.id_department'))
    add_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    state = db.Column(db.Boolean, default=True, nullable=False)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'user'), default='user', nullable=False)
    state = db.Column(db.Boolean, default=True, nullable=False)
