import config


def normalise_heading(line):
    """Prepare one line for comparison with known section headings."""

    heading = line.strip().lower()
    heading = heading.rstrip(":")

    return heading.strip()


def find_section_name(line):
    """Return the standard section name for a heading line."""

    heading = normalise_heading(line)

    for section_name, alternatives in config.SECTION_HEADINGS.items():
        if heading in alternatives:
            return section_name

    return ""


def find_inline_section(line):
    """Detect a heading and content written on the same line."""

    lower_line = line.lower().strip()

    for section_name, alternatives in config.SECTION_HEADINGS.items():
        for heading in alternatives:
            heading_with_colon = heading + ":"

            if lower_line.startswith(heading_with_colon):
                content = line[len(heading_with_colon):].strip()
                return section_name, content

    return "", ""


def detect_sections(text):
    """Divide resume text into recognised sections."""

    sections = {}
    general_lines = []
    current_section = ""
    detected_headings = []

    for line in text.splitlines():
        clean_line = line.strip()

        if not clean_line:
            continue

        section_name = find_section_name(clean_line)

        if section_name:
            current_section = section_name

            if section_name not in sections:
                sections[section_name] = []

            if section_name not in detected_headings:
                detected_headings.append(section_name)

            continue

        inline_section, inline_content = find_inline_section(clean_line)

        if inline_section:
            current_section = inline_section

            if inline_section not in sections:
                sections[inline_section] = []

            if inline_content:
                sections[inline_section].append(inline_content)

            if inline_section not in detected_headings:
                detected_headings.append(inline_section)

            continue

        if current_section:
            sections[current_section].append(clean_line)
        else:
            general_lines.append(clean_line)

    section_text = {}

    for section_name, lines in sections.items():
        section_text[section_name] = "\n".join(lines)

    if general_lines:
        section_text["general"] = "\n".join(general_lines)

    if not detected_headings:
        section_text = {"general": text.strip()}

    return {
        "sections": section_text,
        "detected_headings": detected_headings,
        "uses_paragraph_analysis": len(detected_headings) == 0,
    }

