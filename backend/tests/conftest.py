import pytest
import asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from unittest.mock import AsyncMock, MagicMock
import os


# Set test environment
os.environ["ENVIRONMENT"] = "test"

from app.main import app
from app.services.qdrant_service import qdrant_service
from app.services.advanced_search_service import advanced_search_service
from app.services.advanced_qdrant_service import advanced_qdrant_service

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def client():
    """Create a test client for FastAPI."""
    return TestClient(app)

@pytest.fixture
def async_client():
    """Create an async test client for FastAPI."""
    return AsyncClient(app=app, base_url="http://test")

@pytest.fixture
def mock_qdrant_service():
    """Mock the Qdrant service for testing."""
    mock = AsyncMock()
    mock.initialize_collection.return_value = True
    mock.get_collection_info.return_value = {
        "status": "green",
        "points_count": 1000,
        "vectors_count": 1000,
        "config": {}
    }
    return mock

@pytest.fixture
def mock_advanced_qdrant_service():
    """Mock the Advanced Qdrant service for testing."""
    mock = AsyncMock()
    mock.initialize_collection.return_value = True
    mock.get_collection_info.return_value = {
        "status": "green",
        "points_count": 1000,
        "vectors_count": 1000,
        "config": {}
    }
    return mock

@pytest.fixture
def mock_search_service():
    """Mock the search service for testing."""
    mock = AsyncMock()
    
    # Mock search results - properly structured to match SearchResponse schema
    mock_result = type('MockSearchResult', (), {
        'query': 'test query',
        'total': 1,
        'results': [
            {
                "id": "case_1",
                "case_name": "Test Contract Case",
                "citation": "123 F.3d 456",
                "court": "Superior Court",
                "jurisdiction": "California", 
                "case_type": "Contract Dispute",
                "summary": "Sample legal contract content...",
                "score": 0.95,
                "industry": "Technology",
                "court_level": "Superior Court"
            }
        ],
        'filters_applied': {},
        'processing_time': 0.123
    })()
    mock.semantic_search.return_value = mock_result
    
    # Mock individual case retrieval
    mock.get_case_by_id.return_value = {
        "id": "case_1",
        "case_name": "Test Contract Case",
        "citation": "123 F.3d 456",
        "court": "Superior Court",
        "jurisdiction": "California",
        "case_type": "Contract Dispute",
        "summary": "Full legal contract content...",
        "industry": "Technology",
        "court_level": "Superior Court",
        "score": 0.95
    }
    
    # Mock filter options
    mock.get_filter_options.return_value = {
        "jurisdictions": ["California", "New York", "Texas"],
        "court_levels": ["Superior Court", "Appeals Court", "Supreme Court"],
        "case_types": ["Contract Dispute", "Intellectual Property", "Employment"],
        "industries": ["Technology", "Healthcare", "Finance"],
        "company_sizes": ["Small", "Medium", "Large"],
        "contract_statuses": ["Active", "Expired", "Pending"],
        "complexity_levels": ["Low", "Medium", "High"],
        "risk_levels": ["Low", "Medium", "High"],
        "renewal_terms": ["Annual", "Quarterly", "Monthly"]
    }
    
    return mock

@pytest.fixture
def sample_search_request():
    """Sample search request for testing."""
    return {
        "query": "commercial software license agreement",
        "limit": 10,
        "filters": {
            "jurisdiction": ["California"],
            "case_type": ["Contract Dispute"]
        }
    }

@pytest.fixture
def sample_legal_case():
    """Sample legal case for testing."""
    return {
        "id": "case_123",
        "title": "Tech Corp vs Software Inc.",
        "content": "This is a commercial software license agreement dispute...",
        "metadata": {
            "jurisdiction": "California",
            "court_level": "Superior Court",
            "case_type": "Contract Dispute",
            "date": "2023-06-15",
            "industry": "Technology",
            "company_size": "Large",
            "contract_status": "Active",
            "complexity_level": "High",
            "risk_level": "Medium"
        },
        "score": 0.95,
        "highlights": ["software license", "commercial agreement"]
    } 