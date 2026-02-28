import json
import os
import sys
import time
from phase4_integration.main import JokeGeneratorApp
from phase1_foundation.logger import logger
import logging

# Disable logging to keep the UI clean for the user
logging.getLogger('joke_generator').setLevel(logging.WARNING)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print("""
    ┌──────────────────────────────────────────────────┐
    │                                                  │
    │           🌟  AI JOKE GENERATOR v1.0  🌟           │
    │         Experience the Future of Comedy          │
    │                                                  │
    └──────────────────────────────────────────────────┘
    """)

def get_user_choice(prompt, options):
    while True:
        print(f"\n{prompt}")
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt.capitalize()}")
        
        choice = input("\nSelect an option (1-3) or 'q' to quit: ").strip().lower()
        
        if choice == 'q':
            return None
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return options[idx]
        
        print("❌ Invalid selection. Please try again.")

def main():
    app = JokeGeneratorApp()
    
    while True:
        clear_screen()
        print_banner()
        
        # User selections
        length = get_user_choice("What kind of joke are you looking for?", ["short", "medium", "long"])
        if not length: break
        
        lameness = get_user_choice("How 'lame' should it be?", ["witty", "average", "cringe"])
        if not lameness: break
        
        clear_screen()
        print_banner()
        print(f"\n✨ Brewing a {length} joke with {lameness} humor...")
        
        # Get joke
        response_json = app.get_joke(length, lameness)
        data = json.loads(response_json)
        
        if data["status"] == "success":
            joke = data["joke"]
            meta = data["meta"]
            
            print("\n" + "─" * 50)
            print("\n    " + joke["text"].replace("\n", "\n    "))
            print("\n" + "─" * 50)
            
            source_tag = "📚 LOCAL FAVORITE" if meta["source"] == "local_ranked" else "🤖 AI GENERATED"
            print(f"\n[ {source_tag} ]")
            print(f"📏 Length: {joke['length_class'].capitalize()} | 🥴 Lameness: {joke['lameness_level'].capitalize()}")
        else:
            print(f"\n❌ Oops! Something went wrong: {data['error']['message']}")
        
        input("\nPress Enter to get another joke...")

    clear_screen()
    print_banner()
    print("\n    Thanks for laughing with us! Goodbye! 👋\n")

if __name__ == "__main__":
    main()
