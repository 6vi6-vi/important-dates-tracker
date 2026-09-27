from models import User
from models.users import User as UserClass


def test_user_creation():
    user = User(1, "Иван Петров", "ivan@example.com")
    assert user.id == 1
    assert user.name == "Иван Петров"
    assert user.email == "ivan@example.com"


def test_user_from_data():
    user = UserClass.from_data(
        {"id": 1, "name": "Иван Петров", "email": "ivan@example.com"}
    )
    assert user.id == 1
    assert user.name == "Иван Петров"


def test_user_matches():
    user = User(1, "Иван Петров", "ivan@example.com")
    assert user.matches("иван")
    assert user.matches("example")
