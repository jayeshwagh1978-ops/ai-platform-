# database/db_manager.py
import sqlite3
import pandas as pd
import streamlit as st
import traceback
from datetime import datetime, timedelta
import os

class DatabaseManager:
    def __init__(self, db_path="placement_platform.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Create a database connection"""
        try:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row  # Return rows as dictionaries
            return conn
        except Exception as e:
            st.error(f"Database connection error: {e}")
            return None
    
    def init_database(self):
        """Initialize database with all required tables"""
        try:
            conn = self.get_connection()
            if conn is None:
                st.error("Failed to connect to database")
                return
            
            cursor = conn.cursor()
            
            # Enable foreign keys
            cursor.execute("PRAGMA foreign_keys = ON")
            
            # Users table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('student', 'college_admin', 'recruiter', 'observer')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
            ''')
            
            # Students table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                full_name TEXT NOT NULL,
                enrollment_number TEXT UNIQUE,
                college_id INTEGER,
                department TEXT,
                semester INTEGER,
                cgpa REAL,
                phone TEXT,
                skills TEXT,
                resume_path TEXT,
                profile_pic_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
            ''')
            
            # Colleges table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS colleges (
                college_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                college_name TEXT UNIQUE NOT NULL,
                university_affiliation TEXT,
                location TEXT,
                accreditation TEXT,
                contact_email TEXT,
                contact_phone TEXT,
                website TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
            ''')
            
            # Recruiters table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS recruiters (
                recruiter_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                company_name TEXT NOT NULL,
                industry TEXT,
                company_size TEXT,
                website TEXT,
                contact_person TEXT,
                contact_email TEXT UNIQUE,
                contact_phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
            ''')
            
            # Jobs table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                job_id INTEGER PRIMARY KEY AUTOINCREMENT,
                recruiter_id INTEGER,
                title TEXT NOT NULL,
                description TEXT,
                requirements TEXT,
                location TEXT,
                job_type TEXT CHECK(job_type IN ('full_time', 'internship', 'contract')),
                salary_range TEXT,
                skills_required TEXT,
                posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                deadline DATE,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (recruiter_id) REFERENCES recruiters(recruiter_id) ON DELETE CASCADE
            )
            ''')
            
            # Applications table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                application_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                job_id INTEGER,
                application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'reviewed', 'shortlisted', 'rejected', 'accepted')),
                cover_letter TEXT,
                resume_path TEXT,
                feedback TEXT,
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
                FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE CASCADE,
                UNIQUE(student_id, job_id)
            )
            ''')
            
            # Placements table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS placements (
                placement_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER UNIQUE,
                job_id INTEGER,
                college_id INTEGER,
                placement_date DATE,
                package_offered REAL,
                joining_date DATE,
                status TEXT CHECK(status IN ('offered', 'accepted', 'joined', 'rejected')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
                FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE CASCADE,
                FOREIGN KEY (college_id) REFERENCES colleges(college_id) ON DELETE CASCADE
            )
            ''')
            
            # Student skills table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS student_skills (
                skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                skill_name TEXT NOT NULL,
                proficiency_level INTEGER CHECK(proficiency_level BETWEEN 1 AND 10),
                certification TEXT,
                verified BOOLEAN DEFAULT 0,
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
            )
            ''')
            
            # Interview feedback table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS interview_feedback (
                feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
                application_id INTEGER,
                interviewer_id INTEGER,
                technical_skills INTEGER CHECK(technical_skills BETWEEN 1 AND 10),
                communication INTEGER CHECK(communication BETWEEN 1 AND 10),
                problem_solving INTEGER CHECK(problem_solving BETWEEN 1 AND 10),
                attitude INTEGER CHECK(attitude BETWEEN 1 AND 10),
                overall_rating INTEGER CHECK(overall_rating BETWEEN 1 AND 10),
                strengths TEXT,
                areas_for_improvement TEXT,
                recommendation TEXT CHECK(recommendation IN ('strong_hire', 'hire', 'consider', 'reject')),
                feedback_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (application_id) REFERENCES applications(application_id) ON DELETE CASCADE,
                FOREIGN KEY (interviewer_id) REFERENCES recruiters(recruiter_id) ON DELETE CASCADE
            )
            ''')
            
            # NEP compliance table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS nep_compliance (
                compliance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                college_id INTEGER,
                year INTEGER,
                multidisciplinary_score INTEGER,
                flexible_curriculum_score INTEGER,
                skill_integration_score INTEGER,
                digital_literacy_score INTEGER,
                research_culture_score INTEGER,
                industry_connect_score INTEGER,
                overall_score REAL,
                FOREIGN KEY (college_id) REFERENCES colleges(college_id) ON DELETE CASCADE
            )
            ''')
            
            # Blockchain credentials table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS blockchain_credentials (
                credential_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                credential_type TEXT NOT NULL,
                credential_hash TEXT UNIQUE NOT NULL,
                issuer TEXT,
                issue_date DATE,
                expiration_date DATE,
                verified BOOLEAN DEFAULT 0,
                blockchain_tx_id TEXT,
                metadata TEXT,
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
            )
            ''')
            
            # Notifications table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                notification_type TEXT CHECK(notification_type IN ('info', 'warning', 'success', 'error', 'job', 'application')),
                is_read BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
            ''')
            
            # Create indexes for performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_jobs_recruiter ON jobs(recruiter_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_applications_student ON applications(student_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_applications_job ON applications(job_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id)')
            
            conn.commit()
            conn.close()
            
            st.success("Database initialized successfully!")
            
        except Exception as e:
            st.error(f"Database initialization error: {e}")
            st.code(traceback.format_exc())
    
    # ================== USER MANAGEMENT ==================
    
    def create_user(self, username, email, password, role):
        """Create a new user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
                (username, email, password, role)
            )
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return user_id
        except Exception as e:
            st.error(f"Error creating user: {e}")
            return None
    
    def authenticate_user(self, username, password):
        """Authenticate a user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = ? AND password_hash = ? AND is_active = 1",
                (username, password)
            )
            user = cursor.fetchone()
            conn.close()
            return dict(user) if user else None
        except Exception as e:
            st.error(f"Authentication error: {e}")
            return None
    
    # ================== STUDENT OPERATIONS ==================
    
    def create_student_profile(self, user_id, student_data):
        """Create student profile"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO students (user_id, full_name, enrollment_number, college_id, 
                                    department, semester, cgpa, phone, skills)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, student_data['full_name'], student_data['enrollment_number'],
                student_data.get('college_id'), student_data['department'], 
                student_data['semester'], student_data.get('cgpa'), 
                student_data['phone'], student_data.get('skills', '')
            ))
            conn.commit()
            student_id = cursor.lastrowid
            conn.close()
            return student_id
        except Exception as e:
            st.error(f"Error creating student profile: {e}")
            return None
    
    def get_student_by_user_id(self, user_id):
        """Get student profile by user ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM students WHERE user_id = ?",
                (user_id,)
            )
            student = cursor.fetchone()
            conn.close()
            return dict(student) if student else None
        except Exception as e:
            st.error(f"Error fetching student: {e}")
            return None
    
    # ================== COLLEGE OPERATIONS ==================
    
    def create_college_profile(self, user_id, college_data):
        """Create college profile"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO colleges (user_id, college_name, university_affiliation, 
                                    location, accreditation, contact_email, contact_phone, website)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, college_data['college_name'], college_data.get('university_affiliation'),
                college_data['location'], college_data.get('accreditation'), 
                college_data['contact_email'], college_data['contact_phone'],
                college_data.get('website', '')
            ))
            conn.commit()
            college_id = cursor.lastrowid
            conn.close()
            return college_id
        except Exception as e:
            st.error(f"Error creating college profile: {e}")
            return None
    
    def get_college_by_user_id(self, user_id):
        """Get college profile by user ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM colleges WHERE user_id = ?",
                (user_id,)
            )
            college = cursor.fetchone()
            conn.close()
            return dict(college) if college else None
        except Exception as e:
            st.error(f"Error fetching college: {e}")
            return None
    
    # ================== RECRUITER OPERATIONS ==================
    
    def create_recruiter_profile(self, user_id, recruiter_data):
        """Create recruiter profile"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO recruiters (user_id, company_name, industry, company_size,
                                      website, contact_person, contact_email, contact_phone)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, recruiter_data['company_name'], recruiter_data.get('industry'),
                recruiter_data.get('company_size'), recruiter_data.get('website'),
                recruiter_data['contact_person'], recruiter_data['contact_email'],
                recruiter_data['contact_phone']
            ))
            conn.commit()
            recruiter_id = cursor.lastrowid
            conn.close()
            return recruiter_id
        except Exception as e:
            st.error(f"Error creating recruiter profile: {e}")
            return None
    
    def get_recruiter_by_user_id(self, user_id):
        """Get recruiter profile by user ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM recruiters WHERE user_id = ?",
                (user_id,)
            )
            recruiter = cursor.fetchone()
            conn.close()
            return dict(recruiter) if recruiter else None
        except Exception as e:
            st.error(f"Error fetching recruiter: {e}")
            return None
    
    # ================== JOB OPERATIONS ==================
    
    def create_job(self, recruiter_id, job_data):
        """Create a new job posting"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO jobs (recruiter_id, title, description, requirements,
                                location, job_type, salary_range, skills_required, deadline)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                recruiter_id, job_data['title'], job_data['description'],
                job_data.get('requirements', ''), job_data['location'],
                job_data['job_type'], job_data.get('salary_range', ''),
                job_data.get('skills_required', ''), job_data.get('deadline')
            ))
            conn.commit()
            job_id = cursor.lastrowid
            conn.close()
            return job_id
        except Exception as e:
            st.error(f"Error creating job: {e}")
            return None
    
    def get_jobs(self, filters=None):
        """Get all jobs with optional filters"""
        try:
            conn = self.get_connection()
            query = '''
                SELECT j.*, r.company_name 
                FROM jobs j
                JOIN recruiters r ON j.recruiter_id = r.recruiter_id
                WHERE j.is_active = 1
            '''
            params = []
            
            if filters:
                conditions = []
                if filters.get('job_type'):
                    conditions.append("j.job_type = ?")
                    params.append(filters['job_type'])
                if filters.get('location'):
                    conditions.append("j.location LIKE ?")
                    params.append(f"%{filters['location']}%")
                if filters.get('skills'):
                    conditions.append("j.skills_required LIKE ?")
                    params.append(f"%{filters['skills']}%")
                
                if conditions:
                    query += " AND " + " AND ".join(conditions)
            
            query += " ORDER BY j.posted_date DESC"
            
            df = pd.read_sql_query(query, conn, params=params)
            conn.close()
            return df
        except Exception as e:
            st.error(f"Error fetching jobs: {e}")
            return pd.DataFrame()
    
    # ================== APPLICATION OPERATIONS ==================
    
    def create_application(self, student_id, job_id, cover_letter="", resume_path=""):
        """Create a job application"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO applications (student_id, job_id, cover_letter, resume_path)
                VALUES (?, ?, ?, ?)
            ''', (student_id, job_id, cover_letter, resume_path))
            conn.commit()
            application_id = cursor.lastrowid
            conn.close()
            return application_id
        except Exception as e:
            st.error(f"Error creating application: {e}")
            return None
    
    def get_student_applications(self, student_id):
        """Get all applications for a student"""
        try:
            conn = self.get_connection()
            query = '''
                SELECT a.*, j.title, r.company_name, j.location
                FROM applications a
                JOIN jobs j ON a.job_id = j.job_id
                JOIN recruiters r ON j.recruiter_id = r.recruiter_id
                WHERE a.student_id = ?
                ORDER BY a.application_date DESC
            '''
            df = pd.read_sql_query(query, conn, params=(student_id,))
            conn.close()
            return df
        except Exception as e:
            st.error(f"Error fetching applications: {e}")
            return pd.DataFrame()
    
    # ================== ANALYTICS & DASHBOARD ==================
    
    def get_dashboard_stats(self, user_id, role):
        """Get dashboard statistics based on user role"""
        try:
            conn = self.get_connection()
            stats = {}
            
            if role == 'student':
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT student_id FROM students WHERE user_id = ?",
                    (user_id,)
                )
                student = cursor.fetchone()
                if student:
                    student_id = student['student_id']
                    # Get application stats
                    cursor.execute('''
                        SELECT COUNT(*) as total,
                               SUM(CASE WHEN status = 'accepted' THEN 1 ELSE 0 END) as accepted,
                               SUM(CASE WHEN status = 'shortlisted' THEN 1 ELSE 0 END) as shortlisted
                        FROM applications
                        WHERE student_id = ?
                    ''', (student_id,))
                    app_stats = cursor.fetchone()
                    stats['applications'] = dict(app_stats)
            
            elif role == 'recruiter':
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT recruiter_id FROM recruiters WHERE user_id = ?",
                    (user_id,)
                )
                recruiter = cursor.fetchone()
                if recruiter:
                    recruiter_id = recruiter['recruiter_id']
                    # Get job stats
                    cursor.execute('''
                        SELECT COUNT(*) as total_jobs,
                               SUM(CASE WHEN is_active = 1 THEN 1 ELSE 0 END) as active_jobs
                        FROM jobs
                        WHERE recruiter_id = ?
                    ''', (recruiter_id,))
                    job_stats = cursor.fetchone()
                    stats['jobs'] = dict(job_stats)
            
            elif role == 'college_admin':
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT college_id FROM colleges WHERE user_id = ?",
                    (user_id,)
                )
                college = cursor.fetchone()
                if college:
                    college_id = college['college_id']
                    # Get student stats
                    cursor.execute('''
                        SELECT COUNT(*) as total_students,
                               AVG(cgpa) as avg_cgpa
                        FROM students
                        WHERE college_id = ?
                    ''', (college_id,))
                    student_stats = cursor.fetchone()
                    stats['students'] = dict(student_stats)
                    
                    # Get placement stats
                    cursor.execute('''
                        SELECT COUNT(*) as total_placements
                        FROM placements
                        WHERE college_id = ?
                    ''', (college_id,))
                    placement_stats = cursor.fetchone()
                    stats['placements'] = dict(placement_stats)
            
            conn.close()
            return stats
            
        except Exception as e:
            st.error(f"Error fetching dashboard stats: {e}")
            return {}
    
    # ================== NEP COMPLIANCE ==================
    
    def save_nep_compliance_score(self, college_id, year, scores):
        """Save NEP 2020 compliance scores"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            overall_score = sum(scores.values()) / len(scores)
            
            cursor.execute('''
                INSERT INTO nep_compliance 
                (college_id, year, multidisciplinary_score, flexible_curriculum_score,
                 skill_integration_score, digital_literacy_score, research_culture_score,
                 industry_connect_score, overall_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                college_id, year,
                scores.get('multidisciplinary', 0),
                scores.get('flexible_curriculum', 0),
                scores.get('skill_integration', 0),
                scores.get('digital_literacy', 0),
                scores.get('research_culture', 0),
                scores.get('industry_connect', 0),
                overall_score
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            st.error(f"Error saving NEP compliance: {e}")
            return False
    
    # ================== NOTIFICATIONS ==================
    
    def create_notification(self, user_id, title, message, notification_type='info'):
        """Create a new notification"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO notifications (user_id, title, message, notification_type)
                VALUES (?, ?, ?, ?)
            ''', (user_id, title, message, notification_type))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            st.error(f"Error creating notification: {e}")
            return False
    
    def get_user_notifications(self, user_id, unread_only=False):
        """Get notifications for a user"""
        try:
            conn = self.get_connection()
            query = '''
                SELECT * FROM notifications 
                WHERE user_id = ?
            '''
            params = [user_id]
            
            if unread_only:
                query += " AND is_read = 0"
            
            query += " ORDER BY created_at DESC LIMIT 20"
            
            df = pd.read_sql_query(query, conn, params=params)
            conn.close()
            return df
        except Exception as e:
            st.error(f"Error fetching notifications: {e}")
            return pd.DataFrame()
    
    # ================== DEMO DATA ==================
    
    def create_demo_data(self):
        """Create demo data for testing"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Create demo users
            demo_users = [
                ('student1', 'student1@demo.com', 'password123', 'student'),
                ('college1', 'college1@demo.com', 'password123', 'college_admin'),
                ('recruiter1', 'recruiter1@demo.com', 'password123', 'recruiter'),
            ]
            
            for user in demo_users:
                cursor.execute(
                    "INSERT OR IGNORE INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
                    user
                )
            
            conn.commit()
            conn.close()
            st.success("Demo data created successfully!")
            return True
        except Exception as e:
            st.error(f"Error creating demo data: {e}")
            return False

# Initialize database manager
try:
    db_manager = DatabaseManager()
except Exception as e:
    st.error(f"Failed to initialize database: {e}")
    db_manager = None
