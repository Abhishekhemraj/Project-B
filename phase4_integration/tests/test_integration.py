import json
import pytest
from unittest.mock import MagicMock, patch
from phase4_integration.main import JokeGeneratorApp

@pytest.fixture
def app():
    with patch('phase3_llm.groq_client.GroqClient') as MockClient:
        instance = MockClient.return_value
        instance.chat_completion.return_value = "Mocked Response"
        return JokeGeneratorApp()

def test_full_flow_local_match(app):
    # Mock filter_jokes to return something
    mock_joke = {"text": "Local Joke", "category": "short"}
    with patch('phase4_integration.main.filter_jokes', return_value=[mock_joke]):
        # Mock ranking to select the first one
        with patch.object(app.ranking_service, 'select_best_joke', return_value=mock_joke):
            response_json = app.get_joke("short", "witty")
            response = json.loads(response_json)
            
            assert response["status"] == "success"
            assert response["joke"]["text"] == "Local Joke"
            assert response["meta"]["source"] == "local_ranked"

def test_full_flow_fallback(app):
    # Mock filter_jokes to return empty list
    with patch('phase4_integration.main.filter_jokes', return_value=[]):
        # Mock generation
        with patch.object(app.fallback_generator, 'generate_joke', return_value="Generated Content"):
            response_json = app.get_joke("medium", "cringe")
            response = json.loads(response_json)
            
            assert response["status"] == "success"
            assert response["joke"]["text"] == "Generated Content"
            assert response["meta"]["source"] == "generated"

def test_full_flow_invalid_input(app):
    response_json = app.get_joke("extra-large", "average")
    response = json.loads(response_json)
    
    assert response["status"] == "error"
    assert "error" in response
