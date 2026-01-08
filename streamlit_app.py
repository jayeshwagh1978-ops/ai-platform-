# In streamlit_app.py, modify the imports section:
try:
    from database.db_manager import DatabaseManager
    db_manager = DatabaseManager()
    DB_AVAILABLE = True
except Exception as e:
    st.warning(f"Database module not available: {e}. Using fallback mode.")
    from database.fallback_db import FallbackDatabase
    db_manager = FallbackDatabase()
    DB_AVAILABLE = False
