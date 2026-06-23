class RoleManager:
    def __init__(self):
        self.roles = {
            "AI Engineer": {
                "skills": ["Python", "Machine Learning", "Deep Learning", "NLP"],
                "level": "High Growth"
            },
            "Data Analyst": {
                "skills": ["Python", "SQL", "Excel", "Power BI"],
                "level": "Stable Demand"
            },
            "DevOps Engineer": {
                "skills": ["Docker", "Kubernetes", "AWS", "CI/CD"],
                "level": "High Demand"
            },
            "Full Stack Developer": {
                "skills": ["HTML", "CSS", "JavaScript", "React", "Python"],
                "level": "Strong Demand"
            },
            "Cybersecurity Analyst": {
                "skills": ["Networking", "Linux", "Security Tools"],
                "level": "Growing"
            }
        }

    def get_roles(self):
        return list(self.roles.keys())

    def get_role_info(self, role):
        return self.roles.get(role, {})
