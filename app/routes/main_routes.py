from flask import (
    Blueprint,
    render_template
)

from flask_login import (
    current_user,
    login_required
)

from ..models.interview import Interview


main_bp = Blueprint(
    "main",
    __name__
)


@main_bp.route("/")
def index():

    return render_template(
        "index.html"
    )


@main_bp.route("/dashboard")
@login_required
def dashboard():

    interviews = Interview.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Interview.created_at.desc()
    ).all()

    return render_template(
        "dashboard.html",
        interviews=interviews
    )