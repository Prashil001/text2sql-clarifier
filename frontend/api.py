"""API client for the Text2SQL Clarifier backend."""

import os
import requests
from typing import Any

# Constants — configurable via BACKEND_URL env var for Docker
BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
QUERY_ENDPOINT = f"{BASE_URL}/query"
HEALTH_ENDPOINT = f"{BASE_URL}/docs"
TIMEOUT_SECONDS = 120


def check_backend_health() -> bool:
    """Check if the backend API is reachable.
    
    Returns:
        True if the backend responds, False otherwise.
    """
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=5)
        return response.status_code == 200
    except (requests.ConnectionError, requests.Timeout):
        return False


def send_query(question: str) -> dict[str, Any]:
    """Send a natural language question to the Text2SQL backend.
    
    Args:
        question: The natural language question to convert to SQL.
        
    Returns:
        The parsed JSON response from the backend.
        
    Raises:
        ConnectionError: If the backend is unreachable.
        TimeoutError: If the request times out.
        ValueError: If the response contains invalid JSON.
        RuntimeError: For HTTP errors with detail messages.
    """
    try:
        response = requests.post(
            QUERY_ENDPOINT,
            json={"question": question},
            timeout=TIMEOUT_SECONDS,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 400:
            error_detail = response.json().get("detail", "Unknown validation error")
            raise RuntimeError(f"Query validation failed: {error_detail}")
        
        if response.status_code == 422:
            raise RuntimeError("Invalid request format. Please rephrase your question.")
            
        response.raise_for_status()
        return response.json()
        
    except requests.ConnectionError:
        raise ConnectionError(
            "Cannot connect to the backend. Please ensure the FastAPI server is running "
            "at http://127.0.0.1:8000"
        )
    except requests.Timeout:
        raise TimeoutError(
            "The request timed out. The AI model may be processing a complex query. "
            "Please try again."
        )
    except requests.JSONDecodeError:
        raise ValueError("Received an invalid response from the backend.")
    except requests.HTTPError as e:
        raise RuntimeError(f"Backend returned an error: {e}")


def is_clarification_response(response: dict[str, Any]) -> bool:
    """Check if the API response is a clarification request.
    
    Args:
        response: The parsed JSON response from the backend.
        
    Returns:
        True if the response is a clarification request.
    """
    return response.get("type") == "clarification"
