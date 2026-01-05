import streamlit as st
import pandas as pd

class NEPAdvisor:
    def __init__(self):
        self.nep_guidelines = self.load_nep_guidelines()
    
    def load_nep_guidelines(self):
        """Load NEP guidelines and major/minor combinations"""
        return {
            "Computer Science": {
                "minors": ["Mathematics", "Economics", "Psychology", "Business Management", "Data Science"],
                "credits": 160,
                "exit_options": ["Certificate (1 year)", "Diploma (2 years)", "Bachelor's (3-4 years)"],
                "skill_components": ["Coding", "Problem Solving", "Logic Building"]
            },
            "Electrical Engineering": {
                "minors": ["Computer Science", "Robotics", "Renewable Energy", "Business Management"],
                "credits": 165,
                "exit_options": ["Diploma (2 years)", "Bachelor's (4 years)"],
                "skill_components": ["Circuit Design", "Embedded Systems", "Power Systems"]
            },
            "Mechanical Engineering": {
                "minors": ["Automotive", "Aerospace", "Robotics", "Business Management"],
                "credits": 168,
                "exit_options": ["Diploma (2 years)", "Bachelor's (4 years)"],
                "skill_components": ["CAD", "Thermodynamics", "Manufacturing"]
            }
        }
    
    def display(self):
        """Display NEP Advisor module"""
        st.header("📚 NEP-Aligned Major/Minor Advisor")
        
        st.info("""
        **National Education Policy (NEP) 2020** emphasizes:
        - Multidisciplinary education
        - Multiple entry/exit options
        - Credit-based flexible system
        - Skill development integrated with academics
        """)
        
        tab1, tab2, tab3 = st.tabs(["🎯 Major/Minor Advisor", "📊 NEP Guidelines", "🎓 Exit Options"])
        
        with tab1:
            self.major_minor_advisor()
        
        with tab2:
            self.nep_guidelines_display()
        
        with tab3:
            self.exit_options()
    
    def major_minor_advisor(self):
        """Major/Minor combination advisor"""
        st.subheader("Find Your Perfect Major/Minor Combination")
        
        # Student input
        col1, col2 = st.columns(2)
        
        with col1:
            interests = st.multiselect(
                "Select your interests:",
                ["Technology", "Business", "Research", "Creative Arts", 
                 "Mathematics", "Science", "Social Sciences", "Engineering"]
            )
        
        with col2:
            career_goals = st.selectbox(
                "Career Goals:",
                ["Industry Job", "Higher Studies", "Research", "Entrepreneurship", 
                 "Government Job", "Startup", "Consulting"]
            )
        
        # Skills assessment
        st.markdown("### Skills Assessment")
        skills = {}
        
        skill_categories = {
            "Technical": ["Programming", "Mathematics", "Logical Reasoning", "Data Analysis"],
            "Creative": ["Design", "Writing", "Presentation", "Innovation"],
            "Interpersonal": ["Communication", "Leadership", "Teamwork", "Networking"]
        }
        
        for category, skill_list in skill_categories.items():
            st.write(f"**{category} Skills**")
            cols = st.columns(len(skill_list))
            for idx, skill in enumerate(skill_list):
                with cols[idx]:
                    skills[skill] = st.select_slider(
                        skill,
                        options=["Low", "Medium", "High"],
                        value="Medium",
                        key=f"skill_{skill}",
                        label_visibility="collapsed"
                    )
        
        if st.button("🔍 Get NEP Recommendations"):
            # Analyze and recommend
            recommendations = self.analyze_recommendations(interests, career_goals, skills)
            
            st.success("Recommendations Generated!")
            
            # Display top recommendations
            st.subheader("🎯 Top Major/Minor Combinations")
            
            for i, rec in enumerate(recommendations[:3], 1):
                with st.expander(f"**Recommendation #{i}: {rec['major']} with {rec['minor']}**", 
                               expanded=i==1):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Why this combination?**")
                        st.write(rec['reason'])
                    
                    with col2:
                        st.write("**Career Prospects:**")
                        for prospect in rec['career_prospects']:
                            st.write(f"• {prospect}")
                    
                    st.write("**Required Courses:**")
                    for course in rec['sample_courses']:
                        st.write(f"• {course}")
                    
                    # Match score
                    st.metric("Match Score", f"{rec['match_score']}%")
    
    def analyze_recommendations(self, interests, career_goals, skills):
        """Analyze and generate recommendations"""
        recommendations = []
        
        # Sample recommendation logic
        if "Technology" in interests or "Programming" in [k for k, v in skills.items() if v == "High"]:
            recommendations.append({
                "major": "Computer Science",
                "minor": "Business Management",
                "reason": "Combines technical skills with business acumen - perfect for tech leadership roles",
                "career_prospects": ["Product Manager", "Tech Consultant", "Software Architect", "Startup Founder"],
                "sample_courses": ["Data Structures", "Business Strategy", "Machine Learning", "Entrepreneurship"],
                "match_score": 85
            })
            
            recommendations.append({
                "major": "Computer Science",
                "minor": "Mathematics",
                "reason": "Strong foundation for research, data science, and advanced computing",
                "career_prospects": ["Data Scientist", "Research Scientist", "Quantitative Analyst", "AI Researcher"],
                "sample_courses": ["Algorithms", "Statistics", "Linear Algebra", "Computational Theory"],
                "match_score": 78
            })
        
        if "Engineering" in interests or any(s in ["CAD", "Thermodynamics"] for s in skills):
            recommendations.append({
                "major": "Mechanical Engineering",
                "minor": "Robotics",
                "reason": "Combine traditional engineering with emerging automation technologies",
                "career_prospects": ["Robotics Engineer", "Automation Specialist", "Manufacturing Engineer", "R&D Engineer"],
                "sample_courses": ["Dynamics", "Control Systems", "Robot Design", "AI in Robotics"],
                "match_score": 72
            })
        
        # Sort by match score
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        return recommendations
    
    def nep_guidelines_display(self):
        """Display NEP guidelines"""
        st.subheader("NEP 2020 Key Guidelines")
        
        guidelines = [
            "**1. Holistic Multidisciplinary Education:** Students can choose subjects across streams",
            "**2. Multiple Entry/Exit Options:** Flexibility to leave and re-enter education system",
            "**3. Credit Bank:** Digital storage of academic credits for lifelong learning",
            "**4. Academic Bank of Credits:** Students can transfer credits between institutions",
            "**5. 4-year Bachelor's Program:** With research component in 4th year",
            "**6. Integrated Skill Development:** Vocational skills integrated with academics"
        ]
        
        for guideline in guidelines:
            st.info(guideline)
        
        # Credit structure
        st.subheader("Typical Credit Structure (NEP)")
        
        credit_data = pd.DataFrame({
            'Year': ['1st Year', '2nd Year', '3rd Year', '4th Year'],
            'Major Credits': [24, 24, 24, 24],
            'Minor Credits': [12, 12, 12, 12],
            'Skill Credits': [4, 4, 4, 4],
            'Total Credits': [40, 40, 40, 40]
        })
        
        st.dataframe(credit_data, use_container_width=True)
    
    def exit_options(self):
        """Display multiple exit options"""
        st.subheader("Multiple Entry/Exit Options (NEP)")
        
        st.warning("""
        ⚠️ **Important:** Exit options allow flexibility but may affect career prospects.
        Choose based on your goals and circumstances.
        """)
        
        # Exit options table
        exit_data = [
            {
                "Exit Point": "After 1 Year",
                "Award": "Certificate",
                "Credits": "40-44",
                "Eligibility": "Entry-level jobs, skill-based roles",
                "Re-entry": "Can continue with credit transfer"
            },
            {
                "Exit Point": "After 2 Years",
                "Award": "Diploma",
                "Credits": "80-88",
                "Eligibility": "Technical roles, government jobs",
                "Re-entry": "Can continue to Bachelor's"
            },
            {
                "Exit Point": "After 3 Years",
                "Award": "Bachelor's Degree",
                "Credits": "120-132",
                "Eligibility": "Most corporate jobs, higher studies",
                "Re-entry": "Can continue to 4th year research"
            },
            {
                "Exit Point": "After 4 Years",
                "Award": "Bachelor's Degree with Research",
                "Credits": "160-176",
                "Eligibility": "Research careers, PhD programs",
                "Re-entry": "Can pursue Master's/PhD"
            }
        ]
        
        st.dataframe(pd.DataFrame(exit_data), use_container_width=True)
        
        # Decision helper
        st.subheader("Exit Option Decision Helper")
        
        col1, col2 = st.columns(2)
        
        with col1:
            financial_constraints = st.select_slider(
                "Financial Constraints:",
                ["None", "Low", "Medium", "High", "Critical"]
            )
            
            job_opportunity = st.selectbox(
                "Have a job opportunity?",
                ["No", "Maybe", "Yes - Entry Level", "Yes - Good Package"]
            )
        
        with col2:
            academic_performance = st.select_slider(
                "Academic Performance:",
                ["Poor", "Below Average", "Average", "Good", "Excellent"]
            )
            
            research_interest = st.selectbox(
                "Interest in Research:",
                ["None", "Low", "Moderate", "High", "Very High"]
            )
        
        if st.button("🤖 Get Exit Recommendation"):
            # Simple recommendation logic
            if financial_constraints in ["High", "Critical"] and job_opportunity != "No":
                st.error("**Consider Exit after 2-3 years** to start earning sooner")
                st.info("You can always return to complete your degree later through credit transfer")
            elif research_interest in ["High", "Very High"] and academic_performance in ["Good", "Excellent"]:
                st.success("**Complete 4-year program** for research component")
                st.info("Bachelor's with research opens doors to PhD programs and research careers")
            else:
                st.warning("**Complete 3-year Bachelor's** for optimal career opportunities")
                st.info("Most corporate jobs require at least a 3-year degree")
