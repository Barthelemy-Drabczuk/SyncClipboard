import pytest

from clip_object import ClipObject


def test_clip_object_init():
    """Test text clipboard object initialization"""
    obj = ClipObject("azerty")

    assert obj.get_content() is not None
    assert isinstance(obj.get_content(), str)
    assert obj.get_content() == "azerty"
    assert obj.get_content_type() == "text"
    assert obj.get_image_data() is None
    assert obj.is_image() is False


def test_clip_object_json():
    """Test text clipboard object JSON serialization"""
    obj = ClipObject("azerty")

    assert obj.to_json() is not None
    assert isinstance(obj.to_json(), dict)
    assert obj.to_json() == {
        "content": "azerty",
        "content_type": "text",
        "image_data": None
    }


def test_clip_object_image():
    """Test image clipboard object initialization"""
    obj = ClipObject("My Image", content_type="image", image_data="base64data")

    assert obj.get_content() == "My Image"
    assert obj.get_content_type() == "image"
    assert obj.get_image_data() == "base64data"
    assert obj.is_image() is True


def test_clip_object_from_image_bytes():
    """Test creating ClipObject from image bytes"""
    image_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'
    obj = ClipObject.from_image_bytes(image_bytes, "PNG")

    assert obj.is_image() is True
    assert obj.get_content() == "Image (PNG)"
    assert obj.get_image_data() is not None
    assert obj.get_image_bytes() == image_bytes
