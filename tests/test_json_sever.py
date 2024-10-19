import json
import os

from config import TEST_DIR
from src.json_saver import JSONSaver


def test_check_dir():
    file_path = os.path.join(TEST_DIR, "test_file.json")
    os.remove(file_path)
    assert not os.path.exists(file_path)
    json_saver = JSONSaver(file_path)
    assert os.path.exists(json_saver.file_path)


def test_add_vacancies():
    file_path = os.path.join(TEST_DIR, "test_file.json")
    json_saver = JSONSaver(file_path)
    json_saver.add_vacancies(
        [
            {
                "name": "Test Vacancy 1",
                "url": "https://example.com",
                "salary": {"from": 10000, "to": 20000, "currency": "RUR"},
                "area": "Area 1",
                "description": "Description 1",
            },
        ]
    )
    with open(file_path, "r", encoding="utf-8") as file:
        result_obtained = json.load(file)
    assert result_obtained == [
        {
            "name": "Test Vacancy 1",
            "url": "https://example.com",
            "salary": {"from": 10000, "to": 20000, "currency": "RUR"},
            "area": "Area 1",
            "description": "Description 1",
        },
    ]

    json_saver.add_vacancies(
        [
            {
                "name": "Test Vacancy 1",
                "url": "https://example.com",
                "salary": {"from": 10000, "to": 20000, "currency": "RUR"},
                "area": "Area 1",
                "description": "Description 1",
            },
            {
                "name": "Test Vacancy 2",
                "url": "https://example2.com",
                "salary": {"from": 10000, "to": 15000, "currency": "RUR"},
                "area": "Area 2",
                "description": "Description 2",
            },
        ]
    )
    with open(file_path, "r", encoding="utf-8") as file:
        result_obtained = json.load(file)
    assert result_obtained == [
        {
            "name": "Test Vacancy 1",
            "url": "https://example.com",
            "salary": {"from": 10000, "to": 20000, "currency": "RUR"},
            "area": "Area 1",
            "description": "Description 1",
        },
        {
            "name": "Test Vacancy 2",
            "url": "https://example2.com",
            "salary": {"from": 10000, "to": 15000, "currency": "RUR"},
            "area": "Area 2",
            "description": "Description 2",
        },
    ]


def testt_clear_file():
    file_path = os.path.join(TEST_DIR, "test_file.json")
    json_saver = JSONSaver(file_path)
    assert os.path.getsize(file_path) > 0
    json_saver.clear_file()
    assert os.path.getsize(file_path) == 0
