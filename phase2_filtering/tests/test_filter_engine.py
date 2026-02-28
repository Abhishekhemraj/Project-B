import pytest
from phase2_filtering.schema import JokeRequest, LengthClass, LamenessLevel
from phase2_filtering.filter_engine import filter_jokes
from pydantic import ValidationError

def test_filter_logic_structure():
    # Since filter_jokes loads from config.CSV_FILE_PATH, 
    # and we updated the file, we can test it returns something.
    req = JokeRequest(length_class=LengthClass.SHORT, lameness_level=LamenessLevel.WITTY)
    results = filter_jokes(req)
    assert isinstance(results, list)
    if results:
        assert "text" in results[0]
        assert "length_class" in results[0]
        assert "lame_score" in results[0]

def test_pydantic_validation():
    with pytest.raises(ValidationError):
        JokeRequest(length_class="invalid", lameness_level="witty")
