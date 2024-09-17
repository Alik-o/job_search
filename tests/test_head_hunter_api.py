from unittest.mock import Mock, patch

from src.head_hunter_api import HeadHunterAPI

api = HeadHunterAPI()


def test_vacancies():
    assert api.vacancies == []


@patch("requests.get")
def test_successful_request(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    response = api._get_response()
    assert response == mock_response


@patch("requests.get")
def test_failed_request(mock_get):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    with patch("builtins.print") as mock_print:
        api._get_response()
        mock_print.assert_called_once_with(f"Ошибка при запросе к API. Код ошибки: {mock_response.status_code}")


@patch("requests.get")
def test_get_vacancies(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"items": ["vacancy1", "vacancy2"], "pages": 1}
    mock_get.return_value = mock_response
    keyword = "test_keyword"
    vacancies = api.get_vacancies(keyword)
    assert vacancies == ["vacancy1", "vacancy2"]
