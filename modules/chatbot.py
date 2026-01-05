import streamlit as st
import pandas as pd
import random
from datetime import datetime

class IntegratedChatbot:
    def __init__(self):
        self.knowledge_base = self.load_knowledge_base()
        self.conversation_history = []
    
    def load_knowledge_base(self):
        """Load chatbot knowledge base"""
        return {
            "placement": {
                "questions": [
                    "how to prepare for placements",
                    "placement process",
                    "campus recruitment",
                    "placement tips"
                ],
                "answers": [
                    "Start preparing at least 6 months before placements. Focus on DSA, projects, and communication skills.",
                    "Campus placement process typically includes: Aptitude test → Technical test → Group Discussion → Technical Interview → HR Interview.",
                    "Top companies visit campus for recruitment between July-December. Maintain CGPA above 7.5 for most companies.",
                    "Key placement tips: 1. Build strong projects 2. Practice coding daily 3. Improve communication 4. Network with alumni"
                ]
            },
            "resume": {
                "questions": [
                    "resume building",
                    "ats friendly resume",
                    "resume tips",
                    "resume format"
                ],
                "answers": [
                    "Use clean format, include projects with impact metrics, tailor for each role, keep 1-2 pages maximum.",
                    "ATS-friendly resumes: Use standard fonts, include keywords from job description, avoid tables and graphics.",
                    "Resume tips: Quantify achievements, use action verbs, include relevant skills, proofread multiple times.",
                    "Recommended formats: Chronological for experienced, Functional for career changers, Combination for most students."
                ]
            },
            "internship": {
                "questions": [
                    "how to get internship",
                    "internship search",
                    "pm internship",
                    "internship tips"
                ],
                "answers": [
                    "Apply 3-4 months before start date. Use LinkedIn, company portals, and college TPO. Have 2-3 good projects.",
                    "Search on: LinkedIn, Internshala, AngelList, company career pages, and through college TPO.",
                    "PM internships: Need strong analytical skills, product thinking, and communication. Build case study portfolio.",
                    "Internship tips: Customize applications, follow up professionally, prepare for interviews, have learning goals."
                ]
            }
        }
    
    def display(self):
        """Display chatbot interface"""
        st.header("🤖 AI Campus Placement Assistant")
        
        st.info("""
        I'm your AI assistant for everything related to campus placements, 
        careers, and education. Ask me anything!
        
        **Try asking about:**
        - Placement preparation tips
        - Resume building advice
        - Internship opportunities
        - Career guidance
        - Interview preparation
        """)
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Hello! I'm your Campus Placement Assistant. How can I help you today?"}
            ]
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask me anything about placements, careers, or education..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get and display AI response
            with st.chat_message("assistant"):
                response = self.get_response(prompt)
                st.markdown(response)
            
            # Add AI response to history
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Quick action buttons
        st.divider()
        st.subheader("Quick Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📝 Resume Review", use_container_width=True):
                self.suggest_resume_tips()
        
        with col2:
            if st.button("💼 Placement Tips", use_container_width=True):
                self.suggest_placement_tips()
        
        with col3:
            if st.button("🎯 Career Advice", use_container_width=True):
                self.suggest_career_advice()
        
        # Common questions
        st.divider()
        st.subheader("Frequently Asked Questions")
        
        faqs = [
            "How to prepare for campus placements?",
            "What is a good resume format?",
            "How to find internship opportunities?",
            "What skills are in demand?",
            "How to prepare for technical interviews?"
        ]
        
        for faq in faqs:
            if st.button(faq, use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": faq})
                response = self.get_response(faq)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
    
    def get_response(self, user_input):
        """Get response for user input"""
        user_input_lower = user_input.lower()
        
        # Check knowledge base
        for category, data in self.knowledge_base.items():
            for question in data["questions"]:
                if question in user_input_lower:
                    return random.choice(data["answers"])
        
        # Default responses based on keywords
        if any(word in user_input_lower for word in ["interview", "technical interview"]):
            return """**Technical Interview Preparation:**
1. **DSA Practice:** LeetCode, GeeksforGeeks (150+ problems)
2. **Projects:** Be ready to explain 2-3 projects in detail
3. **System Design:** For senior roles, practice design problems
4. **Mock Interviews:** Practice with peers or platforms like Pramp
5. **Company-specific:** Research recent interview experiences on Glassdoor"""
        
        elif any(word in user_input_lower for word in ["salary", "package", "lpa"]):
            return """**Salary Information (2024 trends):**
- **Software Developer:** 8-15 LPA (Entry), 15-30 LPA (Mid), 30-50+ LPA (Senior)
- **Data Scientist:** 10-18 LPA (Entry), 18-35 LPA (Mid), 35-60+ LPA (Senior)
- **Product Manager:** 12-20 LPA (Entry), 20-40 LPA (Mid), 40-70+ LPA (Senior)

*Note: Packages vary by company, location, and skills.*"""
        
        elif any(word in user_input_lower for word in ["cgpa", "grades", "marks"]):
            return """**CGPA and Placements:**
- **Top Companies (FAANG):** Usually require 8.0+ CGPA
- **Good Product Companies:** 7.5+ CGPA
- **Service Companies:** 7.0+ CGPA
- **Startups:** Focus more on skills and projects

**If CGPA is low (<7.0):**
1. Build exceptional projects
2. Contribute to open source
3. Get certified in relevant skills
4. Network and get referrals"""
        
        elif any(word in user_input_lower for word in ["skill", "learn", "course"]):
            return """**Top Skills to Learn (2024):**
**High Demand:**
1. **AI/ML:** TensorFlow, PyTorch, LLMs
2. **Cloud:** AWS, Azure, GCP certifications
3. **DevOps:** Docker, Kubernetes, CI/CD
4. **Data Science:** Python, SQL, Analytics

**Good to have:**
1. **Full Stack:** React, Node.js, databases
2. **Mobile:** Flutter, React Native
3. **Cybersecurity:** Basic security concepts
4. **Soft Skills:** Communication, leadership"""
        
        # Default response
        default_responses = [
            "I understand you're asking about campus placements. Could you be more specific about what you need help with?",
            "That's a great question about career preparation. Could you provide more details so I can give you the best advice?",
            "I'd be happy to help with that! To give you the most accurate information, could you tell me more about your specific situation?",
            "For detailed guidance on this topic, I recommend checking our specialized modules for Resume Building, Career Advisor, or Placement Predictor."
        ]
        
        return random.choice(default_responses)
    
    def suggest_resume_tips(self):
        """Suggest resume tips"""
        tips = """**🤖 AI Resume Tips:**
1. **Format:** Clean, professional, 1-2 pages maximum
2. **Keywords:** Include keywords from job description
3. **Quantify:** Use numbers to show impact (e.g., "Improved performance by 30%")
4. **Projects:** Include 2-3 good projects with GitHub links
5. **Skills:** List relevant technical skills prominently
6. **Tailor:** Customize for each application
7. **Proofread:** No spelling or grammar errors

**Use our AI Resume Builder module for personalized optimization!**"""
        
        st.session_state.messages.append({"role": "assistant", "content": tips})
        st.rerun()
    
    def suggest_placement_tips(self):
        """Suggest placement tips"""
        tips = """**🎯 Placement Preparation Timeline:**
**6 Months Before:**
- Build strong coding foundation (DSA)
- Start 2-3 good projects
- Improve communication skills

**3 Months Before:**
- Practice mock interviews
- Update resume
- Research companies

**1 Month Before:**
- Intensive coding practice
- Company-specific preparation
- GD/PI practice

**Current Week:**
- Revise core concepts
- Practice previous papers
- Stay confident and calm

**Use our Placement Predictor module to assess your chances!**"""
        
        st.session_state.messages.append({"role": "assistant", "content": tips})
        st.rerun()
    
    def suggest_career_advice(self):
        """Suggest career advice"""
        advice = """**🧭 Career Path Guidance:**
**Based on current trends (2024):**

**🔥 High Growth Fields:**
1. **AI/ML Engineering:** 30%+ annual growth
2. **Cloud Computing:** 25%+ annual growth  
3. **Cybersecurity:** 28%+ annual growth
4. **Data Science:** 22%+ annual growth

**💡 Career Advice:**
1. **Specialize but stay flexible:** Have a core specialty but learn adjacent skills
2. **Build portfolio:** GitHub, blog, contributions
3. **Network:** Connect with professionals in target roles
4. **Continuous learning:** Take 1-2 courses per year
5. **Soft skills:** Communication is as important as technical skills

**Use our Career Advisor module for personalized guidance!**"""
        
        st.session_state.messages.append({"role": "assistant", "content": advice})
        st.rerun()
