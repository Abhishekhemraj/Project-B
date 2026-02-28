from unittest.mock import MagicMock
from phase3_llm.groq_client import GroqClient
from phase3_llm.ranking_service import RankingService
from phase3_llm.fallback_generator import FallbackGenerator

def main():
    print("--- Phase 3: Groq API Integration Demo (Mocked) ---")
    
    # Initialize client and mock the internal groq client
    client = GroqClient(api_key="mock-key")
    client.client = MagicMock()
    
    # 1. Ranking Demo
    print("\n[Ranking Demo]")
    ranking_service = RankingService(client)
    
    # Mock response for selecting ID 1
    mock_rank_response = MagicMock()
    mock_rank_response.choices[0].message.content = "1"
    client.client.chat.completions.create.return_value = mock_rank_response
    
    jokes = [
        {"text": "Local Joke A", "category": "short"},
        {"text": "Local Joke B", "category": "medium"}
    ]
    query_info = {"length_class": "medium", "energy_level": "low"}
    
    selected = ranking_service.select_best_joke(jokes, query_info)
    print(f"Input Jokes: {len(jokes)}")
    print(f"Groq Selected: {selected.get('text')}")

    # 2. Fallback Generation Demo
    print("\n[Fallback Generation Demo]")
    generator = FallbackGenerator(client)
    
    # Mock response for generating a joke
    mock_gen_response = MagicMock()
    mock_gen_response.choices[0].message.content = "Why did the computer go to the doctor? Because it had a virus!"
    client.client.chat.completions.create.return_value = mock_gen_response
    
    generated_joke = generator.generate_joke("short", "high")
    print(f"Query: short, high")
    print(f"Groq Generated: {generated_joke}")

if __name__ == "__main__":
    main()
