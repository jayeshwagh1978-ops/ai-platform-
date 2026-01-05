"""
AI helper functions for the campus placement platform
"""

def analyze_resume_text(resume_text):
    """
    Analyze resume text for improvements
    """
    # This is a placeholder function
    # In production, integrate with OpenAI API or other AI services
    
    analysis = {
        "ats_score": 75,
        "keyword_match": 65,
        "readability": "Good",
        "action_verbs": 12,
        "quantifiable_results": 3,
        "suggestions": [
            "Add more quantifiable results",
            "Include more industry-specific keywords",
            "Start bullet points with action verbs"
        ]
    }
    
    return analysis

def predict_placement_probability(student_data):
    """
    Predict placement probability based on student data
    """
    # Simple prediction logic (replace with ML model in production)
    score = 0
    
    # CGPA contribution
    cgpa = student_data.get('cgpa', 7.0)
    score += min(cgpa * 7.5, 30)  # Max 30 points for CGPA
    
    # Internships contribution
    internships = student_data.get('internships', 0)
    score += internships * 10  # 10 points per internship
    
    # Projects contribution
    projects = student_data.get('projects', 0)
    score += min(projects * 5, 20)  # Max 20 points for projects
    
    # Skills contribution
    skills = student_data.get('skills', [])
    score += min(len(skills) * 3, 15)  # Max 15 points for skills
    
    # Backlogs penalty
    backlogs = student_data.get('backlogs', 0)
    score -= backlogs * 5
    
    # Normalize to percentage
    probability = max(0, min(100, score)) / 100
    
    return probability

def get_career_recommendations(student_profile):
    """
    Get career recommendations based on student profile
    """
    # Simple recommendation logic
    recommendations = []
    
    if student_profile.get('technical_skills'):
        if 'python' in student_profile.get('technical_skills', []).lower():
            recommendations.append({
                "career": "Data Science",
                "match": 85,
                "reason": "Python skills are essential for Data Science roles"
            })
            recommendations.append({
                "career": "Software Development", 
                "match": 80,
                "reason": "Python is widely used in software development"
            })
    
    if student_profile.get('cgpa', 0) >= 8.0:
        recommendations.append({
            "career": "Product Management",
            "match": 75,
            "reason": "High academic performance suitable for PM roles"
        })
    
    # Sort by match score
    recommendations.sort(key=lambda x: x['match'], reverse=True)
    
    return recommendations[:3]  # Return top 3
