from typing import List, Dict
from phase1_foundation.data_loader import load_jokes
from phase1_foundation import config
from phase2_filtering.schema import JokeRequest, LengthClass, LamenessLevel
from phase2_filtering.energy_mapper import get_energy_level

def filter_jokes(request: JokeRequest, data_file: str = config.CSV_FILE_PATH) -> List[Dict[str, str]]:
    """
    Loads jokes using Phase 1 loader and filters by length and lame score.
    """
    all_jokes = load_jokes(data_file)
    matches = []
    
    # Mapping for local CSV filtering
    # Highly Lame (cringe) = 3, Moderately Lame (average) = 2, Decent Joke (witty) = 1
    lame_score_map = {
        LamenessLevel.CRINGE: 3,
        LamenessLevel.AVERAGE: 2,
        LamenessLevel.WITTY: 1
    }
    target_score = lame_score_map.get(request.lameness_level)

    for joke in all_jokes:
        if joke["category"] == request.length_class.value and joke.get("lame_score") == target_score:
            matches.append({
                "text": joke["text"],
                "length_class": joke["category"],
                "lame_score": joke["lame_score"]
            })
            
    return matches


