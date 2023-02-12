import pytest

from webapp import Webapp, ClipUser

def test_get_user():
    webapp = Webapp()
    my_user: ClipUser = webapp.get_user(1)

    assert isinstance(my_user, ClipUser)
    assert my_user.get_id() == 1
    assert isinstance(my_user.get_username(), str)
    assert isinstance(my_user.get_password(), str)
    assert len(my_user.get_password()) == 64