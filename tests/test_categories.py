from models import Category


def test_category_creation():
    category = Category(1, "День рождения")
    assert category.id == 1
    assert category.name == "День рождения"


def test_category_matches():
    category = Category(1, "День рождения")
    assert category.matches("рождения")
    assert not category.matches("работа")
