"""
Database utilities for the campus placement platform
"""

import sqlite3
import pandas as pd
from contextlib import contextmanager
import json

class DatabaseManager:
    def __init__(self, db_path='placement.db'):
        self.db_path = db_path
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()
    
    def init_database(self):
        """Initialize database with required tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Students table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    student_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT,
                    department TEXT,
                    semester INTEGER,
                    cgpa REAL,
                    backlogs INTEGER,
                    skills TEXT,
                    placement_status TEXT,
                    placement_company TEXT,
                    resume_path TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Companies table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS companies (
                    company_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    industry TEXT,
                    website TEXT,
                    contact_person TEXT,
                    contact_email TEXT,
                    contact_phone TEXT,
                    description TEXT,
                    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Placements table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS placements (
                    placement_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT,
                    company_id TEXT,
                    role TEXT,
                    package REAL,
                    placement_date DATE,
                    status TEXT,
                    FOREIGN KEY (student_id) REFERENCES students (student_id),
                    FOREIGN KEY (company_id) REFERENCES companies (company_id)
                )
            ''')
            
            # Internships table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS internships (
                    internship_id TEXT PRIMARY KEY,
                    company TEXT,
                    role TEXT,
                    location TEXT,
                    duration TEXT,
                    stipend REAL,
                    requirements TEXT,
                    deadline DATE,
                    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def add_student(self, student_data):
        """Add a new student to database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Convert skills list to JSON string
            if 'skills' in student_data and isinstance(student_data['skills'], list):
                student_data['skills'] = json.dumps(student_data['skills'])
            
            cursor.execute('''
                INSERT INTO students 
                (student_id, name, email, phone, department, semester, cgpa, backlogs, skills, placement_status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                student_data.get('student_id'),
                student_data.get('name'),
                student_data.get('email'),
                student_data.get('phone'),
                student_data.get('department'),
                student_data.get('semester'),
                student_data.get('cgpa'),
                student_data.get('backlogs'),
                student_data.get('skills'),
                student_data.get('placement_status', 'Not Placed')
            ))
            
            conn.commit()
            return cursor.lastrowid
    
    def get_students(self, filters=None):
        """Get students with optional filters"""
        query = "SELECT * FROM students"
        params = []
        
        if filters:
            conditions = []
            for key, value in filters.items():
                if value:
                    conditions.append(f"{key} = ?")
                    params.append(value)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
        
        with self.get_connection() as conn:
            df = pd.read_sql_query(query, conn, params=params if params else None)
        
        return df
    
    def update_placement_status(self, student_id, company, role, package):
        """Update student placement status"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Update student record
            cursor.execute('''
                UPDATE students 
                SET placement_status = ?, placement_company = ?
                WHERE student_id = ?
            ''', ('Placed', company, student_id))
            
            # Add to placements table
            cursor.execute('''
                INSERT INTO placements (student_id, company_id, role, package, placement_date, status)
                VALUES (?, ?, ?, ?, DATE('now'), 'Confirmed')
            ''', (student_id, company, role, package))
            
            conn.commit()
    
    def add_internship(self, internship_data):
        """Add a new internship opportunity"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO internships 
                (internship_id, company, role, location, duration, stipend, requirements, deadline)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                internship_data.get('internship_id'),
                internship_data.get('company'),
                internship_data.get('role'),
                internship_data.get('location'),
                internship_data.get('duration'),
                internship_data.get('stipend'),
                internship_data.get('requirements'),
                internship_data.get('deadline')
            ))
            
            conn.commit()
            return cursor.lastrowid
