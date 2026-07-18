from modules.section_detector import detect_sections


def test_detect_common_sections():
    text = """SUMMARY
Python developer
SKILLS
Python, SQL, Git
PROJECTS
Resume screening system
EDUCATION
B.Tech in Computer Science"""

    result = detect_sections(text)

    assert result["sections"]["skills"] == "Python, SQL, Git"
    assert "projects" in result["detected_headings"]
    assert result["uses_paragraph_analysis"] is False


def test_detect_inline_skill_heading():
    result = detect_sections("Skills: Python, SQL, Git")

    assert result["sections"]["skills"] == "Python, SQL, Git"


def test_paragraph_resume_uses_general_section():
    text = "I developed Python applications and worked with SQL databases."
    result = detect_sections(text)

    assert result["uses_paragraph_analysis"] is True
    assert result["sections"]["general"] == text


def test_detect_additional_resume_sections():
    text = """INTERESTS
Artificial Intelligence
STRENGTHS
Problem solving
LANGUAGES
English and Hindi
ACHIEVEMENTS
Won a coding competition"""

    result = detect_sections(text)

    assert result["sections"]["interests"] == "Artificial Intelligence"
    assert result["sections"]["strengths"] == "Problem solving"
    assert result["sections"]["languages"] == "English and Hindi"
    assert result["sections"]["achievements"] == "Won a coding competition"
