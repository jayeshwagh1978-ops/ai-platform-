-- Campus Placement Management System Database Schema

-- Users Table (Unified for all roles)
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('student', 'college_admin', 'recruiter', 'tpo')),
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
);

-- Students Table
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    roll_number VARCHAR(20) UNIQUE NOT NULL,
    department VARCHAR(50) NOT NULL,
    semester INTEGER CHECK (semester BETWEEN 1 AND 10),
    cgpa DECIMAL(3,2) CHECK (cgpa BETWEEN 0.00 AND 10.00),
    backlogs INTEGER DEFAULT 0,
    graduation_year INTEGER,
    resume_file_path TEXT,
    github_profile TEXT,
    linkedin_profile TEXT,
    portfolio_website TEXT,
    placement_status VARCHAR(20) DEFAULT 'Not Placed' CHECK (placement_status IN ('Not Placed', 'Placed', 'Intern', 'Higher Studies')),
    placement_company_id INTEGER,
    placement_package DECIMAL(10,2),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (placement_company_id) REFERENCES companies(company_id)
);

-- Student Skills Table
CREATE TABLE IF NOT EXISTS student_skills (
    skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    skill_name VARCHAR(50) NOT NULL,
    skill_level VARCHAR(20) CHECK (skill_level IN ('Beginner', 'Intermediate', 'Advanced')),
    skill_category VARCHAR(20) DEFAULT 'Technical',
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    UNIQUE(student_id, skill_name)
);

-- Student Education Table
CREATE TABLE IF NOT EXISTS student_education (
    education_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    degree VARCHAR(50) NOT NULL,
    institution VARCHAR(100) NOT NULL,
    specialization VARCHAR(50),
    cgpa DECIMAL(3,2),
    start_year INTEGER,
    end_year INTEGER,
    is_current BOOLEAN DEFAULT 0,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

-- Student Projects Table
CREATE TABLE IF NOT EXISTS student_projects (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    project_title VARCHAR(100) NOT NULL,
    project_description TEXT,
    technologies_used TEXT,
    project_duration VARCHAR(30),
    project_link TEXT,
    github_link TEXT,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

-- Student Work Experience Table
CREATE TABLE IF NOT EXISTS student_experience (
    experience_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    company_name VARCHAR(100) NOT NULL,
    position VARCHAR(50) NOT NULL,
    start_date DATE,
    end_date DATE,
    is_current BOOLEAN DEFAULT 0,
    location VARCHAR(50),
    description TEXT,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

-- Colleges Table
CREATE TABLE IF NOT EXISTS colleges (
    college_id INTEGER PRIMARY KEY AUTOINCREMENT,
    college_name VARCHAR(100) UNIQUE NOT NULL,
    college_code VARCHAR(20) UNIQUE,
    address TEXT,
    city VARCHAR(50),
    state VARCHAR(50),
    pin_code VARCHAR(10),
    website TEXT,
    contact_email VARCHAR(100),
    contact_phone VARCHAR(15),
    accreditation VARCHAR(20),
    established_year INTEGER,
    total_students INTEGER DEFAULT 0,
    total_faculty INTEGER DEFAULT 0,
    placement_officer_id INTEGER,
    FOREIGN KEY (placement_officer_id) REFERENCES users(user_id)
);

-- College Departments Table
CREATE TABLE IF NOT EXISTS college_departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    college_id INTEGER NOT NULL,
    department_name VARCHAR(50) NOT NULL,
    hod_name VARCHAR(100),
    hod_email VARCHAR(100),
    total_students INTEGER DEFAULT 0,
    placement_rate DECIMAL(5,2),
    avg_package DECIMAL(10,2),
    FOREIGN KEY (college_id) REFERENCES colleges(college_id) ON DELETE CASCADE,
    UNIQUE(college_id, department_name)
);

-- Companies Table
CREATE TABLE IF NOT EXISTS companies (
    company_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name VARCHAR(100) UNIQUE NOT NULL,
    industry VARCHAR(50),
    website TEXT,
    description TEXT,
    logo_url TEXT,
    founded_year INTEGER,
    employee_count VARCHAR(50),
    headquarters VARCHAR(100),
    contact_person VARCHAR(100),
    contact_email VARCHAR(100),
    contact_phone VARCHAR(15),
    hr_email VARCHAR(100),
    is_verified BOOLEAN DEFAULT 0,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Job Postings Table
CREATE TABLE IF NOT EXISTS job_postings (
    job_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    job_title VARCHAR(100) NOT NULL,
    job_description TEXT NOT NULL,
    job_type VARCHAR(20) CHECK (job_type IN ('Full-time', 'Internship', 'Contract', 'Part-time')),
    location VARCHAR(100),
    salary_min DECIMAL(10,2),
    salary_max DECIMAL(10,2),
    salary_currency VARCHAR(3) DEFAULT 'INR',
    vacancies INTEGER DEFAULT 1,
    min_cgpa DECIMAL(3,2),
    max_backlogs INTEGER DEFAULT 0,
    required_skills TEXT,
    benefits TEXT,
    application_deadline DATE,
    posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);

-- Campus Drives Table
CREATE TABLE IF NOT EXISTS campus_drives (
    drive_id INTEGER PRIMARY KEY AUTOINCREMENT,
    college_id INTEGER NOT NULL,
    company_id INTEGER NOT NULL,
    drive_date DATE NOT NULL,
    drive_mode VARCHAR(20) CHECK (drive_mode IN ('Online', 'Offline', 'Hybrid')),
    venue TEXT,
    coordinator_name VARCHAR(100),
    coordinator_contact VARCHAR(15),
    registration_deadline DATE,
    drive_status VARCHAR(20) DEFAULT 'Scheduled' CHECK (drive_status IN ('Scheduled', 'Ongoing', 'Completed', 'Cancelled')),
    total_registered INTEGER DEFAULT 0,
    total_selected INTEGER DEFAULT 0,
    FOREIGN KEY (college_id) REFERENCES colleges(college_id),
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

-- Drive Job Mapping Table
CREATE TABLE IF NOT EXISTS drive_jobs (
    mapping_id INTEGER PRIMARY KEY AUTOINCREMENT,
    drive_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    FOREIGN KEY (drive_id) REFERENCES campus_drives(drive_id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES job_postings(job_id) ON DELETE CASCADE,
    UNIQUE(drive_id, job_id)
);

-- Student Applications Table
CREATE TABLE IF NOT EXISTS student_applications (
    application_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    drive_id INTEGER,
    application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    application_status VARCHAR(20) DEFAULT 'Applied' CHECK (application_status IN ('Applied', 'Shortlisted', 'Rejected', 'Interview', 'Selected', 'Offer Accepted', 'Offer Declined')),
    resume_version TEXT,
    cover_letter TEXT,
    applied_via VARCHAR(20) DEFAULT 'Portal',
    notes TEXT,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES job_postings(job_id),
    FOREIGN KEY (drive_id) REFERENCES campus_drives(drive_id),
    UNIQUE(student_id, job_id)
);

-- Interview Rounds Table
CREATE TABLE IF NOT EXISTS interview_rounds (
    round_id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_id INTEGER NOT NULL,
    round_number INTEGER NOT NULL,
    round_type VARCHAR(30) CHECK (round_type IN ('Aptitude', 'Technical', 'HR', 'Group Discussion', 'Case Study', 'Presentation')),
    scheduled_date TIMESTAMP,
    interview_mode VARCHAR(20) CHECK (interview_mode IN ('Online', 'Offline')),
    interview_link TEXT,
    venue TEXT,
    interviewer_name VARCHAR(100),
    interviewer_role VARCHAR(50),
    round_status VARCHAR(20) DEFAULT 'Scheduled' CHECK (round_status IN ('Scheduled', 'Completed', 'Cancelled', 'Rescheduled')),
    feedback TEXT,
    score DECIMAL(5,2),
    passed BOOLEAN,
    FOREIGN KEY (application_id) REFERENCES student_applications(application_id) ON DELETE CASCADE
);

-- Placements Table (Final Results)
CREATE TABLE IF NOT EXISTS placements (
    placement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER UNIQUE NOT NULL,
    company_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    drive_id INTEGER,
    placement_date DATE NOT NULL,
    joining_date DATE,
    package_offered DECIMAL(10,2) NOT NULL,
    package_currency VARCHAR(3) DEFAULT 'INR',
    offer_letter_url TEXT,
    placement_status VARCHAR(20) DEFAULT 'Offer Accepted' CHECK (placement_status IN ('Offer Pending', 'Offer Accepted', 'Offer Declined', 'Joined', 'Left')),
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES companies(company_id),
    FOREIGN KEY (job_id) REFERENCES job_postings(job_id),
    FOREIGN KEY (drive_id) REFERENCES campus_drives(drive_id)
);

-- NEP Course Planning Table
CREATE TABLE IF NOT EXISTS nep_course_plans (
    plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    major_subject VARCHAR(50) NOT NULL,
    minor_subject VARCHAR(50),
    specialization VARCHAR(50),
    total_credits INTEGER DEFAULT 160,
    major_credits INTEGER DEFAULT 80,
    minor_credits INTEGER DEFAULT 40,
    skill_credits INTEGER DEFAULT 20,
    elective_credits INTEGER DEFAULT 20,
    planned_courses TEXT, -- JSON array of courses
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

-- AI Resume Templates Table
CREATE TABLE IF NOT EXISTS resume_templates (
    template_id INTEGER PRIMARY KEY AUTOINCREMENT,
    template_name VARCHAR(50) NOT NULL,
    template_description TEXT,
    template_html TEXT NOT NULL,
    template_css TEXT,
    category VARCHAR(20) DEFAULT 'Professional',
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Student Resumes Table
CREATE TABLE IF NOT EXISTS student_resumes (
    resume_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    template_id INTEGER,
    resume_title VARCHAR(100) NOT NULL,
    resume_data TEXT NOT NULL, -- JSON data
    resume_html TEXT,
    resume_pdf_path TEXT,
    ats_score INTEGER,
    is_primary BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (template_id) REFERENCES resume_templates(template_id)
);

-- Career Plans Table
CREATE TABLE IF NOT EXISTS career_plans (
    plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    target_role VARCHAR(100) NOT NULL,
    target_industry VARCHAR(50),
    target_companies TEXT, -- JSON array
    timeline_months INTEGER DEFAULT 24,
    current_step VARCHAR(50),
    skills_gap TEXT, -- JSON array
    action_items TEXT, -- JSON array
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

-- Placement Predictions Table
CREATE TABLE IF NOT EXISTS placement_predictions (
    prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    prediction_date DATE NOT NULL,
    placement_probability DECIMAL(5,2) CHECK (placement_probability BETWEEN 0 AND 100),
    predicted_companies TEXT, -- JSON array
    predicted_package DECIMAL(10,2),
    key_factors TEXT, -- JSON object
    model_version VARCHAR(20),
    confidence_score DECIMAL(5,2),
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

-- Chatbot Conversations Table
CREATE TABLE IF NOT EXISTS chatbot_conversations (
    conversation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_id VARCHAR(100) NOT NULL,
    user_message TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    message_type VARCHAR(20) DEFAULT 'text',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Notifications Table
CREATE TABLE IF NOT EXISTS notifications (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    notification_type VARCHAR(30) NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT 0,
    action_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Audit Log Table
CREATE TABLE IF NOT EXISTS audit_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action VARCHAR(50) NOT NULL,
    entity_type VARCHAR(50),
    entity_id INTEGER,
    old_values TEXT,
    new_values TEXT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

-- Indexes for Performance
CREATE INDEX idx_students_user_id ON students(user_id);
CREATE INDEX idx_students_department ON students(department);
CREATE INDEX idx_students_placement_status ON students(placement_status);
CREATE INDEX idx_jobs_company_id ON job_postings(company_id);
CREATE INDEX idx_jobs_is_active ON job_postings(is_active);
CREATE INDEX idx_applications_student_id ON student_applications(student_id);
CREATE INDEX idx_applications_job_id ON student_applications(job_id);
CREATE INDEX idx_applications_status ON student_applications(application_status);
CREATE INDEX idx_interviews_application_id ON interview_rounds(application_id);
CREATE INDEX idx_drives_college_id ON campus_drives(college_id);
CREATE INDEX idx_drives_company_id ON campus_drives(company_id);
CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_is_read ON notifications(is_read);
