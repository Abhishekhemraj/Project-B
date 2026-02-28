import os
from phase3_llm.groq_client import GroqClient
from phase3_llm.fallback_generator import FallbackGenerator

def test_real_connection():
    print("Testing real Groq API connection...")
    client = GroqClient()
    if not client.api_key:
        print("FAILED: No API key found in environment.")
        return

    generator = FallbackGenerator(client)
    try:
        joke = generator.generate_joke("short", "low")
        print("\nSUCCESS! Groq generated a joke:")
        print(f"Joke: {joke}")
    except Exception as e:
        print(f"\nFAILED: Error calling Groq API: {e}")

if __name__ == "__main__":
    test_real_connection()
