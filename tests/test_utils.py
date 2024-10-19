from src.utils import printing


def test_printing(capsys):
    list_vacancies = ["test1", "test2"]
    printing(list_vacancies)
    message = capsys.readouterr().out
    assert message == "test1\ntest2\n"
