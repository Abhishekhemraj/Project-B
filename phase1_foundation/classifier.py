from phase1_foundation import config

def classify_joke(joke_text: str) -> str:
    """Classifies a joke based on character count."""
    length = len(joke_text)
    
    if length < config.SHORT_THRESHOLD:
        return "short"
    elif length < config.MEDIUM_THRESHOLD:
        return "medium"
    else:
        return "long"
