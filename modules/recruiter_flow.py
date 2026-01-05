import streamlit as st
import pandas as pd

class RecruiterFlow:
    def __init__(self):
        self.recruiter_data = self.initialize_recruiter_data()
    
    def initialize_recruiter_data(self):
        """Initialize recruiter data"""
        return {
            "company_profile": {},
            "job_postings": [],
            "candidates": [],
            "interviews": []
        }
    
    def display(self):
        """Display recruiter workflow"""
        st.header("💼 Recruiter Hiring Platform")
        
        # Get current step
        from modules.workflow_manager import WorkflowManager
        workflow = WorkflowManager()
        current_step = workflow.workflows["recruiter"]["current_step"]
        
        # Display step
        if current_step == 1:
            self.step1_company_profile()
        elif current_step == 2:
            self.step2_job_posting()
        elif current_step == 3:
            self.step3_candidate_search()
        elif current_step == 4:
            self.step4_ai_screening()
        elif current_step == 5:
            self.step5_interview_scheduling()
        elif current_step == 6:
            self.step6_candidate_evaluation()
        elif current_step == 7:
            self.step7_offer_management()
        elif current_step == 8:
            self.step8_hiring_analytics()
    
    def step1_company_profile(self):
        """Step 1: Company Profile"""
        st.subheader("🏢 Company Profile Setup")
        
        with st.form("company_profile_form"):
            company_name = st.text_input("Company Name*")
            industry = st.selectbox("Industry*",
                ["IT/Software", "Finance/Banking", "Consulting", "Manufacturing",
                 "E-commerce", "Healthcare", "Education", "Automotive"])
            website = st.text_input("Website")
            
            col1, col2 = st.columns(2)
            with col1:
                contact_person = st.text_input("Contact Person*")
                email = st.text_input("Email*")
            with col2:
                phone = st.text_input("Phone*")
                hr_email = st.text_input("HR Email for Applications")
            
            company_description = st.text_area("Company Description", height=150)
            
            if st.form_submit_button("💾 Save Company Profile"):
                self.recruiter_data["company_profile"] = {
                    "name": company_name,
                    "industry": industry,
                    "website": website,
                    "contact": {
                        "person": contact_person,
                        "email": email,
                        "phone": phone,
                        "hr_email": hr_email
                    },
                    "description": company_description
                }
                st.success("Company profile saved!")
    
    def step2_job_posting(self):
        """Step 2: Job Posting"""
        st.subheader("📋 Create Job Posting")
        
        if not self.recruiter_data["company_profile"]:
            st.warning("Please complete company profile first")
            return
        
        with st.form("job_posting_form"):
            job_title = st.text_input("Job Title*", "Software Development Engineer")
            
            col1, col2 = st.columns(2)
            with col1:
                job_type = st.selectbox("Job Type*", 
                    ["Full-time", "Internship", "Contract", "Part-time"])
                location = st.text_input("Location*", "Bangalore")
            with col2:
                salary = st.number_input("Salary (LPA)", 0.0, 50.0, 12.0, 1.0)
                vacancies = st.number_input("Vacancies", 1, 100, 5)
            
            # Requirements
            st.subheader("Requirements")
            cgpa_min = st.number_input("Minimum CGPA", 0.0, 10.0, 7.0, 0.1)
            backlogs_allowed = st.number_input("Maximum Backlogs Allowed", 0, 10, 2)
            
            required_skills = st.multiselect("Required Skills",
                ["Python", "Java", "C++", "JavaScript", "React", "SQL",
                 "Machine Learning", "Data Analysis", "AWS", "Communication",
                 "Problem Solving", "Teamwork"],
                default=["Python", "SQL"])
            
            job_description = st.text_area("Job Description*", height=200,
                value="We are looking for a talented software engineer...")
            
            if st.form_submit_button("📢 Post Job"):
                job_id = f"JOB{len(self.recruiter_data['job_postings']) + 1:03d}"
                self.recruiter_data["job_postings"].append({
                    "id": job_id,
                    "title": job_title,
                    "type": job_type,
                    "location": location,
                    "salary": salary,
                    "vacancies": vacancies,
                    "requirements": {
                        "cgpa_min": cgpa_min,
                        "backlogs_allowed": backlogs_allowed,
                        "skills": required_skills
                    },
                    "description": job_description,
                    "posted_date": pd.Timestamp.now().strftime("%Y-%m-%d")
                })
                st.success(f"Job posted successfully! Job ID: {job_id}")
    
    # ... (Other steps would follow similar pattern)
