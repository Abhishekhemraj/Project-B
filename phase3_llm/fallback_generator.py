from phase3_llm.groq_client import GroqClient

class FallbackGenerator:
    def __init__(self, client: GroqClient):
        self.client = client

    def generate_joke(self, length_class: str, lameness_level: str) -> str:
        """
        Generates a new joke when no local matches are found.
        """
        style_descriptions = {
            "cringe": "highly lame: extremely cheesy, eye-rolling dad joke",
            "average": "moderately lame: mildly clever but corny pun",
            "witty": "decent joke: genuinely funny with a clever punchline"
        }
        style = style_descriptions.get(lameness_level, "mildly funny")

        prompt = (
            f"Generate a brand new joke with the following attributes:\n"
            f"- Length: {length_class}\n"
            f"- Category: {style}\n\n"
            "Constraints:\n"
            "- Return only the text of the joke.\n"
            "- No extra explanation or commentary.\n"
            "- Ensure it fits the category perfectly."
        )



        messages = [
            {"role": "system", "content": "You are a hilarious joke generator."},
            {"role": "user", "content": prompt}
        ]

        try:
            return self.client.chat_completion(messages)
        except Exception as e:
            return f"Error generating joke: {str(e)}"
