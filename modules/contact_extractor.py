import re

import config


def load_name_ner_model():
    """Load the configured spaCy model for person-name detection."""

    import spacy

    return spacy.load(config.NAME_NER_MODEL)


def get_opening_text(text):
    """Return the opening resume lines where a candidate name normally appears."""

    lines = []

    for line in text.splitlines():
        clean_line = line.strip()

        if clean_line:
            lines.append(clean_line)

        if len(lines) >= config.NAME_SCAN_LINE_LIMIT:
            break

    opening_text = "\n".join(lines)

    return opening_text[:config.NAME_SCAN_CHARACTER_LIMIT]


def clean_name(name):
    """Remove unwanted punctuation and spacing from a detected name."""

    name = re.sub(r"[^A-Za-zÀ-ÖØ-öø-ÿ.' -]", "", name)

    return " ".join(name.split()).strip("-., ")


def valid_name(name):
    """Check whether a detected value looks like a person's name."""

    words = name.split()

    if len(words) < config.MINIMUM_NAME_WORDS:
        return False

    if len(words) > config.MAXIMUM_NAME_WORDS:
        return False

    lower_name = name.lower()

    for alternatives in config.SECTION_HEADINGS.values():
        if lower_name in alternatives:
            return False

    for word in words:
        if word.lower().strip(".,") in config.NAME_ROLE_WORDS:
            return False

    return True


def detect_name_from_header(text):
    """Detect an all-caps name line near the top of a resume."""

    opening_text = get_opening_text(text)

    for line in opening_text.splitlines():
        name = clean_name(line)

        if name and name == name.upper() and valid_name(name):
            return name, line.strip(), "High"

    return "", "", "Low"


def detect_name_with_ner(text, nlp):
    """Use NER to find a person name near the top of the resume."""

    if nlp is None:
        return "", "", "Low"

    opening_text = get_opening_text(text)

    # Run NER one line at a time so a name cannot merge with the job title below it.
    for line in opening_text.splitlines():
        document = nlp(line)

        for entity in document.ents:
            if entity.label_ == config.PERSON_ENTITY_LABEL:
                name = clean_name(entity.text)

                if valid_name(name):
                    return name, line.strip(), "High"

    return "", "", "Low"


def create_name_from_file(file_name):
    """Create a readable fallback name from the resume filename."""

    name = file_name.rsplit(config.FILE_NAME_SEPARATOR, 1)[0]
    name = name.replace("_", " ").replace("-", " ")
    name = re.sub(r"\b(resume|cv|curriculum vitae)\b", "", name, flags=re.I)

    return " ".join(name.split()).title()


def extract_email(text):
    """Return the first valid-looking email address in the resume."""

    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return ""


def valid_phone_number(phone_text):
    """Check phone length and reject values that look like year ranges."""

    digits = re.sub(r"\D", "", phone_text)

    if len(digits) < config.MINIMUM_PHONE_DIGITS:
        return False

    if len(digits) > config.MAXIMUM_PHONE_DIGITS:
        return False

    if re.fullmatch(r"\s*\d{4}\s*[-–—]\s*\d{4}\s*", phone_text):
        return False

    return True


def find_phone_in_text(text):
    """Find the first valid-looking contact number in text."""

    pattern = (
        r"(?:\+\d{1,3}[\s.-]*)?"
        r"(?:\(\d{2,4}\)|\d{2,5})"
        r"[\s.-]*\d{3,5}[\s.-]*\d{3,5}"
    )

    for match in re.finditer(pattern, text):
        phone = " ".join(match.group(0).split())

        if valid_phone_number(phone):
            return phone

    return ""


def extract_phone(text):
    """Prefer phone numbers on explicitly labelled contact lines."""

    for line in text.splitlines():
        lower_line = line.lower()

        if any(label in lower_line for label in config.CONTACT_LINE_LABELS):
            phone = find_phone_in_text(line)

            if phone:
                return phone

        segments = [line]

        for separator in config.CONTACT_SEGMENT_SEPARATORS:
            new_segments = []

            for segment in segments:
                new_segments.extend(segment.split(separator))

            segments = new_segments

        for segment in segments:
            phone = find_phone_in_text(segment)

            if phone:
                return phone

    return find_phone_in_text(text)


def extract_candidate_contact(text, file_name, nlp=None):
    """Extract editable identity and contact details from a resume."""

    name, name_evidence, confidence = detect_name_from_header(text)

    if not name:
        name, name_evidence, confidence = detect_name_with_ner(text, nlp)

    if not name:
        name = create_name_from_file(file_name)
        name_evidence = file_name
        confidence = "Low"

    return {
        "name": name,
        "email": extract_email(text),
        "phone": extract_phone(text),
        "name_evidence": name_evidence,
        "name_confidence": confidence,
    }
