from modules.section_detector import detect_sections


def test_detect_bracketed_txt_headings():
    text = """NISHA REDDY

[ PROFILE ]
React developer

[ SKILL TOOLBOX ]
HTML | CSS | JavaScript

[ PROJECTS ]
Service Booking Portal
"""

    result = detect_sections(text)

    assert result["detected_headings"] == ["summary", "skills", "projects"]
    assert "React developer" in result["sections"]["summary"]
    assert "HTML" in result["sections"]["skills"]
    assert "Service Booking Portal" in result["sections"]["projects"]


def test_ascii_divider_is_not_a_heading():
    result = detect_sections("======\nPlain paragraph only\n------")

    assert result["detected_headings"] == []
    assert result["uses_paragraph_analysis"] is True

