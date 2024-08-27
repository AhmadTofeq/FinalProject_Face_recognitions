from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, current_app, Response
from sqlalchemy.orm import joinedload
from sqlalchemy import text  # Add this import
from app import db
import json
from app.models import Faculty, Department, Staff, User
from werkzeug.security import generate_password_hash, check_password_hash
import os
from werkzeug.utils import secure_filename
from back_end_process.Pyhton_files.video_processing import StaffProcessor
from back_end_process.Pyhton_files.main import second_test_camera
import logging
from datetime import datetime, timedelta
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

    # Call the stored procedure to deactivate the staff member
    result = db.session.execute(
        text("CALL sp_delete_staff(:staffId)"),
        {'staffId': staff_id}
    )
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
    add_by_user_id = session['user_id']

    try:
        # Call the stored procedure to add a new staff member
        db.session.execute(
            text("CALL sp_add_staff(:staffName, :phone, :email, :gender, :departmentId, :addedByUserId, @newStaffId)"),
            {
                'staffName': staff_name,
                'phone': phone,
                'email': email,
                'gender': gender,
                'departmentId': id_department,
                'addedByUserId': add_by_user_id
            }
        )

        # Commit the transaction to save the new staff member
        db.session.commit()

        # Fetch the new staff ID
        new_staff_id = db.session.execute(text("SELECT @newStaffId")).scalar()

        if new_staff_id is None:
            raise ValueError("Failed to retrieve the new staff ID.")

        # Process the video if provided
        if 'video' in request.files and request.files['video'].filename != '':
            video = request.files['video']
            video_path = f"app/videos/{new_staff_id}.mp4"
            video.save(video_path)

            # Process the video to extract images
            StaffProcessor().insert_staff(video_path, staff_name, new_staff_id)  
            if os.path.exists(video_path): 
                os.remove(video_path)

        session['message'] = 'Staff added successfully.'
        session['message_type'] = 'success'
    
    except Exception as e:
        logging.error(f"Error adding staff: {str(e)}")
        db.session.rollback()  # Roll back the transaction on error
        session['message'] = f'Error adding staff: {str(e)}'
        session['message_type'] = 'error'

    return redirect(url_for('main.staff'))

@bp.route('/update_staff', methods=['POST'])
def update_staff():
    try:
        # Ensure the user is an admin
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

        # Update staff member using stored procedure
        db.session.execute(
            text("CALL sp_update_staff(:staffId, :staffName, :phone, :email, :gender, :departmentId)"),
            {
                'staffId': staff_id,
                'staffName': request.form['name'],
                'phone': request.form['phone'],
                'email': request.form['email'],
                'gender': request.form['gender'],
                'departmentId': request.form['department_id']
            }
        )
        db.session.commit()

        # Check if video processing is needed
        if (current_name != request.form['name'] or 
            current_email != request.form['email'] or 
            'video' in request.files and request.files['video'].filename != ''):
            
            if 'video' in request.files and request.files['video'].filename != '':
                video = request.files['video']
                video_path = f"app/videos/{staff_id}.mp4"
                video.save(video_path)
            else:
                video_path = ""

            # Process the video to extract images
            StaffProcessor().updated_staff(video_path, request.form['name'], staff_id)
            if os.path.exists(video_path): 
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

#registration presentation part
@bp.route('/presentation')
def presentation():
    staff_members = Staff.query.filter_by(state=True).all()
    faculties = Faculty.query.all()
    departments = Department.query.all()

    # Execute the query to fetch all presentations
    result = db.session.execute(text("SELECT * FROM get_all_presentations"))
    presentations = result.fetchall()

    presentations = [
        {
            **dict(zip(result.keys(), presentation)),
            'presenters': presentation.presenters,  # Use the presenters directly from the view
            'faculty_id': presentation.faculty_id,
            'department_id': presentation.department_id
        }
        for presentation in presentations
    ]

    message = session.pop('message', None)
    message_type = session.pop('message_type', None)

    return render_template('presentation.html', presentations=presentations, faculties=faculties, departments=departments, staff_members=staff_members, message=message, message_type=message_type)



@bp.route('/register_presentation', methods=['POST'])
def register_presentation():
    list_ides=[int(i) for i in request.form.getlist('presenter[]')]
    try:
        db.session.execute(
            text('''CALL add_presntaion(
                 :title1,
                 :date_time1,
                 :duration1,
                 :hall1,
                 :point_presenter1,
                 :point_attendance1,
                 :max_late1,
                 :id_dep1,
                 :init_by1,
                 :staff_ids)'''),
            {
                "title1": request.form.get('title_pres'),
                "date_time1": request.form.get('date_time'),
                "duration1": request.form.get('duration'),
                "hall1": request.form.get('hall'),
                "point_presenter1": request.form.get('point_presenter'),
                "point_attendance1": request.form.get('point_attendance'),
                "max_late1": request.form.get('max_late'),
                "id_dep1": request.form.get('department'),
                "init_by1": session['user_id'],
                "staff_ids": json.dumps(list_ides)
            }
        )
        db.session.commit()
        session['message'] = 'Presentation registered successfully.'
        session['message_type'] = 'success'
    except Exception as e:
        db.session.rollback()  # Roll back the transaction in case of an error
        session['message'] = 'Presentation registered NOT successfull.'
        session['message_type'] = 'NOT success'
    return redirect(url_for('main.presentation'))


@bp.route('/update_presentation', methods=['POST'])
def update_presentation():
    id_presentation = request.form.get('id_presentation')
    try:
        db.session.execute(
            text('''CALL Update_presentation(
                 :title1,
                 :date_time1,
                 :duration1,
                 :hall1,
                 :point_presenter1,
                 :point_attendance1,
                 :max_late1,
                 :id_dep1,
                 :id_presentation1
                 )'''),
            {
                "title1": request.form.get('title_pres'),
                "date_time1": request.form.get('date_time'),
                "duration1": request.form.get('duration'),
                "hall1": request.form.get('hall'),
                "point_presenter1": request.form.get('point_presenter'),
                "point_attendance1": request.form.get('point_attendance'),
                "max_late1": request.form.get('max_late'),
                "id_dep1": request.form.get('department'),
                "id_presentation1": id_presentation 
            }
        )
        db.session.commit()
        session['message'] = 'Presentation updated successfully.'
        session['message_type'] = 'success'
    except Exception as e:
        db.session.rollback()
        session['message'] = 'Presentation update NOT successful.'
        session['message_type'] = 'error'
        print(f"Error updating presentation: {e}")  
    return redirect(url_for('main.presentation'))  

@bp.route('/delete_presentation', methods=['POST'])
def delete_presentation():
    id_presentation = request.form.get('id_presentation')  

    if not id_presentation:
        session['message'] = 'Presentation ID is missing.'
        session['message_type'] = 'error'
        return redirect(url_for('main.presentation')) 

    try:
        db.session.execute(
            text('''CALL delet_presntaion(
                     :id
                     )'''),
            {"id": id_presentation}  # Pass the presentation ID to the stored procedure
        )
        db.session.commit()
        session['message'] = 'Presentation deleted successfully.'
        session['message_type'] = 'success'
    except Exception as e:
        db.session.rollback()  
        session['message'] = 'Presentation deletion NOT successful.'
        session['message_type'] = 'error'
        print(f"Error deleting presentation: {e}")  # Log the error for debugging

    return redirect(url_for('main.presentation'))  

@bp.route('/second_test_camera')
def show_second_test_camera_page():
    return render_template('second_test_camera.html')

@bp.route('/second_test_camera_feed')
def second_test_camera_feed():
    return second_test_camera()

#confrance page part
@bp.route('/conferences', methods=['GET', 'POST'])
def conferences():
    search_query = request.form.get('search_query', '')  
    not_passed = request.form.get('not_passed', 'off') == 'on' 

    # Execute the stored procedure with the search query and checkbox state
    result = db.session.execute(
        text("CALL SearchConferences(:search_query, :not_passed)"),
        {"search_query": search_query, "not_passed": not_passed}
    )
    presentations = result.fetchall()

    presentations_with_names = []
    for presentation in presentations:
        faculty = Faculty.query.get(presentation.faculty_id)
        department = Department.query.get(presentation.department_id)
        
        presentation_dict = {
            'id_presentation': presentation.id_presentation,
            'title_pres': presentation.title_pres,
            'date_time': presentation.date_time,
            'presenters': presentation.presenters,
            'duration': presentation.duration,
            'hall': presentation.hall,
            'point_presenter': presentation.point_presenter,
            'point_attendance': presentation.point_attendance,
            'max_late': presentation.max_late,
            'department_id': presentation.department_id,
            'faculty_id': presentation.faculty_id,
            'added_by': presentation.added_by,
            'faculty_name': faculty.name_faculty if faculty else 'N/A',
            'department_name': department.name_department if department else 'N/A'
        }
        
        presentations_with_names.append(presentation_dict)

    # Retrieve and clear message from session
    message = session.pop('message', None)
    message_type = session.pop('message_type', None)

    return render_template('conferences.html', presentations=presentations_with_names, 
                           search_query=search_query, not_passed=not_passed, 
                           message=message, message_type=message_type)


@bp.route('/start_conference/<int:id_presentation>', methods=['GET'])
def start_conference(id_presentation):
    # Fetch the presentation details
    presentation = db.session.execute(
        text("SELECT * FROM presentations WHERE id_presentation = :id_presentation"),
        {"id_presentation": id_presentation}
    ).fetchone()

    if presentation is None:
        session['message'] = 'Conference not found.'
        session['message_type'] = 'error'
        return redirect(url_for('main.conferences'))

    # Check if presentation.date_time is already a datetime object
    if isinstance(presentation.date_time, datetime):
        presentation_datetime = presentation.date_time
    else:
        # Convert the date_time string to a datetime object if it's not already one
        presentation_datetime = datetime.strptime(presentation.date_time, '%Y-%m-%d %H:%M:%S')

    # Check if more than 1 day has passed
    if datetime.now() > presentation_datetime + timedelta(days=1):
        session['message'] = 'Sorry, this conference has expired.'
        session['message_type'] = 'error'
        return redirect(url_for('main.conferences'))

    # If the conference has not expired, redirect to the conference settings page
    return redirect(url_for('main.conferences_sitting', id_presentation=id_presentation))

@bp.route('/conferences_sitting/<int:id_presentation>')
def conferences_sitting(id_presentation):
    # Fetch the presentation details from the custom view
    presentation = db.session.execute(
        text("SELECT * FROM get_all_presentations WHERE id_presentation = :id_presentation"),
        {"id_presentation": id_presentation}
    ).fetchone()

    if presentation is None:
        session['message'] = 'Conference not found.'
        session['message_type'] = 'error'
        return redirect(url_for('main.conferences'))

    # Pass the presentation details to the template
    return render_template('conferences_sitting.html', presentation=presentation, current_time=datetime.now())
