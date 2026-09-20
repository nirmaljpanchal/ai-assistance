import docx
import pymupdf


class ExtractionError(Exception):
    pass


def extract_text(path: str, mime_type: str) -> str:
    if mime_type == "application/pdf":
        text = _extract_pdf(path)
    elif mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = _extract_docx(path)
    else:
        raise ExtractionError(f"Unsupported mime type: {mime_type}")

    text = text.strip()
    if not text:
        raise ExtractionError("No extractable text found in document")
    return text


def _extract_pdf(path: str) -> str:
    with pymupdf.open(path) as pdf:  # type: ignore[no-untyped-call]
        return "\n\n".join(page.get_text() for page in pdf)


def _extract_docx(path: str) -> str:
    document = docx.Document(path)
    return "\n\n".join(p.text for p in document.paragraphs if p.text.strip())
