import csv
import re

import config


def normalise_skill(skill):
    """Prepare a skill name for consistent comparison."""

    return " ".join(skill.lower().strip().split())


def load_skill_aliases():
    """Load skill aliases from the configured CSV file."""

    aliases = {}

    if not config.SKILL_ALIASES_FILE.exists():
        return aliases

    with open(config.SKILL_ALIASES_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            alias = normalise_skill(row.get("alias", ""))
            standard_skill = normalise_skill(row.get("standard_skill", ""))

            if alias and standard_skill:
                aliases[alias] = standard_skill

    return aliases


def get_skill_names(skill, aliases):
    """Return the standard skill and any aliases that represent it."""

    normal_skill = normalise_skill(skill)
    standard_skill = aliases.get(normal_skill, normal_skill)
    skill_names = [standard_skill]

    for alias, alias_standard_skill in aliases.items():
        if alias_standard_skill == standard_skill and alias not in skill_names:
            skill_names.append(alias)

    if normal_skill not in skill_names:
        skill_names.append(normal_skill)

    return skill_names


def text_contains_skill(text, skill_name):
    """Check for a complete skill name rather than a partial word match."""

    normal_skill_name = normalise_skill(skill_name)
    escaped_skill = re.escape(normal_skill_name)
    pattern = r"(?<!\w)" + escaped_skill + r"(?!\w)"

    return re.search(pattern, text.lower()) is not None


def split_evidence_lines(text):
    """Divide resume text into short lines for explainable evidence."""

    evidence_text = text

    for separator in config.EVIDENCE_SENTENCE_SEPARATORS:
        evidence_text = evidence_text.replace(separator, "\n")

    evidence_lines = []

    for line in evidence_text.splitlines():
        clean_line = line.strip()

        if clean_line:
            evidence_lines.append(clean_line)

    return evidence_lines


def find_skill_evidence(text, skill_names):
    """Return the first resume line that contains the skill or an alias."""

    for line in split_evidence_lines(text):
        for skill_name in skill_names:
            if text_contains_skill(line, skill_name):
                return line

    return ""


def match_skill_list(skills, resume_text, aliases):
    """Match one list of job skills and collect evidence."""

    matched_skills = []
    missing_skills = []
    evidence = []

    for skill in skills:
        skill_names = get_skill_names(skill, aliases)
        evidence_line = find_skill_evidence(resume_text, skill_names)

        if evidence_line:
            matched_skills.append(skill)
            evidence.append({"skill": skill, "evidence": evidence_line})
        else:
            missing_skills.append(skill)

    if len(skills) == 0:
        percentage = 0
    else:
        percentage = len(matched_skills) / len(skills) * config.PERCENT_DIVISOR

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "evidence": evidence,
        "percentage": round(percentage, 2),
    }


def match_job_skills(required_skills, preferred_skills, resume_text):
    """Match required and preferred job skills against the resume."""

    aliases = load_skill_aliases()
    required_result = match_skill_list(required_skills, resume_text, aliases)
    preferred_result = match_skill_list(preferred_skills, resume_text, aliases)

    return {
        "required": required_result,
        "preferred": preferred_result,
    }
