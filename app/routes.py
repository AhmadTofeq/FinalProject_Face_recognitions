from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app import db
from app.models import Faculty, Department, Staff, User
from werkzeug.security import check_password_hash

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    error = session.pop('error', None)
    return render_template('index.html', error=error)

@bp.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    if user:
        if user.state == 0:
            response = {'success': False, 'message': 'Your account is inactive.'}
        elif check_password_hash(user.password, password):
            session['username'] = user.username
            session['role'] = user.role
            response = {'success': True, 'message': 'Login successful.', 'redirect': url_for('main.staff')}
        else:
            response = {'success': False, 'message': 'Invalid password.'}
    else:
        response = {'success': False, 'message': 'Username not found.'}

    return jsonify(response)

@bp.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

@bp.route('/about_us')
def about_us():
    return render_template('about_us.html')


@bp.route('/staff', methods=['GET'])
def staff():
    departments = Department.query.all()
    staff_members = Staff.query.filter_by(state=True).all()
    return render_template('staff.html', departments=departments, staff_members=staff_members)

@bp.route('/add_staff', methods=['POST'])
def add_staff():
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    gender = request.form.get('gender')
    department_id = request.form.get('department_id')
    add_by_user_id = request.form.get('add_by_user_id')  # Assuming the current user ID is available

    new_staff = Staff(
        staff_name=name,
        phone=phone,
        email=email,
        gender=gender,
        id_department=department_id,
        add_by_user_id=add_by_user_id
    )
    db.session.add(new_staff)
    db.session.commit()
    flash('Staff member added successfully', 'success')
    return redirect(url_for('main.staff'))

@bp.route('/update_staff/<int:id>', methods=['POST'])
def update_staff(id):
    staff = Staff.query.get_or_404(id)
    staff.staff_name = request.form.get('name')
    staff.phone = request.form.get('phone')
    staff.email = request.form.get('email')
    staff.gender = request.form.get('gender')
    staff.id_department = request.form.get('department_id')
    db.session.commit()
    flash('Staff member updated successfully', 'success')
    return redirect(url_for('main.staff'))

@bp.route('/delete_staff/<int:id>', methods=['POST'])
def delete_staff(id):
    staff = Staff.query.get_or_404(id)
    staff.state = False
    db.session.commit()
    flash('Staff member deactivated successfully', 'success')
    return redirect(url_for('main.staff'))
