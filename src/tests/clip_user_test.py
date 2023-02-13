import pytest

from clip_user import ClipUser


def init_user() -> tuple[ClipUser, list[str, str, str]]:
    params: list[str, str, str] = ["JohnDoe", "badpassword", "emaill@email.fr"]
    return (ClipUser(params[0], params[1], params[2]), params)


def test_user_init():
    usr, params = init_user()

    assert usr is not None
    assert isinstance(usr, ClipUser)
    assert usr.get_username() == params[0]
    assert usr.get_password() == hash(params[1])
    assert usr.get_email() == params[2]
    assert usr.get_id() == hash( params[0] + str(hash(params[1])) + params[2] )

def test_user_to_json():
    usr, params = init_user()

    assert usr.to_json() is not None
    assert isinstance(usr.to_json(), dict)
    assert usr.to_json() == {
        "id": usr.get_id(),
        "username": usr.get_username(),
        "password": usr.get_password(),
        "email": usr.get_email()
    }


def test_user_str():
    usr, params = init_user()

    assert str(usr) == str(usr.to_json())

