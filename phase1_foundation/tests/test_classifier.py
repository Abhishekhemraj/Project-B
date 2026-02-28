from phase1_foundation.classifier import classify_joke

def test_classify_short():
    assert classify_joke("Short.") == "short"

def test_classify_medium():
    medium_joke = "A" * 60
    assert classify_joke(medium_joke) == "medium"

def test_classify_long():
    long_joke = "A" * 160
    assert classify_joke(long_joke) == "long"
