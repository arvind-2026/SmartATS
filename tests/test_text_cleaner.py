from modules.text_cleaner import clean_resume_text
from modules.text_cleaner import create_analysis_text


def test_clean_repeated_spaces():
    result = clean_resume_text("Python     SQL")

    assert result == "Python SQL"


def test_preserve_skill_symbols():
    result = clean_resume_text("C++  C#  .NET")

    assert result == "C++ C# .NET"


def test_replace_bullet_character():
    result = clean_resume_text("• Python")

    assert result == "- Python"


def test_create_single_line_analysis_text():
    result = create_analysis_text("Python\nSQL\nGit")

    assert result == "Python SQL Git"

