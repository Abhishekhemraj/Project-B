import json
from typing import List, Dict
from phase3_llm.groq_client import GroqClient

class RankingService:
    def __init__(self, client: GroqClient):
        self.client = client

    def select_best_joke(self, jokes: List[Dict[str, str]], query_info: Dict[str, str]) -> Dict[str, str]:
        """
        Sends top N jokes to Groq and asks it to select the best one.
        """
        if not jokes:
            return {}

        joke_texts = [f"ID {i}: {j['text']}" for i, j in enumerate(jokes)]
        prompt = (
            f"I have a list of jokes. Please select the BEST one that fits the following criteria:\n"
            f"Length Class: {query_info.get('length_class')}\n"
            f"Lameness Level: {query_info.get('lameness_level')}\n\n"
            "Criteria Definitions:\n"
            "- Witty: Clever, sharp, well-structured humor.\n"
            "- Average: Standard humor, broadly appealing.\n"
            "- Cringe: Weaponized dad jokes, puns so bad they are 'good', or pure cringe.\n\n"
            "Jokes:\n" + "\n".join(joke_texts) + "\n\n"
            "Respond ONLY with the ID number of the joke you selected."
        )

        messages = [
            {"role": "system", "content": "You are a comedy judge specializing in matching jokes to audience energy levels."},
            {"role": "user", "content": prompt}
        ]

        try:
            response = self.client.chat_completion(messages)
            # Simple parsing for the ID
            selected_id = int(''.join(filter(str.isdigit, response)))
            if 0 <= selected_id < len(jokes):
                return jokes[selected_id]
        except Exception:
            # Fallback to first joke if ranking fails
            return jokes[0]
            
        return jokes[0]
