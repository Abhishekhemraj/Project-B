import os
import time
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from groq import Groq, RateLimitError, APIConnectionError

# Load environment variables from .env
load_dotenv()

class GroqClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key or self.api_key == "your_groq_api_key_here":
            # We don't raise error yet to allow for mocking in tests
            pass
        self.client = Groq(api_key=self.api_key)

    def chat_completion(self, messages: List[Dict[str, str]], retries: int = 3, delay: int = 2) -> str:
        """
        Generic chat completion with error handling and retry logic.
        """
        for i in range(retries):
            try:
                response = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    temperature=0.8,
                )
                return response.choices[0].message.content
            except RateLimitError:
                if i == retries - 1:
                    raise
                time.sleep(delay * (i + 1))
            except APIConnectionError:
                if i == retries - 1:
                    raise
                time.sleep(delay)
            except Exception as e:
                # Catch-all for other errors
                raise e
        return ""
