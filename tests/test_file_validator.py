import config
from modules.file_validator import get_file_extension
from modules.file_validator import validate_file
from modules.file_validator import validate_file_count


def test_get_pdf_extension():
    assert get_file_extension("resume.PDF") == "pdf"


def test_file_without_extension():
    assert get_file_extension("resume") == ""


def test_valid_pdf_file():
    result = validate_file("resume.pdf", 1000)

    assert result["valid"] is True


def test_empty_file():
    result = validate_file("resume.pdf", 0)

    assert result["valid"] is False
    assert result["message"] == config.EMPTY_FILE_MESSAGE


def test_unsupported_file():
    result = validate_file("resume.jpg", 1000)

    assert result["valid"] is False
    assert result["message"] == config.INVALID_FILE_MESSAGE


def test_file_larger_than_limit():
    large_size = (config.MAX_FILE_SIZE_MB * config.BYTES_PER_MB) + 1
    result = validate_file("resume.pdf", large_size)

    assert result["valid"] is False
    assert result["message"] == config.TOO_LARGE_FILE_MESSAGE


def test_too_many_files():
    number_of_files = config.MAX_FILES_PER_BATCH + 1
    result, message = validate_file_count(number_of_files)

    assert result is False
    assert message == config.TOO_MANY_FILES_MESSAGE

