import json

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from flask_login import (
    login_required,
    current_user
)

from ..extensions import db
from ..models.resume import Resume
from ..models.interview import Interview

from ..services.question_generator import (
    generate_questions
)

from ..services.evaluator import (
    evaluate_answers
)


interview_bp = Blueprint(
    "interview",
    __name__,
    url_prefix="/interview"
)


# -------------------------------------------------
# START INTERVIEW
# -------------------------------------------------

@interview_bp.route(
    "/start/<int:resume_id>",
    methods=["GET", "POST"]
)
@login_required
def start(resume_id):

    resume = Resume.query.filter_by(
        id=resume_id,
        user_id=current_user.id
    ).first_or_404()

    try:

        analysis = json.loads(
            resume.analysis_json or "{}"
        )

    except (TypeError, ValueError):

        analysis = {}

    if request.method == "POST":

        difficulty = request.form.get(
            "difficulty",
            "medium"
        ).lower().strip()

        if difficulty not in {
            "easy",
            "medium",
            "hard"
        }:

            difficulty = "medium"

        try:

            count = int(
                request.form.get(
                    "count",
                    8
                )
            )

        except (TypeError, ValueError):

            count = 8

        count = max(
            3,
            min(count, 15)
        )

        # -----------------------------------------
        # Get previously asked questions
        # -----------------------------------------

        previous_questions = []

        old_interviews = (
            Interview.query
            .filter_by(
                user_id=current_user.id,
                resume_id=resume.id
            )
            .order_by(
                Interview.created_at.desc()
            )
            .limit(30)
            .all()
        )

        for old_interview in old_interviews:

            try:

                old_questions = json.loads(
                    old_interview.questions_json
                    or "[]"
                )

            except (TypeError, ValueError):

                old_questions = []

            for item in old_questions:

                if isinstance(item, dict):

                    question = str(
                        item.get(
                            "question",
                            ""
                        )
                    ).strip()

                    if question:
                        previous_questions.append(
                            question
                        )

        # -----------------------------------------
        # Generate new questions
        # -----------------------------------------

        questions = generate_questions(
            resume.extracted_text,
            analysis,
            difficulty,
            count,
            previous_questions
        )

        # -----------------------------------------
        # Create interview
        # -----------------------------------------

        interview = Interview(

            user_id=current_user.id,

            resume_id=resume.id,

            questions_json=json.dumps(
                questions,
                ensure_ascii=False
            ),

            answers_json="[]",

            score=0,

            feedback=""
        )

        db.session.add(interview)

        db.session.commit()

        return redirect(
            url_for(
                "interview.take",
                interview_id=interview.id
            )
        )

    return render_template(
        "interview_setup.html",
        resume=resume
    )


# -------------------------------------------------
# TAKE INTERVIEW
# -------------------------------------------------

@interview_bp.route(
    "/take/<int:interview_id>",
    methods=["GET", "POST"]
)
@login_required
def take(interview_id):

    interview = Interview.query.filter_by(
        id=interview_id,
        user_id=current_user.id
    ).first_or_404()

    try:

        questions = json.loads(
            interview.questions_json or "[]"
        )

    except (TypeError, ValueError):

        questions = []

    # -----------------------------------------
    # Submit answers
    # -----------------------------------------

    if request.method == "POST":

        answers = []

        for i in range(len(questions)):

            answer = request.form.get(
                f"answer_{i}",
                ""
            ).strip()

            answers.append(answer)

        # -----------------------------------------
        # Evaluate answers
        # -----------------------------------------

        evaluation = evaluate_answers(
            questions,
            answers
        )

        # -----------------------------------------
        # Save answers
        # -----------------------------------------

        interview.answers_json = json.dumps(
            answers,
            ensure_ascii=False
        )

        # Total marks
        interview.score = evaluation["score"]

        # Store detailed result
        interview.feedback = json.dumps(
            {
                "text": evaluation["feedback"],
                "max_score": evaluation["max_score"],
                "percentage": evaluation["percentage"],
                "details": evaluation["details"]
            },
            ensure_ascii=False
        )

        db.session.commit()

        return redirect(
            url_for(
                "interview.result",
                interview_id=interview.id
            )
        )

    return render_template(
        "interview.html",
        interview=interview,
        questions=questions
    )


# -------------------------------------------------
# RESULT PAGE
# -------------------------------------------------

@interview_bp.route(
    "/result/<int:interview_id>"
)
@login_required
def result(interview_id):

    interview = Interview.query.filter_by(
        id=interview_id,
        user_id=current_user.id
    ).first_or_404()

    try:

        questions = json.loads(
            interview.questions_json or "[]"
        )

    except (TypeError, ValueError):

        questions = []

    try:

        answers = json.loads(
            interview.answers_json or "[]"
        )

    except (TypeError, ValueError):

        answers = []

    try:

        stored_result = json.loads(
            interview.feedback or "{}"
        )

    except (TypeError, ValueError):

        stored_result = {}

    # Compatibility with old interviews
    if not isinstance(stored_result, dict):

        stored_result = {

            "text": str(
                interview.feedback or ""
            ),

            "max_score": len(
                questions
            ) * 10,

            "percentage": 0,

            "details": []
        }

    return render_template(
        "result.html",

        interview=interview,

        questions=questions,

        answers=answers,

        result=stored_result
    )