import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_manager import DatabaseManager
import json
from datetime import datetime, timedelta

def seed_sample_data():
    """Seed database with sample data for testing"""
    db = DatabaseManager()
    
    with db.get_connection() as conn:
        # Check if data already exists
        cursor = conn.execute("SELECT COUNT(*) as count FROM students")
        if cursor.fetchone()['count'] > 10:  # Already seeded
            print("Sample data already exists")
            return
        
        print("Seeding sample data...")
        
        # Create sample students
        departments = ['Computer Science', 'Electrical Engineering', 
                      'Mechanical Engineering', 'Civil Engineering', 'Information Technology']
        
        for i in range(1, 51):
            # Create user
            conn.execute(
                """INSERT INTO users (username, email, password_hash, role, full_name, phone) 
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (f'student{i}', f'student{i}@college.edu', 
                 '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',  # 'password' hash
                 'student', f'Student {i}', f'9876543{i:03d}')
            )
            user_id = conn.lastrowid
            
            # Create student
            department = departments[i % len(departments)]
            cgpa = round(7.0 + (i % 30) / 10, 2)  # CGPA between 7.0 and 9.9
            semester = (i % 8) + 3  # Semester between 3 and 10
            
            conn.execute(
                """INSERT INTO students (user_id, roll_number, department, semester, cgpa, backlogs, graduation_year) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (user_id, f'20BCS{i:03d}', department, semester, cgpa, i % 4, 2024)
            )
            student_id = conn.lastrowid
            
            # Add skills
            tech_skills = ['Python', 'Java', 'C++', 'JavaScript', 'React', 'Node.js', 'SQL']
            soft_skills = ['Communication', 'Teamwork', 'Leadership', 'Problem Solving']
            
            for skill in tech_skills[: (i % 5) + 2]:  # 2-6 skills per student
                conn.execute(
                    """INSERT INTO student_skills (student_id, skill_name, skill_level, skill_category) 
                       VALUES (?, ?, ?, ?)""",
                    (student_id, skill, ['Beginner', 'Intermediate', 'Advanced'][i % 3], 'Technical')
                )
            
            for skill in soft_skills[: (i % 3) + 1]:  # 1-3 soft skills
                conn.execute(
                    """INSERT INTO student_skills (student_id, skill_name, skill_level, skill_category) 
                       VALUES (?, ?, ?, ?)""",
                    (student_id, skill, ['Beginner', 'Intermediate', 'Advanced'][i % 3], 'Soft')
                )
            
            # Add placements for some students
            if i % 3 == 0:  # 1/3rd students placed
                conn.execute(
                    """UPDATE students SET placement_status = 'Placed', 
                       placement_company_id = (SELECT company_id FROM companies LIMIT 1 OFFSET i % 3),
                       placement_package = ? WHERE student_id = ?""",
                    (round(8.0 + (i % 12), 2), student_id)  # Package between 8-20 LPA
                )
        
        # Create sample companies if not exists
        cursor = conn.execute("SELECT COUNT(*) as count FROM companies")
        if cursor.fetchone()['count'] < 5:
            companies = [
                ('Google', 'Technology', 'https://google.com', 'Search engine and technology company', 
                 'Sundar Pichai', 'careers@google.com', '+1-650-253-0000', 'university@google.com'),
                ('Microsoft', 'Software', 'https://microsoft.com', 'Software and cloud computing company',
                 'Satya Nadella', 'recruit@microsoft.com', '+1-425-882-8080', 'university@microsoft.com'),
                ('Amazon', 'E-commerce', 'https://amazon.com', 'E-commerce and cloud computing company',
                 'Andy Jassy', 'university@amazon.com', '+1-206-266-1000', 'campus@amazon.com'),
                ('TCS', 'IT Services', 'https://tcs.com', 'IT services and consulting',
                 'Rajesh Gopinathan', 'careers@tcs.com', '+91-22-6778-9999', 'campus@tcs.com'),
                ('Infosys', 'IT Services', 'https://infosys.com', 'IT services and consulting',
                 'Salil Parekh', 'careers@infosys.com', '+91-80-2852-0261', 'campus@infosys.com')
            ]
            
            for company in companies:
                conn.execute(
                    """INSERT INTO companies 
                       (company_name, industry, website, description, contact_person, 
                        contact_email, contact_phone, hr_email, is_verified) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (*company, 1)
                )
        
        # Create sample job postings
        cursor = conn.execute("SELECT company_id FROM companies")
        company_ids = [row['company_id'] for row in cursor.fetchall()]
        
        job_templates = [
            ('Software Development Engineer', 'Develop and maintain software applications', 'Full-time', 
             'Bangalore', 12.0, 25.0, 10, 7.5, 2, 'Python,Java,SQL,Algorithms', 'Health insurance, stock options'),
            ('Data Scientist', 'Build machine learning models and analyze data', 'Full-time',
             'Hyderabad', 10.0, 22.0, 5, 8.0, 1, 'Python,SQL,Machine Learning,Statistics', 'Flexible hours, remote work'),
            ('Product Manager', 'Define product strategy and roadmap', 'Full-time',
             'Mumbai', 15.0, 30.0, 3, 8.5, 0, 'Product Management,Analytics,Communication', 'Stock options, bonus'),
            ('Software Engineer Intern', 'Summer internship for software development', 'Internship',
             'Remote', 0.5, 0.8, 20, 7.0, 2, 'Python,JavaScript,Basic Algorithms', 'Stipend, mentorship, return offer'),
            ('DevOps Engineer', 'Build and maintain CI/CD pipelines', 'Full-time',
             'Chennai', 9.0, 20.0, 5, 7.0, 3, 'AWS,Docker,Kubernetes,Linux', 'Health insurance, learning budget')
        ]
        
        for i in range(20):
            company_id = company_ids[i % len(company_ids)]
            job_template = job_templates[i % len(job_templates)]
            deadline = (datetime.now() + timedelta(days=30 + (i * 7))).strftime('%Y-%m-%d')
            
            conn.execute(
                """INSERT INTO job_postings 
                   (company_id, job_title, job_description, job_type, location, 
                    salary_min, salary_max, vacancies, min_cgpa, max_backlogs, 
                    required_skills, benefits, application_deadline) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (company_id, *job_template[:9], deadline)
            )
        
        # Create sample applications
        cursor = conn.execute("SELECT student_id FROM students LIMIT 20")
        student_ids = [row['student_id'] for row in cursor.fetchall()]
        
        cursor = conn.execute("SELECT job_id FROM job_postings LIMIT 10")
        job_ids = [row['job_id'] for row in cursor.fetchall()]
        
        statuses = ['Applied', 'Shortlisted', 'Rejected', 'Interview', 'Selected']
        
        for student_id in student_ids:
            for job_id in job_ids[: (student_id % 3) + 1]:  # 1-3 applications per student
                status = statuses[(student_id + job_id) % len(statuses)]
                
                conn.execute(
                    """INSERT INTO student_applications 
                       (student_id, job_id, application_status) 
                       VALUES (?, ?, ?)""",
                    (student_id, job_id, status)
                )
        
        print("Sample data seeded successfully!")

if __name__ == "__main__":
    seed_sample_data()
