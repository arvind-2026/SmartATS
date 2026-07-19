from types import SimpleNamespace

from modules.contact_extractor import create_name_from_file
from modules.contact_extractor import detect_name_with_ner
from modules.contact_extractor import detect_name_from_header
from modules.contact_extractor import extract_candidate_contact
from modules.contact_extractor import extract_email
from modules.contact_extractor import extract_phone
from modules.contact_extractor import valid_phone_number


def fake_name_model(text):
    entity = SimpleNamespace(text="Jane Doe", label_="PERSON")

    return SimpleNamespace(ents=[entity])


def test_extract_name_with_ner():
    name, evidence, confidence = detect_name_with_ner(
        "Jane Doe\nPython Developer",
        fake_name_model,
    )

    assert name == "Jane Doe"
    assert evidence == "Jane Doe"
    assert confidence == "High"


def test_extract_email_address():
    assert extract_email("Email: jane@example.com") == "jane@example.com"


def test_extract_labelled_phone_number():
    text = "Experience: 2020 - 2024\nMobile: +91 98765 43210"

    assert extract_phone(text) == "+91 98765 43210"


def test_reject_year_range_as_phone():
    assert valid_phone_number("2020 - 2024") is False


def test_filename_name_fallback():
    assert create_name_from_file("jane_doe_resume.pdf") == "Jane Doe"


def test_extract_complete_contact():
    text = "Jane Doe\nEmail: jane@example.com\nPhone: +91 98765 43210"
    result = extract_candidate_contact(text, "resume.pdf", fake_name_model)

    assert result["name"] == "Jane Doe"
    assert result["email"] == "jane@example.com"
    assert result["phone"] == "+91 98765 43210"


def test_ner_does_not_merge_name_with_job_title():
    calls = []

    def line_name_model(text):
        calls.append(text)

        if text == "JANE DOE":
            entity = SimpleNamespace(text="JANE DOE", label_="PERSON")
            return SimpleNamespace(ents=[entity])

        entity = SimpleNamespace(text="JUNIOR", label_="PERSON")
        return SimpleNamespace(ents=[entity])

    name, evidence, confidence = detect_name_with_ner(
        "JANE DOE\nJUNIOR PYTHON DEVELOPER",
        line_name_model,
    )

    assert name == "JANE DOE"
    assert evidence == "JANE DOE"
    assert confidence == "High"
    assert calls[0] == "JANE DOE"


def test_phone_does_not_include_address_zip_code():
    text = (
        "123 Tech Way, San Francisco, CA 94102 "
        "• (555) 019-2834 • jane.doe@email.com"
    )

    assert extract_phone(text) == "(555) 019-2834"


def test_detect_uppercase_name_from_resume_header():
    text = "JANE      DOE\nJUNIOR PYTHON DEVELOPER"

    name, evidence, confidence = detect_name_from_header(text)

    assert name == "JANE DOE"
    assert evidence == "JANE      DOE"
    assert confidence == "High"


def test_job_title_is_not_accepted_as_name():
    name, evidence, confidence = detect_name_from_header(
        "JUNIOR PYTHON DEVELOPER"
    )

    assert name == ""
    assert evidence == ""
    assert confidence == "Low"
