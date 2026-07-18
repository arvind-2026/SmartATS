from io import BytesIO

from docx import Document

import config
from modules.resume_extractor import check_extraction_quality
from modules.resume_extractor import extract_resume_text


def create_docx_bytes():
    document = Document()
    document.add_paragraph(
        "Python developer with experience building web applications and working with SQL databases."
    )
    file_stream = BytesIO()
    document.save(file_stream)

    return file_stream.getvalue()


def test_extract_txt_resume():
    resume_text = "Python developer with SQL and Git experience. " * 4
    result = extract_resume_text("resume.txt", resume_text.encode("utf-8"))

    assert result["success"] is True
    assert result["quality"] == "High"
    assert "Python developer" in result["text"]


def test_extract_docx_resume():
    result = extract_resume_text("resume.docx", create_docx_bytes())

    assert result["success"] is True
    assert "Python developer" in result["text"]


def test_blank_txt_resume():
    result = extract_resume_text("resume.txt", b"")

    assert result["success"] is False
    assert result["quality"] == "Failed"


def test_short_resume_has_low_quality():
    quality, warning = check_extraction_quality("Python developer", "txt")

    assert quality == "Low"
    assert warning == config.LOW_TEXT_MESSAGE


def test_corrupt_pdf_resume():
    result = extract_resume_text("resume.pdf", b"This is not a real PDF")

    assert result["success"] is False
    assert result["message"] == config.CORRUPT_FILE_MESSAGE


def test_unknown_resume_format():
    result = extract_resume_text("resume.jpg", b"image data")

    assert result["success"] is False
    assert result["message"] == config.INVALID_FILE_MESSAGE


def test_column_scan_range_is_valid():
    assert config.MINIMUM_COLUMN_SPLIT_PERCENT < config.MAXIMUM_COLUMN_SPLIT_PERCENT
    assert config.COLUMN_SCAN_STEP_PERCENT > 0
