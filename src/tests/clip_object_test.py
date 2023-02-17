import pytest

from clip_object import ClipObject


def test_clip_object_init():
    obj = ClipObject("azerty")

    assert obj.get_content() is not None
    assert isinstance(obj.get_content(), str)
    assert obj.get_content() == "azerty"


def test_clip_object_json():
    obj = ClipObject("azerty")

    assert obj.to_json() is not None
    assert isinstance(obj.to_json(), dict)
    assert obj.to_json() == {"content": obj.get_content()}