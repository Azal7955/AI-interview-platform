from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from ..extensions import db
from ..models.user import User


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


@auth_bp.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if current_user.is_authenticated:

        return redirect(
            url_for("main.dashboard")
        )

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        if (
            not name
            or not email
            or len(password) < 6
        ):

            flash(
                "Please fill all fields. Password must contain at least 6 characters.",
                "error"
            )

            return render_template(
                "register.html"
            )

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash(
                "This email is already registered.",
                "error"
            )

            return render_template(
                "register.html"
            )

        user = User(
            name=name,
            email=email
        )

        user.set_password(
            password
        )

        db.session.add(user)

        db.session.commit()

        flash(
            "Registration successful!",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "register.html"
    )


@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if current_user.is_authenticated:

        return redirect(
            url_for("main.dashboard")
        )

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        user = User.query.filter_by(
            email=email
        ).first()

        if (
            not user
            or not user.check_password(password)
        ):

            flash(
                "Invalid email or password.",
                "error"
            )

            return render_template(
                "login.html"
            )

        login_user(user)

        return redirect(
            url_for("main.dashboard")
        )

    return render_template(
        "login.html"
    )


@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("main.index")
    )