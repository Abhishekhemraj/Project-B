from phase2_filtering.schema import JokeRequest, LengthClass, LamenessLevel
from phase2_filtering.filter_engine import filter_jokes

def main():
    print("--- Phase 2: Filtering Demo (Updated) ---")
    
    queries = [
        JokeRequest(length_class=LengthClass.SHORT, lameness_level=LamenessLevel.WITTY),
        JokeRequest(length_class=LengthClass.MEDIUM, lameness_level=LamenessLevel.AVERAGE),
        JokeRequest(length_class=LengthClass.LONG, lameness_level=LamenessLevel.CRINGE),
    ]

    for req in queries:
        print(f"\nQuery: Length={req.length_class.value}, Lameness={req.lameness_level.value}")
        matches = filter_jokes(req)
        print(f"Match count: {len(matches)}")
        for m in matches[:3]:
            print(f"  - {m['text'][:60]}...")

if __name__ == "__main__":
    main()
