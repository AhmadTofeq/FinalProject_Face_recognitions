from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Faculty(db.Model):
    __tablename__ = 'faculty'
    id_faculty = db.Column(db.Integer, primary_key=True)
    name_faculty = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Faculty {self.name_faculty}>'

class Department(db.Model):
    __tablename__ = 'department'
    id_department = db.Column(db.Integer, primary_key=True)
    name_department = db.Column(db.String(255), nullable=False)
    id_faculty = db.Column(db.Integer, db.ForeignKey('faculty.id_faculty'))

    # Define the relationship to Staff
    staff_members = db.relationship('Staff', back_populates='department')

    def __repr__(self):
        return f'<Department {self.name_department}>'

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

    # Define the relationships
    department = db.relationship('Department', back_populates='staff_members')
    added_by_user = db.relationship('User')

    def __repr__(self):
        return f'<Staff {self.staff_name}>'

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'user'), default='user', nullable=False)
    state = db.Column(db.Boolean, default=True, nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'
