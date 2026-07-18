from modules.csv_manager import convert_list_to_text


def test_convert_list_to_text():
    skills = ["Python", "SQL", "Git"]

    result = convert_list_to_text(skills)

    assert result == "Python; SQL; Git"


def test_convert_empty_list_to_text():
    result = convert_list_to_text([])

    assert result == ""

