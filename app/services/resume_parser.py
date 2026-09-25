from pathlib import Path


def extract_resume_text(path):

    suffix = Path(path).suffix.lower()

    if suffix == ".pdf":

        from pypdf import PdfReader

        reader = PdfReader(path)

        text = []

        for page in reader.pages:

            text.append(
                page.extract_text() or ""
            )

        return "\n".join(text)

    if suffix == ".docx":

        from docx import Document

        document = Document(path)

        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

    raise ValueError(
        "Unsupported resume format."
    )