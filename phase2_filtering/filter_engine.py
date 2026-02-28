from typing import List, Dict
from phase1_foundation.data_loader import load_jokes
from phase1_foundation import config
from phase2_filtering.schema import JokeRequest, LengthClass
from phase2_filtering.energy_mapper import get_energy_level

def filter_jokes(request: JokeRequest, data_file: str = config.CSV_FILE_PATH) -> List[Dict[str, str]]:
    """
    Loads jokes using Phase 1 loader and filters by length and energy.
    """
    all_jokes = load_jokes(data_file)
    matches = []
    
    for joke in all_jokes:
        # Filter only by length class now
        if joke["category"] == request.length_class.value:
            matches.append({
                "text": joke["text"],
                "length_class": joke["category"]
            })
            
    return matches
