from phase1_foundation.data_loader import load_jokes
from phase1_foundation import config

def main():
    print("--- Phase 1: Foundation & Core Dataset Demo ---")
    try:
        jokes = load_jokes(config.CSV_FILE_PATH)
        print(f"\nTotal jokes loaded: {len(jokes)}")
        
        print("\nSample Classifications:")
        for joke in jokes[:5]:
            print(f"- Category: [{joke['category']:<6}] | Text: {joke['text'][:50]}...")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
