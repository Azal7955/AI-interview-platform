import json
import os

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app
)

from flask_login import (
    login_required,
    current_user
)

from werkzeug.utils import secure_filename

from ..extensions import db
from ..models.resume import Resume

from ..services.resume_parser import (
    extract_resume_text
)

from ..services.resume_analyzer import (
    analyze_resume
)


resume_bp = Blueprint(
    "resume",
    __name__,
    url_prefix="/resume"
)


def allowed_file(filename):

    return (
        "."
        in filename
        and filename.rsplit(
            ".",
            1
        )[1].lower()
        in current_app.config[
            "ALLOWED_EXTENSIONS"
        ]
    )


@resume_bp.route(
    "/upload",
    methods=["GET", "POST"]
)
@login_required
def upload():

    if request.method == "POST":

        uploaded = request.files.get(
            "resume"
        )

        if (
            not uploaded
            or not uploaded.filename
        ):

            flash(
                "Please select a PDF or DOCX resume.",
                "error"
            )

            return render_template(
                "upload_resume.html"
            )

        if not allowed_file(
            uploaded.filename
        ):

            flash(
                "Only PDF and DOCX files are supported.",
                "error"
            )

            return render_template(
                "upload_resume.html"
            )

        filename = secure_filename(
            uploaded.filename
        )

        user_dir = os.path.join(
            current_app.config[
                "UPLOAD_FOLDER"
            ],
            str(current_user.id)
        )

        os.makedirs(
            user_dir,
            exist_ok=True
        )

        path = os.path.join(
            user_dir,
            filename
        )

        uploaded.save(path)

        try:

            text = extract_resume_text(
                path
            )

            if len(text.strip()) < 40:

                raise ValueError(
                    "Not enough readable text was found."
                )

            analysis = analyze_resume(
                text
            )

            resume = Resume(
                user_id=current_user.id,
                filename=filename,
                extracted_text=text,
                analysis_json=json.dumps(
                    analysis
                )
            )

            db.session.add(resume)

            db.session.commit()

            return redirect(
                url_for(
                    "resume.analysis",
                    resume_id=resume.id
                )
            )

        except Exception as exc:

            flash(
                f"Resume processing failed: {exc}",
                "error"
            )

    return render_template(
        "upload_resume.html"
    )


@resume_bp.route(
    "/analysis/<int:resume_id>"
)
@login_required
def analysis(resume_id):

    resume = Resume.query.filter_by(
        id=resume_id,
        user_id=current_user.id
    ).first_or_404()

    analysis_data = json.loads(
        resume.analysis_json or "{}"
    )

    return render_template(
        "resume_analysis.html",
        resume=resume,
        analysis=analysis_data
    )