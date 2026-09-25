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

    analysis = json.loads(
        resume.analysis_json or "{}"
    )

    if request.method == "POST":

        difficulty = request.form.get(
            "difficulty",
            "medium"
        )

        count = min(
            max(
                int(
                    request.form.get(
                        "count",
                        8
                    )
                ),
                3
            ),
            15
        )

        questions = generate_questions(
            resume.extracted_text,
            analysis,
            difficulty,
            count
        )

        interview = Interview(
            user_id=current_user.id,
            resume_id=resume.id,
            questions_json=json.dumps(
                questions
            ),
            answers_json="[]"
        )

        db.session.add(
            interview
        )

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

    questions = json.loads(
        interview.questions_json or "[]"
    )

    if request.method == "POST":

        answers = []

        for i in range(
            len(questions)
        ):

            answer = request.form.get(
                f"answer_{i}",
                ""
            ).strip()

            answers.append(answer)

        result = evaluate_answers(
            questions,
            answers
        )

        interview.answers_json = json.dumps(
            answers
        )

        interview.score = result["score"]

        interview.feedback = result[
            "feedback"
        ]

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


@interview_bp.route(
    "/result/<int:interview_id>"
)
@login_required
def result(interview_id):

    interview = Interview.query.filter_by(
        id=interview_id,
        user_id=current_user.id
    ).first_or_404()

    questions = json.loads(
        interview.questions_json or "[]"
    )

    answers = json.loads(
        interview.answers_json or "[]"
    )

    return render_template(
        "result.html",
        interview=interview,
        questions=questions,
        answers=answers
    )