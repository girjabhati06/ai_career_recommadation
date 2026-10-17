from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

# Load trained AI model
model = joblib.load("career_model.pkl")


# Target skill levels for each career
career_targets = {
    "Software Developer": {
        "Programming": 5,
        "Mathematics": 3,
        "Communication": 3,
        "Creativity": 3,
        "Problem Solving": 5,
        "Technology Interest": 5,
        "Learning Ability": 5
    },

    "Data Scientist": {
        "Programming": 4,
        "Mathematics": 5,
        "Communication": 3,
        "Creativity": 3,
        "Problem Solving": 5,
        "Technology Interest": 5,
        "Learning Ability": 5
    },

    "Data Analyst": {
        "Programming": 3,
        "Mathematics": 5,
        "Communication": 4,
        "Creativity": 3,
        "Problem Solving": 4,
        "Technology Interest": 4,
        "Learning Ability": 4
    },

    "Web Developer": {
        "Programming": 5,
        "Mathematics": 2,
        "Communication": 3,
        "Creativity": 4,
        "Problem Solving": 4,
        "Technology Interest": 5,
        "Learning Ability": 4
    },

    "UI/UX Designer": {
        "Programming": 2,
        "Mathematics": 2,
        "Communication": 4,
        "Creativity": 5,
        "Problem Solving": 4,
        "Technology Interest": 4,
        "Learning Ability": 4
    },

    "Cybersecurity Analyst": {
        "Programming": 4,
        "Mathematics": 4,
        "Communication": 3,
        "Creativity": 3,
        "Problem Solving": 5,
        "Technology Interest": 5,
        "Learning Ability": 5
    },

    "Digital Marketer": {
        "Programming": 2,
        "Mathematics": 3,
        "Communication": 5,
        "Creativity": 5,
        "Problem Solving": 3,
        "Technology Interest": 4,
        "Learning Ability": 4
    },

    "Database Administrator": {
        "Programming": 4,
        "Mathematics": 3,
        "Communication": 3,
        "Creativity": 2,
        "Problem Solving": 5,
        "Technology Interest": 5,
        "Learning Ability": 5
    },

    "Cloud Engineer": {
        "Programming": 4,
        "Mathematics": 3,
        "Communication": 3,
        "Creativity": 2,
        "Problem Solving": 5,
        "Technology Interest": 5,
        "Learning Ability": 5
    },

    "AI/ML Engineer": {
        "Programming": 5,
        "Mathematics": 5,
        "Communication": 3,
        "Creativity": 3,
        "Problem Solving": 5,
        "Technology Interest": 5,
        "Learning Ability": 5
    }
}


# Career roadmaps
career_roadmaps = {
    "Software Developer": [
        "Learn Python or C++ programming",
        "Learn Data Structures and Algorithms",
        "Learn SQL and databases",
        "Learn Git and GitHub",
        "Build 2-3 software projects",
        "Prepare for internships and technical interviews"
    ],

    "Data Scientist": [
        "Learn Python and statistics",
        "Learn NumPy, Pandas and Matplotlib",
        "Learn SQL and data analysis",
        "Learn Machine Learning",
        "Build data science projects",
        "Create a portfolio and prepare for internships"
    ],

    "Data Analyst": [
        "Learn Excel and data handling",
        "Learn SQL",
        "Learn Python and Pandas",
        "Learn data visualization",
        "Practice Power BI or Tableau",
        "Build data analysis projects"
    ],

    "Web Developer": [
        "Learn HTML and CSS",
        "Learn JavaScript",
        "Learn frontend frameworks",
        "Learn backend development",
        "Learn databases",
        "Build and deploy web projects"
    ],

    "UI/UX Designer": [
        "Learn UI/UX design principles",
        "Learn Figma",
        "Practice wireframing",
        "Learn user research",
        "Create mobile and web designs",
        "Build a professional design portfolio"
    ],

    "Cybersecurity Analyst": [
        "Learn networking fundamentals",
        "Learn Linux basics",
        "Learn cybersecurity fundamentals",
        "Practice ethical security concepts",
        "Learn security tools and monitoring",
        "Build cybersecurity projects and labs"
    ],

    "Digital Marketer": [
        "Learn digital marketing fundamentals",
        "Learn SEO",
        "Learn social media marketing",
        "Learn content marketing",
        "Understand analytics",
        "Create marketing campaigns and projects"
    ],

    "Database Administrator": [
        "Learn SQL",
        "Learn database design",
        "Learn MySQL or PostgreSQL",
        "Learn database security",
        "Practice backup and recovery",
        "Build database management projects"
    ],

    "Cloud Engineer": [
        "Learn networking fundamentals",
        "Learn Linux",
        "Learn cloud computing concepts",
        "Learn AWS, Azure or Google Cloud",
        "Practice cloud deployment",
        "Build cloud-based projects"
    ],

    "AI/ML Engineer": [
        "Learn Python",
        "Learn mathematics and statistics",
        "Learn NumPy and Pandas",
        "Learn Machine Learning",
        "Learn Deep Learning fundamentals",
        "Build AI/ML projects"
    ]
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    # Get student ratings
    programming = int(request.form["programming"])
    mathematics = int(request.form["mathematics"])
    communication = int(request.form["communication"])
    creativity = int(request.form["creativity"])
    problem_solving = int(request.form["problem_solving"])
    technology_interest = int(request.form["technology_interest"])
    learning_ability = int(request.form["learning_ability"])

    # Prepare student data
    student_data = [[
        programming,
        mathematics,
        communication,
        creativity,
        problem_solving,
        technology_interest,
        learning_ability
    ]]

    # Get prediction probabilities
    probabilities = model.predict_proba(student_data)[0]

    # Match careers with probabilities
    career_scores = list(zip(model.classes_, probabilities))

    # Sort from highest to lowest
    career_scores.sort(key=lambda x: x[1], reverse=True)

    # Top 3 careers
    top_careers = []

    for career, score in career_scores[:3]:
        top_careers.append({
            "career": career,
            "confidence": round(score * 100, 2)
        })

    # Best career
    best_career = top_careers[0]["career"]
    best_confidence = top_careers[0]["confidence"]

    # Current skills
    current_skills = {
        "Programming": programming,
        "Mathematics": mathematics,
        "Communication": communication,
        "Creativity": creativity,
        "Problem Solving": problem_solving,
        "Technology Interest": technology_interest,
        "Learning Ability": learning_ability
    }

    # Target skills for recommended career
    target_skills = career_targets[best_career]

    # Calculate skill gaps
    skill_gaps = []

    for skill, current_score in current_skills.items():

        target_score = target_skills[skill]
        gap = target_score - current_score

        if gap <= 0:
            status = "Strong"
        elif gap == 1:
            status = "Moderate"
        else:
            status = "Needs Improvement"

        skill_gaps.append({
            "skill": skill,
            "current": current_score,
            "target": target_score,
            "gap": max(gap, 0),
            "status": status
        })

    # Career roadmap
    roadmap = career_roadmaps[best_career]

    # Send all results to result.html
    return render_template(
        "result.html",
        career=best_career,
        confidence=best_confidence,
        top_careers=top_careers,
        skills=current_skills,
        skill_gaps=skill_gaps,
        roadmap=roadmap
    )


if __name__ == "__main__":
    app.run(debug=True)