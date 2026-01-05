from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any
import json

@dataclass
class User:
    user_id: Optional[int] = None
    username: str = ""
    email: str = ""
    password_hash: str = ""
    role: str = ""
    full_name: str = ""
    phone: Optional[str] = None
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    is_active: bool = True
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})

@dataclass
class Student:
    student_id: Optional[int] = None
    user_id: int = 0
    roll_number: str = ""
    department: str = ""
    semester: Optional[int] = None
    cgpa: Optional[float] = None
    backlogs: int = 0
    graduation_year: Optional[int] = None
    resume_file_path: Optional[str] = None
    github_profile: Optional[str] = None
    linkedin_profile: Optional[str] = None
    portfolio_website: Optional[str] = None
    placement_status: str = "Not Placed"
    placement_company_id: Optional[int] = None
    placement_package: Optional[float] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Student':
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})

@dataclass
class Company:
    company_id: Optional[int] = None
    company_name: str = ""
    industry: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    founded_year: Optional[int] = None
    employee_count: Optional[str] = None
    headquarters: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    hr_email: Optional[str] = None
    is_verified: bool = False
    registered_at: Optional[datetime] = None

@dataclass
class JobPosting:
    job_id: Optional[int] = None
    company_id: int = 0
    job_title: str = ""
    job_description: str = ""
    job_type: str = "Full-time"
    location: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    salary_currency: str = "INR"
    vacancies: int = 1
    min_cgpa: Optional[float] = None
    max_backlogs: int = 0
    required_skills: Optional[List[str]] = None
    benefits: Optional[str] = None
    application_deadline: Optional[datetime] = None
    posted_date: Optional[datetime] = None
    is_active: bool = True
    
    def to_dict(self) -> Dict:
        data = self.__dict__.copy()
        if self.required_skills:
            data['required_skills'] = ','.join(self.required_skills)
        return {k: v for k, v in data.items() if v is not None}
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'JobPosting':
        data = data.copy()
        if 'required_skills' in data and data['required_skills']:
            data['required_skills'] = data['required_skills'].split(',')
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})

@dataclass
class StudentApplication:
    application_id: Optional[int] = None
    student_id: int = 0
    job_id: int = 0
    drive_id: Optional[int] = None
    application_date: Optional[datetime] = None
    application_status: str = "Applied"
    resume_version: Optional[str] = None
    cover_letter: Optional[str] = None
    applied_via: str = "Portal"
    notes: Optional[str] = None

# More models can be added as needed...
