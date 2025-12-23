import pytest
from unittest.mock import Mock, patch, MagicMock

from db_management import MongoCRUD
from clip_user import ClipUser
from clip_object import ClipObject


@pytest.fixture
def mock_mongo():
    """Mock MongoDB client"""
    with patch('db_management.MongoClient') as mock:
        mock_client = MagicMock()
        mock.return_value = mock_client
        yield mock_client


def test_insert_user(mock_mongo):
    """Test inserting a user into the database"""
    my_db = MongoCRUD()
    my_user = ClipUser("JohnDoe", "badpassword", "email@email.fr")

    result = my_db.insert_user(my_user)

    assert result == my_db
    my_db.users.insert_one.assert_called_once()


def test_insert_transaction(mock_mongo):
    """Test inserting a clipboard transaction"""
    my_db = MongoCRUD()
    clip_obj = ClipObject("test content")
    user_id = 12345

    result = my_db.insert_transaction(user_id, clip_obj)

    assert result == my_db
    my_db.transactions.insert_one.assert_called_once()


def test_get_user(mock_mongo):
    """Test getting a user by username and password"""
    my_db = MongoCRUD()
    user_data = {
        "username": "JohnDoe",
        "password": hash("badpassword"),
        "email": "email@email.fr"
    }
    my_db.users.find_one.return_value = user_data

    result = my_db.get_user("JohnDoe", "badpassword")

    assert result is not None
    assert isinstance(result, ClipUser)
    assert result.get_username() == "JohnDoe"


def test_get_user_not_found(mock_mongo):
    """Test getting a user that doesn't exist"""
    my_db = MongoCRUD()
    my_db.users.find_one.return_value = None

    result = my_db.get_user("NonExistent", "password")

    assert result is None


def test_get_n_last_user_transaction(mock_mongo):
    """Test getting last N transactions for a user"""
    my_db = MongoCRUD()
    mock_transactions = [
        {"content": "item1", "timestamp": 1234567890},
        {"content": "item2", "timestamp": 1234567891}
    ]
    mock_cursor = MagicMock()
    mock_cursor.sort.return_value.limit.return_value = mock_transactions
    my_db.transactions.find.return_value = mock_cursor

    result = my_db.get_n_last_user_transaction(12345, 2)

    assert len(result) == 2
    my_db.transactions.find.assert_called_once_with({"user_id": 12345})