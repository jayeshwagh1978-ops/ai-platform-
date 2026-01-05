import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

class PMInternshipAI:
    def __init__(self):
        self.internship_data = self.load_internship_data()
        self.skills_required = {
            "Technical": ["SQL", "Data Analysis", "A/B Testing", "Metrics Definition", 
                         "API Understanding", "Basic Coding"],
            "Business": ["Market Research", "Competitive Analysis", "ROI Calculation", 
                        "Business Case Development", "Stakeholder Management"],
            "Product": ["PRD Writing", "User Stories", "Wireframing", "Roadmapping",
                       "Prioritization", "User Research"]
        }
    
    def load_internship_data(self):
        """Load sample internship data"""
        data = {
            'internship_id': ['PM001', 'PM002', 'PM003', 'PM004', 'PM005'],
            'company': ['Google', 'Microsoft', 'Amazon', 'Adobe', 'Swiggy'],
            'role': ['APM Intern', 'Product Intern', 'Product Management Intern', 
                    'Technical PM Intern', 'Product Intern'],
            'location': ['Bangalore', 'Hyderabad', 'Mumbai', 'Noida', 'Bangalore'],
            'duration': ['3 months', '6 months', '4 months', '3 months', '2 months'],
            'stipend': [80000, 70000, 65000, 75000, 60000],
            'application_deadline': ['2024-03-15', '2024-04-10', '2024-03-31', 
                                    '2024-04-15', '2024-05-01'],
            'eligibility_cgpa': [8.0, 7.5, 7.0, 8.5, 7.0],
            'requirements': [
                'Strong analytical skills, SQL knowledge, 3rd/4th year students',
                'Product thinking, communication skills, any year',
                'Technical background, customer obsession, penultimate year',
                'Technical degree, design thinking, final year',
                'Growth mindset, data-driven, any year'
            ]
        }
        return pd.DataFrame(data)
    
    def display(self):
        """Display PM Internship AI module"""
        st.header("💼 AI-Powered PM Internship Assistant")
        
        tab1, tab2, tab3 = st.tabs(["🔍 Find Internships", "🎯 PM Skill Analyzer", "📝 Application Assistant"])
        
        with tab1:
            self.find_internships()
        
        with tab2:
            self.skill_analyzer()
        
        with tab3:
            self.application_assistant()
    
    def find_internships(self):
        """Find and filter PM internships"""
        st.subheader("Find Product Management Internships")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            location_filter = st.multiselect("Location", 
                ["All"] + list(self.internship_data['location'].unique()),
                default=["All"])
        
        with col2:
            cgpa_filter = st.slider("Minimum CGPA Required", 0.0, 10.0, 7.0, 0.5)
        
        with col3:
            stipend_filter = st.slider("Minimum Stipend (₹)", 0, 100000, 50000, 5000)
        
        # Apply filters
        filtered_data = self.internship_data.copy()
        
        if "All" not in location_filter and location_filter:
            filtered_data = filtered_data[filtered_data['location'].isin(location_filter)]
        
        filtered_data = filtered_data[filtered_data['eligibility_cgpa'] <= cgpa_filter]
        filtered_data = filtered_data[filtered_data['stipend'] >= stipend_filter]
        
        # Display internships
        st.subheader(f"Found {len(filtered_data)} Internships")
        
        for _, internship in filtered_data.iterrows():
            with st.expander(f"**{internship['role']} at {internship['company']}**"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Location:** {internship['location']}")
                    st.write(f"**Duration:** {internship['duration']}")
                    st.write(f"**Stipend:** ₹{internship['stipend']:,}/month")
                
                with col2:
                    st.write(f"**Deadline:** {internship['application_deadline']}")
                    st.write(f"**Min CGPA:** {internship['eligibility_cgpa']}")
                    st.write(f"**ID:** {internship['internship_id']}")
                
                st.write(f"**Requirements:** {internship['requirements']}")
                
                # Apply button
                if st.button(f"Apply to {internship['company']}", 
                           key=f"apply_{internship['internship_id']}"):
                    st.success(f"Application started for {internship['role']}!")
                    st.session_state.current_application = internship['internship_id']
    
    def skill_analyzer(self):
        """Analyze PM skills and suggest improvements"""
        st.subheader("PM Skill Gap Analyzer")
        
        st.info("""
        Assess your current Product Management skills and get personalized recommendations 
        for internship readiness.
        """)
        
        # Self-assessment
        st.markdown("### Self-Assessment")
        
        skill_levels = {}
        for category, skills in self.skills_required.items():
            st.markdown(f"#### {category} Skills")
            for skill in skills:
                skill_levels[skill] = st.select_slider(
                    skill,
                    options=["Beginner", "Intermediate", "Advanced"],
                    value="Beginner",
                    key=f"skill_{skill}"
                )
        
        # Analyze button
        if st.button("🔍 Analyze Skill Gaps"):
            # Calculate scores
            beginner_count = sum(1 for level in skill_levels.values() if level == "Beginner")
            intermediate_count = sum(1 for level in skill_levels.values() if level == "Intermediate")
            advanced_count = sum(1 for level in skill_levels.values() if level == "Advanced")
            
            total_score = (beginner_count * 1 + intermediate_count * 2 + advanced_count * 3)
            max_score = len(skill_levels) * 3
            percentage = (total_score / max_score) * 100
            
            # Display results
            st.subheader("Analysis Results")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Overall Score", f"{percentage:.1f}%")
            with col2:
                st.metric("Beginner Skills", beginner_count)
            with col3:
                st.metric("Advanced Skills", advanced_count)
            
            # Progress bars for each category
            st.subheader("Category-wise Analysis")
            
            for category, skills in self.skills_required.items():
                cat_skills = {k: v for k, v in skill_levels.items() if k in skills}
                cat_beginner = sum(1 for level in cat_skills.values() if level == "Beginner")
                cat_total = len(cat_skills)
                cat_score = 100 * (cat_total - cat_beginner * 0.5) / cat_total
                
                st.write(f"**{category}:** {cat_score:.1f}%")
                st.progress(cat_score / 100)
            
            # Recommendations
            st.subheader("🤖 AI Recommendations")
            
            # Find weakest category
            weakest_cat = min(self.skills_required.keys(), 
                            key=lambda cat: sum(1 for skill in self.skills_required[cat] 
                                              if skill_levels.get(skill) == "Beginner"))
            
            recommendations = [
                f"**1. Focus on {weakest_cat} Skills:** Take online courses or work on projects",
                "**2. Build a Product Portfolio:** Create case studies of product improvements",
                "**3. Network with PMs:** Connect with product managers on LinkedIn",
                "**4. Read PM Books:** 'Cracking the PM Interview', 'Inspired'",
                "**5. Practice Case Studies:** Solve product case studies regularly"
            ]
            
            for rec in recommendations:
                st.info(rec)
    
    def application_assistant(self):
        """Assist with PM internship applications"""
        st.subheader("PM Internship Application Assistant")
        
        st.warning("""
        ⚠️ **Important:** PM internships are highly competitive. 
        Use this tool to strengthen your application.
        """)
        
        # Application form
        with st.form("pm_application_form"):
            st.markdown("### Application Details")
            
            col1, col2 = st.columns(2)
            with col1:
                target_company = st.text_input("Target Company*")
                target_role = st.selectbox("Target Role*",
                    ["APM Intern", "Product Intern", "Technical PM Intern", 
                     "Growth PM Intern", "Product Marketing Intern"])
            
            with col2:
                current_cgpa = st.number_input("Current CGPA*", 0.0, 10.0, 8.0, 0.1)
                graduation_year = st.number_input("Graduation Year*", 2024, 2030, 2025)
            
            # Why PM question
            st.markdown("### Why Product Management?")
            why_pm = st.text_area(
                "Explain why you want to pursue Product Management (100-200 words)*",
                height=150,
                value="I'm passionate about solving customer problems at scale..."
            )
            
            # Product sense question
            st.markdown("### Product Sense Test")
            product_question = st.selectbox(
                "Choose a product to analyze:",
                ["Instagram", "Uber", "Spotify", "Amazon", "Zoom", "Other"]
            )
            
            if product_question == "Other":
                product_question = st.text_input("Enter product name")
            
            product_analysis = st.text_area(
                f"What's one improvement you'd make to {product_question} and why?",
                height=150
            )
            
            # Resume upload
            st.markdown("### Upload Your Resume")
            resume_file = st.file_uploader("Upload your resume (PDF/DOCX)", 
                                         type=['pdf', 'docx'])
            
            if st.form_submit_button("🚀 Get AI Feedback on Application"):
                # Analyze application
                with st.spinner("AI is analyzing your application..."):
                    import time
                    time.sleep(3)
                    
                    # Generate feedback
                    st.success("Application Analysis Complete!")
                    
                    # Score application
                    score = 0
                    feedback_points = []
                    
                    # Check CGPA
                    if current_cgpa >= 8.0:
                        score += 20
                        feedback_points.append("✅ Good CGPA for PM roles")
                    else:
                        score += 10
                        feedback_points.append("⚠️ CGPA could be improved for competitive roles")
                    
                    # Check why PM answer length
                    if len(why_pm.split()) >= 100:
                        score += 30
                        feedback_points.append("✅ Comprehensive 'Why PM' answer")
                    else:
                        score += 15
                        feedback_points.append("⚠️ 'Why PM' answer could be more detailed")
                    
                    # Check product analysis
                    if len(product_analysis.split()) >= 50:
                        score += 30
                        feedback_points.append("✅ Good product thinking demonstrated")
                    else:
                        score += 15
                        feedback_points.append("⚠️ Product analysis needs more depth")
                    
                    # Resume check
                    if resume_file is not None:
                        score += 20
                        feedback_points.append("✅ Resume uploaded successfully")
                    else:
                        feedback_points.append("❌ Resume not uploaded - critical for applications")
                    
                    # Display results
                    st.subheader(f"Application Score: {score}/100")
                    st.progress(score / 100)
                    
                    st.subheader("Feedback Points")
                    for point in feedback_points:
                        st.write(point)
                    
                    # AI Suggestions
                    st.subheader("🤖 AI Suggestions for Improvement")
                    
                    suggestions = [
                        "**1. Strengthen your 'Why PM' story:** Connect personal experiences to PM skills",
                        f"**2. Deepen product analysis:** Research {product_question} more thoroughly",
                        "**3. Quantify achievements:** Add numbers to your resume wherever possible",
                        "**4. Practice PM interviews:** Do mock interviews with experienced PMs",
                        "**5. Network:** Reach out to current PMs at target companies"
                    ]
                    
                    for suggestion in suggestions:
                        st.info(suggestion)
