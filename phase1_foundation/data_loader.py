import csv
import os
from typing import List, Dict
from phase1_foundation.logger import logger
from phase1_foundation.classifier import classify_joke
from phase1_foundation import config

def load_jokes(file_path: str) -> List[Dict[str, str]]:
    """Reads jokes from a CSV file and classifies them."""
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    
    jokes = []
    logger.info(f"Loading jokes from {file_path}...")
    
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                text = row.get(config.COL_TEXT, "")
                if text:
                    category = classify_joke(text)
                    jokes.append({
                        "text": text,
                        "category": category
                    })
        
        logger.info(f"Successfully loaded {len(jokes)} jokes.")
    except Exception as e:
        logger.error(f"Error loading jokes: {str(e)}")
        raise e
        
    return jokes
