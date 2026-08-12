import os
# Set a dummy API key for testing so it doesn't fail the 500 API key check
os.environ["GEMINI_API_KEY"] = "dummy_key_for_testing"

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# We will mock the Gemini API call to prevent actual network calls during testing
@pytest.fixture(autouse=True)
def mock_gemini(mocker):
    # Mocking genai.GenerativeModel.generate_content
    mock_model = mocker.patch("main.model")
    mock_response = mocker.MagicMock()
    mock_response.text = "Mocked response from Gemini"
    mock_model.generate_content.return_value = mock_response
    return mock_model

def test_analyze_endpoint(mock_gemini):
    response = client.post("/analyze", json={"text": "Test text to analyze"})
    assert response.status_code == 200
    assert response.json() == {"result": "Mocked response from Gemini"}
    mock_gemini.generate_content.assert_called_once()

def test_summarize_endpoint(mock_gemini):
    response = client.post("/summarize", json={"text": "Test text to summarize"})
    assert response.status_code == 200
    assert response.json() == {"result": "Mocked response from Gemini"}
    mock_gemini.generate_content.assert_called_once()

def test_classify_endpoint(mock_gemini):
    response = client.post("/classify", json={"text": "Test text to classify"})
    assert response.status_code == 200
    assert response.json() == {"result": "Mocked response from Gemini"}
    mock_gemini.generate_content.assert_called_once()
