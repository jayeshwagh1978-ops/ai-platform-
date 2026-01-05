import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from database.db_manager import db_manager

class CollegeFlow:
    def __init__(self):
        self.college_data = self.initialize_college_data()
        self.current_step = 1
    
    def initialize_college_data(self):
        """Initialize college data"""
        return {
            "college_id": 1,  # Default college ID
            "college_name": "ABC Engineering College",
            "students": self.generate_sample_students(),
            "companies": self.generate_sample_companies(),
            "drives": self.generate_sample_drives(),
            "placements": self.generate_sample_placements(),
            "interviews": self.generate_sample_interviews()
        }
    
    def generate_sample_students(self):
        """Generate sample student data"""
        np.random.seed(42)
        n_students = 150
        
        departments = ["Computer Science", "Electrical Engineering", 
                      "Mechanical Engineering", "Civil Engineering", "Information Technology"]
        years = [2022, 2023, 2024]
        
        data = []
        for i in range(n_students):
            dept = departments[i % len(departments)]
            grad_year = years[i % len(years)]
            
            student = {
                "student_id": f"S{i+1:04d}",
                "name": f"Student {i+1}",
                "department": dept,
                "semester": np.random.randint(3, 9),
                "cgpa": round(6.5 + np.random.random() * 3, 2),
                "backlogs": np.random.randint(0, 4),
                "graduation_year": grad_year,
                "placement_status": "Not Placed" if i < 100 else "Placed",
                "company": None if i < 100 else ["Google", "Microsoft", "Amazon", "TCS", "Infosys"][i % 5],
                "package": None if i < 100 else round(8 + np.random.random() * 12, 2),
                "email": f"student{i+1}@college.edu",
                "phone": f"+91 98765{np.random.randint(10000, 99999)}"
            }
            
            # Add some interns
            if 50 <= i < 70:
                student["placement_status"] = "Intern"
                student["company"] = ["TechCorp", "StartupX", "InnovateLabs"][i % 3]
                student["package"] = round(0.5 + np.random.random() * 0.5, 2)
            
            data.append(student)
        
        return pd.DataFrame(data)
    
    def generate_sample_companies(self):
        """Generate sample company data"""
        companies = [
            {
                "company_id": "C001",
                "name": "Google",
                "industry": "Technology",
                "website": "https://google.com",
                "contact_person": "John Doe",
                "contact_email": "campus@google.com",
                "contact_phone": "+1-650-253-0000",
                "recruitment_status": "Active",
                "visits_this_year": 3,
                "total_hires": 25,
                "avg_package": 22.5
            },
            {
                "company_id": "C002",
                "name": "Microsoft",
                "industry": "Software",
                "website": "https://microsoft.com",
                "contact_person": "Jane Smith",
                "contact_email": "university@microsoft.com",
                "contact_phone": "+1-425-882-8080",
                "recruitment_status": "Active",
                "visits_this_year": 2,
                "total_hires": 18,
                "avg_package": 20.0
            },
            {
                "company_id": "C003",
                "name": "Amazon",
                "industry": "E-commerce",
                "website": "https://amazon.com",
                "contact_person": "Bob Johnson",
                "contact_email": "campus@amazon.com",
                "contact_phone": "+1-206-266-1000",
                "recruitment_status": "Active",
                "visits_this_year": 2,
                "total_hires": 15,
                "avg_package": 18.5
            },
            {
                "company_id": "C004",
                "name": "TCS",
                "industry": "IT Services",
                "website": "https://tcs.com",
                "contact_person": "Alice Brown",
                "contact_email": "campus@tcs.com",
                "contact_phone": "+91-22-6778-9999",
                "recruitment_status": "Active",
                "visits_this_year": 4,
                "total_hires": 45,
                "avg_package": 8.5
            },
            {
                "company_id": "C005",
                "name": "Infosys",
                "industry": "IT Services",
                "website": "https://infosys.com",
                "contact_person": "Charlie Wilson",
                "contact_email": "campus@infosys.com",
                "contact_phone": "+91-80-2852-0261",
                "recruitment_status": "Active",
                "visits_this_year": 3,
                "total_hires": 38,
                "avg_package": 8.0
            }
        ]
        return pd.DataFrame(companies)
    
    def generate_sample_drives(self):
        """Generate sample campus drives"""
        drives = []
        companies = ["Google", "Microsoft", "Amazon", "TCS", "Infosys"]
        
        for i in range(10):
            drive_date = datetime.now() + timedelta(days=np.random.randint(10, 90))
            
            drive = {
                "drive_id": f"D{i+1:03d}",
                "company": companies[i % len(companies)],
                "date": drive_date.strftime("%Y-%m-%d"),
                "mode": np.random.choice(["Online", "Offline", "Hybrid"]),
                "venue": "Main Campus Auditorium" if i % 2 == 0 else "Virtual",
                "coordinator": f"Coordinator {i+1}",
                "status": "Scheduled" if i < 7 else "Completed",
                "registered": np.random.randint(50, 200),
                "selected": np.random.randint(5, 25) if i >= 7 else 0,
                "job_roles": "SDE, Data Scientist" if i % 2 == 0 else "PM, Business Analyst"
            }
            drives.append(drive)
        
        return pd.DataFrame(drives)
    
    def generate_sample_placements(self):
        """Generate sample placement records"""
        placements = []
        companies = ["Google", "Microsoft", "Amazon", "TCS", "Infosys", 
                    "Adobe", "Intel", "Oracle", "Cisco", "IBM"]
        
        for i in range(50):
            placement = {
                "placement_id": f"P{i+1:04d}",
                "student_id": f"S{np.random.randint(1000, 1150):04d}",
                "student_name": f"Student {i+151}",
                "department": np.random.choice(["Computer Science", "Electrical", "Mechanical", "Civil", "IT"]),
                "company": companies[i % len(companies)],
                "job_role": np.random.choice(["Software Engineer", "Data Scientist", "Product Manager", 
                                            "Business Analyst", "DevOps Engineer"]),
                "package": round(8 + np.random.random() * 22, 2),
                "placement_date": (datetime.now() - timedelta(days=np.random.randint(1, 365))).strftime("%Y-%m-%d"),
                "status": np.random.choice(["Offer Accepted", "Joined", "Completed Internship"])
            }
            placements.append(placement)
        
        return pd.DataFrame(placements)
    
    def generate_sample_interviews(self):
        """Generate sample interview records"""
        interviews = []
        rounds = ["Aptitude Test", "Technical Round 1", "Technical Round 2", "HR Round", "Managerial Round"]
        
        for i in range(30):
            interview_date = datetime.now() + timedelta(days=np.random.randint(1, 30))
            
            interview = {
                "interview_id": f"I{i+1:04d}",
                "student_id": f"S{np.random.randint(1000, 1100):04d}",
                "student_name": f"Student {np.random.randint(1, 150)}",
                "company": np.random.choice(["Google", "Microsoft", "Amazon", "TCS", "Infosys"]),
                "round": rounds[i % len(rounds)],
                "date": interview_date.strftime("%Y-%m-%d"),
                "time": f"{np.random.randint(9, 17):02d}:00",
                "mode": np.random.choice(["Online", "Offline"]),
                "interviewer": f"Interviewer {np.random.randint(1, 20)}",
                "status": np.random.choice(["Scheduled", "Completed", "Cancelled"]),
                "result": "Pending" if i < 20 else np.random.choice(["Selected", "Rejected", "On Hold"])
            }
            interviews.append(interview)
        
        return pd.DataFrame(interviews)
    
    def display(self):
        """Display complete college admin workflow"""
        st.header("🏫 College Placement Management System")
    
        # Get current step from session state
        current_step = st.session_state.get('current_step_college', 1)
        self.current_step = current_step
    
        # Display step header
        step_names = {
            1: "👨‍🎓 Student Database",
            2: "📊 Analytics Dashboard",
            3: "🏢 Company Registration",
            4: "📅 Drive Scheduling",
            5: "🎯 Student-Company Matching",
            6: "📝 Interview Management",
            7: "✅ Placement Records",
            8: "📈 Performance Reports"
        }
    
        # Create header with progress
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"Step {current_step}: {step_names[current_step]}")
        with col2:
            progress = current_step / 8
            st.progress(progress)
            st.caption(f"Step {current_step} of 8")
    
        # Display appropriate step
        if current_step == 1:
            self.step1_student_database()
        elif current_step == 2:
            self.step2_analytics_dashboard()
        elif current_step == 3:
            self.step3_company_registration()
        elif current_step == 4:
            self.step4_drive_scheduling()
        elif current_step == 5:
            self.step5_student_company_matching()
        elif current_step == 6:
            self.step6_interview_management()
        elif current_step == 7:
            self.step7_placement_records()
        elif current_step == 8:
            self.step8_performance_reports()
    
        # Navigation
        self.display_workflow_navigation(current_step)
    
    def step1_student_database(self):
        """Step 1: Student Database Management"""
        st.info("Manage and view all student records in the college")
        
        # Search and filters
        col1, col2, col3 = st.columns(3)
        with col1:
            search = st.text_input("🔍 Search by Name/ID")
        with col2:
            department_filter = st.selectbox("Filter by Department", 
                ["All"] + list(self.college_data["students"]["department"].unique()))
        with col3:
            placement_filter = st.selectbox("Filter by Placement Status", 
                ["All", "Placed", "Not Placed", "Intern"])
        
        # Filter data
        filtered_students = self.college_data["students"].copy()
        if search:
            filtered_students = filtered_students[
                filtered_students["name"].str.contains(search, case=False) |
                filtered_students["student_id"].str.contains(search, case=False)
            ]
        if department_filter != "All":
            filtered_students = filtered_students[filtered_students["department"] == department_filter]
        if placement_filter != "All":
            filtered_students = filtered_students[filtered_students["placement_status"] == placement_filter]
        
        # Display statistics
        total_students = len(filtered_students)
        placed_count = len(filtered_students[filtered_students["placement_status"] == "Placed"])
        intern_count = len(filtered_students[filtered_students["placement_status"] == "Intern"])
        placement_rate = (placed_count / total_students * 100) if total_students > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Students", total_students)
        with col2:
            st.metric("Placed Students", placed_count)
        with col3:
            st.metric("Interns", intern_count)
        with col4:
            st.metric("Placement Rate", f"{placement_rate:.1f}%")
        
        # Display student table
        st.subheader("Student Records")
        
        # Select columns to display
        display_cols = st.multiselect("Select columns to display",
            ["student_id", "name", "department", "semester", "cgpa", "backlogs", 
             "placement_status", "company", "package", "email"],
            default=["student_id", "name", "department", "cgpa", "placement_status", "company"])
        
        if display_cols:
            st.dataframe(filtered_students[display_cols], width='stretch', height=400)
            
            # Export option
            if st.button("📥 Export to CSV", width='stretch'):
                csv = filtered_students[display_cols].to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"student_records_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
        # Student details view
        if not filtered_students.empty:
            st.subheader("Student Details")
            selected_student = st.selectbox("Select Student for Details", 
                filtered_students["name"].tolist())
            
            if selected_student:
                student_data = filtered_students[filtered_students["name"] == selected_student].iloc[0]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Personal Information:**")
                    st.write(f"**ID:** {student_data['student_id']}")
                    st.write(f"**Name:** {student_data['name']}")
                    st.write(f"**Email:** {student_data['email']}")
                    st.write(f"**Phone:** {student_data['phone']}")
                
                with col2:
                    st.write("**Academic Information:**")
                    st.write(f"**Department:** {student_data['department']}")
                    st.write(f"**Semester:** {student_data['semester']}")
                    st.write(f"**CGPA:** {student_data['cgpa']}")
                    st.write(f"**Backlogs:** {student_data['backlogs']}")
                
                st.write("**Placement Status:**")
                status_color = "🟢" if student_data['placement_status'] == 'Placed' else \
                              "🟡" if student_data['placement_status'] == 'Intern' else "🔴"
                st.write(f"{status_color} **{student_data['placement_status']}**")
                
                if student_data['company']:
                    st.write(f"**Company:** {student_data['company']}")
                    if student_data['package']:
                        st.write(f"**Package:** ₹{student_data['package']} LPA")
    
    def step2_analytics_dashboard(self):
        """Step 2: Analytics Dashboard"""
        st.info("Comprehensive analytics and insights for placement management")
        
        # Dashboard with multiple metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_students = len(self.college_data["students"])
            st.metric("Total Students", total_students, "150")
        with col2:
            placed = len(self.college_data["students"][self.college_data["students"]["placement_status"] == "Placed"])
            st.metric("Placed", placed, f"+{placed-40}")
        with col3:
            placement_rate = (placed / total_students * 100) if total_students > 0 else 0
            st.metric("Placement Rate", f"{placement_rate:.1f}%", "+5.2%")
        with col4:
            avg_package = self.college_data["students"]["package"].mean()
            st.metric("Avg Package", f"₹{avg_package:.1f}L", "+2.1L")
        
        # Visualizations
        st.subheader("📈 Placement Analytics")
        
        tab1, tab2, tab3, tab4 = st.tabs(["Department-wise", "Company-wise", "Trends", "Predictions"])
        
        with tab1:
            # Department-wise placement
            dept_stats = self.college_data["students"].groupby("department").agg({
                "student_id": "count",
                "placement_status": lambda x: (x == "Placed").sum()
            }).reset_index()
            dept_stats["placement_rate"] = (dept_stats["placement_status"] / dept_stats["student_id"] * 100)
            
            fig1 = px.bar(dept_stats, x="department", y="placement_rate",
                         title="Placement Rate by Department",
                         color="placement_rate",
                         color_continuous_scale="Viridis")
            st.plotly_chart(fig1, width='stretch')
            
            # Department-wise packages
            dept_packages = self.college_data["students"][self.college_data["students"]["placement_status"] == "Placed"]
            if not dept_packages.empty:
                fig2 = px.box(dept_packages, x="department", y="package",
                             title="Package Distribution by Department")
                st.plotly_chart(fig2, width='stretch')
        
        with tab2:
            # Company-wise statistics
            company_stats = self.college_data["placements"].groupby("company").agg({
                "placement_id": "count",
                "package": "mean"
            }).reset_index().rename(columns={"placement_id": "hires", "package": "avg_package"})
            
            col1, col2 = st.columns(2)
            with col1:
                fig3 = px.bar(company_stats, x="company", y="hires",
                             title="Hires by Company")
                st.plotly_chart(fig3, use_container_width=True)
            
            with col2:
                fig4 = px.bar(company_stats, x="company", y="avg_package",
                             title="Average Package by Company")
                st.plotly_chart(fig4, use_container_width=True)
        
        with tab3:
            # Monthly trends (simulated)
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            placements_trend = [5, 8, 12, 15, 20, 25, 30, 35, 40, 42, 45, 50]
            interviews_trend = [20, 25, 30, 35, 40, 45, 50, 55, 60, 62, 65, 70]
            
            trend_data = pd.DataFrame({
                'Month': months,
                'Placements': placements_trend,
                'Interviews': interviews_trend
            })
            
            fig5 = px.line(trend_data, x='Month', y=['Placements', 'Interviews'],
                          title="Monthly Placement Trends",
                          markers=True)
            st.plotly_chart(fig5, use_container_width=True)
            
            # CGPA vs Package scatter
            placed_students = self.college_data["students"][self.college_data["students"]["placement_status"] == "Placed"]
            if not placed_students.empty:
                fig6 = px.scatter(placed_students, x="cgpa", y="package",
                                 color="department",
                                 title="CGPA vs Package Analysis",
                                 trendline="ols")
                st.plotly_chart(fig6, use_container_width=True)
        
        with tab4:
            # Predictive analytics
            st.subheader("🤖 AI-Powered Predictions")
            
            # Current placement prediction
            current_rate = placement_rate
            target_rate = 85.0
            
            fig7 = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=current_rate,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Current Placement Rate"},
                delta={'reference': target_rate},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "red"},
                        {'range': [50, 75], 'color': "yellow"},
                        {'range': [75, 100], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "black", 'width': 4},
                        'thickness': 0.75,
                        'value': target_rate
                    }
                }
            ))
            st.plotly_chart(fig7, use_container_width=True)
            
            # Key metrics affecting placement
            st.subheader("Key Performance Indicators")
            
            metrics_data = {
                'Metric': ['CGPA > 8.0', 'Internship Experience', 'Technical Skills', 
                          'Communication Skills', 'Projects Completed'],
                'Current': [45, 60, 70, 65, 55],
                'Target': [60, 75, 85, 80, 70]
            }
            
            metrics_df = pd.DataFrame(metrics_data)
            metrics_df['Gap'] = metrics_df['Target'] - metrics_df['Current']
            
            for _, row in metrics_df.iterrows():
                progress = row['Current'] / row['Target']
                color = "green" if progress >= 0.9 else "orange" if progress >= 0.7 else "red"
                
                st.write(f"**{row['Metric']}:** {row['Current']}% (Target: {row['Target']}%)")
                st.progress(progress)
    
    def step3_company_registration(self):
        """Step 3: Company Registration & Management"""
        st.info("Register and manage companies for campus recruitment")
        
        tab1, tab2, tab3 = st.tabs(["🏢 Register New", "📋 Company Directory", "📊 Company Analytics"])
        
        with tab1:
            st.subheader("Register New Company")
            
            with st.form("company_registration_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    company_name = st.text_input("Company Name*")
                    industry = st.selectbox("Industry*",
                        ["IT/Software", "Finance/Banking", "Consulting", "Manufacturing",
                         "E-commerce", "Healthcare", "Education", "Automotive", "Other"])
                    website = st.text_input("Website")
                    founded_year = st.number_input("Founded Year", 1900, datetime.now().year, 2000)
                
                with col2:
                    contact_person = st.text_input("Contact Person*")
                    contact_email = st.text_input("Contact Email*")
                    contact_phone = st.text_input("Contact Phone*")
                    hr_email = st.text_input("HR Email for Applications")
                
                company_description = st.text_area("Company Description", height=150,
                    placeholder="Brief description of the company, culture, and opportunities...")
                
                # Recruitment preferences
                st.subheader("Recruitment Preferences")
                col1, col2 = st.columns(2)
                with col1:
                    preferred_departments = st.multiselect("Preferred Departments",
                        ["Computer Science", "Electrical Engineering", "Mechanical Engineering",
                         "Civil Engineering", "Information Technology", "All Departments"])
                    min_cgpa = st.number_input("Minimum CGPA Preferred", 0.0, 10.0, 7.0, 0.5)
                with col2:
                    job_roles = st.text_input("Common Job Roles (comma-separated)",
                        "Software Engineer, Data Analyst, Product Manager")
                    avg_package = st.number_input("Average Package Offered (LPA)", 0.0, 50.0, 12.0, 1.0)
                
                if st.form_submit_button("✅ Register Company"):
                    # Generate company ID
                    company_id = f"C{len(self.college_data['companies']) + 100:03d}"
                    
                    # Add to companies dataframe
                    new_company = pd.DataFrame([{
                        "company_id": company_id,
                        "name": company_name,
                        "industry": industry,
                        "website": website,
                        "contact_person": contact_person,
                        "contact_email": contact_email,
                        "contact_phone": contact_phone,
                        "hr_email": hr_email,
                        "recruitment_status": "Active",
                        "visits_this_year": 0,
                        "total_hires": 0,
                        "avg_package": avg_package,
                        "preferred_departments": ", ".join(preferred_departments) if preferred_departments else "All",
                        "min_cgpa": min_cgpa,
                        "job_roles": job_roles
                    }])
                    
                    self.college_data["companies"] = pd.concat([self.college_data["companies"], new_company], ignore_index=True)
                    st.success(f"Company {company_name} registered successfully! Company ID: {company_id}")
                    
                    # Show next steps
                    st.info(f"""
                    **Next Steps:**
                    1. Share login credentials with {contact_person}
                    2. Schedule campus drive in Drive Scheduling module
                    3. Add job postings through recruiter portal
                    """)
        
        with tab2:
            st.subheader("Company Directory")
            
            # Search and filters
            col1, col2 = st.columns(2)
            with col1:
                search_company = st.text_input("Search Company")
            with col2:
                industry_filter = st.selectbox("Filter by Industry", 
                    ["All"] + list(self.college_data["companies"]["industry"].unique()))
            
            # Filter companies
            filtered_companies = self.college_data["companies"].copy()
            if search_company:
                filtered_companies = filtered_companies[
                    filtered_companies["name"].str.contains(search_company, case=False)
                ]
            if industry_filter != "All":
                filtered_companies = filtered_companies[filtered_companies["industry"] == industry_filter]
            
            # Display companies
            for _, company in filtered_companies.iterrows():
                with st.expander(f"🏢 {company['name']} ({company['industry']})", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Contact Information:**")
                        st.write(f"**Contact:** {company['contact_person']}")
                        st.write(f"**Email:** {company['contact_email']}")
                        st.write(f"**Phone:** {company['contact_phone']}")
                        st.write(f"**Website:** {company['website']}")
                    
                    with col2:
                        st.write("**Recruitment Stats:**")
                        st.write(f"**Status:** {company['recruitment_status']}")
                        st.write(f"**Visits this year:** {company['visits_this_year']}")
                        st.write(f"**Total hires:** {company['total_hires']}")
                        st.write(f"**Avg package:** ₹{company['avg_package']}L")
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button(f"📅 Schedule Drive", key=f"schedule_{company['company_id']}", width='stretch'):
                            st.session_state.selected_company = company['name']
                            from modules.workflow_manager import WorkflowManager
                            workflow = WorkflowManager()
                            workflow.workflows["college"]["current_step"] = 4
                            st.rerun()
                    
                    with col2:
                        if st.button(f"✏️ Edit", key=f"edit_{company['company_id']}", width='stretch'):
                            st.info(f"Editing {company['name']} - Form would appear here")
                    
                    with col3:
                        if st.button(f"📧 Contact", key=f"contact_{company['company_id']}", width='stretch'):
                            st.info(f"Opening email to {company['contact_email']}")
            
            # Company statistics
            st.subheader("Company Statistics")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Companies", len(filtered_companies))
            with col2:
                active = len(filtered_companies[filtered_companies["recruitment_status"] == "Active"])
                st.metric("Active", active)
            with col3:
                total_hires = filtered_companies["total_hires"].sum()
                st.metric("Total Hires", total_hires)
            with col4:
                avg_package_all = filtered_companies["avg_package"].mean()
                st.metric("Avg Package", f"₹{avg_package_all:.1f}L")
        
        with tab3:
            st.subheader("Company Analytics")
            
            # Industry distribution
            industry_dist = self.college_data["companies"]["industry"].value_counts()
            fig1 = px.pie(values=industry_dist.values, names=industry_dist.index,
                         title="Companies by Industry")
            st.plotly_chart(fig1, use_container_width=True)
            
            # Top hiring companies
            top_companies = self.college_data["companies"].sort_values("total_hires", ascending=False).head(10)
            fig2 = px.bar(top_companies, x="name", y="total_hires",
                         title="Top 10 Companies by Hires",
                         color="total_hires")
            st.plotly_chart(fig2, use_container_width=True)
            
            # Package distribution by industry
            fig3 = px.box(self.college_data["companies"], x="industry", y="avg_package",
                         title="Package Distribution by Industry")
            st.plotly_chart(fig3, use_container_width=True)
    
    def step4_drive_scheduling(self):
        """Step 4: Campus Drive Scheduling"""
        st.info("Schedule and manage campus recruitment drives")
        
        tab1, tab2, tab3 = st.tabs(["📅 Schedule New Drive", "📋 Upcoming Drives", "📊 Drive Analytics"])
        
        with tab1:
            st.subheader("Schedule New Campus Drive")
            
            with st.form("drive_scheduling_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    # Company selection
                    companies = self.college_data["companies"]["name"].tolist()
                    selected_company = st.selectbox("Select Company*", companies)
                    
                    # Get company details
                    company_details = self.college_data["companies"][
                        self.college_data["companies"]["name"] == selected_company
                    ].iloc[0]
                    
                    drive_date = st.date_input("Drive Date*", 
                        min_value=datetime.now().date(),
                        value=datetime.now().date() + timedelta(days=30))
                    
                    drive_mode = st.selectbox("Drive Mode*", 
                        ["Online", "Offline", "Hybrid"])
                
                with col2:
                    # Time and venue
                    drive_time = st.time_input("Start Time*", datetime.strptime("10:00", "%H:%M"))
                    
                    if drive_mode in ["Offline", "Hybrid"]:
                        venue = st.text_input("Venue*", "Main Campus Auditorium")
                    else:
                        venue = st.text_input("Online Platform", "Microsoft Teams")
                    
                    registration_deadline = st.date_input("Registration Deadline*",
                        min_value=datetime.now().date(),
                        value=datetime.now().date() + timedelta(days=15))
                
                # Job roles for this drive
                st.subheader("Job Details")
                col1, col2, col3 = st.columns(3)
                with col1:
                    job_roles = st.text_input("Job Roles*", company_details.get("job_roles", "Software Engineer"))
                with col2:
                    vacancies = st.number_input("Number of Vacancies", 1, 100, 10)
                with col3:
                    package_range = st.text_input("Package Range (LPA)", f"{company_details['avg_package']-2}-{company_details['avg_package']+2}")
                
                # Eligibility criteria
                st.subheader("Eligibility Criteria")
                col1, col2, col3 = st.columns(3)
                with col1:
                    min_cgpa = st.number_input("Minimum CGPA", 0.0, 10.0, float(company_details.get("min_cgpa", 7.0)), 0.1)
                with col2:
                    max_backlogs = st.number_input("Maximum Backlogs", 0, 10, int(company_details.get("max_backlogs", 2)))
                with col3:
                    eligible_departments = st.multiselect("Eligible Departments",
                        ["Computer Science", "Electrical Engineering", "Mechanical Engineering",
                         "Civil Engineering", "Information Technology", "All Departments"],
                        default=["Computer Science", "Information Technology"])
                
                # Drive coordinator
                st.subheader("Drive Coordination")
                col1, col2 = st.columns(2)
                with col1:
                    coordinator_name = st.text_input("Coordinator Name*", "Placement Officer")
                    coordinator_email = st.text_input("Coordinator Email*", "placement@college.edu")
                with col2:
                    coordinator_phone = st.text_input("Coordinator Phone*", "+91 9876543210")
                    expected_students = st.number_input("Expected Students", 50, 500, 150)
                
                if st.form_submit_button("✅ Schedule Drive"):
                    # Generate drive ID
                    drive_id = f"D{len(self.college_data['drives']) + 100:03d}"
                    
                    # Add to drives dataframe
                    new_drive = pd.DataFrame([{
                        "drive_id": drive_id,
                        "company": selected_company,
                        "date": drive_date.strftime("%Y-%m-%d"),
                        "time": drive_time.strftime("%H:%M"),
                        "mode": drive_mode,
                        "venue": venue,
                        "coordinator": coordinator_name,
                        "coordinator_contact": coordinator_phone,
                        "registration_deadline": registration_deadline.strftime("%Y-%m-%d"),
                        "status": "Scheduled",
                        "registered": 0,
                        "selected": 0,
                        "job_roles": job_roles,
                        "vacancies": vacancies,
                        "package_range": package_range,
                        "min_cgpa": min_cgpa,
                        "max_backlogs": max_backlogs,
                        "eligible_departments": ", ".join(eligible_departments),
                        "expected_students": expected_students
                    }])
                    
                    self.college_data["drives"] = pd.concat([self.college_data["drives"], new_drive], ignore_index=True)
                    
                    st.success(f"✅ Campus drive scheduled successfully!")
                    st.balloons()
                    
                    # Show drive summary
                    st.subheader("Drive Summary")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Drive ID:** {drive_id}")
                        st.write(f"**Company:** {selected_company}")
                        st.write(f"**Date:** {drive_date.strftime('%d %b %Y')}")
                        st.write(f"**Time:** {drive_time.strftime('%I:%M %p')}")
                    with col2:
                        st.write(f"**Mode:** {drive_mode}")
                        st.write(f"**Venue:** {venue}")
                        st.write(f"**Registration Deadline:** {registration_deadline.strftime('%d %b %Y')}")
                        st.write(f"**Expected Students:** {expected_students}")
        
        with tab2:
            st.subheader("Upcoming & Active Drives")
            
            # Filter drives
            today = datetime.now().strftime("%Y-%m-%d")
            upcoming_drives = self.college_data["drives"][
                (self.college_data["drives"]["status"] == "Scheduled") |
                (self.college_data["drives"]["date"] >= today)
            ]
            
            completed_drives = self.college_data["drives"][
                self.college_data["drives"]["status"] == "Completed"
            ]
            
            # Display upcoming drives
            st.write(f"**📅 Upcoming Drives ({len(upcoming_drives)})**")
            if not upcoming_drives.empty:
                for _, drive in upcoming_drives.sort_values("date").iterrows():
                    days_until = (datetime.strptime(drive["date"], "%Y-%m-%d") - datetime.now()).days
                    
                    with st.expander(f"{drive['company']} - {drive['date']} ({days_until} days)", expanded=False):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Drive Details:**")
                            st.write(f"**ID:** {drive['drive_id']}")
                            st.write(f"**Mode:** {drive['mode']}")
                            st.write(f"**Venue:** {drive['venue']}")
                            st.write(f"**Time:** {drive.get('time', '10:00')}")
                        
                        with col2:
                            st.write("**Registration:**")
                            st.write(f"**Deadline:** {drive.get('registration_deadline', 'N/A')}")
                            st.write(f"**Registered:** {drive['registered']}/{drive.get('expected_students', 150)}")
                            st.write(f"**Vacancies:** {drive.get('vacancies', 10)}")
                            st.write(f"**Status:** {drive['status']}")
                        
                        # Action buttons
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("👥 View Registrations", key=f"view_{drive['drive_id']}", width='stretch'):
                                st.info(f"Showing registrations for {drive['company']} drive")
                        
                        with col2:
                            if st.button("📝 Manage", key=f"manage_{drive['drive_id']}", width='stretch'):
                                st.info(f"Managing {drive['company']} drive")
                        
                        with col3:
                            if drive['status'] == 'Scheduled' and st.button("✅ Mark Complete", key=f"complete_{drive['drive_id']}", width='stretch'):
                                self.college_data["drives"].loc[
                                    self.college_data["drives"]["drive_id"] == drive['drive_id'], 
                                    'status'
                                ] = 'Completed'
                                st.success(f"Drive marked as completed!")
                                st.rerun()
            else:
                st.info("No upcoming drives scheduled")
            
            # Display completed drives
            st.write(f"**✅ Completed Drives ({len(completed_drives)})**")
            if not completed_drives.empty:
                summary_data = completed_drives[['company', 'date', 'registered', 'selected']].copy()
                summary_data['selection_rate'] = (summary_data['selected'] / summary_data['registered'] * 100).round(1)
                st.dataframe(summary_data, use_container_width=True)
        
        with tab3:
            st.subheader("Drive Analytics")
            
            # Drive statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_drives = len(self.college_data["drives"])
                st.metric("Total Drives", total_drives)
            with col2:
                completed = len(self.college_data["drives"][self.college_data["drives"]["status"] == "Completed"])
                st.metric("Completed", completed)
            with col3:
                total_registered = self.college_data["drives"]["registered"].sum()
                st.metric("Total Registered", total_registered)
            with col4:
                total_selected = self.college_data["drives"]["selected"].sum()
                st.metric("Total Selected", total_selected)
            
            # Selection rate by company
            if not self.college_data["drives"].empty:
                drive_stats = self.college_data["drives"].groupby("company").agg({
                    "drive_id": "count",
                    "registered": "sum",
                    "selected": "sum"
                }).reset_index()
                drive_stats["selection_rate"] = (drive_stats["selected"] / drive_stats["registered"] * 100).round(1)
                
                fig1 = px.bar(drive_stats, x="company", y="selection_rate",
                             title="Selection Rate by Company",
                             color="selection_rate")
                st.plotly_chart(fig1, use_container_width=True)
            
            # Monthly drive trend
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            drives_per_month = [2, 3, 4, 3, 5, 4, 2, 1, 3, 4, 5, 3]  # Sample data
            
            trend_data = pd.DataFrame({
                'Month': months,
                'Drives': drives_per_month
            })
            
            fig2 = px.line(trend_data, x='Month', y='Drives',
                          title="Monthly Drive Trend",
                          markers=True)
            st.plotly_chart(fig2, use_container_width=True)
    
    def step5_student_company_matching(self):
        """Step 5: Student-Company Matching"""
        st.info("AI-powered matching of students with suitable companies")
        
        tab1, tab2, tab3 = st.tabs(["🤖 AI Matching", "🎯 Manual Matching", "📊 Match Analytics"])
        
        with tab1:
            st.subheader("AI-Powered Student-Company Matching")
            
            # Select parameters for matching
            col1, col2 = st.columns(2)
            with col1:
                match_algorithm = st.selectbox("Matching Algorithm",
                    ["Skills-based", "CGPA-weighted", "Hybrid (Skills + CGPA)", "Company-specific"])
                
                min_match_score = st.slider("Minimum Match Score", 0, 100, 70)
            
            with col2:
                companies_to_match = st.multiselect("Select Companies to Match",
                    self.college_data["companies"]["name"].tolist(),
                    default=self.college_data["companies"]["name"].tolist()[:3])
                
                departments_to_include = st.multiselect("Departments to Include",
                    ["Computer Science", "Electrical Engineering", "Mechanical Engineering",
                     "Civil Engineering", "Information Technology", "All"],
                    default=["Computer Science", "Information Technology"])
            
            if st.button("🔍 Run AI Matching", type="primary", width='stretch'):
                with st.spinner("Running AI matching algorithm..."):
                    # Simulate AI matching
                    import time
                    time.sleep(2)
                    
                    # Generate sample matches
                    matches = []
                    students = self.college_data["students"][
                        self.college_data["students"]["placement_status"] == "Not Placed"
                    ]
                    
                    if departments_to_include and "All" not in departments_to_include:
                        students = students[students["department"].isin(departments_to_include)]
                    
                    for _, student in students.head(20).iterrows():
                        for company in companies_to_match[:3]:
                            # Calculate match score (simplified)
                            cgpa_score = min(student["cgpa"] * 10, 30)  # Max 30 points for CGPA
                            skills_score = 40  # Assuming average skills
                            department_match = 20 if student["department"] in ["Computer Science", "IT"] else 15
                            backlogs_penalty = student["backlogs"] * 5
                            
                            match_score = cgpa_score + skills_score + department_match - backlogs_penalty
                            match_score = min(100, max(0, match_score))
                            
                            if match_score >= min_match_score:
                                matches.append({
                                    "student_id": student["student_id"],
                                    "student_name": student["name"],
                                    "department": student["department"],
                                    "cgpa": student["cgpa"],
                                    "company": company,
                                    "match_score": match_score,
                                    "recommended_role": "Software Engineer" if student["department"] in ["CS", "IT"] else "Engineer",
                                    "reason": f"Strong {student['department']} background with CGPA {student['cgpa']}"
                                })
                    
                    matches_df = pd.DataFrame(matches)
                    
                    if not matches_df.empty:
                        st.success(f"Found {len(matches_df)} potential matches!")
                        
                        # Display matches
                        st.subheader("Top Matches")
                        matches_df = matches_df.sort_values("match_score", ascending=False)
                        st.dataframe(matches_df, use_container_width=True)
                        
                        # Export matches
                        csv = matches_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Matches",
                            data=csv,
                            file_name=f"student_matches_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
                        
                        # Send recommendations
                        if st.button("📧 Send Recommendations to Students"):
                            st.success("Recommendations sent to students!")
                    else:
                        st.warning("No matches found with current criteria")
        
        with tab2:
            st.subheader("Manual Student-Company Matching")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Select Students:**")
                unplaced_students = self.college_data["students"][
                    self.college_data["students"]["placement_status"] == "Not Placed"
                ]
                
                selected_students = st.multiselect(
                    "Choose Students",
                    unplaced_students.apply(lambda x: f"{x['name']} ({x['student_id']}) - {x['department']}", axis=1).tolist(),
                    key="manual_students"
                )
                
                if selected_students:
                    st.write("**Selected Students:**")
                    for student in selected_students:
                        st.write(f"• {student}")
            
            with col2:
                st.write("**Select Company & Role:**")
                selected_company = st.selectbox("Company", 
                    self.college_data["companies"]["name"].tolist())
                
                job_role = st.text_input("Job Role", "Software Engineer")
                
                package = st.number_input("Package (LPA)", 0.0, 50.0, 12.0, 0.5)
            
            if st.button("✅ Create Manual Match", type="primary", width='stretch'):
                if selected_students and selected_company:
                    # Extract student IDs
                    student_ids = [s.split("(")[1].split(")")[0] for s in selected_students]
                    
                    st.success(f"Matched {len(student_ids)} students with {selected_company} for {job_role} role!")
                    
                    # Show next steps
                    st.info("""
                    **Next Steps:**
                    1. Notify selected students
                    2. Schedule interviews
                    3. Update student records after placement
                    """)
                else:
                    st.error("Please select both students and company")
        
        with tab3:
            st.subheader("Matching Analytics")
            
            # Match success rate
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Matches Made", "127")
            with col2:
                st.metric("Match Success Rate", "68%")
            with col3:
                st.metric("Avg Time to Match", "14 days")
            
            # Department-wise match success
            dept_data = {
                'Department': ['CS', 'IT', 'EE', 'ME', 'CE'],
                'Matches': [45, 38, 22, 15, 7],
                'Success Rate': [75, 70, 65, 60, 55]
            }
            
            dept_df = pd.DataFrame(dept_data)
            
            fig1 = px.bar(dept_df, x='Department', y='Success Rate',
                         title="Match Success Rate by Department",
                         color='Success Rate')
            st.plotly_chart(fig1, use_container_width=True)
            
            # Company-wise matches
            company_data = {
                'Company': ['Google', 'Microsoft', 'Amazon', 'TCS', 'Infosys'],
                'Matches': [25, 22, 20, 35, 25],
                'Acceptance Rate': [85, 82, 80, 75, 78]
            }
            
            company_df = pd.DataFrame(company_data)
            
            fig2 = px.scatter(company_df, x='Matches', y='Acceptance Rate',
                             size='Acceptance Rate', color='Company',
                             title="Company-wise Match Performance")
            st.plotly_chart(fig2, use_container_width=True)
    
    def step6_interview_management(self):
        """Step 6: Interview Management"""
        st.info("Schedule and track student interviews")
        
        tab1, tab2, tab3 = st.tabs(["📅 Schedule Interview", "📋 Interview Calendar", "📊 Interview Analytics"])
        
        with tab1:
            st.subheader("Schedule New Interview")
            
            with st.form("interview_scheduling_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    # Student selection
                    students = self.college_data["students"][
                        self.college_data["students"]["placement_status"].isin(["Not Placed", "Intern"])
                    ]
                    student_options = students.apply(
                        lambda x: f"{x['name']} ({x['student_id']}) - {x['department']}", axis=1
                    ).tolist()
                    
                    selected_student = st.selectbox("Select Student*", student_options)
                    
                    # Extract student ID
                    student_id = selected_student.split("(")[1].split(")")[0] if selected_student else ""
                    
                    company = st.selectbox("Company*", 
                        self.college_data["companies"]["name"].tolist())
                    
                    interview_round = st.selectbox("Interview Round*",
                        ["Aptitude Test", "Technical Round 1", "Technical Round 2", 
                         "HR Round", "Managerial Round", "Final Round"])
                
                with col2:
                    interview_date = st.date_input("Interview Date*",
                        min_value=datetime.now().date(),
                        value=datetime.now().date() + timedelta(days=7))
                    
                    interview_time = st.time_input("Interview Time*", datetime.strptime("10:00", "%H:%M"))
                    
                    interview_mode = st.selectbox("Interview Mode*",
                        ["Online", "Offline", "Phone"])
                
                # Additional details
                col1, col2 = st.columns(2)
                with col1:
                    if interview_mode in ["Online", "Phone"]:
                        meeting_link = st.text_input("Meeting Link/Phone Number*")
                    else:
                        venue = st.text_input("Venue*", "Company Office")
                
                with col2:
                    interviewer_name = st.text_input("Interviewer Name")
                    interviewer_role = st.text_input("Interviewer Role", "Senior Engineer")
                
                job_role = st.text_input("Job Role", "Software Engineer")
                notes = st.text_area("Additional Notes", placeholder="Any special instructions...")
                
                if st.form_submit_button("✅ Schedule Interview"):
                    # Generate interview ID
                    interview_id = f"I{len(self.college_data['interviews']) + 1000:04d}"
                    
                    # Get student name
                    student_name = selected_student.split("(")[0].strip()
                    
                    # Add to interviews dataframe
                    new_interview = pd.DataFrame([{
                        "interview_id": interview_id,
                        "student_id": student_id,
                        "student_name": student_name,
                        "company": company,
                        "round": interview_round,
                        "date": interview_date.strftime("%Y-%m-%d"),
                        "time": interview_time.strftime("%H:%M"),
                        "mode": interview_mode,
                        "meeting_link": meeting_link if interview_mode in ["Online", "Phone"] else "",
                        "venue": venue if interview_mode == "Offline" else "",
                        "interviewer": interviewer_name,
                        "interviewer_role": interviewer_role,
                        "job_role": job_role,
                        "status": "Scheduled",
                        "result": "Pending",
                        "notes": notes
                    }])
                    
                    self.college_data["interviews"] = pd.concat(
                        [self.college_data["interviews"], new_interview], 
                        ignore_index=True
                    )
                    
                    st.success(f"✅ Interview scheduled for {student_name} with {company}!")
                    
                    # Show interview details
                    st.subheader("Interview Details")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Interview ID:** {interview_id}")
                        st.write(f"**Student:** {student_name}")
                        st.write(f"**Company:** {company}")
                        st.write(f"**Round:** {interview_round}")
                    
                    with col2:
                        st.write(f"**Date:** {interview_date.strftime('%d %b %Y')}")
                        st.write(f"**Time:** {interview_time.strftime('%I:%M %p')}")
                        st.write(f"**Mode:** {interview_mode}")
                        if interview_mode in ["Online", "Phone"]:
                            st.write(f"**Link:** {meeting_link}")
        
        with tab2:
            st.subheader("Interview Calendar")
            
            # Filter options
            col1, col2, col3 = st.columns(3)
            with col1:
                view_type = st.selectbox("View", ["Upcoming", "Today", "This Week", "All"])
            with col2:
                status_filter = st.selectbox("Status", ["All", "Scheduled", "Completed", "Cancelled"])
            with col3:
                company_filter = st.selectbox("Company", ["All"] + self.college_data["companies"]["name"].tolist())
            
            # Filter interviews
            filtered_interviews = self.college_data["interviews"].copy()
            
            if status_filter != "All":
                filtered_interviews = filtered_interviews[filtered_interviews["status"] == status_filter]
            
            if company_filter != "All":
                filtered_interviews = filtered_interviews[filtered_interviews["company"] == company_filter]
            
            # Filter by date based on view type
            today = datetime.now().date()
            if view_type == "Today":
                filtered_interviews = filtered_interviews[
                    filtered_interviews["date"] == today.strftime("%Y-%m-%d")
                ]
            elif view_type == "This Week":
                week_start = today - timedelta(days=today.weekday())
                week_end = week_start + timedelta(days=6)
                filtered_interviews = filtered_interviews[
                    (filtered_interviews["date"] >= week_start.strftime("%Y-%m-%d")) &
                    (filtered_interviews["date"] <= week_end.strftime("%Y-%m-%d"))
                ]
            elif view_type == "Upcoming":
                filtered_interviews = filtered_interviews[
                    filtered_interviews["date"] >= today.strftime("%Y-%m-%d")
                ]
            
            # Display interviews
            if not filtered_interviews.empty:
                st.write(f"**Found {len(filtered_interviews)} interviews**")
                
                for _, interview in filtered_interviews.sort_values(["date", "time"]).iterrows():
                    # Determine status color
                    status_color = {
                        "Scheduled": "🟡",
                        "Completed": "🟢",
                        "Cancelled": "🔴"
                    }.get(interview["status"], "⚪")
                    
                    with st.expander(
                        f"{status_color} {interview['company']} - {interview['student_name']} ({interview['date']})",
                        expanded=False
                    ):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Interview Details:**")
                            st.write(f"**ID:** {interview['interview_id']}")
                            st.write(f"**Round:** {interview['round']}")
                            st.write(f"**Job Role:** {interview.get('job_role', 'N/A')}")
                            st.write(f"**Time:** {interview['time']}")
                        
                        with col2:
                            st.write("**Status & Results:**")
                            st.write(f"**Status:** {interview['status']}")
                            st.write(f"**Result:** {interview['result']}")
                            st.write(f"**Mode:** {interview['mode']}")
                            if interview['mode'] in ["Online", "Phone"] and interview.get('meeting_link'):
                                st.write(f"**Link:** {interview['meeting_link']}")
                        
                        # Action buttons
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if interview['status'] == 'Scheduled' and st.button("✅ Mark Complete", key=f"complete_{interview['interview_id']}", width='stretch'):
                                self.college_data["interviews"].loc[
                                    self.college_data["interviews"]["interview_id"] == interview['interview_id'],
                                    'status'
                                ] = 'Completed'
                                st.rerun()
                        
                        with col2:
                            if st.button("✏️ Update", key=f"update_{interview['interview_id']}", width='stretch'):
                                st.info(f"Update form for {interview['student_name']}")
                        
                        with col3:
                            if st.button("📧 Remind", key=f"remind_{interview['interview_id']}", width='stretch'):
                                st.success(f"Reminder sent to {interview['student_name']}")
            else:
                st.info("No interviews found with current filters")
            
            # Quick statistics
            st.subheader("Today's Summary")
            today_interviews = self.college_data["interviews"][
                self.college_data["interviews"]["date"] == today.strftime("%Y-%m-%d")
            ]
            
            if not today_interviews.empty:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total", len(today_interviews))
                with col2:
                    scheduled = len(today_interviews[today_interviews["status"] == "Scheduled"])
                    st.metric("Scheduled", scheduled)
                with col3:
                    completed = len(today_interviews[today_interviews["status"] == "Completed"])
                    st.metric("Completed", completed)
                with col4:
                    selected = len(today_interviews[today_interviews["result"] == "Selected"])
                    st.metric("Selected", selected)
        
        with tab3:
            st.subheader("Interview Analytics")
            
            # Overall statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_interviews = len(self.college_data["interviews"])
                st.metric("Total Interviews", total_interviews)
            with col2:
                completion_rate = (len(self.college_data["interviews"][
                    self.college_data["interviews"]["status"] == "Completed"
                ]) / total_interviews * 100) if total_interviews > 0 else 0
                st.metric("Completion Rate", f"{completion_rate:.1f}%")
            with col3:
                selection_rate = (len(self.college_data["interviews"][
                    self.college_data["interviews"]["result"] == "Selected"
                ]) / total_interviews * 100) if total_interviews > 0 else 0
                st.metric("Selection Rate", f"{selection_rate:.1f}%")
            with col4:
                avg_interviews_per_student = total_interviews / len(self.college_data["students"]) * 100
                st.metric("Per Student", f"{avg_interviews_per_student:.1f}%")
            
            # Company-wise interview performance
            if not self.college_data["interviews"].empty:
                company_stats = self.college_data["interviews"].groupby("company").agg({
                    "interview_id": "count",
                    "result": lambda x: (x == "Selected").sum()
                }).reset_index()
                company_stats = company_stats.rename(columns={
                    "interview_id": "total_interviews",
                    "result": "selected"
                })
                company_stats["selection_rate"] = (company_stats["selected"] / company_stats["total_interviews"] * 100).round(1)
                
                fig1 = px.bar(company_stats, x="company", y="selection_rate",
                             title="Selection Rate by Company",
                             color="selection_rate")
                st.plotly_chart(fig1, use_container_width=True)
            
            # Interview round success rate
            round_data = {
                'Round': ['Aptitude', 'Technical 1', 'Technical 2', 'HR', 'Managerial'],
                'Success Rate': [85, 65, 55, 75, 60],
                'Avg Duration': [60, 45, 60, 30, 45]
            }
            
            round_df = pd.DataFrame(round_data)
            
            fig2 = px.scatter(round_df, x='Success Rate', y='Avg Duration',
                             size='Success Rate', color='Round',
                             title="Interview Round Analysis")
            st.plotly_chart(fig2, use_container_width=True)
    
    def step7_placement_records(self):
        """Step 7: Placement Records Management"""
        st.info("Manage and track all placement records")
        
        tab1, tab2, tab3 = st.tabs(["✅ Placement Records", "📋 Offer Management", "📊 Placement Analytics"])
        
        with tab1:
            st.subheader("Placement Records")
            
            # Search and filters
            col1, col2, col3 = st.columns(3)
            with col1:
                search_record = st.text_input("Search by Student/Company")
            with col2:
                department_filter = st.selectbox("Filter by Department", 
                    ["All"] + list(self.college_data["placements"]["department"].unique()))
            with col3:
                company_filter = st.selectbox("Filter by Company", 
                    ["All"] + list(self.college_data["placements"]["company"].unique()))
            
            # Filter placements
            filtered_placements = self.college_data["placements"].copy()
            if search_record:
                filtered_placements = filtered_placements[
                    filtered_placements["student_name"].str.contains(search_record, case=False) |
                    filtered_placements["company"].str.contains(search_record, case=False)
                ]
            if department_filter != "All":
                filtered_placements = filtered_placements[filtered_placements["department"] == department_filter]
            if company_filter != "All":
                filtered_placements = filtered_placements[filtered_placements["company"] == company_filter]
            
            # Display statistics
            total_placements = len(filtered_placements)
            total_package = filtered_placements["package"].sum()
            avg_package = filtered_placements["package"].mean() if total_placements > 0 else 0
            max_package = filtered_placements["package"].max() if total_placements > 0 else 0
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Placements", total_placements)
            with col2:
                st.metric("Total Package", f"₹{total_package:.1f}L")
            with col3:
                st.metric("Avg Package", f"₹{avg_package:.1f}L")
            with col4:
                st.metric("Max Package", f"₹{max_package:.1f}L")
            
            # Display placement records
            st.subheader("Placement Details")
            display_cols = st.multiselect("Select columns to display",
                ["placement_id", "student_id", "student_name", "department", "company", 
                 "job_role", "package", "placement_date", "status"],
                default=["student_name", "department", "company", "job_role", "package", "placement_date"])
            
            if display_cols:
                st.dataframe(filtered_placements[display_cols], width='stretch', height=400)
                
                # Export option
                csv = filtered_placements[display_cols].to_csv(index=False)
                st.download_button(
                    label="📥 Export to CSV",
                    data=csv,
                    file_name=f"placement_records_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            
            # Add new placement record
            with st.expander("➕ Add New Placement Record", expanded=False):
                with st.form("new_placement_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        student_id = st.text_input("Student ID*")
                        student_name = st.text_input("Student Name*")
                        department = st.selectbox("Department*",
                            ["Computer Science", "Electrical Engineering", "Mechanical Engineering",
                             "Civil Engineering", "Information Technology"])
                    
                    with col2:
                        company = st.text_input("Company*")
                        job_role = st.text_input("Job Role*")
                        package = st.number_input("Package (LPA)*", 0.0, 50.0, 12.0, 0.5)
                    
                    placement_date = st.date_input("Placement Date*", datetime.now().date())
                    status = st.selectbox("Status*", 
                        ["Offer Accepted", "Joined", "Completed Internship", "Offer Pending"])
                    
                    if st.form_submit_button("✅ Add Placement Record"):
                        # Generate placement ID
                        placement_id = f"P{len(self.college_data['placements']) + 1000:04d}"
                        
                        # Add to placements dataframe
                        new_placement = pd.DataFrame([{
                            "placement_id": placement_id,
                            "student_id": student_id,
                            "student_name": student_name,
                            "department": department,
                            "company": company,
                            "job_role": job_role,
                            "package": package,
                            "placement_date": placement_date.strftime("%Y-%m-%d"),
                            "status": status
                        }])
                        
                        self.college_data["placements"] = pd.concat(
                            [self.college_data["placements"], new_placement], 
                            ignore_index=True
                        )
                        
                        # Update student record
                        student_idx = self.college_data["students"][
                            self.college_data["students"]["student_id"] == student_id
                        ].index
                        
                        if not student_idx.empty:
                            self.college_data["students"].loc[student_idx[0], "placement_status"] = "Placed"
                            self.college_data["students"].loc[student_idx[0], "company"] = company
                            self.college_data["students"].loc[student_idx[0], "package"] = package
                        
                        st.success(f"✅ Placement record added for {student_name}!")
        
        with tab2:
            st.subheader("Offer Management")
            
            # Pending offers
            st.write("**⏳ Pending Offers**")
            pending_offers = self.college_data["placements"][
                self.college_data["placements"]["status"] == "Offer Pending"
            ]
            
            if not pending_offers.empty:
                for _, offer in pending_offers.iterrows():
                    with st.expander(f"{offer['student_name']} - {offer['company']} (₹{offer['package']}L)", expanded=False):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Offer Details:**")
                            st.write(f"**Student:** {offer['student_name']}")
                            st.write(f"**Department:** {offer['department']}")
                            st.write(f"**Job Role:** {offer['job_role']}")
                            st.write(f"**Package:** ₹{offer['package']}L")
                        
                        with col2:
                            st.write("**Status:** Offer Pending")
                            st.write(f"**Days Pending:** {(datetime.now() - datetime.strptime(offer['placement_date'], '%Y-%m-%d')).days}")
                            
                            # Action buttons
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("✅ Accept", key=f"accept_{offer['placement_id']}", width='stretch'):
                                    self.college_data["placements"].loc[
                                        self.college_data["placements"]["placement_id"] == offer['placement_id'],
                                        'status'
                                    ] = 'Offer Accepted'
                                    st.success("Offer accepted!")
                                    st.rerun()
                            
                            with col2:
                                if st.button("❌ Decline", key=f"decline_{offer['placement_id']}", width='stretch'):
                                    self.college_data["placements"].loc[
                                        self.college_data["placements"]["placement_id"] == offer['placement_id'],
                                        'status'
                                    ] = 'Offer Declined'
                                    st.success("Offer declined!")
                                    st.rerun()
            else:
                st.info("No pending offers")
            
            # Accepted offers
            st.write("**✅ Accepted Offers**")
            accepted_offers = self.college_data["placements"][
                self.college_data["placements"]["status"] == "Offer Accepted"
            ]
            
            if not accepted_offers.empty:
                st.dataframe(accepted_offers[["student_name", "company", "job_role", "package", "placement_date"]], 
                           use_container_width=True)
            else:
                st.info("No accepted offers")
        
        with tab3:
            st.subheader("Placement Analytics")
            
            # Monthly placement trend
            if not self.college_data["placements"].empty:
                # Convert to datetime and extract month
                placements_with_date = self.college_data["placements"].copy()
                placements_with_date["month"] = pd.to_datetime(
                    placements_with_date["placement_date"]
                ).dt.strftime("%Y-%m")
                
                monthly_stats = placements_with_date.groupby("month").agg({
                    "placement_id": "count",
                    "package": "mean"
                }).reset_index()
                monthly_stats = monthly_stats.rename(columns={
                    "placement_id": "placements",
                    "package": "avg_package"
                })
                
                fig1 = px.line(monthly_stats, x="month", y="placements",
                              title="Monthly Placement Trend",
                              markers=True)
                st.plotly_chart(fig1, use_container_width=True)
            
            # Package distribution
            fig2 = px.histogram(self.college_data["placements"], x="package",
                               title="Package Distribution",
                               nbins=20)
            st.plotly_chart(fig2, use_container_width=True)
            
            # Top packages
            st.subheader("🏆 Top 10 Packages")
            top_packages = self.college_data["placements"].sort_values("package", ascending=False).head(10)
            st.dataframe(top_packages[["student_name", "department", "company", "job_role", "package"]], 
                       use_container_width=True)
    
    def step8_performance_reports(self):
        """Step 8: Performance Reports & Analytics"""
        st.info("Generate comprehensive performance reports and analytics")
        
        tab1, tab2, tab3 = st.tabs(["📈 Overall Performance", "🏫 Department Reports", "📋 Custom Reports"])
        
        with tab1:
            st.subheader("Overall College Performance")
            
            # Key Performance Indicators
            st.write("**🎯 Key Performance Indicators (KPIs)**")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_students = len(self.college_data["students"])
                st.metric("Total Students", total_students)
            with col2:
                placed = len(self.college_data["students"][self.college_data["students"]["placement_status"] == "Placed"])
                placement_rate = (placed / total_students * 100) if total_students > 0 else 0
                st.metric("Placement Rate", f"{placement_rate:.1f}%", "+5.2%")
            with col3:
                avg_package = self.college_data["students"]["package"].mean()
                st.metric("Avg Package", f"₹{avg_package:.1f}L", "+2.1L")
            with col4:
                top_package = self.college_data["students"]["package"].max()
                st.metric("Highest Package", f"₹{top_package:.1f}L")
            
            # Year-over-Year Comparison
            st.subheader("📅 Year-over-Year Comparison")
            
            years = [2021, 2022, 2023, 2024]
            placement_rates = [65, 72, 78, 82]
            avg_packages = [10.5, 12.2, 14.5, 16.8]
            
            comparison_data = pd.DataFrame({
                'Year': years,
                'Placement Rate': placement_rates,
                'Avg Package': avg_packages
            })
            
            fig1 = px.line(comparison_data, x='Year', y=['Placement Rate', 'Avg Package'],
                          title="Year-over-Year Performance",
                          markers=True)
            st.plotly_chart(fig1, use_container_width=True)
            
            # Placement Distribution by Company Type
            st.subheader("🏢 Placement Distribution by Company Type")
            
            company_types = {
                'Product-Based': ['Google', 'Microsoft', 'Amazon', 'Adobe'],
                'Service-Based': ['TCS', 'Infosys', 'Wipro', 'Cognizant'],
                'Startups': ['TechCorp', 'InnovateLabs', 'StartupX']
            }
            
            company_data = []
            for ctype, companies in company_types.items():
                placements = self.college_data["placements"][
                    self.college_data["placements"]["company"].isin(companies)
                ]
                company_data.append({
                    'Type': ctype,
                    'Placements': len(placements),
                    'Avg Package': placements['package'].mean() if not placements.empty else 0
                })
            
            company_df = pd.DataFrame(company_data)
            
            col1, col2 = st.columns(2)
            with col1:
                fig2 = px.pie(company_df, values='Placements', names='Type',
                             title="Placements by Company Type")
                st.plotly_chart(fig2, use_container_width=True)
            
            with col2:
                fig3 = px.bar(company_df, x='Type', y='Avg Package',
                             title="Avg Package by Company Type",
                             color='Avg Package')
                st.plotly_chart(fig3, use_container_width=True)
            
            # Performance Summary
            st.subheader("📊 Performance Summary")
            
            summary_data = {
                'Metric': ['Placement Rate', 'Avg Package', 'Highest Package', 
                          'Internship Rate', 'Multiple Offers', 'Dream Offers'],
                'Current': [82, 16.8, 42.5, 15, 8, 12],
                'Target': [85, 18.0, 50.0, 20, 10, 15],
                'Trend': ['↗️', '↗️', '↗️', '→', '↗️', '↗️']
            }
            
            summary_df = pd.DataFrame(summary_data)
            st.dataframe(summary_df, use_container_width=True)
        
        with tab2:
            st.subheader("Department-wise Performance Reports")
            
            # Select department
            departments = self.college_data["students"]["department"].unique()
            selected_dept = st.selectbox("Select Department", departments)
            
            if selected_dept:
                # Department statistics
                dept_students = self.college_data["students"][
                    self.college_data["students"]["department"] == selected_dept
                ]
                dept_placements = self.college_data["placements"][
                    self.college_data["placements"]["department"] == selected_dept
                ]
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    total = len(dept_students)
                    st.metric("Total Students", total)
                with col2:
                    placed = len(dept_students[dept_students["placement_status"] == "Placed"])
                    placement_rate = (placed / total * 100) if total > 0 else 0
                    st.metric("Placement Rate", f"{placement_rate:.1f}%")
                with col3:
                    avg_package = dept_placements["package"].mean() if not dept_placements.empty else 0
                    st.metric("Avg Package", f"₹{avg_package:.1f}L")
                with col4:
                    top_companies = dept_placements["company"].value_counts().head(3)
                    st.metric("Top Recruiters", ", ".join(top_companies.index.tolist()) if not top_companies.empty else "N/A")
                
                # Top packages in department
                st.subheader(f"🏆 Top Packages in {selected_dept}")
                if not dept_placements.empty:
                    top_dept_packages = dept_placements.sort_values("package", ascending=False).head(10)
                    st.dataframe(top_dept_packages[["student_name", "company", "job_role", "package"]], 
                               use_container_width=True)
                else:
                    st.info(f"No placement records for {selected_dept}")
                
                # Company-wise distribution
                st.subheader(f"🏢 Company-wise Placements in {selected_dept}")
                if not dept_placements.empty:
                    company_dist = dept_placements["company"].value_counts().reset_index()
                    company_dist.columns = ['Company', 'Placements']
                    
                    fig = px.bar(company_dist, x='Company', y='Placements',
                                title=f"Placements by Company in {selected_dept}")
                    st.plotly_chart(fig, use_container_width=True)
                
                # Generate department report
                if st.button("📄 Generate Department Report", type="primary", width='stretch'):
                    st.success(f"Report generated for {selected_dept} department!")
                    
                    # Show report preview
                    with st.expander("📋 Report Preview", expanded=True):
                        st.write(f"""
                        ## {selected_dept} Department Placement Report
                        **Generated on:** {datetime.now().strftime('%d %B %Y')}
                        
                        ### Executive Summary
                        - **Total Students:** {total}
                        - **Placement Rate:** {placement_rate:.1f}%
                        - **Average Package:** ₹{avg_package:.1f} LPA
                        - **Highest Package:** ₹{dept_placements['package'].max() if not dept_placements.empty else 0:.1f} LPA
                        
                        ### Top Recruiters
                        {', '.join([f"{company} ({count})" for company, count in top_companies.items()]) if not top_companies.empty else "No data"}
                        
                        ### Recommendations
                        1. Focus on improving placement rate by {max(0, 85 - placement_rate):.1f}%
                        2. Target companies with higher packages
                        3. Enhance skill development programs
                        """)
        
        with tab3:
            st.subheader("Custom Report Generator")
            
            # Report configuration
            col1, col2 = st.columns(2)
            with col1:
                report_type = st.selectbox("Report Type",
                    ["Placement Summary", "Company Analysis", "Student Performance", 
                     "Trend Analysis", "Comparative Analysis"])
                
                time_period = st.selectbox("Time Period",
                    ["Current Year", "Last Year", "Last 3 Years", "Custom"])
                
                if time_period == "Custom":
                    start_date = st.date_input("Start Date")
                    end_date = st.date_input("End Date")
            
            with col2:
                metrics = st.multiselect("Select Metrics",
                    ["Placement Rate", "Average Package", "Highest Package", 
                     "Total Placements", "Company-wise Analysis", "Department-wise Analysis",
                     "Trend Analysis", "Success Rate", "Conversion Rate"],
                    default=["Placement Rate", "Average Package", "Total Placements"])
                
                format_type = st.selectbox("Report Format",
                    ["PDF", "Excel", "HTML", "Dashboard"])
            
            # Additional filters
            st.subheader("Filters")
            col1, col2, col3 = st.columns(3)
            with col1:
                department_filter = st.multiselect("Departments", 
                    list(self.college_data["students"]["department"].unique()))
            with col2:
                company_filter = st.multiselect("Companies",
                    list(self.college_data["companies"]["name"].unique()))
            with col3:
                package_range = st.slider("Package Range (LPA)", 0.0, 50.0, (0.0, 50.0))
            
            # Generate report
            if st.button("🚀 Generate Custom Report", type="primary", width='stretch'):
                with st.spinner("Generating report..."):
                    import time
                    time.sleep(3)
                    
                    st.success("✅ Report generated successfully!")
                    
                    # Show report summary
                    st.subheader("Report Summary")
                    
                    summary_data = {
                        'Report Type': report_type,
                        'Time Period': time_period,
                        'Metrics Included': ', '.join(metrics),
                        'Departments Filtered': ', '.join(department_filter) if department_filter else 'All',
                        'Companies Filtered': ', '.join(company_filter) if company_filter else 'All',
                        'Package Range': f"₹{package_range[0]}L - ₹{package_range[1]}L",
                        'Format': format_type
                    }
                    
                    for key, value in summary_data.items():
                        st.write(f"**{key}:** {value}")
                    
                    # Download options
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.download_button(
                            label="📥 Download PDF",
                            data="Sample PDF content",
                            file_name=f"placement_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf"
                        )
                    with col2:
                        st.download_button(
                            label="📥 Download Excel",
                            data="Sample Excel content",
                            file_name=f"placement_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
                            mime="application/vnd.ms-excel"
                        )
                    with col3:
                        st.download_button(
                            label="📥 Download HTML",
                            data="<h1>Sample Report</h1>",
                            file_name=f"placement_report_{datetime.now().strftime('%Y%m%d')}.html",
                            mime="text/html"
                        )
                    
                    # Preview key findings
                    st.subheader("Key Findings Preview")
                    
                    findings = [
                        f"📈 **Placement Rate:** {placement_rate:.1f}% (Target: 85%)",
                        f"💰 **Average Package:** ₹{avg_package:.1f}L (Growth: +12% YoY)",
                        f"🏆 **Highest Package:** ₹{top_package:.1f}L",
                        f"🏢 **Top Recruiter:** {self.college_data['companies'].iloc[0]['name']}",
                        f"🎯 **Department Leader:** {self.college_data['students']['department'].value_counts().index[0]}",
                        f"📊 **Selection Rate:** 68% (Improvement needed in HR rounds)"
                    ]
                    
                    for finding in findings:
                        st.write(finding)
    
    def display_workflow_navigation(self, current_step):
        """Display navigation buttons for workflow"""
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if current_step > 1 and st.button("⬅️ Previous Step", width='stretch'):
                from modules.workflow_manager import WorkflowManager
                workflow = WorkflowManager()
                workflow.workflows["college"]["current_step"] = current_step - 1
                st.rerun()
        
        with col3:
            if current_step < 8 and st.button("Next Step ➡️", width='stretch'):
                from modules.workflow_manager import WorkflowManager
                workflow = WorkflowManager()
                workflow.workflows["college"]["current_step"] = current_step + 1
                st.rerun()
