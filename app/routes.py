from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify ,current_app
from sqlalchemy.orm import joinedload
from app import db
from app.models import Faculty, Department, Staff, User
from werkzeug.security import generate_password_hash, check_password_hash
import os
from werkzeug.utils import secure_filename
from app.video_processing import process_video
import logging

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
            session['user_id'] = user.id  # Store user id in session
            response = {'success': True, 'message': 'Login successful.', 'redirect': url_for('main.staff')}
        else:
            response = {'success': False, 'message': 'Invalid username or password.'}
    else:
        response = {'success': False, 'message': 'Invalid username or password.'}

    return jsonify(response)

@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logout successful'})

@bp.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

@bp.route('/about_us')
def about_us():
    return render_template('about_us.html')


@bp.route('/check-session', methods=['GET'])
def check_session():
    authenticated = 'username' in session
    return jsonify({'authenticated': authenticated})


@bp.route('/get_user_info', methods=['GET'])
def get_user_info():
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        if user:
            return jsonify({'username': user.name})
    return jsonify({'username': None})

@bp.route('/home')
def home():
    return render_template('home.html')

@bp.route('/conferences')
def conferences():
    return render_template('conferences.html')

@bp.route('/r-conferences')
def r_conferences():
    return render_template('r-conferences.html')

@bp.route('/test-camera')
def test_camera():
    return render_template('test-camera.html')

@bp.route('/model-train')
def model_train():
    return render_template('model-train.html')

#users part
@bp.route('/users')
def users():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('main.index'))

    users = User.query.filter_by(state=True).all()
    message = session.pop('message', None)
    message_type = session.pop('message_type', None)
    return render_template('users.html', users=users, message=message, message_type=message_type)

@bp.route('/update_user', methods=['POST'])
def update_user():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('main.index'))
    user_id = request.form['id']
    user = User.query.get(user_id)
    
    user.name = request.form['name']
    user.username = request.form['username']
    password = request.form['password']
    if password:
        user.password = generate_password_hash(password)
    user.role = request.form['role']

    db.session.commit()
    session['message'] = 'User updated successfully.'
    session['message_type'] = 'success'
    
    return redirect(url_for('main.users'))

@bp.route('/delete_user', methods=['POST'])
def delete_user():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('main.index'))

    user_id = request.form['id']
    user = User.query.get(user_id)
    
    if user:
        user.state = False
        db.session.commit()
        session['message'] = 'User deleted successfully.'
        session['message_type'] = 'success'
    else:
        session['message'] = 'User not found.'
        session['message_type'] = 'error'
    
    return redirect(url_for('main.users'))

@bp.route('/register_user', methods=['POST'])
def register_user():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('main.index'))
    name = request.form['name']
    username = request.form['username']
    password = generate_password_hash(request.form['password'])
    role = request.form['role']

    new_user = User(name=name, username=username, password=password, role=role)
    db.session.add(new_user)
    db.session.commit()

    session['message'] = 'User registered successfully.'
    session['message_type'] = 'success'
    
    return redirect(url_for('main.users'))

@bp.route('/staff')
def staff():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('main.index'))

    search_query = request.args.get('search')
    if search_query:
        staff_members = Staff.query.filter(
            Staff.state == True,
            (Staff.staff_name.ilike(f'%{search_query}%')) |
            (Staff.email.ilike(f'%{search_query}%'))
        ).all()
    else:
        staff_members = Staff.query.filter_by(state=True).all()

    departments = Department.query.all()
    message = session.pop('message', None)
    message_type = session.pop('message_type', None)
    return render_template('staff.html', staff_members=staff_members, departments=departments, message=message, message_type=message_type)

@bp.route('/delete_staff', methods=['POST'])
def delete_staff():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('main.index'))

    staff_id = request.form['id_staff']
    staff = Staff.query.get(staff_id)

    if not staff:
        session['message'] = 'Staff not found.'
        session['message_type'] = 'error'
        return redirect(url_for('main.staff'))

    staff.state = False
    db.session.commit()

    session['message'] = 'Staff deactivated successfully.'
    session['message_type'] = 'success'
    return redirect(url_for('main.staff'))

@bp.route('/add_staff', methods=['POST'])
def add_staff():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('main.index'))

    staff_name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    gender = request.form['gender']
    id_department = request.form['department_id']
    
    # Assuming the currently logged-in user's ID is stored in the session
    add_by_user_id = session['user_id']
    
    new_staff = Staff(
        staff_name=staff_name,
        phone=phone,
        email=email,
        gender=gender,
        id_department=id_department,
        add_by_user_id=add_by_user_id,
        state=True
    )
    
    db.session.add(new_staff)
    db.session.commit()

    if 'video' in request.files:
        video = request.files['video']
        # Process the video to extract images
        process_video(video, email)
    
    session['message'] = 'Staff added successfully.'
    session['message_type'] = 'success'
    
    return redirect(url_for('main.staff'))

@bp.route('/update_staff', methods=['POST'])
def update_staff():
    try:
        if 'role' not in session or session['role'] != 'admin':
            return redirect(url_for('main.index'))

        logging.debug(f"Form data: {request.form}")
        logging.debug(f"Files: {request.files}")

        staff_id = request.form['id_staff']
        staff = Staff.query.get(staff_id)
        
        if not staff:
            session['message'] = 'Staff not found.'
            session['message_type'] = 'error'
            return redirect(url_for('main.staff'))

        staff.staff_name = request.form['name']
        staff.phone = request.form['phone']
        staff.email = request.form['email']
        staff.gender = request.form['gender']
        staff.id_department = request.form['department_id']
        
        db.session.commit()

        if 'video' in request.files:
            video = request.files['video']
            # Process the video to extract images
            process_video(video, staff.email)
        
        session['message'] = 'Staff updated successfully.'
        session['message_type'] = 'success'
        
        return redirect(url_for('main.staff'))

    except Exception as e:
        logging.error(f"Error updating staff: {str(e)}")
        session['message'] = f'Error updating staff: {str(e)}'
        session['message_type'] = 'error'
        return redirect(url_for('main.staff'))
