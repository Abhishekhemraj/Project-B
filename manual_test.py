import sys
from phase4_integration.main import JokeGeneratorApp

def run_interactive():
    app = JokeGeneratorApp()
    print("========================================")
    print("   AI Joke Generator: Manual Testing    ")
    print("========================================")
    print("Input Options:")
    print("- Length: short, medium, long")
    print("- Energy: low, medium, high")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            length = input("Enter Length Class: ").strip().lower()
            if length in ['exit', 'quit']: break
            
            energy = input("Enter Energy Level: ").strip().lower()
            if energy in ['exit', 'quit']: break

            print("\n--- Processing ---\n")
            result = app.get_joke(length, energy)
            print(result)
            print("\n" + "="*40 + "\n")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_interactive()
