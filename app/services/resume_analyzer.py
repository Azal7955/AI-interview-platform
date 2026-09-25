import json
import os
import re
import requests


SKILLS = [
    "Python",
    "Java",
    "C++",
    "C",
    "JavaScript",
    "TypeScript",
    "HTML",
    "CSS",
    "Flask",
    "Django",
    "FastAPI",
    "React",
    "Node.js",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "Git",
    "GitHub",
    "Docker",
    "AWS",
    "Azure",
    "Machine Learning",
    "Deep Learning",
    "TensorFlow",
    "PyTorch",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "Power BI",
    "Tableau",
    "Excel",
    "REST API",
    "OpenCV",
    "NLP",
    "Data Science",
    "Cybersecurity",
    "Arduino",
    "ESP32"
]


def local_analysis(text):

    lower_text = text.lower()

    found_skills = []

    for skill in SKILLS:

        if skill.lower() in lower_text:

            found_skills.append(skill)

    education = []

    projects = []

    experience = []

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if re.search(
            r"\b(b\.?tech|b\.?e\.?|m\.?tech|mca|bca|bsc|msc|bachelor|master|degree|diploma)\b",
            line,
            re.I
        ):

            education.append(line)

        if re.search(
            r"\b(project|developed|built|created)\b",
            line,
            re.I
        ):

            projects.append(line)

        if re.search(
            r"\b(experience|intern|internship|developer|engineer|analyst)\b",
            line,
            re.I
        ):

            experience.append(line)

    return {

        "summary":
            f"Detected {len(found_skills)} technical skills "
            "from the resume.",

        "skills":
            found_skills,

        "education":
            education[:8],

        "projects":
            projects[:8],

        "experience":
            experience[:8],

        "strengths": [

            "Technical skills were detected.",

            "Projects and experience can be used "
            "for personalized questions."

        ],

        "improvements": [

            "Add measurable achievements.",

            "Use consistent skill names.",

            "Describe project results clearly."

        ]
    }


def openai_analysis(text):

    api_key = os.getenv(
        "OPENAI_API_KEY"
    )

    if not api_key:

        return None

    model = os.getenv(
        "OPENAI_MODEL",
        "gpt-5"
    )

    prompt = f"""
Analyze this resume for an interview platform.

Return ONLY valid JSON.

Required keys:

summary
skills
education
projects
experience
strengths
improvements

All list values must be JSON arrays.

Resume:

{text[:16000]}
"""

    response = requests.post(

        "https://api.openai.com/v1/responses",

        headers={
            "Authorization":
                f"Bearer {api_key}",

            "Content-Type":
                "application/json"
        },

        json={

            "model": model,

            "input": prompt,

            "store": False

        },

        timeout=90
    )

    response.raise_for_status()

    data = response.json()

    output = data.get(
        "output_text",
        ""
    ).strip()

    if not output:

        return None

    return json.loads(output)


def analyze_resume(text):

    try:

        result = openai_analysis(
            text
        )

        if result:

            return result

    except Exception:

        pass

    return local_analysis(text)