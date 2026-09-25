import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "change-this-secret-key"
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'instance' / 'interview.db'}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = str(BASE_DIR / "uploads")

    MAX_CONTENT_LENGTH = 8 * 1024 * 1024

    ALLOWED_EXTENSIONS = {
        "pdf",
        "docx"
    }

    OPENAI_API_KEY = os.getenv(
        "OPENAI_API_KEY",
        ""
    )

    OPENAI_MODEL = os.getenv(
        "OPENAI_MODEL",
        "gpt-5"
    )