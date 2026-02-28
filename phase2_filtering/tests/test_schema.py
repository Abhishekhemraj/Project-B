import pytest
from pydantic import ValidationError
from phase2_filtering.schema import JokeRequest, LengthClass, LamenessLevel

def test_valid_request():
    req = JokeRequest(length_class="short", lameness_level="witty")
    assert req.length_class == LengthClass.SHORT
    assert req.lameness_level == LamenessLevel.WITTY

def test_invalid_length():
    with pytest.raises(ValidationError):
        JokeRequest(length_class="extra-long", lameness_level="average")

def test_invalid_lameness_level():
    with pytest.raises(ValidationError):
        JokeRequest(length_class="short", lameness_level="super-lame")
