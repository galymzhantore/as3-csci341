"""
CSCI 341 Assignment 3 - Part 2
Caregivers Platform - SQLAlchemy Queries
"""

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, Date, Time, DECIMAL, ForeignKey, CheckConstraint
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import select, func, and_, or_
from datetime import date, time
import os

# Database Configuration
# Update these values with your PostgreSQL credentials
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'caregivers_platform')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine and base
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
metadata = MetaData()

# ============================================
# TABLE DEFINITIONS (ORM Models)
# ============================================

from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'USER'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    given_name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False)
    profile_description = Column(Text)
    password = Column(String(255), nullable=False)

class Caregiver(Base):
    __tablename__ = 'caregiver'
    
    caregiver_user_id = Column(Integer, ForeignKey('USER.user_id', ondelete='CASCADE'), primary_key=True)
    photo = Column(String(500))
    gender = Column(String(20), nullable=False)
    caregiving_type = Column(String(50), nullable=False)
    hourly_rate = Column(DECIMAL(10, 2), nullable=False)

class Member(Base):
    __tablename__ = 'member'
    
    member_user_id = Column(Integer, ForeignKey('USER.user_id', ondelete='CASCADE'), primary_key=True)
    house_rules = Column(Text)
    dependent_description = Column(Text)

class Address(Base):
    __tablename__ = 'address'
    
    member_user_id = Column(Integer, ForeignKey('member.member_user_id', ondelete='CASCADE'), primary_key=True)
    house_number = Column(String(20), nullable=False)
    street = Column(String(200), nullable=False)
    town = Column(String(100), nullable=False)

class Job(Base):
    __tablename__ = 'job'
    
    job_id = Column(Integer, primary_key=True, autoincrement=True)
    member_user_id = Column(Integer, ForeignKey('member.member_user_id', ondelete='CASCADE'), nullable=False)
    required_caregiving_type = Column(String(50), nullable=False)
    other_requirements = Column(Text)
    date_posted = Column(Date, nullable=False)

class JobApplication(Base):
    __tablename__ = 'job_application'
    
    caregiver_user_id = Column(Integer, ForeignKey('caregiver.caregiver_user_id', ondelete='CASCADE'), primary_key=True)
    job_id = Column(Integer, ForeignKey('job.job_id', ondelete='CASCADE'), primary_key=True)
    date_applied = Column(Date, nullable=False)

class Appointment(Base):
    __tablename__ = 'appointment'
    
    appointment_id = Column(Integer, primary_key=True, autoincrement=True)
    caregiver_user_id = Column(Integer, ForeignKey('caregiver.caregiver_user_id', ondelete='CASCADE'), nullable=False)
    member_user_id = Column(Integer, ForeignKey('member.member_user_id', ondelete='CASCADE'), nullable=False)
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    work_hours = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)

# ============================================
# MAIN EXECUTION
# ============================================

def print_separator(title):
    """Print a formatted separator for query results"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def execute_queries():
    """Execute all required queries for Part 2"""
    
    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # ============================================
        # 2. Table Creation (already done via SQL script, but we can verify)
        # ============================================
        print_separator("2. VERIFY TABLE CREATION")
        print("Tables are created via the SQL script. Verifying existence...")
        print(f"Tables: {Base.metadata.tables.keys()}")
        
        # ============================================
        # 3. Sample Data (already inserted via SQL script)
        # ============================================
        print_separator("3. SAMPLE DATA VERIFICATION")
        user_count = session.query(User).count()
        print(f"Total Users: {user_count}")
        caregiver_count = session.query(Caregiver).count()
        print(f"Total Caregivers: {caregiver_count}")
        member_count = session.query(Member).count()
        print(f"Total Members: {member_count}")
        
        # ============================================
        # 4. UPDATE QUERIES
        # ============================================
        print_separator("4a. UPDATE - Arman Armanov's Phone Number")
        user_to_update = session.query(User).filter(
            User.given_name == 'Arman',
            User.surname == 'Armanov'
        ).first()
        
        if user_to_update:
            old_phone = user_to_update.phone_number
            user_to_update.phone_number = '+77771111111'
            session.commit()
            print(f"Updated Arman Armanov's phone:")
            print(f"  Old: {old_phone}")
            print(f"  New: {user_to_update.phone_number}")
        else:
            print("Arman Armanov not found!")
        
        print_separator("4b. UPDATE - Caregiver Hourly Rates")
        print("Adjusting hourly rates:")
        print("  - Elderly Care in Astana: increase by 10%")
        print("  - All other caregivers: increase by 5%")
        
        # Get caregivers in Astana with Elderly Care
        elderly_astana = session.query(Caregiver).join(User).filter(
            User.city == 'Astana',
            Caregiver.caregiving_type == 'Elderly Care'
        ).all()
        
        for caregiver in elderly_astana:
            old_rate = float(caregiver.hourly_rate)
            caregiver.hourly_rate = old_rate * 1.10
            print(f"  User {caregiver.caregiver_user_id}: ${old_rate:.2f} -> ${caregiver.hourly_rate:.2f} (10% increase)")
        
        # Get all other caregivers
        other_caregivers = session.query(Caregiver).join(User).filter(
            or_(
                User.city != 'Astana',
                Caregiver.caregiving_type != 'Elderly Care'
            )
        ).all()
        
        for caregiver in other_caregivers:
            old_rate = float(caregiver.hourly_rate)
            caregiver.hourly_rate = old_rate * 1.05
            print(f"  User {caregiver.caregiver_user_id}: ${old_rate:.2f} -> ${caregiver.hourly_rate:.2f} (5% increase)")
        
        session.commit()
        
        # ============================================
        # 5. DELETE QUERIES
        # ============================================
        print_separator("5a. DELETE - Jobs Posted by Amina Aminova")
        
        amina = session.query(User).filter(
            User.given_name == 'Amina',
            User.surname == 'Aminova'
        ).first()
        
        if amina:
            jobs_to_delete = session.query(Job).filter(
                Job.member_user_id == amina.user_id
            ).all()
            
            print(f"Deleting {len(jobs_to_delete)} job(s) posted by Amina Aminova (User ID: {amina.user_id})")
            for job in jobs_to_delete:
                print(f"  - Job ID {job.job_id}: {job.required_caregiving_type}")
                session.delete(job)
            session.commit()
        else:
            print("Amina Aminova not found!")
        
        print_separator("5b. DELETE - Members on Kabanbay Batyr Street")
        
        # Find members on Kabanbay Batyr
        members_to_delete = session.query(Member).join(Address).filter(
            Address.street == 'Kabanbay Batyr'
        ).all()
        
        print(f"Deleting {len(members_to_delete)} member(s) living on Kabanbay Batyr:")
        for member in members_to_delete:
            user_info = session.query(User).filter(User.user_id == member.member_user_id).first()
            print(f"  - User ID {member.member_user_id}: {user_info.given_name} {user_info.surname}")
            session.delete(member)
        
        session.commit()
        
        # ============================================
        # 6. SIMPLE QUERIES
        # ============================================
        print_separator("6a. SIMPLE QUERY - Accepted Appointments")
        
        accepted = session.query(Appointment).filter(
            Appointment.status == 'accepted'
        ).all()
        
        print(f"Found {len(accepted)} accepted appointment(s):")
        for apt in accepted:
            print(f"  Appointment ID: {apt.appointment_id}, Date: {apt.appointment_date}, "
                  f"Time: {apt.appointment_time}, Hours: {apt.work_hours}")
        
        print_separator("6b. SIMPLE QUERY - Jobs with 'soft-spoken' Keyword")
        
        soft_spoken_jobs = session.query(Job).filter(
            Job.other_requirements.ilike('%soft-spoken%')
        ).all()
        
        print(f"Found {len(soft_spoken_jobs)} job(s) requiring soft-spoken caregivers:")
        for job in soft_spoken_jobs:
            print(f"  Job ID: {job.job_id}, Type: {job.required_caregiving_type}, "
                  f"Requirements: {job.other_requirements[:50]}...")
        
        print_separator("6c. SIMPLE QUERY - Babysitter Jobs")
        
        babysitter_jobs = session.query(Job).filter(
            Job.required_caregiving_type == 'Babysitter'
        ).all()
        
        print(f"Found {len(babysitter_jobs)} Babysitter job(s):")
        for job in babysitter_jobs:
            print(f"  Job ID: {job.job_id}, Posted: {job.date_posted}, "
                  f"Requirements: {job.other_requirements[:50]}...")
        
        print_separator("6d. SIMPLE QUERY - Members in Astana with 'No pets' Rule")
        
        astana_no_pets = session.query(Member).join(User).filter(
            User.city == 'Astana',
            Member.house_rules.ilike('%No pets%')
        ).all()
        
        print(f"Found {len(astana_no_pets)} member(s) in Astana with 'No pets' rule:")
        for member in astana_no_pets:
            user_info = session.query(User).filter(User.user_id == member.member_user_id).first()
            print(f"  User ID: {member.member_user_id}, Name: {user_info.given_name} {user_info.surname}")
        
        # ============================================
        # 7. COMPLEX QUERIES (Joins and Aggregation)
        # ============================================
        print_separator("7a. COMPLEX QUERY - Jobs with Application Count")
        
        # Jobs with their application counts
        job_app_counts = session.query(
            Job.job_id,
            Job.required_caregiving_type,
            Job.date_posted,
            func.count(JobApplication.caregiver_user_id).label('application_count')
        ).outerjoin(JobApplication).group_by(
            Job.job_id,
            Job.required_caregiving_type,
            Job.date_posted
        ).all()
        
        print(f"Jobs with application counts:")
        for job_id, care_type, posted_date, app_count in job_app_counts:
            print(f"  Job ID {job_id} ({care_type}): {app_count} application(s)")
        
        print_separator("7b. COMPLEX QUERY - Caregivers with Appointment Count")
        
        caregiver_stats = session.query(
            Caregiver.caregiver_user_id,
            User.given_name,
            User.surname,
            Caregiver.caregiving_type,
            func.count(Appointment.appointment_id).label('appointment_count')
        ).join(User, User.user_id == Caregiver.caregiver_user_id)\
         .outerjoin(Appointment, Appointment.caregiver_user_id == Caregiver.caregiver_user_id)\
         .group_by(
            Caregiver.caregiver_user_id,
            User.given_name,
            User.surname,
            Caregiver.caregiving_type
         ).all()
        
        print("Caregivers with appointment counts:")
        for user_id, given_name, surname, care_type, apt_count in caregiver_stats:
            print(f"  {given_name} {surname} ({care_type}): {apt_count} appointment(s)")
        
        print_separator("7c. COMPLEX QUERY - Average Hourly Rate by Caregiving Type")
        
        avg_rates = session.query(
            Caregiver.caregiving_type,
            func.avg(Caregiver.hourly_rate).label('avg_rate'),
            func.count(Caregiver.caregiver_user_id).label('caregiver_count')
        ).group_by(Caregiver.caregiving_type).all()
        
        print("Average hourly rates by caregiving type:")
        for care_type, avg_rate, count in avg_rates:
            print(f"  {care_type}: ${avg_rate:.2f} (based on {count} caregiver(s))")
        
        # ============================================
        # 8. DERIVED ATTRIBUTE QUERY
        # ============================================
        print_separator("8. DERIVED ATTRIBUTE - Total Cost of Accepted Appointments")
        
        apt_costs = session.query(
            Appointment.appointment_id,
            User.given_name.label('caregiver_first'),
            User.surname.label('caregiver_last'),
            Appointment.work_hours,
            Caregiver.hourly_rate,
            (Appointment.work_hours * Caregiver.hourly_rate).label('total_cost')
        ).join(Caregiver, Caregiver.caregiver_user_id == Appointment.caregiver_user_id)\
         .join(User, User.user_id == Caregiver.caregiver_user_id)\
         .filter(Appointment.status == 'accepted')\
         .all()
        
        print("Total cost for accepted appointments:")
        total_revenue = 0
        for apt_id, first_name, last_name, hours, rate, cost in apt_costs:
            print(f"  Appointment {apt_id}: {first_name} {last_name} - "
                  f"{hours} hours × ${rate:.2f}/hr = ${cost:.2f}")
            total_revenue += float(cost)
        
        print(f"\nTotal Revenue from Accepted Appointments: ${total_revenue:.2f}")
        
        # ============================================
        # 9. CREATE VIEW
        # ============================================
        print_separator("9. CREATE VIEW - Job Applications with Caregiver Details")
        
        view_query = Text("""
            CREATE OR REPLACE VIEW job_application_details AS
            SELECT 
                ja.job_id,
                j.required_caregiving_type,
                u_cg.given_name AS caregiver_name,
                u_cg.surname AS caregiver_surname,
                cg.hourly_rate,
                ja.date_applied
            FROM job_application ja
            JOIN caregiver cg ON ja.caregiver_user_id = cg.caregiver_user_id
            JOIN "USER" u_cg ON cg.caregiver_user_id = u_cg.user_id
            JOIN job j ON ja.job_id = j.job_id;
        """)
        
        try:
            session.execute(view_query)
            session.commit()
            print("View 'job_application_details' created successfully.")
            
            # Verify view creation
            result = session.execute(text("SELECT * FROM job_application_details LIMIT 3"))
            print("\nSample data from view:")
            for row in result:
                print(f"  Job {row.job_id} ({row.required_caregiving_type}): Applied by {row.caregiver_name} {row.caregiver_surname} (${row.hourly_rate}/hr)")
                
        except Exception as e:
            session.rollback()
            print(f"Error creating view: {e}")
            
        print_separator("ALL QUERIES EXECUTED SUCCESSFULLY!")
        
    except Exception as e:
        print(f"\nError occurred: {e}")
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    print("="*80)
    print("CSCI 341 Assignment 3 - Part 2: SQLAlchemy Queries")
    print("Caregivers Platform Database")
    print("="*80)
    
    print("\nConnecting to database...")
    print(f"Database: {DB_NAME}")
    print(f"Host: {DB_HOST}:{DB_PORT}")
    print(f"User: {DB_USER}")
    
    print("\nNOTE: Make sure you have:")
    print("1. Created the database using the caregivers_platform_part1.sql script")
    print("2. Installed required packages: pip install sqlalchemy psycopg2-binary")
    print("3. Set environment variables or updated the DB credentials in this script")
    
    input("\nPress Enter to continue with query execution...")
    
    execute_queries()
