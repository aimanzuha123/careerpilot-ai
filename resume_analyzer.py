class ResumeAnalyzer:
    def __init__(self):
        pass

    def analyze(self, text):
        words = text.lower().split()
        skills = ["python", "sql", "docker", "aws", "react", "ml"]
        found = [s for s in skills if s in words]

        return {
            "matched_skills": found,
            "gap_skills": [s for s in skills if s not in found],
            "score": int((len(found) / len(skills)) * 100)
        }