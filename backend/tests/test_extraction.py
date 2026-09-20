from pathlib import Path

import docx
import pymupdf
import pytest

from app.services.extraction import ExtractionError, extract_text

PDF_MIME = "application/pdf"
DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


@pytest.fixture
def sample_pdf(tmp_path: Path) -> Path:
    path = tmp_path / "sample.pdf"
    document = pymupdf.open()
    page = document.new_page()
    page.insert_text((72, 72), "Hello from a test PDF document.")
    document.save(path)
    document.close()
    return path


@pytest.fixture
def empty_pdf(tmp_path: Path) -> Path:
    path = tmp_path / "empty.pdf"
    document = pymupdf.open()
    document.new_page()
    document.save(path)
    document.close()
    return path


@pytest.fixture
def sample_docx(tmp_path: Path) -> Path:
    path = tmp_path / "sample.docx"
    document = docx.Document()
    document.add_paragraph("Hello from a test DOCX document.")
    document.save(path)
    return path


def test_extract_text_from_pdf(sample_pdf: Path) -> None:
    text = extract_text(str(sample_pdf), PDF_MIME)
    assert "Hello from a test PDF document" in text


def test_extract_text_from_docx(sample_docx: Path) -> None:
    text = extract_text(str(sample_docx), DOCX_MIME)
    assert "Hello from a test DOCX document" in text


def test_extract_text_raises_on_empty_document(empty_pdf: Path) -> None:
    with pytest.raises(ExtractionError):
        extract_text(str(empty_pdf), PDF_MIME)


def test_extract_text_raises_on_unsupported_mime(sample_pdf: Path) -> None:
    with pytest.raises(ExtractionError):
        extract_text(str(sample_pdf), "text/plain")
