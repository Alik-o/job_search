from src.vacancy import Vacancy


def test_vacancy_init():
    name = "Test Vacancy"
    url = "https://example.com"
    salary = {"from": 1000, "to": 2000, "currency": "USD"}
    area = "New York"
    description = "Test description"

    vacancy = Vacancy(name, url, salary, area, description)
    assert vacancy.name == name
    assert vacancy.url == url
    assert vacancy.salary == salary
    assert vacancy.area == area
    assert vacancy.description == description


def test_gt_true():
    vacancy1 = Vacancy("name", "url", {"from": 10000, "to": 20000, "currency": "RUR"}, "area", "description")
    vacancy2 = Vacancy("name", "url", {"from": 10000, "to": 15000, "currency": "RUR"}, "area", "description")
    assert vacancy1 > vacancy2


def test_none_from():
    vacancy = Vacancy("name", "url", {"from": None, "to": 20000, "currency": "RUR"}, "area", "description")
    assert vacancy.salary == {"from": 0, "to": 20000, "currency": "RUR"}


def test_none_to():
    vacancy = Vacancy("name", "url", {"from": 100000, "to": None, "currency": "RUR"}, "area", "description")
    assert vacancy.salary == {"from": 100000, "to": 100000, "currency": "RUR"}


def test_vacancy_to_dict():
    vacancy1 = Vacancy(
        "Test Vacancy 1",
        "https://example.com",
        {"from": 10000, "to": 20000, "currency": "RUR"},
        "Area 1",
        "Description 1",
    )
    vacancy2 = Vacancy(
        "Test Vacancy 2",
        "https://example.com",
        {"from": 10000, "to": 15000, "currency": "RUR"},
        "Area 2",
        "Description 2",
    )
    expected_output = [
        {
            "name": "Test Vacancy 1",
            "url": "https://example.com",
            "salary": {"from": 10000, "to": 20000, "currency": "RUR"},
            "area": "Area 1",
            "description": "Description 1",
        },
        {
            "name": "Test Vacancy 2",
            "url": "https://example.com",
            "salary": {"from": 10000, "to": 15000, "currency": "RUR"},
            "area": "Area 2",
            "description": "Description 2",
        },
    ]
    assert Vacancy.to_dict([vacancy1, vacancy2]) == expected_output


def test_vacancy_description_tags():
    vacancy = Vacancy(
        "Test Vacancy",
        "https://example.com",
        {"from": 10000, "to": 20000, "currency": "RUR"},
        "Area",
        "<highlighttext>Description</highlighttext>",
    )
    expected_output = [
        {
            "name": "Test Vacancy",
            "url": "https://example.com",
            "salary": {"from": 10000, "to": 20000, "currency": "RUR"},
            "area": "Area",
            "description": "Description",
        }
    ]
    assert Vacancy.to_dict([vacancy]) == expected_output


def test_vacancy_description_none():
    vacancy = Vacancy(
        "Test Vacancy", "https://example.com", {"from": 10000, "to": 20000, "currency": "RUR"}, "Area", None
    )
    expected_output = [
        {
            "name": "Test Vacancy",
            "url": "https://example.com",
            "salary": {"from": 10000, "to": 20000, "currency": "RUR"},
            "area": "Area",
            "description": None,
        }
    ]
    assert Vacancy.to_dict([vacancy]) == expected_output
