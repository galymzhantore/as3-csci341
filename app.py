"""
CSCI 341 Assignment 3 - Part 3
Caregivers Platform - Flask Web Application with CRUD Operations
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Import models from part 2
from caregivers_platform_part2 import (
    User, Caregiver, Member, Address, Job, JobApplication, Appointment, Base
)

# Database Configuration
# Use DB_URL if provided, otherwise construct from individual components
DATABASE_URL = os.getenv('DB_URL')
if not DATABASE_URL:
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'caregivers_platform')
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Setup database
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Create tables if they don't exist
Base.metadata.create_all(engine)

# ============================================
# HOME ROUTE
# ============================================

@app.route('/')
def index():
    """Home page with navigation to all CRUD operations"""
    return render_template('index.html')

# ============================================
# USER CRUD OPERATIONS
# ============================================

@app.route('/users')
def list_users():
    """List all users"""
    session = Session()
    try:
        users = session.query(User).all()
        return render_template('users/list.html', users=users)
    finally:
        session.close()

@app.route('/users/create', methods=['GET', 'POST'])
def create_user():
    """Create a new user"""
    if request.method == 'POST':
        session = Session()
        try:
            user = User(
                email=request.form['email'],
                given_name=request.form['given_name'],
                surname=request.form['surname'],
                city=request.form['city'],
                phone_number=request.form['phone_number'],
                profile_description=request.form.get('profile_description', ''),
                password=request.form['password']
            )
            session.add(user)
            session.commit()
            flash('User created successfully!', 'success')
            return redirect(url_for('list_users'))
        except Exception as e:
            session.rollback()
            flash(f'Error creating user: {str(e)}', 'error')
        finally:
            session.close()
    
    return render_template('users/create.html')

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    """Edit an existing user"""
    session = Session()
    try:
        user = session.get(User, user_id)
        if not user:
            flash('User not found!', 'error')
            return redirect(url_for('list_users'))
        
        if request.method == 'POST':
            user.email = request.form['email']
            user.given_name = request.form['given_name']
            user.surname = request.form['surname']
            user.city = request.form['city']
            user.phone_number = request.form['phone_number']
            user.profile_description = request.form.get('profile_description', '')
            
            session.commit()
            flash('User updated successfully!', 'success')
            return redirect(url_for('list_users'))
        
        return render_template('users/edit.html', user=user)
    finally:
        session.close()

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete a user"""
    session = Session()
    try:
        user = session.get(User, user_id)
        if user:
            session.delete(user)
            session.commit()
            flash('User deleted successfully!', 'success')
        else:
            flash('User not found!', 'error')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting user: {str(e)}', 'error')
    finally:
        session.close()
    
    return redirect(url_for('list_users'))

# ============================================
# CAREGIVER CRUD OPERATIONS
# ============================================

@app.route('/caregivers')
def list_caregivers():
    """List all caregivers"""
    session = Session()
    try:
        caregivers = session.query(Caregiver, User).join(
            User, User.user_id == Caregiver.caregiver_user_id
        ).all()
        return render_template('caregivers/list.html', caregivers=caregivers)
    finally:
        session.close()

@app.route('/caregivers/create', methods=['GET', 'POST'])
def create_caregiver():
    """Create a new caregiver"""
    session = Session()
    try:
        if request.method == 'POST':
            caregiver = Caregiver(
                caregiver_user_id=request.form['user_id'],
                photo=request.form.get('photo', ''),
                gender=request.form['gender'],
                caregiving_type=request.form['caregiving_type'],
                hourly_rate=request.form['hourly_rate']
            )
            session.add(caregiver)
            session.commit()
            flash('Caregiver created successfully!', 'success')
            return redirect(url_for('list_caregivers'))
        
        # Get users who are not yet caregivers
        users = session.query(User).outerjoin(Caregiver).filter(
            Caregiver.caregiver_user_id == None
        ).all()
        return render_template('caregivers/create.html', users=users)
    except Exception as e:
        session.rollback()
        flash(f'Error creating caregiver: {str(e)}', 'error')
        return redirect(url_for('list_caregivers'))
    finally:
        session.close()

@app.route('/caregivers/<int:caregiver_id>/edit', methods=['GET', 'POST'])
def edit_caregiver(caregiver_id):
    """Edit an existing caregiver"""
    session = Session()
    try:
        caregiver = session.get(Caregiver, caregiver_id)
        if not caregiver:
            flash('Caregiver not found!', 'error')
            return redirect(url_for('list_caregivers'))
        
        if request.method == 'POST':
            caregiver.photo = request.form.get('photo', '')
            caregiver.gender = request.form['gender']
            caregiver.caregiving_type = request.form['caregiving_type']
            caregiver.hourly_rate = request.form['hourly_rate']
            
            session.commit()
            flash('Caregiver updated successfully!', 'success')
            return redirect(url_for('list_caregivers'))
        
        user = session.get(User, caregiver_id)
        return render_template('caregivers/edit.html', caregiver=caregiver, user=user)
    finally:
        session.close()

@app.route('/caregivers/<int:caregiver_id>/delete', methods=['POST'])
def delete_caregiver(caregiver_id):
    """Delete a caregiver"""
    session = Session()
    try:
        caregiver = session.get(Caregiver, caregiver_id)
        if caregiver:
            session.delete(caregiver)
            session.commit()
            flash('Caregiver deleted successfully!', 'success')
        else:
            flash('Caregiver not found!', 'error')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting caregiver: {str(e)}', 'error')
    finally:
        session.close()
    
    return redirect(url_for('list_caregivers'))

# ============================================
# MEMBER CRUD OPERATIONS
# ============================================

@app.route('/members')
def list_members():
    """List all members"""
    session = Session()
    try:
        members = session.query(Member, User).join(
            User, User.user_id == Member.member_user_id
        ).all()
        return render_template('members/list.html', members=members)
    finally:
        session.close()

@app.route('/members/create', methods=['GET', 'POST'])
def create_member():
    """Create a new member"""
    session = Session()
    try:
        if request.method == 'POST':
            member = Member(
                member_user_id=request.form['user_id'],
                house_rules=request.form.get('house_rules', ''),
                dependent_description=request.form.get('dependent_description', '')
            )
            session.add(member)
            session.commit()
            flash('Member created successfully!', 'success')
            return redirect(url_for('list_members'))
        
        # Get users who are not yet members
        users = session.query(User).outerjoin(Member).filter(
            Member.member_user_id == None
        ).all()
        return render_template('members/create.html', users=users)
    except Exception as e:
        session.rollback()
        flash(f'Error creating member: {str(e)}', 'error')
        return redirect(url_for('list_members'))
    finally:
        session.close()

@app.route('/members/<int:member_id>/edit', methods=['GET', 'POST'])
def edit_member(member_id):
    """Edit an existing member"""
    session = Session()
    try:
        member = session.get(Member, member_id)
        if not member:
            flash('Member not found!', 'error')
            return redirect(url_for('list_members'))
        
        if request.method == 'POST':
            member.house_rules = request.form.get('house_rules', '')
            member.dependent_description = request.form.get('dependent_description', '')
            
            session.commit()
            flash('Member updated successfully!', 'success')
            return redirect(url_for('list_members'))
        
        user = session.get(User, member_id)
        return render_template('members/edit.html', member=member, user=user)
    finally:
        session.close()

@app.route('/members/<int:member_id>/delete', methods=['POST'])
def delete_member(member_id):
    """Delete a member"""
    session = Session()
    try:
        member = session.get(Member, member_id)
        if member:
            session.delete(member)
            session.commit()
            flash('Member deleted successfully!', 'success')
        else:
            flash('Member not found!', 'error')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting member: {str(e)}', 'error')
    finally:
        session.close()
    
    return redirect(url_for('list_members'))

# ============================================
# JOB CRUD OPERATIONS
# ============================================

@app.route('/jobs')
def list_jobs():
    """List all jobs"""
    session = Session()
    try:
        jobs = session.query(Job, User).join(
            Member, Member.member_user_id == Job.member_user_id
        ).join(
            User, User.user_id == Member.member_user_id
        ).all()
        return render_template('jobs/list.html', jobs=jobs)
    finally:
        session.close()

@app.route('/jobs/create', methods=['GET', 'POST'])
def create_job():
    """Create a new job"""
    session = Session()
    try:
        if request.method == 'POST':
            job = Job(
                member_user_id=request.form['member_id'],
                required_caregiving_type=request.form['caregiving_type'],
                other_requirements=request.form.get('other_requirements', ''),
                date_posted=datetime.strptime(request.form['date_posted'], '%Y-%m-%d').date()
            )
            session.add(job)
            session.commit()
            flash('Job created successfully!', 'success')
            return redirect(url_for('list_jobs'))
        
        members = session.query(Member, User).join(
            User, User.user_id == Member.member_user_id
        ).all()
        return render_template('jobs/create.html', members=members)
    except Exception as e:
        session.rollback()
        flash(f'Error creating job: {str(e)}', 'error')
        return redirect(url_for('list_jobs'))
    finally:
        session.close()

@app.route('/jobs/<int:job_id>/edit', methods=['GET', 'POST'])
def edit_job(job_id):
    """Edit an existing job"""
    session = Session()
    try:
        job = session.get(Job, job_id)
        if not job:
            flash('Job not found!', 'error')
            return redirect(url_for('list_jobs'))
        
        if request.method == 'POST':
            job.required_caregiving_type = request.form['caregiving_type']
            job.other_requirements = request.form.get('other_requirements', '')
            job.date_posted = datetime.strptime(request.form['date_posted'], '%Y-%m-%d').date()
            
            session.commit()
            flash('Job updated successfully!', 'success')
            return redirect(url_for('list_jobs'))
        
        return render_template('jobs/edit.html', job=job)
    finally:
        session.close()

@app.route('/jobs/<int:job_id>/delete', methods=['POST'])
def delete_job(job_id):
    """Delete a job"""
    session = Session()
    try:
        job = session.get(Job, job_id)
        if job:
            session.delete(job)
            session.commit()
            flash('Job deleted successfully!', 'success')
        else:
            flash('Job not found!', 'error')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting job: {str(e)}', 'error')
    finally:
        session.close()
    
    return redirect(url_for('list_jobs'))

# ============================================
# APPOINTMENT CRUD OPERATIONS
# ============================================

@app.route('/appointments')
def list_appointments():
    """List all appointments"""
    from sqlalchemy.orm import aliased
    
    session = Session()
    try:
        # Aliases for User table to distinguish between caregiver and member
        CaregiverUser = aliased(User)
        MemberUser = aliased(User)
        
        appointments = session.query(
            Appointment, 
            CaregiverUser.given_name.label('caregiver_name'), 
            CaregiverUser.surname.label('caregiver_surname'),
            MemberUser.given_name.label('member_name'), 
            MemberUser.surname.label('member_surname')
        ).join(
            Caregiver, Appointment.caregiver_user_id == Caregiver.caregiver_user_id
        ).join(
            CaregiverUser, Caregiver.caregiver_user_id == CaregiverUser.user_id
        ).join(
            Member, Appointment.member_user_id == Member.member_user_id
        ).join(
            MemberUser, Member.member_user_id == MemberUser.user_id
        ).all()
        
        return render_template('appointments/list.html', appointments=appointments)
    finally:
        session.close()

@app.route('/appointments/create', methods=['GET', 'POST'])
def create_appointment():
    """Create a new appointment"""
    session = Session()
    try:
        if request.method == 'POST':
            appointment = Appointment(
                caregiver_user_id=request.form['caregiver_id'],
                member_user_id=request.form['member_id'],
                appointment_date=datetime.strptime(request.form['appointment_date'], '%Y-%m-%d').date(),
                appointment_time=datetime.strptime(request.form['appointment_time'][:5], '%H:%M').time(),
                work_hours=request.form['work_hours'],
                status=request.form['status']
            )
            session.add(appointment)
            session.commit()
            flash('Appointment created successfully!', 'success')
            return redirect(url_for('list_appointments'))
        
        caregivers = session.query(Caregiver, User).join(
            User, User.user_id == Caregiver.caregiver_user_id
        ).all()
        members = session.query(Member, User).join(
            User, User.user_id == Member.member_user_id
        ).all()
        return render_template('appointments/create.html', caregivers=caregivers, members=members)
    except Exception as e:
        session.rollback()
        flash(f'Error creating appointment: {str(e)}', 'error')
        return redirect(url_for('list_appointments'))
    finally:
        session.close()

@app.route('/appointments/<int:appointment_id>/edit', methods=['GET', 'POST'])
def edit_appointment(appointment_id):
    """Edit an existing appointment"""
    session = Session()
    try:
        appointment = session.get(Appointment, appointment_id)
        if not appointment:
            flash('Appointment not found!', 'error')
            return redirect(url_for('list_appointments'))
        
        if request.method == 'POST':
            appointment.appointment_date = datetime.strptime(request.form['appointment_date'], '%Y-%m-%d').date()
            appointment.appointment_time = datetime.strptime(request.form['appointment_time'][:5], '%H:%M').time()
            appointment.work_hours = request.form['work_hours']
            appointment.status = request.form['status']
            
            session.commit()
            flash('Appointment updated successfully!', 'success')
            return redirect(url_for('list_appointments'))
        
        return render_template('appointments/edit.html', appointment=appointment)
    finally:
        session.close()

@app.route('/appointments/<int:appointment_id>/delete', methods=['POST'])
def delete_appointment(appointment_id):
    """Delete an appointment"""
    session = Session()
    try:
        appointment = session.get(Appointment, appointment_id)
        if appointment:
            session.delete(appointment)
            session.commit()
            flash('Appointment deleted successfully!', 'success')
        else:
            flash('Appointment not found!', 'error')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting appointment: {str(e)}', 'error')
    finally:
        session.close()
    
    return redirect(url_for('list_appointments'))

# ============================================
# DASHBOARD & STATISTICS
# ============================================

@app.route('/dashboard')
def dashboard():
    """Dashboard with statistics"""
    session = Session()
    try:
        stats = {
            'total_users': session.query(User).count(),
            'total_caregivers': session.query(Caregiver).count(),
            'total_members': session.query(Member).count(),
            'total_jobs': session.query(Job).count(),
            'total_applications': session.query(JobApplication).count(),
            'total_appointments': session.query(Appointment).count(),
            'accepted_appointments': session.query(Appointment).filter(
                Appointment.status == 'accepted'
            ).count()
        }
        return render_template('dashboard.html', stats=stats)
    finally:
        session.close()

if __name__ == '__main__':
    print("="*80)
    print("CSCI 341 Assignment 3 - Part 3: Web Application")
    print("Caregivers Platform - Flask CRUD Application")
    print("="*80)
    print("\nStarting Flask development server...")
    print("Access the application at: http://127.0.0.1:5002")
    print("\nPress Ctrl+C to stop the server")
    print("="*80)
    
    app.run(debug=True, host='0.0.0.0', port=5002)
