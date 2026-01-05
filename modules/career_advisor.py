import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

class CareerAdvisor:
    def __init__(self):
        self.career_paths = self.load_career_paths()
        self.skills_data = self.load_skills_data()
    
    def load_career_paths(self):
        """Load career paths data"""
        return {
            "Software Development": {
                "entry_level": ["Software Engineer", "Frontend Developer", "Backend Developer"],
                "mid_level": ["Senior Developer", "Tech Lead", "Architect"],
                "senior_level": ["Engineering Manager", "CTO", "VP Engineering"],
                "skills": ["Programming", "System Design", "Algorithms", "Testing"],
                "growth": "High",
                "avg_salary_entry": "8-12 LPA",
                "avg_salary_senior": "30-50+ LPA"
            },
            "Data Science": {
                "entry_level": ["Data Analyst", "Business Analyst", "Junior Data Scientist"],
                "mid_level": ["Data Scientist", "ML Engineer", "Data Engineer"],
                "senior_level": ["Lead Data Scientist", "Head of Analytics", "Chief Data Officer"],
                "skills": ["Statistics", "Machine Learning", "Python/R", "Data Visualization"],
                "growth": "Very High",
                "avg_salary_entry": "6-10 LPA",
                "avg_salary_senior": "25-40+ LPA"
            },
            "Product Management": {
                "entry_level": ["Associate Product Manager", "Product Analyst"],
                "mid_level": ["Product Manager", "Senior Product Manager"],
                "senior_level": ["Director of Product", "VP Product", "CPO"],
                "skills": ["Product Strategy", "User Research", "Data Analysis", "Stakeholder Management"],
                "growth": "High",
                "avg_salary_entry": "10-15 LPA",
                "avg_salary_senior": "40-70+ LPA"
            }
        }
    
    def load_skills_data(self):
        """Load skills demand data"""
        return {
            "High Demand": ["AI/ML", "Cloud Computing", "Cybersecurity", "Data Science", "DevOps"],
            "Growing": ["Blockchain", "IoT", "AR/VR", "Quantum Computing", "Edge Computing"],
            "Stable": ["Web Development", "Mobile Development", "Database Management", "Testing"],
            "Declining": ["Legacy Systems", "Manual Testing", "Traditional IT Support"]
        }
    
    def display(self):
        """Display Career Advisor module"""
        st.header("🎯 AI Career Advisor")
        
        st.info("""
        Get personalized career guidance based on your skills, interests, and market trends.
        Our AI analyzes thousands of career paths to find the best fit for you.
        """)
        
        tab1, tab2, tab3 = st.tabs(["🧭 Career Path Finder", "📈 Market Trends", "🎓 Education Planner"])
        
        with tab1:
            self.career_path_finder()
        
        with tab2:
            self.market_trends()
        
        with tab3:
            self.education_planner()
    
    def career_path_finder(self):
        """Career path recommendation system"""
        st.subheader("Find Your Ideal Career Path")
        
        # User profile
        st.markdown("### Your Profile")
        
        col1, col2 = st.columns(2)
        
        with col1:
            degree = st.selectbox(
                "Current/Major Degree:",
                ["Computer Science", "Electrical Engineering", "Mechanical Engineering",
                 "Civil Engineering", "Information Technology", "Electronics", "Other"]
            )
            
            year_of_study = st.selectbox(
                "Year of Study:",
                ["1st Year", "2nd Year", "3rd Year", "4th Year", "Graduated"]
            )
        
        with col2:
            cgpa = st.slider("Current CGPA:", 0.0, 10.0, 8.0, 0.1)
            interests = st.multiselect(
                "Areas of Interest:",
                ["Coding", "Data Analysis", "Design", "Management", "Research",
                 "Business", "Hardware", "Networking", "Security", "Cloud"]
            )
        
        # Skills assessment
        st.markdown("### Skills Assessment")
        
        technical_skills = st.multiselect(
            "Technical Skills (Select all that apply):",
            ["Python", "Java", "JavaScript", "C++", "SQL", "HTML/CSS", 
             "React", "Node.js", "AWS", "Docker", "Git", "Machine Learning",
             "Data Analysis", "Android", "iOS", "Cybersecurity"],
            default=["Python", "SQL"]
        )
        
        # Career preferences
        st.markdown("### Career Preferences")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            work_env = st.selectbox(
                "Preferred Work Environment:",
                ["Startup", "MNC", "Product Company", "Service Company", 
                 "Research Lab", "Government", "Freelance"]
            )
        
        with col2:
            salary_exp = st.selectbox(
                "Salary Expectations (Entry Level):",
                ["< 5 LPA", "5-8 LPA", "8-12 LPA", "12-15 LPA", "15+ LPA"]
            )
        
        with col3:
            location_pref = st.multiselect(
                "Location Preference:",
                ["Metro Cities", "Tier 2 Cities", "Remote", "Abroad", "Flexible"]
            )
        
        if st.button("🔍 Find Career Paths", type="primary"):
            with st.spinner("Analyzing your profile against career paths..."):
                # Simulate analysis
                import time
                time.sleep(2)
                
                # Get recommendations
                recommendations = self.analyze_career_paths(
                    degree, interests, technical_skills, work_env
                )
                
                st.success("Career Analysis Complete!")
                
                # Display recommendations
                st.subheader("🎯 Top Career Recommendations")
                
                for i, (career, details) in enumerate(recommendations.items()):
                    with st.expander(f"**{i+1}. {career}**", expanded=i==0):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Career Progression:**")
                            st.write(f"• **Entry:** {', '.join(details['entry_level'][:2])}")
                            st.write(f"• **Mid:** {', '.join(details['mid_level'][:2])}")
                            st.write(f"• **Senior:** {', '.join(details['senior_level'][:2])}")
                            
                            st.write("**Growth Potential:**", details['growth'])
                        
                        with col2:
                            st.write("**Salary Range:**")
                            st.write(f"• **Entry:** {details['avg_salary_entry']}")
                            st.write(f"• **Senior:** {details['avg_salary_senior']}")
                        
                        # Skills match
                        st.write("**Key Skills Required:**")
                        for skill in details['skills']:
                            status = "✅" if skill.lower() in [s.lower() for s in technical_skills] else "📚"
                            st.write(f"{status} {skill}")
                        
                        # Action plan
                        st.write("**Recommended Action Plan:**")
                        st.info(f"""
                        1. Complete courses in {details['skills'][0]} and {details['skills'][1]}
                        2. Build 2-3 projects demonstrating these skills
                        3. Apply for {details['entry_level'][0]} roles
                        4. Network with professionals in this field
                        """)
    
    def analyze_career_paths(self, degree, interests, skills, work_env):
        """Analyze and recommend career paths"""
        # Simple matching logic
        recommendations = {}
        
        if any(skill in ["Python", "Machine Learning", "Data Analysis"] for skill in skills):
            if "Data Analysis" in interests or "Research" in interests:
                recommendations["Data Science"] = self.career_paths["Data Science"]
        
        if any(skill in ["Python", "Java", "JavaScript", "React"] for skill in skills):
            if "Coding" in interests or "Design" in interests:
                recommendations["Software Development"] = self.career_paths["Software Development"]
        
        if "Management" in interests or "Business" in interests:
            recommendations["Product Management"] = self.career_paths["Product Management"]
        
        # If no specific match, show all
        if not recommendations:
            recommendations = self.career_paths
        
        return recommendations
    
    def market_trends(self):
        """Display job market trends"""
        st.subheader("📈 Current Job Market Trends")
        
        # Skills demand
        st.markdown("### Skills in Demand (2024)")
        
        for demand_level, skills in self.skills_data.items():
            with st.expander(f"{demand_level} Skills"):
                cols = st.columns(3)
                for idx, skill in enumerate(skills):
                    with cols[idx % 3]:
                        st.info(skill)
        
        # Salary trends
        st.markdown("### Salary Trends by Role")
        
        salary_data = pd.DataFrame({
            'Role': ['Software Engineer', 'Data Scientist', 'Product Manager', 
                    'DevOps Engineer', 'Cloud Architect', 'ML Engineer'],
            'Entry Level (LPA)': [8, 10, 12, 9, 11, 12],
            'Mid Level (LPA)': [18, 22, 25, 20, 28, 24],
            'Senior Level (LPA)': [35, 40, 50, 38, 55, 45],
            'Growth (YoY)': ['15%', '20%', '18%', '22%', '25%', '30%']
        })
        
        st.dataframe(salary_data, use_container_width=True)
        
        # Industry trends
        st.markdown("### Emerging Industries")
        
        trends = [
            ("🌱 **Green Tech**", "Renewable energy, EVs, sustainable solutions", "High"),
            ("🤖 **AI & Automation**", "Generative AI, process automation, robotics", "Very High"),
            ("🔗 **Web3 & Blockchain**", "DeFi, NFTs, decentralized applications", "Moderate"),
            ("☁️ **Cloud Computing**", "Multi-cloud, edge computing, serverless", "High"),
            ("🛡️ **Cybersecurity**", "Zero trust, cloud security, IoT security", "Very High")
        ]
        
        for trend, description, growth in trends:
            with st.expander(f"{trend} - Growth: {growth}"):
                st.write(description)
    
    def education_planner(self):
        """Education and certification planner"""
        st.subheader("🎓 Education & Certification Planner")
        
        st.info("""
        Plan your further education and certifications based on your career goals.
        Certifications can significantly boost your employability.
        """)
        
        # Select career path for planning
        selected_career = st.selectbox(
            "Select Career Path for Education Planning:",
            list(self.career_paths.keys())
        )
        
        if selected_career:
            career_info = self.career_paths[selected_career]
            
            # Recommended education path
            st.markdown(f"### Education Path for {selected_career}")
            
            education_path = {
                "Undergraduate": {
                    "Computer Science": "Best foundation",
                    "Related Engineering": "Good alternative",
                    "Mathematics/Statistics": "For Data Science track"
                },
                "Postgraduate": {
                    "M.Tech/MS": "For specialization",
                    "MBA": "For management track",
                    "PhD": "For research careers"
                },
                "Online Certifications": self.get_certifications(selected_career)
            }
            
            for level, options in education_path.items():
                with st.expander(f"{level} Options"):
                    if isinstance(options, dict):
                        for option, desc in options.items():
                            st.write(f"**{option}:** {desc}")
                    else:
                        st.write(options)
            
            # Timeline planner
            st.markdown("### Suggested Timeline")
            
            timeline_data = pd.DataFrame({
                'Year': ['Year 1-2', 'Year 3-4', 'Year 5-6', 'Year 7+'],
                'Focus': ['Build Foundation', 'Specialize & Intern', 'Gain Experience', 'Leadership & Advanced'],
                'Actions': [
                    'Core courses, basic projects, programming skills',
                    'Advanced courses, internships, certifications',
                    'Full-time role, skill enhancement, networking',
                    'Senior roles, management, strategic thinking'
                ]
            })
            
            st.dataframe(timeline_data, use_container_width=True)
    
    def get_certifications(self, career):
        """Get recommended certifications for career"""
        certs = {
            "Software Development": [
                "AWS Certified Developer",
                "Google Professional Cloud Developer",
                "Microsoft Certified: Azure Developer",
                "Oracle Java Certifications"
            ],
            "Data Science": [
                "Google Professional Data Engineer",
                "AWS Certified Data Analytics",
                "Microsoft Certified: Azure Data Scientist",
                "TensorFlow Developer Certificate"
            ],
            "Product Management": [
                "Pragmatic Marketing Certification",
                "Product School Certification",
                "AIPMM Certified Product Manager",
                "Stanford Innovation & Entrepreneurship"
            ]
        }
        
        return "\n".join([f"• {cert}" for cert in certs.get(career, [])])
