import sys
import random
from phase2_filtering.schema import JokeRequest, LengthClass
from phase2_filtering.filter_engine import filter_jokes
from phase3_llm.groq_client import GroqClient
from phase3_llm.ranking_service import RankingService
from phase3_llm.fallback_generator import FallbackGenerator
from phase4_integration.formatter import ResponseFormatter
from phase1_foundation.logger import logger

class JokeGeneratorApp:
    def __init__(self):
        self.groq_client = GroqClient()
        self.ranking_service = RankingService(self.groq_client)
        self.fallback_generator = FallbackGenerator(self.groq_client)
        self.formatter = ResponseFormatter()

    def get_joke(self, length: str, lameness: str = "average") -> str:
        """
        Main execution flow:
        1. Validate Input
        2. Filter Local
        3. Rank or Generate
        4. Format Output
        """
        try:
            # 1. Validate Input
            request = JokeRequest(length_class=length, lameness_level=lameness)
            logger.info(f"Processing request: {request}")

            # 2. Filter Local Dataset
            local_matches = filter_jokes(request)
            
            if local_matches:
                # Randomly sample 10 jokes from the matches to provide variety
                sample_size = min(10, len(local_matches))
                top_matches = random.sample(local_matches, sample_size)
                logger.info(f"Found {len(local_matches)} local matches. Ranking a random sample of {sample_size} with Groq...")
                
                # 3a. Rank with Groq
                selected_joke = self.ranking_service.select_best_joke(
                    top_matches, 
                    {
                        "length_class": length, 
                        "lameness_level": lameness
                    }
                )
                selected_joke["lameness_level"] = lameness
                return self.formatter.format_joke_response(selected_joke, source="local_ranked")
            
            else:
                logger.info("No local matches found. Triggering Fallback Generator...")
                # 3b. Generate with Groq
                generated_text = self.fallback_generator.generate_joke(length, lameness)
                
                joke_data = {
                    "text": generated_text,
                    "length_class": length,
                    "lameness_level": lameness
                }
                return self.formatter.format_joke_response(joke_data, source="generated")

        except Exception as e:
            logger.error(f"Application error: {str(e)}")
            return self.formatter.format_error_response(str(e))

if __name__ == "__main__":
    app = JokeGeneratorApp()
    # Basic CLI usage for testing
    if len(sys.argv) > 2:
        print(app.get_joke(sys.argv[1], sys.argv[2]))
    else:
        print("Usage: python -m phase4_integration.main <length> <lameness>")
