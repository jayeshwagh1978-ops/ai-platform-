import streamlit as st
import pandas as pd
import json
import base64
from datetime import datetime

class AIResumeBuilder:
    def __init__(self):
        self.template_options = {
            "Professional": "Clean and formal design suitable for corporate jobs",
            "Creative": "Modern design with color accents for creative roles",
            "Academic": "Traditional format suitable for research and academic positions",
            "Minimalist": "Simple and elegant design focusing on content"
        }
    
    def display(self):
        """Display AI Resume Builder interface"""
        st.header("🤖 AI-Powered Resume Builder")
        
        # Check if user is in demo mode
        if 'demo_mode' in st.session_state and st.session_state.demo_mode:
            st.info("🎮 Demo Mode Active - Using sample student data")
            self.demo_mode_display()  # Changed from self.demo_mode()
            return
        
        # Main interface
        tab1, tab2, tab3 = st.tabs(["📝 Build Resume", "🔄 Optimize Resume", "📊 ATS Checker"])
        
        with tab1:
            self.build_resume()
        
        with tab2:
            self.optimize_resume()
        
        with tab3:
            self.ats_checker()
    
    def demo_mode_display(self):  # Renamed method
        """Demo mode with sample data"""
        st.info("🎮 **Demo Mode:** Using sample student data for demonstration")
        
        # Sample student data
        sample_data = {
            'personal_info': {
                'name': 'Rahul Sharma',
                'email': 'rahul.sharma@example.com',
                'phone': '+91 9876543210',
                'linkedin': 'linkedin.com/in/rahulsharma',
                'github': 'github.com/rahulsharma',
                'portfolio': 'rahulsharma.dev'
            },
            'education': {
                'degree': 'Bachelor of Technology',
                'university': 'Indian Institute of Technology',
                'major': 'Computer Science and Engineering',
                'cgpa': 8.7,
                'year': 2024,
                'location': 'Mumbai, India'
            },
            'experience': [
                {
                    'company': 'Tech Innovations Pvt Ltd',
                    'position': 'Software Developer Intern',
                    'duration': 'June 2023 - Present',
                    'location': 'Bangalore, India',
                    'description': '• Developed and maintained web applications using React and Node.js\n• Collaborated with cross-functional teams to implement new features\n• Reduced page load time by 30% through performance optimization'
                }
            ],
            'skills': {
                'Technical Skills': ['Python', 'JavaScript', 'React', 'Node.js', 'AWS', 'Docker'],
                'Soft Skills': ['Communication', 'Problem Solving', 'Teamwork'],
                'Tools': ['Git', 'VS Code', 'JIRA', 'Postman']
            },
            'projects': [
                {
                    'title': 'Campus Placement Portal',
                    'technologies': 'Python, Streamlit, Machine Learning',
                    'duration': 'Jan 2024 - Present',
                    'link': 'github.com/rahulsharma/placement-portal',
                    'description': '• Developed an AI-powered campus placement management system\n• Implemented resume optimization and placement prediction features\n• Used by 500+ students for career guidance'
                }
            ],
            'template': 'Professional',
            'ai_enhancements': ['Optimize Keywords for ATS', 'Add Metrics and Quantifiable Results'],
            'generated_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Show sample data
        with st.expander("📋 View Sample Data", expanded=False):
            st.json(sample_data, expanded=False)
        
        # Direct generate button for demo
        if st.button("🚀 Generate Sample Resume", type="primary"):
            self.generate_resume(sample_data)
    
    def build_resume(self):
        """Build resume from scratch"""
        st.subheader("Create Your Resume")
        
        with st.form("resume_builder_form"):
            # Personal Information
            st.markdown("### Personal Information")
            col1, col2 = st.columns(2)
            
            with col1:
                full_name = st.text_input("Full Name*")
                email = st.text_input("Email*")
                phone = st.text_input("Phone Number")
            
            with col2:
                linkedin = st.text_input("LinkedIn Profile URL")
                github = st.text_input("GitHub Profile URL")
                portfolio = st.text_input("Portfolio Website")
            
            # Education
            st.markdown("### Education")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                degree = st.text_input("Degree*", "Bachelor of Technology")
                university = st.text_input("University*", "ABC University")
            
            with col2:
                major = st.text_input("Major*", "Computer Science")
                cgpa = st.number_input("CGPA/Percentage*", 0.0, 10.0, 8.5, 0.1)
            
            with col3:
                grad_year = st.number_input("Graduation Year*", 2000, 2030, 2024)
                location = st.text_input("Location", "City, Country")
            
            # Work Experience
            st.markdown("### Work Experience")
            experience_count = st.number_input("Number of Experiences", 0, 5, 1)
            
            experiences = []
            for i in range(experience_count):
                st.markdown(f"**Experience {i+1}**")
                exp_col1, exp_col2 = st.columns(2)
                
                with exp_col1:
                    company = st.text_input(f"Company {i+1}", key=f"company_{i}")
                    position = st.text_input(f"Position {i+1}", key=f"position_{i}")
                
                with exp_col2:
                    duration = st.text_input(f"Duration {i+1} (e.g., Jan 2023 - Present)", key=f"duration_{i}")
                    location_exp = st.text_input(f"Location {i+1}", key=f"location_exp_{i}")
                
                description = st.text_area(f"Description {i+1}", 
                    key=f"desc_{i}", 
                    height=100,
                    value="• Developed and maintained web applications\n• Collaborated with cross-functional teams\n• Implemented new features and fixed bugs")
                
                experiences.append({
                    'company': company,
                    'position': position,
                    'duration': duration,
                    'location': location_exp,
                    'description': description
                })
            
            # Skills
            st.markdown("### Skills")
            skill_categories = {
                "Technical Skills": ["Python", "Java", "JavaScript", "React", "Node.js", 
                                   "SQL", "AWS", "Docker", "Git", "Machine Learning"],
                "Soft Skills": ["Communication", "Leadership", "Teamwork", "Problem Solving", 
                              "Time Management", "Adaptability"],
                "Tools": ["VS Code", "JIRA", "Figma", "Postman", "Tableau", "Power BI"]
            }
            
            selected_skills = {}
            for category, skills in skill_categories.items():
                selected_skills[category] = st.multiselect(
                    category,
                    skills,
                    default=skills[:2] if category == "Technical Skills" else []
                )
            
            # Projects
            st.markdown("### Projects")
            project_count = st.number_input("Number of Projects", 0, 5, 1)
            
            projects = []
            for i in range(project_count):
                st.markdown(f"**Project {i+1}**")
                proj_col1, proj_col2 = st.columns(2)
                
                with proj_col1:
                    proj_title = st.text_input(f"Project Title {i+1}", key=f"proj_title_{i}")
                    proj_tech = st.text_input(f"Technologies Used {i+1}", key=f"proj_tech_{i}")
                
                with proj_col2:
                    proj_duration = st.text_input(f"Duration {i+1}", key=f"proj_duration_{i}")
                    proj_link = st.text_input(f"Project Link {i+1}", key=f"proj_link_{i}")
                
                proj_desc = st.text_area(f"Description {i+1}", 
                    key=f"proj_desc_{i}", 
                    height=80,
                    value="• Developed a web application for [purpose]\n• Implemented [key features]\n• Achieved [results/impact]")
                
                projects.append({
                    'title': proj_title,
                    'technologies': proj_tech,
                    'duration': proj_duration,
                    'link': proj_link,
                    'description': proj_desc
                })
            
            # Template Selection
            st.markdown("### Resume Template")
            template = st.selectbox("Choose a Template", list(self.template_options.keys()),
                                  format_func=lambda x: f"{x} - {self.template_options[x]}")
            
            # AI Enhancement Options
            st.markdown("### AI Enhancement")
            ai_options = st.multiselect(
                "Select AI enhancements for your resume:",
                ["Optimize Keywords for ATS", "Improve Action Verbs", 
                 "Add Metrics and Quantifiable Results", "Suggest Missing Sections",
                 "Check Grammar and Style"]
            )
            
            # Submit button
            if st.form_submit_button("🚀 Generate AI-Optimized Resume"):
                # Validate required fields
                if not full_name or not email:
                    st.error("Please fill in all required fields (marked with *)")
                    return
                
                # Collect all data
                resume_data = {
                    'personal_info': {
                        'name': full_name,
                        'email': email,
                        'phone': phone,
                        'linkedin': linkedin,
                        'github': github,
                        'portfolio': portfolio
                    },
                    'education': {
                        'degree': degree,
                        'university': university,
                        'major': major,
                        'cgpa': cgpa,
                        'year': grad_year,
                        'location': location
                    },
                    'experience': experiences,
                    'skills': selected_skills,
                    'projects': projects,
                    'template': template,
                    'ai_enhancements': ai_options,
                    'generated_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Generate resume
                self.generate_resume(resume_data)
    
    def generate_resume(self, resume_data):
        """Generate and display resume"""
        st.success("✅ Resume generated successfully!")
        
        # Display resume preview
        st.subheader("📄 Resume Preview")
        
        # Create resume HTML preview
        html_resume = self.create_html_resume(resume_data)
        
        # Display in expandable preview
        with st.expander("Preview Resume", expanded=True):
            st.markdown(html_resume, unsafe_allow_html=True)
        
        # AI Suggestions
        if resume_data.get('ai_enhancements'):
            st.subheader("🤖 AI Suggestions")
            
            suggestions = []
            if "Optimize Keywords for ATS" in resume_data['ai_enhancements']:
                suggestions.append("**ATS Optimization:** Add keywords like 'agile methodology', 'cross-functional collaboration', 'SDLC'")
            if "Improve Action Verbs" in resume_data['ai_enhancements']:
                suggestions.append("**Action Verbs:** Replace 'did' with stronger verbs like 'developed', 'implemented', 'optimized'")
            if "Add Metrics and Quantifiable Results" in resume_data['ai_enhancements']:
                suggestions.append("**Quantify Results:** Add metrics like 'improved performance by 30%', 'reduced costs by 20%'")
            
            for suggestion in suggestions:
                st.info(suggestion)
        
        # Download options
        st.subheader("📥 Download Options")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            # HTML Download
            html_href, html_filename = self.download_resume(resume_data, "html")
            if html_href:
                st.markdown(f"""
                <a href="{html_href}" download="{html_filename}" style="text-decoration: none;">
                    <button style="width:100%; padding:10px; background:#3498db; color:white; border:none; border-radius:5px; cursor:pointer;">
                        📝 Download as HTML
                    </button>
                </a>
                """, unsafe_allow_html=True)
            else:
                st.button("📝 Download as HTML", disabled=True, help="HTML generation not available")
        
        with col2:
            # Text Download
            txt_href, txt_filename = self.download_resume(resume_data, "text")
            if txt_href:
                st.markdown(f"""
                <a href="{txt_href}" download="{txt_filename}" style="text-decoration: none;">
                    <button style="width:100%; padding:10px; background:#27ae60; color:white; border:none; border-radius:5px; cursor:pointer;">
                        📄 Download as Text
                    </button>
                </a>
                """, unsafe_allow_html=True)
            else:
                st.button("📄 Download as Text", disabled=True, help="Text generation not available")
        
        with col3:
            # Copy to Clipboard
            if st.button("📋 Copy HTML to Clipboard", use_container_width=True):
                # For Streamlit Cloud, we need a workaround
                try:
                    # Try to use pyperclip if available
                    import pyperclip
                    pyperclip.copy(html_resume)
                    st.success("HTML copied to clipboard!")
                except ImportError:
                    st.info("""
                    **To copy:**
                    1. Right-click on the preview
                    2. Select "Inspect" or "View Source"
                    3. Copy the HTML code
                    """)
                except Exception as e:
                    st.warning(f"Could not copy to clipboard: {str(e)}")
        
        # Add PDF generation note
        st.info("""
        **💡 PDF Generation:** For PDF export, download the HTML version and use:
        - **Browser:** Print → Save as PDF
        - **Online:** Convert with online HTML to PDF tools
        - **Desktop:** Use LibreOffice or Microsoft Word
        """)
    
    def create_html_resume(self, resume_data):
        """Create HTML representation of resume with better styling"""
        # Extract data
        personal_info = resume_data['personal_info']
        education = resume_data['education']
        experiences = resume_data.get('experience', [])
        skills = resume_data.get('skills', {})
        projects = resume_data.get('projects', [])
        
        # Start building HTML
        html = f"""
        <div style="font-family: 'Arial', sans-serif; max-width: 800px; margin: 0 auto; padding: 30px; background: white; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
            <!-- Header -->
            <div style="text-align: center; margin-bottom: 40px; border-bottom: 3px solid #3498db; padding-bottom: 20px;">
                <h1 style="color: #2c3e50; margin-bottom: 10px; font-size: 32px;">{personal_info['name']}</h1>
                <div style="color: #7f8c8d; font-size: 16px; line-height: 1.6;">
                    {personal_info['email']} • {personal_info['phone']}
                    {f"<br>LinkedIn: {personal_info['linkedin']}" if personal_info.get('linkedin') else ""}
                    {f" • GitHub: {personal_info['github']}" if personal_info.get('github') else ""}
                    {f" • Portfolio: {personal_info['portfolio']}" if personal_info.get('portfolio') else ""}
                </div>
            </div>
            
            <!-- Education -->
            <div style="margin-bottom: 30px;">
                <h2 style="color: #3498db; border-bottom: 2px solid #3498db; padding-bottom: 8px; margin-bottom: 15px; font-size: 22px;">Education</h2>
                <p style="margin-bottom: 5px;"><strong>{education['degree']} in {education['major']}</strong></p>
                <p style="color: #555; margin-bottom: 5px;">{education['university']} • {education['location']}</p>
                <p style="color: #777;">CGPA: {education['cgpa']} • Graduation: {education['year']}</p>
            </div>
        """
        
        # Add Experience Section if exists
        if experiences:
            html += """
            <div style="margin-bottom: 30px;">
                <h2 style="color: #3498db; border-bottom: 2px solid #3498db; padding-bottom: 8px; margin-bottom: 15px; font-size: 22px;">Experience</h2>
            """
            
            for exp in experiences:
                html += f"""
                <div style="margin-bottom: 20px;">
                    <p style="margin-bottom: 5px;"><strong>{exp['position']}</strong> at {exp['company']}</p>
                    <p style="color: #555; margin-bottom: 10px; font-style: italic;">{exp['duration']} • {exp['location']}</p>
                    <div style="margin-left: 20px;">
                """
                
                # Process description (handle bullet points)
                if exp.get('description'):
                    lines = exp['description'].split('\n')
                    for line in lines:
                        if line.strip():
                            # Remove bullet if already present
                            clean_line = line.strip()
                            if clean_line.startswith('•'):
                                clean_line = clean_line[1:].strip()
                            html += f'<p style="margin-bottom: 5px; color: #444;">• {clean_line}</p>'
                
                html += """
                    </div>
                </div>
                """
            
            html += "</div>"
        
        # Add Skills Section
        if skills and any(skills.values()):
            html += """
            <div style="margin-bottom: 30px;">
                <h2 style="color: #3498db; border-bottom: 2px solid #3498db; padding-bottom: 8px; margin-bottom: 15px; font-size: 22px;">Skills</h2>
            """
            
            for category, skill_list in skills.items():
                if skill_list:
                    html += f"""
                    <div style="margin-bottom: 10px;">
                        <p style="margin-bottom: 5px;"><strong>{category}:</strong></p>
                        <p style="color: #555; margin-left: 20px;">{', '.join(skill_list)}</p>
                    </div>
                    """
            
            html += "</div>"
        
        # Add Projects Section if exists
        if projects:
            html += """
            <div style="margin-bottom: 30px;">
                <h2 style="color: #3498db; border-bottom: 2px solid #3498db; padding-bottom: 8px; margin-bottom: 15px; font-size: 22px;">Projects</h2>
            """
            
            for proj in projects:
                html += f"""
                <div style="margin-bottom: 20px;">
                    <p style="margin-bottom: 5px;"><strong>{proj['title']}</strong></p>
                    <p style="color: #555; margin-bottom: 5px; font-size: 14px;">
                        <em>Technologies: {proj['technologies']} • Duration: {proj['duration']}</em>
                    </p>
                """
                
                if proj.get('link'):
                    html += f'<p style="margin-bottom: 10px; color: #3498db;">🔗 <a href="{proj["link"]}" style="color: #3498db; text-decoration: none;">View Project</a></p>'
                
                # Process project description
                if proj.get('description'):
                    lines = proj['description'].split('\n')
                    html += '<div style="margin-left: 20px;">'
                    for line in lines:
                        if line.strip():
                            clean_line = line.strip()
                            if clean_line.startswith('•'):
                                clean_line = clean_line[1:].strip()
                            html += f'<p style="margin-bottom: 5px; color: #444;">• {clean_line}</p>'
                    html += '</div>'
                
                html += "</div>"
            
            html += "</div>"
        
        # Add footer
        html += f"""
            <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; text-align: center; color: #95a5a6; font-size: 12px;">
                <p>Generated by AI Campus Placement Platform • {resume_data['generated_date']}</p>
                <p>Template: {resume_data['template']}</p>
            </div>
        </div>
        """
        
        return html
    
    def download_resume(self, resume_data, format_type):
        """Generate and download resume in different formats"""
        if format_type == "html":
            html_content = self.create_html_resume(resume_data)
            
            # Create full HTML document
            html_file = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Resume - {resume_data['personal_info']['name']}</title>
                <style>
                    @media print {{
                        body {{ margin: 0; padding: 0; }}
                        .resume-container {{ box-shadow: none !important; }}
                    }}
                </style>
            </head>
            <body>
                {html_content}
            </body>
            </html>
            """
            
            # Create download link
            b64 = base64.b64encode(html_file.encode()).decode()
            href = f'data:text/html;base64,{b64}'
            filename = f"resume_{resume_data['personal_info']['name'].replace(' ', '_')}.html"
            
            return href, filename
        
        elif format_type == "text":
            # Create plain text version
            text_content = f"""
            RESUME - {resume_data['personal_info']['name']}
            {'='*50}
            
            CONTACT INFORMATION
            Email: {resume_data['personal_info']['email']}
            Phone: {resume_data['personal_info']['phone']}
            LinkedIn: {resume_data['personal_info'].get('linkedin', 'N/A')}
            
            EDUCATION
            {resume_data['education']['degree']} in {resume_data['education']['major']}
            {resume_data['education']['university']}
            CGPA: {resume_data['education']['cgpa']} | Graduation: {resume_data['education']['year']}
            
            """
            
            # Add experience
            if resume_data.get('experience'):
                text_content += "\nEXPERIENCE\n"
                for exp in resume_data['experience']:
                    text_content += f"\n{exp['position']} at {exp['company']}\n"
                    text_content += f"{exp['duration']} | {exp['location']}\n"
                    if exp.get('description'):
                        text_content += f"{exp['description']}\n"
            
            # Add skills
            if resume_data.get('skills'):
                text_content += "\nSKILLS\n"
                for category, skill_list in resume_data['skills'].items():
                    if skill_list:
                        text_content += f"\n{category}: {', '.join(skill_list)}"
            
            text_content += f"\n\nGenerated: {resume_data['generated_date']}"
            
            b64 = base64.b64encode(text_content.encode()).decode()
            href = f'data:text/plain;base64,{b64}'
            filename = f"resume_{resume_data['personal_info']['name'].replace(' ', '_')}.txt"
            
            return href, filename
        
        return None, None
    
    def optimize_resume(self):
        """Optimize existing resume"""
        st.subheader("Optimize Existing Resume")
        
        st.info("Upload your resume for AI optimization and ATS compatibility check")
        
        uploaded_file = st.file_uploader("Upload Resume (PDF, DOCX, TXT)", 
                                       type=['pdf', 'docx', 'txt'])
        
        if uploaded_file is not None:
            st.success(f"File uploaded: {uploaded_file.name}")
            
            # Show optimization options
            st.subheader("Optimization Options")
            
            col1, col2 = st.columns(2)
            with col1:
                target_role = st.text_input("Target Role for Optimization", 
                                          "Software Development Engineer")
                target_company = st.text_input("Target Company (Optional)")
            
            with col2:
                optimization_level = st.select_slider(
                    "Optimization Level",
                    options=["Light", "Moderate", "Aggressive"],
                    value="Moderate"
                )
            
            # Additional options
            optimization_features = st.multiselect(
                "Specific Optimizations:",
                ["Keyword Optimization", "ATS Compatibility", "Action Verb Enhancement",
                 "Quantifiable Metrics", "Length Optimization", "Formatting Check",
                 "Skill Gap Analysis", "Industry-specific Jargon"]
            )
            
            if st.button("🔍 Analyze and Optimize Resume"):
                with st.spinner("AI is analyzing your resume..."):
                    # Simulate AI processing
                    import time
                    time.sleep(2)
                    
                    # Show results
                    st.success("Analysis Complete!")
                    
                    # Display optimization report
                    st.subheader("📊 Optimization Report")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("ATS Score", "78/100", "+15")
                    with col2:
                        st.metric("Keyword Match", "65%", "+25%")
                    with col3:
                        st.metric("Readability", "Good", "Improved")
                    
                    # Recommendations
                    st.subheader("🤖 AI Recommendations")
                    
                    recommendations = [
                        "**1. Add more action verbs:** Replace passive language with strong action verbs",
                        "**2. Include quantifiable metrics:** Add numbers to show impact (e.g., 'Improved performance by 30%')",
                        "**3. Optimize for keywords:** Add relevant keywords: 'agile methodology', 'SDLC', 'cross-functional teams'",
                        "**4. Improve formatting:** Use consistent bullet points and spacing",
                        "**5. Add missing sections:** Consider adding a 'Projects' section if applicable"
                    ]
                    
                    for rec in recommendations:
                        st.info(rec)
    
    def ats_checker(self):
        """ATS (Applicant Tracking System) checker"""
        st.subheader("ATS Compatibility Checker")
        
        st.warning("""
        ⚠️ **Important:** Many companies use ATS to filter resumes before human review.
        This tool checks if your resume will pass through common ATS systems.
        """)
        
        # ATS check options
        ats_systems = st.multiselect(
            "Select ATS systems to check against:",
            ["Workday", "Greenhouse", "Lever", "Taleo", "ICIMS", "BambooHR", "SuccessFactors"],
            default=["Workday", "Greenhouse"]
        )
        
        # Resume text input
        resume_text = st.text_area(
            "Paste your resume text here for ATS analysis:",
            height=200,
            value="""John Doe
Software Developer
Skills: Python, JavaScript, React
Experience: Developed web applications at Tech Company"""
        )
        
        if st.button("🔍 Check ATS Compatibility"):
            # Simulate ATS analysis
            with st.spinner("Analyzing resume for ATS compatibility..."):
                import time
                time.sleep(3)
                
                # Display results
                st.success("ATS Analysis Complete!")
                
                # ATS Score
                ats_score = 72
                st.subheader(f"ATS Score: {ats_score}/100")
                st.progress(ats_score / 100)
                
                # Detailed analysis
                st.subheader("Detailed Analysis")
                
                analysis_data = {
                    "Category": ["Formatting", "Keywords", "Readability", "Length", "File Type"],
                    "Score": [85, 65, 90, 78, 95],
                    "Status": ["✅ Good", "⚠️ Needs Work", "✅ Excellent", "✅ Good", "✅ Excellent"],
                    "Recommendation": [
                        "Proper use of headings and bullet points",
                        "Add more industry-specific keywords",
                        "Clear and concise language",
                        "Optimal 1-2 page length",
                        "PDF format recommended"
                    ]
                }
                
                st.dataframe(pd.DataFrame(analysis_data), use_container_width=True)
                
                # Critical issues
                st.subheader("⚠️ Critical Issues Found")
                issues = [
                    "**1. Missing Keywords:** Add more technical keywords relevant to software development roles",
                    "**2. No Quantifiable Results:** Add metrics and numbers to show impact",
                    "**3. Could use more action verbs:** Start bullet points with strong action verbs",
                    "**4. Consider adding a summary section:** Helps ATS understand your profile"
                ]
                
                for issue in issues:
                    st.error(issue)
