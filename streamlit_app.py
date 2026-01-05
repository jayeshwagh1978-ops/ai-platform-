import streamlit as st
import pandas as pd

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

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/graduation-cap.png", width=100)
    st.title("Platform Navigation")
    
    # Demo mode info
    if st.session_state.demo_mode:
        st.success("🎮 Demo Mode Active")
    
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
    
    # Show workflow based on selected role
    if st.session_state.selected_role == "👨‍🎓 Student":
        st.session_state.workflow_manager.display_student_workflow()
    elif st.session_state.selected_role == "🏫 College Admin":
        st.session_state.workflow_manager.display_college_workflow()
    elif st.session_state.selected_role == "💼 Recruiter":
        st.session_state.workflow_manager.display_recruiter_workflow()
    else:
        st.session_state.workflow_manager.display_observer_dashboard()

# Main content
if st.session_state.selected_role == "👨‍🎓 Student":
    current_step = st.session_state.get('current_step_student', 1)
    st.session_state.student_flow.current_step = current_step
    st.session_state.student_flow.display()
    
elif st.session_state.selected_role == "🏫 College Admin":
    current_step = st.session_state.get('current_step_college', 1)
    st.session_state.college_flow.current_step = current_step
    st.session_state.college_flow.display()
    
elif st.session_state.selected_role == "💼 Recruiter":
    st.session_state.recruiter_flow.display()
    
else:
    st.session_state.workflow_manager.display_observer_view()

# Footer
st.divider()
st.markdown("""
<div style="text-align: center">
    <p>🎓 <b>AI Campus Placement Platform</b> | National Level Hackathon Project</p>
    <p>Built with ❤️ using Streamlit & Python</p>
</div>
""", unsafe_allow_html=True)
