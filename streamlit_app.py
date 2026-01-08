import streamlit as st
import pandas as pd
import json

# Try to import database modules with fallbacks
try:
    from database.db_manager import DatabaseManager
    DB_AVAILABLE = True
except ImportError as e:
    DB_AVAILABLE = False
    st.warning(f"Database module not available: {e}")

from modules.workflow_manager import WorkflowManager
from modules.student_flow import StudentFlow
from modules.college_flow import CollegeFlow
from modules.recruiter_flow import RecruiterFlow

# Import new modules for enhanced features
try:
    from modules.video_interview_simulator import VideoInterviewSimulator
    VIDEO_INTERVIEW_AVAILABLE = True
except ImportError:
    VIDEO_INTERVIEW_AVAILABLE = False
    
try:
    from modules.ai_chatbot import AIChatbotAssistant
    CHATBOT_AVAILABLE = True
except ImportError:
    CHATBOT_AVAILABLE = False

try:
    from modules.blockchain_credentials import BlockchainManager
    BLOCKCHAIN_AVAILABLE = True
except ImportError:
    BLOCKCHAIN_AVAILABLE = False

try:
    from modules.nlp_job_parser import NLPJobParser
    NLP_PARSER_AVAILABLE = True
except ImportError:
    NLP_PARSER_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="AI Campus Placement Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'workflow_manager' not in st.session_state:
    st.session_state.workflow_manager = WorkflowManager()

if 'student_flow' not in st.session_state:
    st.session_state.student_flow = StudentFlow()

if 'college_flow' not in st.session_state:
    st.session_state.college_flow = CollegeFlow()

if 'recruiter_flow' not in st.session_state:
    st.session_state.recruiter_flow = RecruiterFlow()

if 'selected_role' not in st.session_state:
    st.session_state.selected_role = None

if 'demo_mode' not in st.session_state:
    st.session_state.demo_mode = True  # Default to demo mode

# Initialize new feature modules
if VIDEO_INTERVIEW_AVAILABLE and 'video_simulator' not in st.session_state:
    st.session_state.video_simulator = VideoInterviewSimulator()

if CHATBOT_AVAILABLE and 'chatbot' not in st.session_state:
    st.session_state.chatbot = AIChatbotAssistant()

if BLOCKCHAIN_AVAILABLE and 'blockchain_manager' not in st.session_state:
    st.session_state.blockchain_manager = BlockchainManager()

if NLP_PARSER_AVAILABLE and 'nlp_parser' not in st.session_state:
    st.session_state.nlp_parser = NLPJobParser()

# Initialize feature flags
if 'show_chatbot' not in st.session_state:
    st.session_state.show_chatbot = False

# Title and description
st.title("🎓 AI-Powered Campus Placement Management System")
st.markdown("""
### National Level Hackathon Project
**A Systematic End-to-End Placement Management Platform**
""")

# Show warning if database not available
if not DB_AVAILABLE:
    st.warning("""
    ⚠️ **Database module not available** - Running in demo mode.
    All data is stored in memory and will be lost when the app restarts.
    """)

# Floating AI Chatbot Assistant (Visible across all pages)
if CHATBOT_AVAILABLE and st.session_state.show_chatbot:
    st.session_state.chatbot.display_floating_chatbot()

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/graduation-cap.png", width=100)
    st.title("Platform Navigation")
    
    # Demo mode info
    if st.session_state.demo_mode:
        st.success("🎮 Demo Mode Active")
    
    # Chatbot toggle for all roles
    if CHATBOT_AVAILABLE:
        chatbot_enabled = st.checkbox("🤖 Enable AI Assistant", value=st.session_state.show_chatbot)
        if chatbot_enabled != st.session_state.show_chatbot:
            st.session_state.show_chatbot = chatbot_enabled
            st.rerun()
    
    st.subheader("Select Your Role")
    
    role = st.radio(
        "Choose your role:",
        ["👨‍🎓 Student", "🏫 College Admin", "💼 Recruiter", "👀 Observer"],
        key="role_selection",
        label_visibility="collapsed"
    )
    
    # Store selected role
    if role != st.session_state.get('selected_role'):
        st.session_state.selected_role = role
        st.rerun()
    
    st.divider()
    
    # Show workflow based on selected role with enhanced features
    if st.session_state.selected_role == "👨‍🎓 Student":
        st.session_state.workflow_manager.display_student_workflow()
        
        # Enhanced student features menu
        with st.expander("🎯 Advanced Features", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                if VIDEO_INTERVIEW_AVAILABLE:
                    if st.button("🎬 Video Interview Practice", use_container_width=True):
                        st.session_state.show_video_interview = True
                if st.button("📊 Predictive Analysis", use_container_width=True):
                    st.session_state.show_predictive_analysis = True
            with col2:
                if BLOCKCHAIN_AVAILABLE:
                    if st.button("🔗 Blockchain Credentials", use_container_width=True):
                        st.session_state.show_blockchain_credentials = True
                if st.button("📈 Skill Gap Analysis", use_container_width=True):
                    st.session_state.show_skill_gap_analysis = True
                    
    elif st.session_state.selected_role == "🏫 College Admin":
        st.session_state.workflow_manager.display_college_workflow()
        
        # Enhanced college features menu
        with st.expander("🏛️ College Analytics", expanded=False):
            if st.button("📊 NEP 2020 Compliance Dashboard"):
                st.session_state.show_nep_compliance = True
            if st.button("🎯 Placement Forecasting"):
                st.session_state.show_placement_forecast = True
            if st.button("📚 Curriculum Mapping"):
                st.session_state.show_curriculum_mapping = True
            if st.button("🌱 Sustainability Metrics"):
                st.session_state.show_sustainability_metrics = True
            if BLOCKCHAIN_AVAILABLE:
                if st.button("👨‍🏫 Faculty Credentials"):
                    st.session_state.show_faculty_credentials = True
                    
    elif st.session_state.selected_role == "💼 Recruiter":
        st.session_state.workflow_manager.display_recruiter_workflow()
        
        # Enhanced recruiter features menu
        with st.expander("💼 Hiring Tools", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                if NLP_PARSER_AVAILABLE:
                    if st.button("📝 NLP Job Parser", use_container_width=True):
                        st.session_state.show_nlp_parser = True
                if st.button("🗺️ Talent Heatmap", use_container_width=True):
                    st.session_state.show_talent_heatmap = True
                if st.button("📊 Hiring Analytics", use_container_width=True):
                    st.session_state.show_hiring_analytics = True
            with col2:
                if st.button("🏆 National Leaderboard", use_container_width=True):
                    st.session_state.show_leaderboard = True
                if st.button("🔄 Internship Pipeline", use_container_width=True):
                    st.session_state.show_internship_pipeline = True
                if st.button("🔔 Notifications", use_container_width=True):
                    st.session_state.show_notifications = True
                    
    else:
        st.session_state.workflow_manager.display_observer_dashboard()

# Main content
if st.session_state.selected_role == "👨‍🎓 Student":
    current_step = st.session_state.get('current_step_student', 1)
    st.session_state.student_flow.current_step = current_step
    
    # Display enhanced student features if activated
    if VIDEO_INTERVIEW_AVAILABLE and st.session_state.get('show_video_interview', False):
        st.header("🎬 Video Interview Simulator")
        st.session_state.video_simulator.display()
        if st.button("← Back to Student Portal"):
            st.session_state.show_video_interview = False
            st.rerun()
    
    elif st.session_state.get('show_predictive_analysis', False):
        st.header("📊 Predictive Analysis Dashboard")
        _display_predictive_analysis()
        if st.button("← Back to Student Portal"):
            st.session_state.show_predictive_analysis = False
            st.rerun()
    
    elif BLOCKCHAIN_AVAILABLE and st.session_state.get('show_blockchain_credentials', False):
        st.header("🔗 Blockchain Credentials")
        st.session_state.blockchain_manager.display_student_credentials()
        if st.button("← Back to Student Portal"):
            st.session_state.show_blockchain_credentials = False
            st.rerun()
    
    elif st.session_state.get('show_skill_gap_analysis', False):
        st.header("📈 Skill Gap Analysis")
        _display_skill_gap_analysis()
        if st.button("← Back to Student Portal"):
            st.session_state.show_skill_gap_analysis = False
            st.rerun()
    
    else:
        # Display regular student flow
        st.session_state.student_flow.display()
        
elif st.session_state.selected_role == "🏫 College Admin":
    current_step = st.session_state.get('current_step_college', 1)
    st.session_state.college_flow.current_step = current_step
    
    # Display enhanced college features if activated
    if st.session_state.get('show_nep_compliance', False):
        st.header("📊 NEP 2020 Compliance Dashboard")
        _display_nep_compliance()
        if st.button("← Back to College Portal"):
            st.session_state.show_nep_compliance = False
            st.rerun()
    
    elif st.session_state.get('show_placement_forecast', False):
        st.header("🎯 XGBoost Placement Forecasting")
        _display_placement_forecast()
        if st.button("← Back to College Portal"):
            st.session_state.show_placement_forecast = False
            st.rerun()
    
    elif st.session_state.get('show_curriculum_mapping', False):
        st.header("📚 Curriculum Mapping & Alignment")
        _display_curriculum_mapping()
        if st.button("← Back to College Portal"):
            st.session_state.show_curriculum_mapping = False
            st.rerun()
    
    elif st.session_state.get('show_sustainability_metrics', False):
        st.header("🌱 Sustainability Metrics")
        _display_sustainability_metrics()
        if st.button("← Back to College Portal"):
            st.session_state.show_sustainability_metrics = False
            st.rerun()
    
    elif BLOCKCHAIN_AVAILABLE and st.session_state.get('show_faculty_credentials', False):
        st.header("👨‍🏫 Blockchain Faculty Credentials")
        st.session_state.blockchain_manager.display_faculty_credentials()
        if st.button("← Back to College Portal"):
            st.session_state.show_faculty_credentials = False
            st.rerun()
    
    else:
        # Display regular college flow
        st.session_state.college_flow.display()
        
elif st.session_state.selected_role == "💼 Recruiter":
    # Display enhanced recruiter features if activated
    if NLP_PARSER_AVAILABLE and st.session_state.get('show_nlp_parser', False):
        st.header("📝 NLP Job Description Parser")
        st.session_state.nlp_parser.display()
        if st.button("← Back to Recruiter Portal"):
            st.session_state.show_nlp_parser = False
            st.rerun()
    
    elif st.session_state.get('show_talent_heatmap', False):
        st.header("🗺️ Campus Talent Heatmap")
        _display_talent_heatmap()
        if st.button("← Back to Recruiter Portal"):
            st.session_state.show_talent_heatmap = False
            st.rerun()
    
    elif st.session_state.get('show_hiring_analytics', False):
        st.header("📊 Hiring Analytics Dashboard")
        _display_hiring_analytics()
        if st.button("← Back to Recruiter Portal"):
            st.session_state.show_hiring_analytics = False
            st.rerun()
    
    elif st.session_state.get('show_leaderboard', False):
        st.header("🏆 National Leaderboard")
        _display_national_leaderboard()
        if st.button("← Back to Recruiter Portal"):
            st.session_state.show_leaderboard = False
            st.rerun()
    
    elif st.session_state.get('show_internship_pipeline', False):
        st.header("🔄 Internship Pipeline Management")
        _display_internship_pipeline()
        if st.button("← Back to Recruiter Portal"):
            st.session_state.show_internship_pipeline = False
            st.rerun()
    
    elif st.session_state.get('show_notifications', False):
        st.header("🔔 Notifications & Alerts")
        _display_notifications()
        if st.button("← Back to Recruiter Portal"):
            st.session_state.show_notifications = False
            st.rerun()
    
    elif st.session_state.get('show_interview_vault', False):
        st.header("🗄️ Interview Feedback Vault")
        _display_interview_feedback_vault()
        if st.button("← Back to Recruiter Portal"):
            st.session_state.show_interview_vault = False
            st.rerun()
    
    else:
        # Display regular recruiter flow
        st.session_state.recruiter_flow.display()
        
else:
    st.session_state.workflow_manager.display_observer_view()

# Footer
st.divider()
st.markdown("""
<div style="text-align: center">
    <p>🎓 <b>AI Campus Placement Platform</b> | National Level Hackathon Project</p>
    <p>Enhanced Features: Video Interview Simulator • AI Chatbot • Blockchain Credentials • NLP Job Parser • Predictive Analytics</p>
    <p>Built with ❤️ using Streamlit & Python</p>
</div>
""", unsafe_allow_html=True)

# Helper functions for enhanced features (to be implemented in respective modules)
def _display_predictive_analysis():
    """Display predictive analysis visualization"""
    st.subheader("Career Path Prediction")
    
    # Mock data - in real implementation, this would come from ML model
    predictions = {
        "Software Engineer": 85,
        "Data Analyst": 75,
        "Product Manager": 60,
        "UX Designer": 45,
        "DevOps Engineer": 70
    }
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Visualization
        st.bar_chart(predictions)
        
    with col2:
        st.metric("Overall Placement Probability", "78%", "5%")
        st.metric("Recommended Skills to Learn", "Python, SQL, AWS")
        
    st.info("💡 Based on your profile, skills, and market trends")

def _display_skill_gap_analysis():
    """Display skill gap analysis"""
    st.subheader("Skill Gap Analysis")
    
    skills_data = {
        "Technical Skills": {"Current": 65, "Required": 85},
        "Communication": {"Current": 75, "Required": 80},
        "Problem Solving": {"Current": 70, "Required": 85},
        "Teamwork": {"Current": 85, "Required": 80}
    }
    
    for skill, levels in skills_data.items():
        gap = levels["Required"] - levels["Current"]
        st.progress(levels["Current"]/100, text=f"{skill}: {levels['Current']}% (Gap: {gap}%)")
        
    st.subheader("Recommended Learning Path")
    st.write("1. Complete Python Advanced Course")
    st.write("2. Practice Data Structures & Algorithms")
    st.write("3. Join Mock Interview Sessions")
    st.write("4. Attend Soft Skills Workshop")

def _display_nep_compliance():
    """Display NEP 2020 compliance dashboard"""
    st.subheader("NEP 2020 Compliance Scorecard")
    
    compliance_metrics = {
        "Multidisciplinary Education": 85,
        "Flexible Curriculum": 90,
        "Skill Integration": 75,
        "Digital Literacy": 95,
        "Research Culture": 70,
        "Industry Connect": 80
    }
    
    overall_score = sum(compliance_metrics.values()) / len(compliance_metrics)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Overall Compliance Score", f"{overall_score:.1f}%")
        st.dataframe(pd.DataFrame.from_dict(compliance_metrics, orient='index', columns=['Score']))
        
    with col2:
        st.subheader("Major-Minor Alignment")
        st.write("**Aligned Majors:** Computer Science, Data Science")
        st.write("**Available Minors:** AI/ML, Cybersecurity, Business Analytics")
        st.write("**Interdisciplinary:** Digital Humanities, Computational Biology")

def _display_placement_forecast():
    """Display XGBoost placement forecasts"""
    st.subheader("Placement Forecast Dashboard")
    
    # Mock forecast data
    forecast_data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Predicted Placements': [45, 52, 60, 65, 70, 75],
        'Confidence Interval': [5, 4, 3, 3, 2, 2]
    })
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Expected Placements", "367", "12%")
    with col2:
        st.metric("Top Recruiting Sector", "IT/Tech", "15 companies")
    with col3:
        st.metric("Average Package", "₹8.5 LPA", "₹0.5 LPA")
    
    st.line_chart(forecast_data.set_index('Month')['Predicted Placements'])
    
    st.subheader("Key Influencing Factors")
    factors = {
        "Student Skills": "High Impact",
        "Industry Trends": "Medium Impact",
        "Economic Conditions": "High Impact",
        "College Reputation": "Medium Impact"
    }
    
    for factor, impact in factors.items():
        st.write(f"✅ **{factor}**: {impact}")

def _display_curriculum_mapping():
    """Display curriculum mapping"""
    st.subheader("Curriculum-Industry Alignment")
    
    subjects = {
        "Data Structures": ["Google", "Amazon", "Microsoft"],
        "Machine Learning": ["Tesla", "NVIDIA", "OpenAI"],
        "Cloud Computing": ["AWS", "Azure", "Google Cloud"],
        "Cybersecurity": ["CrowdStrike", "Palo Alto", "IBM"]
    }
    
    for subject, companies in subjects.items():
        with st.expander(f"📘 {subject}"):
            st.write(f"**Industry Alignment:** {len(companies)*20}%")
            st.write(f"**Top Recruiters:** {', '.join(companies)}")
            st.write(f"**Learning Techniques:** Project-based, Peer Learning, Case Studies")

def _display_sustainability_metrics():
    """Display sustainability metrics"""
    st.subheader("Sustainability Dashboard")
    
    metrics = {
        "Carbon Footprint": "15% reduction",
        "Digital Adoption": "90% paperless",
        "Energy Efficiency": "Solar powered 40%",
        "Green Campus": "ISO 14001 Certified"
    }
    
    for metric, value in metrics.items():
        st.info(f"🌿 **{metric}:** {value}")
        
    st.subheader("AR/VR Campus Tour")
    st.write("Experience our virtual campus tour:")
    st.video("https://www.youtube.com/watch?v=example")  # Replace with actual tour

def _display_talent_heatmap():
    """Display campus talent heatmap"""
    st.subheader("Campus Talent Distribution")
    
    # Mock heatmap data
    import numpy as np
    heatmap_data = np.random.rand(10, 10)
    
    st.write("**Skill Density Across Campuses**")
    st.image("https://via.placeholder.com/800x400?text=Talent+Heatmap+Visualization", 
             caption="Interactive Talent Heatmap")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Top Skills by Region:**")
        st.write("1. Python Programming")
        st.write("2. Data Analysis")
        st.write("3. Cloud Computing")
    with col2:
        st.write("**Highest Density Campuses:**")
        st.write("1. IIT Delhi")
        st.write("2. BITS Pilani")
        st.write("3. NIT Trichy")

def _display_hiring_analytics():
    """Display hiring analytics"""
    st.subheader("Hiring Analytics Dashboard")
    
    analytics = {
        "Time-to-Hire": "24 days",
        "Cost-per-Hire": "₹45,000",
        "Offer Acceptance Rate": "78%",
        "Candidate Satisfaction": "4.2/5"
    }
    
    for metric, value in analytics.items():
        st.metric(metric, value)
        
    st.subheader("Interview Feedback Analytics")
    feedback_data = pd.DataFrame({
        'Category': ['Technical', 'Communication', 'Problem Solving', 'Cultural Fit'],
        'Average Score': [4.1, 3.8, 4.3, 3.9],
        'Improvement': ['+0.2', '+0.1', '+0.3', '+0.1']
    })
    
    st.bar_chart(feedback_data.set_index('Category')['Average Score'])

def _display_national_leaderboard():
    """Display national leaderboard"""
    st.subheader("🏆 National Placement Leaderboard")
    
    leaderboard = pd.DataFrame({
        'Rank': [1, 2, 3, 4, 5],
        'College': ['IIT Bombay', 'IIT Delhi', 'BITS Pilani', 'NIT Trichy', 'IIIT Hyderabad'],
        'Placements': [95, 92, 90, 88, 85],
        'Avg Package (LPA)': [21.5, 20.8, 18.2, 16.5, 17.8]
    })
    
    st.dataframe(leaderboard, use_container_width=True)
    
    st.subheader("Top Performing Companies")
    companies = ["Microsoft", "Google", "Amazon", "Adobe", "Goldman Sachs"]
    st.write(", ".join(companies))

def _display_internship_pipeline():
    """Display internship pipeline"""
    st.subheader("Internship Pipeline Management")
    
    pipeline_stages = {
        "Applied": 150,
        "Screening": 75,
        "Interview": 40,
        "Offered": 25,
        "Hired": 15
    }
    
    col1, col2 = st.columns(2)
    with col1:
        for stage, count in pipeline_stages.items():
            st.write(f"**{stage}:** {count} students")
    with col2:
        conversion_rate = (pipeline_stages["Hired"] / pipeline_stages["Applied"]) * 100
        st.metric("Conversion Rate", f"{conversion_rate:.1f}%")
        
    st.subheader("Fast-Track Opportunities")
    st.write("🚀 **Accelerated Placement Program**")
    st.write("Top 10% of interns get pre-placement offers")
    st.write("⏱️ **Reduced Hiring Timeline:** 2 weeks vs 6 weeks")

def _display_notifications():
    """Display notifications"""
    st.subheader("🔔 Notifications Center")
    
    notifications = [
        {"type": "📧", "message": "New job posting from Google", "time": "2 hours ago"},
        {"type": "👥", "message": "5 new candidates matched your criteria", "time": "1 day ago"},
        {"type": "📊", "message": "Monthly hiring report ready", "time": "2 days ago"},
        {"type": "🎓", "message": "Campus drive scheduled for IIT Delhi", "time": "3 days ago"}
    ]
    
    for notif in notifications:
        st.write(f"{notif['type']} **{notif['message']}**")
        st.caption(notif['time'])
        st.divider()

def _display_interview_feedback_vault():
    """Display interview feedback vault"""
    st.subheader("Interview Feedback Vault")
    
    feedback_categories = ["Technical Skills", "Communication", "Problem Solving", 
                          "Cultural Fit", "Leadership Potential"]
    
    selected_category = st.selectbox("Filter by Category", feedback_categories)
    
    # Mock feedback data
    feedback_data = pd.DataFrame({
        'Candidate': ['Alice Johnson', 'Bob Smith', 'Charlie Brown'],
        'Technical': [4.5, 3.8, 4.2],
        'Communication': [4.0, 3.5, 4.5],
        'Overall': [4.3, 3.7, 4.4],
        'Recommendation': ['Strong Hire', 'Consider', 'Hire']
    })
    
    st.dataframe(feedback_data, use_container_width=True)
    
    st.subheader("Feedback Analytics")
    st.write("**Most Common Areas for Improvement:**")
    st.write("1. Communication clarity")
    st.write("2. Real-world project experience")
    st.write("3. Technical depth in specialized areas")
