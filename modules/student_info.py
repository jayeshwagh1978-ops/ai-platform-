import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

class StudentInfoModule:
    def __init__(self):
        self.students_df = self.load_sample_data()
    
    def load_sample_data(self):
        """Load sample student data"""
        data = {
            'student_id': ['S001', 'S002', 'S003', 'S004', 'S005'],
            'name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Charlie Wilson'],
            'email': ['john@college.edu', 'jane@college.edu', 'bob@college.edu', 'alice@college.edu', 'charlie@college.edu'],
            'phone': ['+91 9876543210', '+91 9876543211', '+91 9876543212', '+91 9876543213', '+91 9876543214'],
            'department': ['Computer Science', 'Electrical Engineering', 'Mechanical Engineering', 'Computer Science', 'Civil Engineering'],
            'semester': [6, 8, 7, 5, 8],
            'cgpa': [8.5, 9.2, 7.8, 8.9, 7.5],
            'backlogs': [0, 0, 2, 0, 1],
            'skills': ['Python, Java, SQL', 'C++, MATLAB, Python', 'AutoCAD, SolidWorks', 'Python, JavaScript, React', 'Structural Analysis, AutoCAD'],
            'placement_status': ['Placed', 'Placed', 'Not Placed', 'Intern', 'Not Placed'],
            'placement_company': ['Google', 'Microsoft', None, 'Amazon', None],
            'resume_link': ['resume1.pdf', 'resume2.pdf', 'resume3.pdf', 'resume4.pdf', 'resume5.pdf']
        }
        return pd.DataFrame(data)
    
    def display(self):
        """Display student information module"""
        st.header("👨‍🎓 Student Information Management")
        
        # Tabs for different functionalities
        tab1, tab2, tab3 = st.tabs(["📋 Student Database", "➕ Add New Student", "📊 Analytics"])
        
        with tab1:
            self.display_student_database()
        
        with tab2:
            self.add_new_student()
        
        with tab3:
            self.display_analytics()
    
    def display_student_database(self):
        """Display student database with filtering options"""
        st.subheader("Student Database")
        
        # Search and filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            search_name = st.text_input("Search by Name")
        with col2:
            filter_dept = st.selectbox("Filter by Department", 
                ["All"] + list(self.students_df['department'].unique()))
        with col3:
            filter_placement = st.selectbox("Filter by Placement Status", 
                ["All", "Placed", "Not Placed", "Intern"])
        
        # Apply filters
        filtered_df = self.students_df.copy()
        if search_name:
            filtered_df = filtered_df[filtered_df['name'].str.contains(search_name, case=False)]
        if filter_dept != "All":
            filtered_df = filtered_df[filtered_df['department'] == filter_dept]
        if filter_placement != "All":
            filtered_df = filtered_df[filtered_df['placement_status'] == filter_placement]
        
        # Display dataframe
        st.dataframe(filtered_df, use_container_width=True)
        
        # Student details view
        if not filtered_df.empty:
            selected_student = st.selectbox("Select Student for Details", 
                filtered_df['name'].tolist())
            
            if selected_student:
                student_data = filtered_df[filtered_df['name'] == selected_student].iloc[0]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Personal Information")
                    st.write(f"**Name:** {student_data['name']}")
                    st.write(f"**Student ID:** {student_data['student_id']}")
                    st.write(f"**Email:** {student_data['email']}")
                    st.write(f"**Phone:** {student_data['phone']}")
                
                with col2:
                    st.subheader("Academic Information")
                    st.write(f"**Department:** {student_data['department']}")
                    st.write(f"**Semester:** {student_data['semester']}")
                    st.write(f"**CGPA:** {student_data['cgpa']}")
                    st.write(f"**Backlogs:** {student_data['backlogs']}")
                
                st.subheader("Skills & Placement")
                st.write(f"**Skills:** {student_data['skills']}")
                st.write(f"**Placement Status:** {student_data['placement_status']}")
                if student_data['placement_company']:
                    st.write(f"**Company:** {student_data['placement_company']}")
    
    def add_new_student(self):
        """Form to add new student"""
        st.subheader("Add New Student")
        
        with st.form("add_student_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name*")
                email = st.text_input("Email*")
                phone = st.text_input("Phone")
                student_id = st.text_input("Student ID*")
            
            with col2:
                department = st.selectbox("Department", 
                    ["Computer Science", "Electrical Engineering", "Mechanical Engineering", 
                     "Civil Engineering", "Electronics Engineering", "Information Technology"])
                semester = st.number_input("Current Semester", 1, 10, 6)
                cgpa = st.number_input("CGPA", 0.0, 10.0, 8.0, 0.1)
                backlogs = st.number_input("Number of Backlogs", 0, 10, 0)
            
            skills = st.multiselect("Skills",
                ["Python", "Java", "C++", "JavaScript", "React", "Node.js", "SQL", 
                 "Machine Learning", "Data Analysis", "AWS", "Docker", "AutoCAD", 
                 "MATLAB", "Communication", "Leadership"],
                default=["Python", "SQL"])
            
            if st.form_submit_button("Add Student"):
                # Generate new student ID if not provided
                if not student_id:
                    student_id = f"S{len(self.students_df) + 1:03d}"
                
                # Add to dataframe (for demo purposes - in real app, save to database)
                new_student = pd.DataFrame({
                    'student_id': [student_id],
                    'name': [name],
                    'email': [email],
                    'phone': [phone],
                    'department': [department],
                    'semester': [semester],
                    'cgpa': [cgpa],
                    'backlogs': [backlogs],
                    'skills': [', '.join(skills)],
                    'placement_status': ['Not Placed'],
                    'placement_company': [None],
                    'resume_link': [None]
                })
                
                # Use pd.concat instead of append (append is deprecated)
                self.students_df = pd.concat([self.students_df, new_student], ignore_index=True)
                st.success(f"Student {name} added successfully!")
                st.rerun()
    
    def display_analytics(self):
        """Display student analytics"""
        st.subheader("Student Analytics")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Students", len(self.students_df))
        with col2:
            placed_count = len(self.students_df[self.students_df['placement_status'] == 'Placed'])
            st.metric("Placed Students", placed_count)
        with col3:
            avg_cgpa = self.students_df['cgpa'].mean()
            st.metric("Average CGPA", f"{avg_cgpa:.2f}")
        
        # Department-wise distribution
        st.subheader("Department Distribution")
        dept_counts = self.students_df['department'].value_counts()
        st.bar_chart(dept_counts)
        
        # Placement statistics - FIXED VERSION
        st.subheader("Placement Statistics")
        
        # Create a summary table
        placement_summary = pd.DataFrame({
            'Department': self.students_df['department'].unique()
        })
        
        # Calculate metrics for each department
        summary_data = []
        for dept in self.students_df['department'].unique():
            dept_students = self.students_df[self.students_df['department'] == dept]
            avg_cgpa = dept_students['cgpa'].mean()
            placed_count = len(dept_students[dept_students['placement_status'] == 'Placed'])
            total_count = len(dept_students)
            placement_rate = (placed_count / total_count * 100) if total_count > 0 else 0
            
            summary_data.append({
                'Department': dept,
                'Students': total_count,
                'Avg CGPA': f"{avg_cgpa:.2f}",
                'Placed': placed_count,
                'Placement Rate': f"{placement_rate:.1f}%"
            })
        
        # Display the summary table
        if summary_data:
            st.dataframe(pd.DataFrame(summary_data), use_container_width=True)
        else:
            st.info("No data available for placement statistics.")
        
        # CGPA distribution by department
        st.subheader("CGPA Distribution by Department")
        
        # Create a pivot table for visualization
        try:
            # For numeric columns only
            numeric_data = self.students_df[['department', 'cgpa']].copy()
            pivot_table = numeric_data.pivot_table(
                values='cgpa', 
                index='department', 
                aggfunc=['mean', 'count', 'min', 'max']
            )
            
            # Flatten column names
            pivot_table.columns = ['Avg CGPA', 'Count', 'Min CGPA', 'Max CGPA']
            pivot_table = pivot_table.reset_index()
            
            # Format numeric columns
            pivot_table['Avg CGPA'] = pivot_table['Avg CGPA'].round(2)
            
            st.dataframe(pivot_table, use_container_width=True)
            
            # Also show as a bar chart
            if not pivot_table.empty:
                chart_data = pivot_table[['department', 'Avg CGPA']].set_index('department')
                st.bar_chart(chart_data)
                
        except Exception as e:
            st.warning(f"Could not create detailed analysis: {str(e)}")
            # Fallback: simple department-CGPA table
            simple_table = self.students_df[['department', 'cgpa']].groupby('department').agg({
                'cgpa': ['mean', 'count']
            }).round(2)
            st.dataframe(simple_table, use_container_width=True)
