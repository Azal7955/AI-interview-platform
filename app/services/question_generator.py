import json
import os
import random
import requests


# ============================================================
# DIFFICULTY-BASED QUESTION POOLS
# ============================================================

QUESTION_POOLS = {
    "easy": {
        "Python": [
            "What is a Python list, and when would you use one?",
            "What is the difference between a list and a tuple in Python?",
            "What is a Python function and how do you define one?",
            "What is the purpose of a Python dictionary?",
            "What are variables in Python?",
            "What is the difference between == and = in Python?",
        ],

        "Flask": [
            "What is Flask and why is it used?",
            "What is a Flask route?",
            "What is the purpose of templates in Flask?",
            "How do you start a basic Flask application?",
            "What is a Flask blueprint?",
            "What is the purpose of app.run()?",
        ],

        "SQL": [
            "What is a primary key in SQL?",
            "What is the purpose of a SELECT query?",
            "What is a SQL table?",
            "What is the difference between DELETE and DROP?",
            "What is a foreign key?",
            "What is the purpose of WHERE in SQL?",
        ],

        "Machine Learning": [
            "What is machine learning?",
            "What is a feature in machine learning?",
            "What is a training dataset?",
            "What is classification?",
            "What is regression?",
            "What is a machine-learning model?",
        ],

        "JavaScript": [
            "What is a variable in JavaScript?",
            "What is a JavaScript function?",
            "What is an array in JavaScript?",
            "What is the purpose of let and const?",
            "What is an object in JavaScript?",
            "What is the DOM?",
        ],

        "React": [
            "What is React?",
            "What is a React component?",
            "What are props in React?",
            "What is JSX?",
            "What is React state?",
            "What is a functional component?",
        ],
    },

    "medium": {
        "Python": [
            "How would you improve the performance of a Python application?",
            "Explain exception handling in Python and give a practical use case.",
            "When would you use a list comprehension instead of a normal loop?",
            "How would you structure a Python project so it remains maintainable?",
            "What is the difference between shallow copy and deep copy?",
            "How would you handle errors in a Python API?",
        ],

        "Flask": [
            "How would you design authentication in a Flask application?",
            "How would you organize a Flask project using blueprints?",
            "How would you validate and safely process form data in Flask?",
            "How would you connect a Flask application to a relational database?",
            "How would you implement file uploads securely in Flask?",
            "How would you create a REST API using Flask?",
        ],

        "SQL": [
            "How would you optimize a slow SQL query?",
            "Explain the difference between INNER JOIN and LEFT JOIN.",
            "When would you create an index?",
            "How would you find duplicate records in a SQL table?",
            "What is normalization and why is it useful?",
            "How would you retrieve the second-highest salary from a table?",
        ],

        "Machine Learning": [
            "How would you detect and reduce overfitting?",
            "Explain the difference between training, validation, and test data.",
            "How would you choose an evaluation metric for a classification problem?",
            "Why is feature scaling useful for some algorithms?",
            "What is cross-validation and why is it useful?",
            "How would you handle missing values in a dataset?",
        ],

        "JavaScript": [
            "How do asynchronous operations work in JavaScript?",
            "Explain promises and async/await.",
            "What is event delegation?",
            "How would you debug a JavaScript function producing an unexpected result?",
            "What is the difference between var, let, and const?",
            "How would you handle errors from an API request?",
        ],

        "React": [
            "How would you improve the performance of a React application?",
            "Explain the difference between state and props in React.",
            "When would you use useEffect?",
            "How would you prevent unnecessary re-renders?",
            "What is conditional rendering in React?",
            "How would you fetch API data in a React application?",
        ],
    },

    "hard": {
        "Python": [
            "A Python API becomes slow under concurrent load. How would you profile it and identify the bottleneck?",
            "How would you design a thread-safe Python service?",
            "Explain Python memory management and how you would investigate a memory leak.",
            "How would you redesign a large Python application to support clean dependency boundaries?",
            "How would you design a scalable Python backend for thousands of concurrent users?",
            "How would you diagnose a production Python application that randomly crashes?",
        ],

        "Flask": [
            "Design a scalable Flask API with authentication, rate limiting, caching, and database transactions.",
            "How would you secure a Flask application against CSRF, XSS, SQL injection, and insecure uploads?",
            "A Flask application works locally but fails under production load. How would you diagnose it?",
            "How would you design background jobs for a Flask application?",
            "How would you design Flask APIs for high availability?",
            "How would you handle database transactions safely in a high-traffic Flask application?",
        ],

        "SQL": [
            "A production query scans millions of rows and causes timeouts. How would you optimize it?",
            "How would you design database indexes for a high-write application?",
            "Explain transaction isolation levels and how they prevent race conditions.",
            "How would you redesign a poorly normalized database?",
            "How would you diagnose database deadlocks in production?",
            "How would you optimize a database serving millions of daily queries?",
        ],

        "Machine Learning": [
            "A model has high validation accuracy but poor performance after deployment. How would you investigate?",
            "How would you design an ML pipeline that prevents data leakage?",
            "How would you handle severe class imbalance when false negatives are costly?",
            "How would you monitor model drift and decide when retraining is required?",
            "How would you design a machine-learning system for real-time predictions?",
            "How would you identify whether poor predictions are caused by data quality or model quality?",
        ],

        "JavaScript": [
            "How would you diagnose a memory leak in a long-running JavaScript application?",
            "Explain the event loop, microtasks, and macrotasks.",
            "How would you design a retry and cancellation strategy for concurrent API requests?",
            "A large JavaScript application has severe UI lag. How would you profile it?",
            "How would you design a scalable frontend architecture for a large application?",
            "How would you debug race conditions in asynchronous JavaScript code?",
        ],

        "React": [
            "How would you architect a large React application to keep state and data fetching maintainable?",
            "A React page becomes slow with thousands of rendered items. How would you optimize it?",
            "How would you design reliable error handling for dependent API requests?",
            "Explain how React reconciliation affects rendering performance.",
            "How would you design a scalable React application with complex global state?",
            "How would you diagnose unnecessary rendering in a large React component tree?",
        ],
    },
}


# ============================================================
# GENERAL RESUME-BASED QUESTIONS
# ============================================================

COMMON_POOLS = {
    "easy": [
        ("HR", "Tell me about yourself."),
        ("Project", "Which project on your resume are you most proud of?"),
        ("Project", "What was your main contribution to one of your projects?"),
        ("Education", "Which subject have you enjoyed learning the most?"),
        ("Experience", "What did you learn from your most recent project?"),
        ("HR", "Why are you interested in this field?"),
    ],

    "medium": [
        ("HR", "Describe a challenge you faced during a project and how you solved it."),
        ("Project", "What technical decision did you make in a project, and why?"),
        ("HR", "Describe a time you had to learn a new technology quickly."),
        ("Experience", "How did you test or validate your project?"),
        ("Education", "Which technical topic would you like to improve and why?"),
        ("Project", "What would you improve if you rebuilt your project?"),
    ],

    "hard": [
        ("HR", "Describe a difficult project outcome and explain what you would do differently."),
        ("Project", "Choose a major technical decision from your resume and defend it against an alternative."),
        ("Project", "How would you redesign your project if the number of users increased significantly?"),
        ("Experience", "How would you identify and resolve a serious production issue when the root cause is unclear?"),
        ("Education", "How would you apply an advanced concept you studied to a real-world system?"),
        ("Project", "What are the biggest scalability limitations of your project?"),
    ],
}


# ============================================================
# TEXT HELPERS
# ============================================================

def clean_text(value):
    return " ".join(str(value).split()).strip()


def normalize_question(value):
    return clean_text(value).lower().rstrip("?.!")


# ============================================================
# FALLBACK QUESTION GENERATOR
# ============================================================

def fallback_questions(
    analysis,
    count,
    difficulty,
    previous_questions=None
):
    previous = {
        normalize_question(q)
        for q in (previous_questions or [])
    }

    candidates = []

    skills = analysis.get("skills", []) or []
    projects = analysis.get("projects", []) or []
    education = analysis.get("education", []) or []
    experience = analysis.get("experience", []) or []

    # --------------------------------------------------------
    # Technical questions based on resume skills
    # --------------------------------------------------------

    for skill in skills:

        skill_name = clean_text(skill)

        pool = QUESTION_POOLS.get(
            difficulty,
            {}
        ).get(
            skill_name,
            []
        )

        for question in pool:
            candidates.append(
                ("Technical", question)
            )

    # --------------------------------------------------------
    # Project questions
    # --------------------------------------------------------

    for project in projects[:6]:

        project = clean_text(project)

        if not project:
            continue

        if difficulty == "easy":

            question = (
                f"Briefly explain your role "
                f"in the project '{project}'."
            )

        elif difficulty == "medium":

            question = (
                f"What technical challenge did "
                f"you solve in '{project}', and how?"
            )

        else:

            question = (
                f"If you had to redesign "
                f"'{project}' for much higher scale, "
                f"what would you change and why?"
            )

        candidates.append(
            ("Project", question)
        )

    # --------------------------------------------------------
    # Experience questions
    # --------------------------------------------------------

    for item in experience[:3]:

        item = clean_text(item)

        if not item:
            continue

        if difficulty == "easy":

            question = (
                f"What did you learn from "
                f"your experience with '{item}'?"
            )

        elif difficulty == "medium":

            question = (
                f"What was your main responsibility "
                f"in '{item}' and how did you handle it?"
            )

        else:

            question = (
                f"What difficult engineering decision "
                f"could arise from your experience with "
                f"'{item}', and how would you evaluate it?"
            )

        candidates.append(
            ("Experience", question)
        )

    # --------------------------------------------------------
    # Education questions
    # --------------------------------------------------------

    for item in education[:2]:

        item = clean_text(item)

        if not item:
            continue

        if difficulty == "easy":

            question = (
                f"What did you learn from "
                f"your studies in '{item}'?"
            )

        elif difficulty == "medium":

            question = (
                f"How have your studies in "
                f"'{item}' helped you in practical projects?"
            )

        else:

            question = (
                f"Which advanced concept from "
                f"'{item}' would you apply to a "
                f"real software system and why?"
            )

        candidates.append(
            ("Education", question)
        )

    # Add general questions.
    candidates.extend(
        COMMON_POOLS[difficulty]
    )

    # --------------------------------------------------------
    # RANDOMIZE
    # --------------------------------------------------------

    random.SystemRandom().shuffle(
        candidates
    )

    selected = []
    used = set(previous)

    for q_type, question in candidates:

        key = normalize_question(question)

        if key in used:
            continue

        used.add(key)

        selected.append(
            {
                "question": question,
                "type": q_type,
                "difficulty": difficulty
            }
        )

        if len(selected) >= count:
            break

    # --------------------------------------------------------
    # Extra questions if resume has little information
    # --------------------------------------------------------

    if len(selected) < count:

        skills = analysis.get(
            "skills",
            []
        ) or ["your technical background"]

        topic = clean_text(
            skills[0]
        )

        extra_templates = {

            "easy": [
                f"What is {topic} used for?",
                f"How did you first learn {topic}?",
                f"Where could {topic} be useful?",
                f"What is one basic feature of {topic}?",
                f"Why is {topic} useful in software development?",
            ],

            "medium": [
                f"How would you use {topic} to solve a practical problem?",
                f"What common mistake can developers make when using {topic}?",
                f"How would you test a feature built with {topic}?",
                f"What trade-off should you consider when choosing {topic}?",
                f"How would you debug a problem involving {topic}?",
            ],

            "hard": [
                f"What architectural trade-off would you evaluate when using {topic} at scale?",
                f"How would you diagnose a difficult production issue involving {topic}?",
                f"How would you improve the reliability of a system built around {topic}?",
                f"What failure modes should an expert consider when designing with {topic}?",
                f"How would you scale a system heavily dependent on {topic}?",
            ],
        }

        extras = extra_templates[
            difficulty
        ].copy()

        random.SystemRandom().shuffle(
            extras
        )

        for question in extras:

            key = normalize_question(
                question
            )

            if key in used:
                continue

            used.add(key)

            selected.append(
                {
                    "question": question,
                    "type": "Technical",
                    "difficulty": difficulty
                }
            )

            if len(selected) >= count:
                break

    return selected[:count]


# ============================================================
# AI QUESTION GENERATOR
# ============================================================

def openai_questions(
    resume_text,
    analysis,
    count,
    difficulty,
    previous_questions=None
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

    previous = list(
        dict.fromkeys(
            clean_text(q)
            for q in (previous_questions or [])
            if clean_text(q)
        )
    )

    previous_text = json.dumps(
        previous[-100:],
        ensure_ascii=False
    )

    prompt = f"""
You are an AI technical interviewer.

Generate exactly {count} NEW interview questions.

DIFFICULTY:
{difficulty.upper()}

STRICT RULES:

1. Every question MUST be {difficulty} difficulty.
2. Every question must be different.
3. Do not repeat any previous question.
4. Do not simply reword a previous question.
5. Questions must be based on the candidate's resume.
6. Technical questions should be based on the candidate's skills.
7. Project questions should be based on projects in the resume.
8. Easy:
   - Fundamentals
   - Definitions
   - Simple understanding
9. Medium:
   - Application
   - Debugging
   - Moderate problem solving
   - Practical scenarios
10. Hard:
   - Architecture
   - Scalability
   - Security
   - Advanced debugging
   - Trade-offs
11. Return ONLY JSON.
12. Do not add explanations outside JSON.

JSON FORMAT:

[
    {{
        "question": "Question text",
        "type": "Technical",
        "difficulty": "{difficulty}"
    }}
]

PREVIOUS QUESTIONS TO AVOID:
{previous_text}

RESUME ANALYSIS:
{json.dumps(analysis, ensure_ascii=False)}

RESUME:
{resume_text[:12000]}
"""

    response = requests.post(
        "https://api.openai.com/v1/responses",

        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
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

    return json.loads(
        output
    )


# ============================================================
# VALIDATE AI QUESTIONS
# ============================================================

def validate_ai_questions(
    result,
    count,
    difficulty,
    previous_questions
):

    if not isinstance(
        result,
        list
    ):
        return []

    previous = {
        normalize_question(q)
        for q in (previous_questions or [])
    }

    seen = set()
    clean = []

    for item in result:

        if not isinstance(
            item,
            dict
        ):
            continue

        question = clean_text(
            item.get(
                "question",
                ""
            )
        )

        if not question:
            continue

        key = normalize_question(
            question
        )

        if key in previous:
            continue

        if key in seen:
            continue

        seen.add(key)

        clean.append(
            {
                "question": question,
                "type": clean_text(
                    item.get(
                        "type",
                        "Technical"
                    )
                ) or "Technical",

                # Always store the difficulty selected
                # by the user.
                "difficulty": difficulty
            }
        )

        if len(clean) >= count:
            break

    return clean


# ============================================================
# MAIN FUNCTION
# ============================================================

def generate_questions(
    resume_text,
    analysis,
    difficulty="medium",
    count=8,
    previous_questions=None
):

    difficulty = str(
        difficulty
    ).lower().strip()

    if difficulty not in {
        "easy",
        "medium",
        "hard"
    }:
        difficulty = "medium"

    count = max(
        3,
        min(
            int(count),
            15
        )
    )

    previous_questions = (
        previous_questions or []
    )

    # Try AI generation first.
    try:

        result = openai_questions(
            resume_text,
            analysis,
            count,
            difficulty,
            previous_questions
        )

        validated = validate_ai_questions(
            result,
            count,
            difficulty,
            previous_questions
        )

        if len(validated) >= count:
            return validated

    except Exception as error:

        print(
            "AI question generation error:",
            error
        )

    # If AI fails, use randomized fallback.
    return fallback_questions(
        analysis,
        count,
        difficulty,
        previous_questions
    )