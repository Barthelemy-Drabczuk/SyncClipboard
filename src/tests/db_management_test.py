import pytest

from db_management import MongoCRUD
from clip_user import ClipUser

def test_insert_user():
    my_db = MongoCRUD()
    my_user = ClipUser("JhonDoe", "badpassword", "email@email.fr")

    my_db.insert_user(my_user.to_json())

    assert len(list(my_db.get_db().users.values.find({"username": "JhonDoe"}))) > 0