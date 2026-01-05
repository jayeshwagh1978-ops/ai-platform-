import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

class StudentFlow:
    def __init__(self):
        self.student_data = self.initialize_student_data()
        self.current_step = 1  # Initialize with default step
    
    def initialize_student_data(self):
        """Initialize student profile data"""
        return {
            "profile": {},
            "resume": {},
            "courses": {},
            "internships": [],
            "career_plan": {},
            "placement_prediction": {},
            "interviews": [],
            "placement_status": {}
        }
    
    def display(self):
        """Display complete student workflow"""
        st.header("👨‍🎓 Student Placement Journey")
        
        # Get current step from session state
        current_step = st.session_state.get('current_step_student', 1)
        self.current_step = current_step
        
        # Display step header
        step_names = {
            1: "🎯 Profile Creation",
            2: "📝 AI Resume Building", 
            3: "📚 NEP Course Planning",
            4: "💼 PM Internship Match",
            5: "🎯 Career Path Planning",
            6: "📊 Placement Prediction",
            7: "🤝 Interview Preparation",
            8: "✅ Placement Tracking"
        }
        
        # Create a progress header
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"Step {current_step}: {step_names[current_step]}")
        with col2:
            progress = current_step / 8
            st.progress(progress)
            st.caption(f"Step {current_step} of 8")
        
        # Display appropriate step
        if current_step == 1:
            self.step1_profile_creation()
        elif current_step == 2:
            self.step2_resume_building()
        elif current_step == 3:
            self.step3_course_planning()
        elif current_step == 4:
            self.step4_internship_matching()
        elif current_step == 5:
            self.step5_career_planning()
        elif current_step == 6:
            self.step6_placement_prediction()
        elif current_step == 7:
            self.step7_interview_preparation()
        elif current_step == 8:
            self.step8_placement_tracking()
        
        # Display navigation at the bottom
        self.display_workflow_navigation(current_step)
    
    def step1_profile_creation(self):
        """Step 1: Student Profile Creation"""
        st.info("Create your student profile to get started with placement preparation")
        
        with st.form("student_profile_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name*", placeholder="Enter your full name")
                roll_no = st.text_input("Roll Number*", placeholder="e.g., 20BCS001")
                email = st.text_input("Email*", placeholder="student@college.edu")
                phone = st.text_input("Phone Number", placeholder="+91 9876543210")
                
            with col2:
                department = st.selectbox("Department*", 
                    ["Computer Science", "Electrical Engineering", "Mechanical Engineering",
                     "Civil Engineering", "Information Technology", "Electronics"])
                semester = st.number_input("Current Semester*", 1, 10, 6)
                cgpa = st.number_input("Current CGPA*", 0.0, 10.0, 8.0, 0.1)
                backlogs = st.number_input("Number of Backlogs", 0, 10, 0)
            
            # Skills assessment
            st.subheader("Skills Assessment")
            technical_skills = st.multiselect("Technical Skills",
                ["Python", "Java", "C++", "JavaScript", "React", "Node.js", "SQL",
                 "Machine Learning", "Data Analysis", "AWS", "Docker", "Git"],
                default=["Python", "SQL"])
            
            # Career interests
            st.subheader("Career Interests")
            career_interests = st.multiselect("Areas of Interest",
                ["Software Development", "Data Science", "Product Management",
                 "Research", "Consulting", "Entrepreneurship", "Higher Studies"])
            
            if st.form_submit_button("✅ Save Profile & Continue", width='stretch'):
                # Save profile data
                self.student_data["profile"] = {
                    "name": name,
                    "roll_no": roll_no,
                    "email": email,
                    "phone": phone,
                    "department": department,
                    "semester": semester,
                    "cgpa": cgpa,
                    "backlogs": backlogs,
                    "technical_skills": technical_skills,
                    "career_interests": career_interests,
                    "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                st.success("Profile created successfully! Moving to Resume Building...")
                st.balloons()
                # Update workflow step
                st.session_state.current_step_student = 2
                st.rerun()
    
    def step2_resume_building(self):
        """Step 2: AI Resume Building"""
        st.info("Build your professional resume with AI assistance")
        
        # Show profile summary if exists
        if self.student_data["profile"]:
            with st.expander("📋 Your Profile Summary", expanded=False):
                profile = self.student_data["profile"]
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Name:** {profile['name']}")
                    st.write(f"**Roll No:** {profile['roll_no']}")
                    st.write(f"**Department:** {profile['department']}")
                with col2:
                    st.write(f"**CGPA:** {profile['cgpa']}")
                    st.write(f"**Skills:** {', '.join(profile['technical_skills'][:3])}")
                    st.write(f"**Interests:** {', '.join(profile['career_interests'])}")
        
        # Simple resume builder
        st.subheader("Build Your Resume")
        
        with st.form("resume_form"):
            # Education
            st.write("**Education Details**")
            college = st.text_input("College/University", "ABC Engineering College")
            degree = st.text_input("Degree", "Bachelor of Technology")
            specialization = st.text_input("Specialization", "Computer Science")
            graduation_year = st.number_input("Graduation Year", 2020, 2030, 2024)
            
            # Projects
            st.write("**Projects**")
            project1 = st.text_input("Project 1 Title", "AI Placement Predictor")
            project1_desc = st.text_area("Project 1 Description", 
                "Developed an AI model to predict placement probability based on student profile")
            
            # Skills
            st.write("**Skills**")
            skills = st.text_area("Your Skills (comma-separated)", 
                "Python, Machine Learning, Data Analysis, SQL, Communication")
            
            if st.form_submit_button("💾 Generate Resume Preview", width='stretch'):
                self.student_data["resume"] = {
                    "education": {
                        "college": college,
                        "degree": degree,
                        "specialization": specialization,
                        "graduation_year": graduation_year
                    },
                    "projects": [
                        {"title": project1, "description": project1_desc}
                    ],
                    "skills": [s.strip() for s in skills.split(",")]
                }
                st.success("Resume details saved!")
        
        # Show resume preview if data exists
        if self.student_data.get("resume"):
            with st.expander("👀 Resume Preview", expanded=True):
                self.preview_resume()
    
    def preview_resume(self):
        """Preview the resume"""
        profile = self.student_data.get("profile", {})
        resume = self.student_data.get("resume", {})
        
        html = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px; border: 1px solid #ddd; border-radius: 10px; background: white;">
            <h1 style="color: #2c3e50;">{profile.get('name', 'Your Name')}</h1>
            <p>{profile.get('email', 'email@example.com')} • {profile.get('phone', 'Phone')}</p>
            
            <h2 style="color: #3498db; border-bottom: 2px solid #3498db;">Education</h2>
            <p><strong>{resume.get('education', {}).get('degree', 'Degree')} in {resume.get('education', {}).get('specialization', 'Specialization')}</strong></p>
            <p>{resume.get('education', {}).get('college', 'College')} • CGPA: {profile.get('cgpa', 'N/A')} • Graduation: {resume.get('education', {}).get('graduation_year', 'Year')}</p>
            
            <h2 style="color: #3498db; border-bottom: 2px solid #3498db;">Skills</h2>
            <p>{', '.join(resume.get('skills', ['Skills']))}</p>
        </div>
        """
        
        st.markdown(html, unsafe_allow_html=True)
    
    def step3_course_planning(self):
        """Step 3: NEP Course Planning"""
        st.info("Plan your courses according to NEP 2020 guidelines")
        
        department = self.student_data["profile"].get("department", "Computer Science")
        
        st.write(f"**Recommended Course Plan for {department}**")
        
        # Simple course selection
        major_courses = st.multiselect("Major Courses",
            ["Data Structures", "Algorithms", "Database Systems", "Computer Networks", 
             "Operating Systems", "Software Engineering"],
            default=["Data Structures", "Algorithms", "Database Systems"])
        
        minor_options = ["Business Management", "Data Science", "Psychology", "Economics"]
        minor_selected = st.selectbox("Minor Specialization", minor_options)
        
        skill_courses = st.multiselect("Skill Enhancement Courses",
            ["Entrepreneurship", "Communication Skills", "Research Methodology", "Project Management"])
        
        if st.button("💾 Save Course Plan", width='stretch'):
            self.student_data["courses"] = {
                "major_courses": major_courses,
                "minor": minor_selected,
                "skill_courses": skill_courses
            }
            st.success("Course plan saved!")
    
    def step4_internship_matching(self):
        """Step 4: PM Internship Matching"""
        st.info("Find Product Management internship opportunities")
        
        # Sample internships
        internships = [
            {"company": "Google", "role": "APM Intern", "location": "Bangalore", "match": "85%"},
            {"company": "Microsoft", "role": "Product Intern", "location": "Hyderabad", "match": "78%"},
            {"company": "Amazon", "role": "PM Intern", "location": "Mumbai", "match": "72%"}
        ]
        
        for intern in internships:
            with st.expander(f"{intern['company']} - {intern['role']} (Match: {intern['match']})"):
                st.write(f"**Location:** {intern['location']}")
                st.write(f"**Match Score:** {intern['match']}")
                if st.button(f"Apply to {intern['company']}", key=f"apply_{intern['company']}", width='stretch'):
                    st.success(f"Application started for {intern['role']}!")
    
    def step5_career_planning(self):
        """Step 5: Career Path Planning"""
        st.info("Plan your career path based on your profile")
        
        profile = self.student_data.get("profile", {})
        
        st.write("**Recommended Career Paths:**")
        
        # Simple career recommendations
        if "Software Development" in profile.get("career_interests", []):
            st.success("**Software Development Engineer**")
            st.write("Path: Junior Developer → Senior Developer → Tech Lead → Engineering Manager")
            st.write("Avg Package: 8-15 LPA (Entry) → 30-50+ LPA (Senior)")
        
        if "Data Science" in profile.get("career_interests", []):
            st.info("**Data Scientist**")
            st.write("Path: Data Analyst → Data Scientist → Senior Data Scientist → Head of Analytics")
            st.write("Avg Package: 6-12 LPA (Entry) → 25-40+ LPA (Senior)")
        
        # Career goal setting
        st.subheader("Set Your Career Goals")
        target_role = st.text_input("Target Role", "Software Development Engineer")
        timeline = st.selectbox("Timeline", ["6 months", "1 year", "2 years", "3 years"])
        
        if st.button("🎯 Save Career Goals", width='stretch'):
            self.student_data["career_plan"] = {
                "target_role": target_role,
                "timeline": timeline
            }
            st.success("Career goals saved!")
    
    def step6_placement_prediction(self):
        """Step 6: Placement Prediction"""
        st.info("Predict your placement probability")
        
        profile = self.student_data.get("profile", {})
        
        # Simple prediction based on CGPA
        cgpa = profile.get("cgpa", 7.0)
        if cgpa >= 8.5:
            probability = "85-95%"
            recommendation = "🎉 Excellent! High chance of placement in top companies"
        elif cgpa >= 7.5:
            probability = "70-85%"
            recommendation = "📈 Good potential with proper preparation"
        elif cgpa >= 6.5:
            probability = "50-70%"
            recommendation = "📚 Needs focused effort and skill improvement"
        else:
            probability = "30-50%"
            recommendation = "🎯 Requires immediate action on academics and skills"
        
        st.metric("Placement Probability", probability)
        st.info(recommendation)
        
        # Save prediction
        self.student_data["placement_prediction"] = {
            "probability": probability,
            "calculated_date": datetime.now().strftime("%Y-%m-%d")
        }
    
    def step7_interview_preparation(self):
        """Step 7: Interview Preparation"""
        st.info("Prepare for technical and HR interviews")
        
        st.write("**Common Interview Questions:**")
        
        questions = [
            "Tell me about yourself",
            "Why do you want to work here?",
            "What are your strengths and weaknesses?",
            "Explain a challenging project you worked on"
        ]
        
        for q in questions:
            with st.expander(f"❓ {q}"):
                answer = st.text_area("Your Answer", key=f"answer_{q}", height=100)
                if st.button("Get AI Feedback", key=f"feedback_{q}", width='stretch'):
                    st.info("""
                    **AI Feedback:**
                    - Structure your answer clearly
                    - Provide specific examples
                    - Connect to the company's values
                    """)
    
    def step8_placement_tracking(self):
        """Step 8: Placement Tracking"""
        st.success("🎉 Congratulations! You've completed your placement journey")
        
        # Summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Profile", "✅ Complete")
        with col2:
            st.metric("Resume", "✅ Built")
        with col3:
            st.metric("Career Plan", "✅ Set")
        
        # Final recommendations
        st.subheader("🎯 Final Recommendations")
        st.write("1. ✅ Continue skill development")
        st.write("2. ✅ Network with professionals")
        st.write("3. ✅ Prepare for interviews")
        st.write("4. ✅ Stay updated with industry trends")
        
        # Restart option
        if st.button("🔄 Start New Journey", width='stretch'):
            self.student_data = self.initialize_student_data()
            st.session_state.current_step_student = 1
            st.rerun()
    
    def display_workflow_navigation(self, current_step):
        """Display navigation buttons"""
        st.divider()
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if current_step > 1 and st.button("⬅️ Previous Step", width='stretch'):
                st.session_state.current_step_student = current_step - 1
                st.rerun()
        
        with col3:
            if current_step < 8 and st.button("Next Step ➡️", width='stretch'):
                st.session_state.current_step_student = current_step + 1
                st.rerun()
