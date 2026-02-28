import pytest
from unittest.mock import MagicMock, patch
from phase3_llm.groq_client import GroqClient, RateLimitError, APIConnectionError
from phase3_llm.ranking_service import RankingService
from phase3_llm.fallback_generator import FallbackGenerator

@pytest.fixture
def mock_groq_client():
    client = GroqClient(api_key="mock-key")
    client.client = MagicMock()
    return client

def test_ranking_path(mock_groq_client):
    # Setup mock response for ranking (returning ID 1)
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "1"
    mock_groq_client.client.chat.completions.create.return_value = mock_response

    ranking_service = RankingService(mock_groq_client)
    jokes = [
        {"text": "Joke 0", "category": "short"},
        {"text": "Joke 1", "category": "medium"}
    ]
    query_info = {"length_class": "medium", "energy_level": "low"}
    
    selected = ranking_service.select_best_joke(jokes, query_info)
    assert selected["text"] == "Joke 1"

def test_fallback_path(mock_groq_client):
    # Setup mock response for generating a joke
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "This is a generated joke."
    mock_groq_client.client.chat.completions.create.return_value = mock_response

    generator = FallbackGenerator(mock_groq_client)
    joke = generator.generate_joke("short", "high")
    assert joke == "This is a generated joke."

def test_groq_client_retry_on_ratelimit(mock_groq_client):
    # Mock RateLimitError for first call, success on second
    mock_groq_client.client.chat.completions.create.side_effect = [
        RateLimitError("Limit reached", response=MagicMock(), body={}),
        MagicMock(choices=[MagicMock(message=MagicMock(content="Success"))])
    ]

    # Use short delay for test
    with patch('time.sleep', return_value=None):
        content = mock_groq_client.chat_completion([{"role": "user", "content": "test"}])
    
    assert content == "Success"
    assert mock_groq_client.client.chat.completions.create.call_count == 2

def test_groq_client_connection_error_handling(mock_groq_client):
    # Mock connection error
    mock_groq_client.client.chat.completions.create.side_effect = APIConnectionError(
        message="Conn failed", request=MagicMock()
    )

    with patch('time.sleep', return_value=None):
        with pytest.raises(APIConnectionError):
            mock_groq_client.chat_completion([{"role": "user", "content": "test"}])
