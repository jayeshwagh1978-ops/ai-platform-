import streamlit as st
import pandas as pd
import plotly.express as px

class CollegeInfoModule:
    def __init__(self):
        self.college_data = self.load_college_data()
    
    def load_college_data(self):
        """Load sample college data"""
        data = {
            'college_id': ['C001', 'C002', 'C003', 'C004'],
            'name': ['ABC Engineering College', 'XYZ Institute of Technology', 
                    'PQR University', 'LMN College of Engineering'],
            'location': ['Mumbai', 'Bangalore', 'Delhi', 'Chennai'],
            'established': [1990, 2000, 1985, 1995],
            'accreditation': ['A+', 'A', 'A++', 'A'],
            'total_students': [5000, 3000, 8000, 4000],
            'faculty_count': [300, 200, 500, 250],
            'departments': ['CSE, ECE, ME, CE', 'CSE, IT, EEE', 'CSE, ME, CE, ECE', 'CSE, ECE'],
            'placement_rate': [85, 78, 92, 81],
            'avg_package': [8.5, 7.2, 12.5, 6.8],
            'top_recruiters': ['Google, Microsoft, Amazon', 'Infosys, TCS, Wipro', 
                             'Google, Amazon, Microsoft, Adobe', 'TCS, Infosys, Cognizant']
        }
        return pd.DataFrame(data)
    
    def display(self):
        """Display college information module"""
        st.header("🏫 College Information System")
        
        tab1, tab2, tab3 = st.tabs(["🏛️ College Database", "📊 Placement Statistics", "🎓 Department Info"])
        
        with tab1:
            self.display_college_database()
        
        with tab2:
            self.display_placement_stats()
        
        with tab3:
            self.display_department_info()
    
    def display_college_database(self):
        """Display college database"""
        st.subheader("College Database")
        
        # Search functionality
        search_term = st.text_input("Search College by Name or Location")
        
        # Filter data
        display_data = self.college_data.copy()
        if search_term:
            display_data = display_data[
                display_data['name'].str.contains(search_term, case=False) |
                display_data['location'].str.contains(search_term, case=False)
            ]
        
        # Display as dataframe
        st.dataframe(display_data, use_container_width=True)
        
        # Detailed view
        if not display_data.empty:
            selected_college = st.selectbox("Select College for Details", 
                display_data['name'].tolist())
            
            if selected_college:
                college = display_data[display_data['name'] == selected_college].iloc[0]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Basic Information")
                    st.write(f"**Name:** {college['name']}")
                    st.write(f"**Location:** {college['location']}")
                    st.write(f"**Established:** {college['established']}")
                    st.write(f"**Accreditation:** {college['accreditation']}")
                
                with col2:
                    st.subheader("Student & Faculty")
                    st.write(f"**Total Students:** {college['total_students']:,}")
                    st.write(f"**Faculty Count:** {college['faculty_count']}")
                    st.write(f"**Departments:** {college['departments']}")
                
                st.subheader("Placement Information")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Placement Rate", f"{college['placement_rate']}%")
                with col2:
                    st.metric("Average Package", f"₹{college['avg_package']} LPA")
                with col3:
                    st.metric("Top Recruiters", 
                            len(college['top_recruiters'].split(',')))
    
    def display_placement_stats(self):
        """Display placement statistics"""
        st.subheader("Placement Statistics")
        
        # Create charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Placement rate bar chart
            fig1 = px.bar(self.college_data, x='name', y='placement_rate',
                         title="Placement Rate by College",
                         labels={'name': 'College', 'placement_rate': 'Placement Rate (%)'})
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Average package bar chart
            fig2 = px.bar(self.college_data, x='name', y='avg_package',
                         title="Average Package by College",
                         labels={'name': 'College', 'avg_package': 'Average Package (LPA)'})
            st.plotly_chart(fig2, use_container_width=True)
        
        # Top recruiters word cloud simulation
        st.subheader("Top Recruiters Across Colleges")
        all_recruiters = []
        for recruiters in self.college_data['top_recruiters']:
            all_recruiters.extend([r.strip() for r in recruiters.split(',')])
        
        from collections import Counter
        recruiter_counts = Counter(all_recruiters)
        
        # Display as table
        st.dataframe(pd.DataFrame.from_dict(recruiter_counts, orient='index', 
                                           columns=['Count']).sort_values('Count', ascending=False))
    
    def display_department_info(self):
        """Display department-wise information"""
        st.subheader("Department Information")
        
        # Extract all departments
        all_depts = []
        for depts in self.college_data['departments']:
            all_depts.extend([d.strip() for d in depts.split(',')])
        
        dept_counts = pd.Series(all_depts).value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Department Popularity**")
            st.dataframe(dept_counts)
        
        with col2:
            # Department availability by college
            dept_matrix = []
            for _, row in self.college_data.iterrows():
                college_depts = [d.strip() for d in row['departments'].split(',')]
                dept_matrix.append({
                    'College': row['name'],
                    'CSE': '✅' if 'CSE' in college_depts else '❌',
                    'ECE': '✅' if 'ECE' in college_depts else '❌',
                    'ME': '✅' if 'ME' in college_depts else '❌',
                    'CE': '✅' if 'CE' in college_depts else '❌',
                    'IT': '✅' if 'IT' in college_depts else '❌',
                    'EEE': '✅' if 'EEE' in college_depts else '❌'
                })
            
            st.write("**Department Availability**")
            st.dataframe(pd.DataFrame(dept_matrix))
