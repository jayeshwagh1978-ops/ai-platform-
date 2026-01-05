import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import plotly.express as px
import plotly.graph_objects as go
import joblib
import os

class PlacementModule:
    def __init__(self):
        self.model = None
        self.load_model()
        
    def load_model(self):
        """Load or train placement prediction model"""
        model_path = "models/placement_model.pkl"
        try:
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
            else:
                self.train_model()
        except:
            self.train_model()
    
    def train_model(self):
        """Train placement prediction model"""
        # Sample training data
        np.random.seed(42)
        n_samples = 1000
        
        data = {
            'cgpa': np.random.uniform(6.0, 10.0, n_samples),
            'backlogs': np.random.randint(0, 5, n_samples),
            'internships': np.random.randint(0, 4, n_samples),
            'projects': np.random.randint(0, 10, n_samples),
            'aptitude_score': np.random.uniform(50, 100, n_samples),
            'coding_score': np.random.uniform(50, 100, n_samples),
            'communication_score': np.random.uniform(50, 100, n_samples),
            'extracurricular': np.random.randint(0, 10, n_samples)
        }
        
        # Placement probability calculation
        placement_prob = (
            data['cgpa'] * 0.3 +
            data['internships'] * 0.2 +
            data['projects'] * 0.15 +
            data['aptitude_score'] * 0.1 +
            data['coding_score'] * 0.1 +
            data['communication_score'] * 0.1 +
            data['extracurricular'] * 0.05 -
            data['backlogs'] * 0.1
        )
        
        # Normalize and create binary target
        placement_prob = (placement_prob - placement_prob.min()) / (placement_prob.max() - placement_prob.min())
        data['placed'] = (placement_prob > 0.5).astype(int)
        
        df = pd.DataFrame(data)
        
        # Train model
        X = df.drop('placed', axis=1)
        y = df['placed']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Create models directory if it doesn't exist
        os.makedirs("models", exist_ok=True)
        joblib.dump(self.model, "models/placement_model.pkl")
    
    def display(self):
        """Display placement module interface"""
        st.header("📊 Campus Placement Analytics & Prediction")
        
        tab1, tab2, tab3 = st.tabs(["🔮 Placement Predictor", "📈 Analytics Dashboard", "🏢 Company Portal"])
        
        with tab1:
            self.placement_predictor()
        with tab2:
            self.analytics_dashboard()
        with tab3:
            self.company_portal()
    
    def placement_predictor(self):
        """Interactive placement prediction tool"""
        st.subheader("Predict Placement Probability")
        
        col1, col2 = st.columns(2)
        
        with col1:
            cgpa = st.slider("CGPA", 6.0, 10.0, 8.5, 0.1)
            backlogs = st.number_input("Number of Backlogs", 0, 10, 0)
            internships = st.number_input("Internships Completed", 0, 10, 2)
            projects = st.number_input("Projects Completed", 0, 50, 5)
        
        with col2:
            aptitude_score = st.slider("Aptitude Test Score", 0, 100, 75)
            coding_score = st.slider("Coding Test Score", 0, 100, 70)
            communication_score = st.slider("Communication Score", 0, 100, 80)
            extracurricular = st.number_input("Extracurricular Activities", 0, 20, 5)
        
        if st.button("🔮 Predict Placement Chance"):
            # Prepare input for prediction
            input_data = pd.DataFrame([[
                cgpa, backlogs, internships, projects,
                aptitude_score, coding_score, communication_score, extracurricular
            ]], columns=[
                'cgpa', 'backlogs', 'internships', 'projects',
                'aptitude_score', 'coding_score', 'communication_score', 'extracurricular'
            ])
            
            # Get prediction
            try:
                prediction = self.model.predict_proba(input_data)[0][1]
            except:
                st.error("Model not loaded. Training model...")
                self.train_model()
                prediction = self.model.predict_proba(input_data)[0][1]
            
            # Display result
            st.subheader("Prediction Result")
            
            # Progress bar
            progress_color = "green" if prediction > 0.7 else "orange" if prediction > 0.4 else "red"
            st.progress(float(prediction))
            st.metric("Placement Probability", f"{prediction:.1%}")
            
            # Recommendations
            st.subheader("📋 Improvement Suggestions")
            
            if prediction < 0.4:
                st.error("""
                **High Risk Area - Immediate Action Required:**
                1. 📚 Improve CGPA above 8.0
                2. 💼 Complete at least 2 internships
                3. 🏆 Participate in coding competitions
                4. 🗣️ Join communication skills workshop
                """)
            elif prediction < 0.7:
                st.warning("""
                **Moderate Chance - Focus Areas:**
                1. 🔧 Complete 2-3 technical projects
                2. 📝 Practice aptitude tests regularly
                3. 🤝 Network with alumni in target companies
                4. 📊 Improve coding test scores above 80%
                """)
            else:
                st.success("""
                **Strong Candidate - Next Steps:**
                1. 🎯 Target top-tier companies
                2. 📄 Prepare company-specific resumes
                3. 💪 Practice advanced coding problems
                4. 🎤 Prepare for behavioral interviews
                """)
            
            # Feature importance
            st.subheader("📊 Key Factors in Prediction")
            if hasattr(self.model, 'feature_importances_'):
                importance = pd.DataFrame({
                    'Feature': self.model.feature_names_in_,
                    'Importance': self.model.feature_importances_
                }).sort_values('Importance', ascending=False)
                
                fig = px.bar(importance.head(5), x='Importance', y='Feature', 
                            orientation='h', title="Top 5 Placement Factors")
                st.plotly_chart(fig, use_container_width=True)
    
    def analytics_dashboard(self):
        """Display placement analytics dashboard"""
        st.subheader("Placement Analytics Dashboard")
        
        # Generate sample analytics data
        np.random.seed(42)
        n_companies = 20
        
        companies = ['Google', 'Microsoft', 'Amazon', 'Adobe', 'TCS', 'Infosys', 
                    'Wipro', 'Accenture', 'IBM', 'Intel', 'Nvidia', 'Oracle', 
                    'SAP', 'Cisco', 'Deloitte', 'PwC', 'EY', 'KPMG', 'Morgan Stanley', 'Goldman Sachs']
        
        analytics_data = pd.DataFrame({
            'Company': companies[:n_companies],
            'Placements': np.random.randint(5, 100, n_companies),
            'Avg_Package': np.random.uniform(5, 25, n_companies),
            'Selection_Rate': np.random.uniform(0.1, 0.5, n_companies),
            'Difficulty': np.random.choice(['Easy', 'Medium', 'Hard'], n_companies)
        })
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Companies", len(analytics_data))
        with col2:
            st.metric("Total Placements", analytics_data['Placements'].sum())
        with col3:
            st.metric("Average Package", f"₹{analytics_data['Avg_Package'].mean():.1f} LPA")
        with col4:
            st.metric("Average Selection Rate", f"{analytics_data['Selection_Rate'].mean()*100:.1f}%")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.bar(analytics_data.sort_values('Placements', ascending=False).head(10),
                         x='Company', y='Placements',
                         title="Top 10 Companies by Placements")
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.bar(analytics_data.sort_values('Avg_Package', ascending=False).head(10),
                         x='Company', y='Avg_Package',
                         title="Top 10 Companies by Package")
            st.plotly_chart(fig2, use_container_width=True)
        
        # Company difficulty analysis
        st.subheader("Company Difficulty Analysis")
        difficulty_counts = analytics_data['Difficulty'].value_counts()
        fig3 = px.pie(values=difficulty_counts.values, names=difficulty_counts.index,
                     title="Company Difficulty Distribution")
        st.plotly_chart(fig3, use_container_width=True)
    
    def company_portal(self):
        """Company registration and job posting portal"""
        st.subheader("Company Registration Portal")
        
        tab1, tab2 = st.tabs(["🏢 Register Company", "📢 Post Job Opening"])
        
        with tab1:
            self.company_registration()
        
        with tab2:
            self.job_posting()
    
    def company_registration(self):
        """Company registration form"""
        st.write("Register your company to participate in campus placements")
        
        with st.form("company_registration"):
            col1, col2 = st.columns(2)
            
            with col1:
                company_name = st.text_input("Company Name*")
                industry = st.selectbox("Industry*",
                    ["IT/Software", "Finance/Banking", "Consulting", "Manufacturing", 
                     "E-commerce", "Healthcare", "Education", "Automotive", "Other"])
                website = st.text_input("Website")
            
            with col2:
                contact_person = st.text_input("Contact Person*")
                email = st.text_input("Email*")
                phone = st.text_input("Phone*")
            
            company_description = st.text_area("Company Description")
            
            if st.form_submit_button("Register Company"):
                st.success(f"Company {company_name} registered successfully!")
                st.info("Our placement team will contact you shortly.")
    
    def job_posting(self):
        """Job posting form"""
        st.write("Post job openings for students")
        
        with st.form("job_posting"):
            job_title = st.text_input("Job Title*")
            
            col1, col2 = st.columns(2)
            with col1:
                job_type = st.selectbox("Job Type*",
                    ["Full-time", "Internship", "Contract", "Part-time"])
                location = st.text_input("Location*")
            
            with col2:
                salary = st.number_input("Salary (LPA)", 0.0, 50.0, 8.0, 0.5)
                vacancies = st.number_input("Number of Vacancies", 1, 100, 5)
            
            # Requirements
            st.subheader("Requirements")
            cgpa_min = st.number_input("Minimum CGPA", 0.0, 10.0, 7.0, 0.1)
            backlogs_allowed = st.number_input("Maximum Backlogs Allowed", 0, 10, 2)
            
            required_skills = st.multiselect("Required Skills",
                ["Python", "Java", "C++", "JavaScript", "React", "SQL", 
                 "Machine Learning", "Data Analysis", "AWS", "Communication"],
                default=["Python", "SQL"])
            
            job_description = st.text_area("Job Description*", height=150)
            
            if st.form_submit_button("Post Job Opening"):
                st.success(f"Job '{job_title}' posted successfully!")
