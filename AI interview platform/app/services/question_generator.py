import json
import os
import requests


QUESTION_TEMPLATES = {

    "Python": [

        "Explain a Python project from your resume.",

        "How would you improve the performance of your Python application?"

    ],

    "Flask": [

        "Explain the Flask project mentioned in your resume.",

        "How would you design authentication in Flask?"

    ],

    "SQL": [

        "Describe a database project you worked on.",

        "How would you optimize a slow SQL query?"

    ],

    "Machine Learning": [

        "Explain the machine-learning project on your resume.",

        "How would you detect overfitting?"

    ],

    "JavaScript": [

        "Explain a JavaScript project you developed.",

        "How do asynchronous operations work in JavaScript?"

    ],

    "React": [

        "Explain the React project on your resume.",

        "How would you improve React application performance?"

    ]
}


def fallback_questions(
    analysis,
    count,
    difficulty
):

    skills = analysis.get(
        "skills",
        []
    )

    questions = []

    for skill in skills:

        if skill in QUESTION_TEMPLATES:

            for question in QUESTION_TEMPLATES[
                skill
            ]:

                questions.append({

                    "question": question,

                    "type": "Technical",

                    "difficulty": difficulty

                })

    for project in analysis.get(
        "projects",
        []
    )[:3]:

        questions.append({

            "question":
                f"Your resume mentions '{project}'. "
                "What was your contribution?",

            "type":
                "Project",

            "difficulty":
                difficulty

        })

    questions.extend([

        {
            "question":
                "Tell me about yourself.",

            "type":
                "HR",

            "difficulty":
                difficulty
        },

        {
            "question":
                "Which project on your resume are you most proud of?",

            "type":
                "HR/Project",

            "difficulty":
                difficulty
        },

        {
            "question":
                "Describe a difficult technical problem you solved.",

            "type":
                "Technical",

            "difficulty":
                difficulty
        },

        {
            "question":
                "What would you improve in one of your projects?",

            "type":
                "Project",

            "difficulty":
                difficulty
        }

    ])

    unique = []

    seen = set()

    for item in questions:

        question = item["question"]

        if question not in seen:

            seen.add(question)

            unique.append(item)

    return unique[:count]


def openai_questions(
    resume_text,
    analysis,
    count,
    difficulty
):

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

You are an AI technical interviewer.

Generate exactly {count} questions.

Base the questions ONLY on this resume.

Test:

- Skills
- Projects
- Education
- Experience
- Technical knowledge
- HR/project knowledge

Difficulty:
{difficulty}

Return ONLY JSON.

Format:

[
  {{
    "question": "...",
    "type": "Technical",
    "difficulty": "{difficulty}"
  }}
]

Resume analysis:

{json.dumps(analysis)}

Resume:

{resume_text[:12000]}
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


def generate_questions(
    resume_text,
    analysis,
    difficulty="medium",
    count=8
):

    try:

        result = openai_questions(

            resume_text,

            analysis,

            count,

            difficulty

        )

        if result:

            return result[:count]

    except Exception:

        pass

    return fallback_questions(

        analysis,

        count,

        difficulty

    )