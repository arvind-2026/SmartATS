import re

import config


def clean_line(line):
    """Clean spacing in one line while preserving useful skill symbols."""

    line = line.replace("\t", " ")
    line = line.replace("\u00a0", " ")
    line = line.replace("•", "-")
    line = line.replace("●", "-")
    line = line.replace("▪", "-")
    line = re.sub(r" +", " ", line)

    return line.strip()


def clean_resume_text(text):
    """Clean extracted resume text without removing important line breaks."""

    if text is None:
        return ""

    text = text.replace("\x00", "")
    source_lines = text.splitlines()
    clean_lines = []
    blank_line_count = 0

    for line in source_lines:
        line = clean_line(line)

        if line:
            clean_lines.append(line)
            blank_line_count = 0
        else:
            blank_line_count += 1

            if blank_line_count <= config.MAXIMUM_BLANK_LINES:
                clean_lines.append("")

    return "\n".join(clean_lines).strip()


def create_analysis_text(text):
    """Create a single-spaced text version for later AI matching."""

    clean_text = clean_resume_text(text)
    analysis_text = clean_text.replace("\n", " ")
    analysis_text = re.sub(r" +", " ", analysis_text)

    return analysis_text.strip()

