from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, current_app
from sqlalchemy.orm import joinedload
from sqlalchemy import text  # Add this import
from app import db
from app.models import Faculty, Department, Staff, User
from werkzeug.security import generate_password_hash, check_password_hash
import os
from werkzeug.utils import secure_filename
from back_end_process.Pyhton_files.video_processing import StaffProcessor
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

@bp.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

@bp.route('/about_us')
def about_us():
    return render_template('about_us.html')

@bp.route('/home')
def home():
    return render_template('home.html')

@bp.route('/conferences')
def conferences():
    return render_template('conferences.html')

@bp.route('/r-conferences')
def r_conferences():
    return render_template('r-conferences.html')

@bp.route('/users')
def users():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('main.index'))

    # Call the stored procedure using text()
    result = db.session.execute(text("CALL GetActiveUsers()"))
    users = result.fetchall()
    
    message = session.pop('message', None)
    message_type = session.pop('message_type', None)
    return render_template('users.html', users=users, message=message, message_type=message_type)

@bp.route('/update_user', methods=['POST'])
def update_user():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('main.index'))
    
    user_id = request.form['id']
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']
    
    # Hash the password if provided
    hashed_password = generate_password_hash(password) if password else None

    # Call the stored procedure using text()
    if hashed_password:
        db.session.execute(
            text("CALL UpdateUser(:id, :name, :username, :password, :role)"),
            {'id': user_id, 'name': name, 'username': username, 'password': hashed_password, 'role': role}
        )
    else:
        db.session.execute(
            text("CALL UpdateUser(:id, :name, :username, NULL, :role)"),
            {'id': user_id, 'name': name, 'username': username, 'role': role}
        )

    db.session.commit()

    session['message'] = 'User updated successfully.'
    session['message_type'] = 'success'
    
    return redirect(url_for('main.users'))

@bp.route('/delete_user', methods=['POST'])
def delete_user():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('main.index'))

    user_id = request.form['id']

    # Call the stored procedure to delete the user
    result = db.session.execute(
        text("CALL DeleteUser(:id)"),
        {'id': user_id}
    )

    # Check the result to ensure the user was deleted
    if result.rowcount > 0:
        session['message'] = 'User deleted successfully.'
        session['message_type'] = 'success'
    else:
        session['message'] = 'User not found.'
        session['message_type'] = 'error'
    
    db.session.commit()

    return redirect(url_for('main.users'))

@bp.route('/register_user', methods=['POST'])
def register_user():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('main.index'))

    name = request.form['name']
    username = request.form['username']
    password = generate_password_hash(request.form['password'])
    role = request.form['role']

    # Call the stored procedure to register the user
    db.session.execute(
        text("CALL RegisterUser(:name, :username, :password, :role)"),
        {'name': name, 'username': username, 'password': password, 'role': role}
    )
    db.session.commit()

    session['message'] = 'User registered successfully.'
    session['message_type'] = 'success'
    
    return redirect(url_for('main.users'))

#Staff part
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

    faculties = Faculty.query.all()
    departments = Department.query.all()
    message = session.pop('message', None)
    message_type = session.pop('message_type', None)
    return render_template('staff.html', staff_members=staff_members, faculties=faculties, departments=departments, message=message, message_type=message_type)


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

    # Deactivate the staff member
    staff.state = False
    db.session.commit()

    # Delete images and labels
    StaffProcessor().delete_images_and_labels(staff_id)

    session['message'] = 'Staff deactivated successfully and all related data deleted.'
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
        video_path = f"app/videos/{new_staff.id_staff}.mp4"
        video.save(video_path)
        # Process the video to extract images
        StaffProcessor().insert_staff(video_path, new_staff.staff_name, new_staff.id_staff)  
        if os.path. exists(video_path): 
            os.remove(video_path)

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

        # Retrieve current values
        current_name = staff.staff_name
        current_email = staff.email

        # Update values
        staff.staff_name = request.form['name']
        staff.phone = request.form['phone']
        staff.email = request.form['email']
        staff.gender = request.form['gender']
        staff.id_department = request.form['department_id']

        db.session.commit()

        # Check if we need to call process_video
        if (current_name != staff.staff_name or 
            current_email != staff.email or 
            'video' in request.files and request.files['video'].filename != ''):
            
            if 'video' in request.files and request.files['video'].filename != '':
                video = request.files['video']
                video_path = f"app/videos/{staff.id_staff}.mp4"
                video.save(video_path)
            else:
                video_path = ""

            # Process the video to extract images
            StaffProcessor().updated_staff(video_path, staff.staff_name, staff.id_staff)
            if os.path. exists(video_path): 
                os.remove(video_path)

        session['message'] = 'Staff updated successfully.'
        session['message_type'] = 'success'
        
        return redirect(url_for('main.staff'))

    except Exception as e:
        logging.error(f"Error updating staff: {str(e)}")
        session['message'] = f'Error updating staff: {str(e)}'
        session['message_type'] = 'error'
        return redirect(url_for('main.staff'))

#model train part
import subprocess
from back_end_process.Pyhton_files.class_.model_training import model_trainning
model_trainning_instance = model_trainning()

# Model train part
@bp.route('/model-train')
def model_train():
    message = session.pop('message', None)
    message_type = session.pop('message_type', None)
    
    # Query to get all staff members whose state is True
    staff_members = Staff.query.filter_by(state=True).all()
    
    return render_template('model_train.html', message=message, message_type=message_type, staff_members=staff_members)


@bp.route('/model-feature-extraction', methods=['POST'])
def model_feature_extraction():
    try:
        # Use the logic for feature extraction
        if model_trainning_instance.model_trainin_Face_net():
            session['message'] = 'Model feature extraction completed successfully.'
            session['message_type'] = 'success'
        else:
            raise Exception('Failed to extract model features.')
    except Exception as e:
        session['message'] = f'Error: {str(e)}'
        session['message_type'] = 'error'

    return redirect(url_for('main.model_train'))

@bp.route('/model-classification', methods=['POST'])
def model_classification():
    try:
        # Use the logic for model classification
        if model_trainning_instance.model_classification():
            session['message'] = 'Model classification completed successfully.'
            session['message_type'] = 'success'
    except Exception as e:
        session['message'] = f'Error: {str(e)}'
        session['message_type'] = 'error'

    return redirect(url_for('main.model_train'))

@bp.route('/delete-model-data', methods=['POST'])
def delete_model_data():
    try:
        # Use the logic for deleting model data
        if model_trainning_instance.clean_Facce_net_model():
            session['message'] = 'Model data deleted successfully.'
            session['message_type'] = 'success'
        else:
            raise Exception('Failed to delete model data.')
    except Exception as e:
        session['message'] = f'Error: {str(e)}'
        session['message_type'] = 'error'

    return redirect(url_for('main.model_train'))

#for the box inside the model page
@bp.route('/handle_button_click', methods=['POST'])
def handle_button_click():
    staff_id = request.form.get('staff_id')
    staff_name = request.form.get('staff_name')

    # Get the directory path for the staff ID
    directory_path = model_trainning_instance.get_directory_images_by_id(staff_id)

    if directory_path != "Null":
        # Open Windows Explorer to the directory path
        try:
            subprocess.Popen(f'explorer "{directory_path}"')
            session['message'] = f'Opened directory for {staff_name}'
            session['message_type'] = 'success'
        except Exception as e:
            session['message'] = f'Error opening directory: {str(e)}'
            session['message_type'] = 'error'
    else:
        session['message'] = f'No directory found for {staff_name}'
        session['message_type'] = 'error'

    return redirect(url_for('main.model_train'))

#test camera part
@bp.route('/test-camera')
def test_camera():
    return render_template('test_camera.html')