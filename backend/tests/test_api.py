import pytest
from unittest.mock import patch, AsyncMock
import json
from datetime import datetime

class TestSearchAPI:
    """Test the search endpoint functionality."""
    
    @pytest.mark.asyncio
    async def test_search_success(self, async_client, mock_search_service, sample_search_request):
        """Test successful search request."""
        with patch('app.api.routes.advanced_search_service', mock_search_service):
            response = await async_client.post("/api/search", json=sample_search_request)
            
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert "processing_time" in data
        assert len(data["results"]) > 0
        assert data["results"][0]["id"] == "case_1"
        
    @pytest.mark.asyncio
    async def test_search_empty_query(self, async_client):
        """Test search with empty query returns 422 (validation error)."""
        response = await async_client.post("/api/search", json={"query": ""})
        
        assert response.status_code == 422  # FastAPI validation error
        error_data = response.json()
        assert "detail" in error_data
        
    @pytest.mark.asyncio
    async def test_search_whitespace_query(self, async_client):
        """Test search with whitespace-only query returns 400."""
        response = await async_client.post("/api/search", json={"query": "   "})
        
        assert response.status_code == 400
        assert "empty" in response.json()["detail"]
        
    @pytest.mark.asyncio
    async def test_search_with_filters(self, async_client, mock_search_service):
        """Test search with various filters."""
        request_data = {
            "query": "commercial contract",
            "limit": 20,
            "filters": {
                "jurisdiction": ["California", "New York"],
                "case_type": ["Contract Dispute"],
                "industry": ["Technology"]
            }
        }
        
        with patch('app.api.routes.advanced_search_service', mock_search_service):
            response = await async_client.post("/api/search", json=request_data)
            
        assert response.status_code == 200
        mock_search_service.semantic_search.assert_called_once()
        
    @pytest.mark.asyncio
    async def test_search_service_error(self, async_client):
        """Test search when service throws an error."""
        mock_service = AsyncMock()
        mock_service.semantic_search.side_effect = Exception("Service error")
        
        with patch('app.api.routes.advanced_search_service', mock_service):
            response = await async_client.post("/api/search", json={"query": "test"})
            
        assert response.status_code == 500
        assert "search failed" in response.json()["detail"]

class TestCaseAPI:
    """Test the individual case retrieval endpoint."""
    
    @pytest.mark.asyncio
    async def test_get_case_success(self, async_client, mock_search_service):
        """Test successful case retrieval."""
        with patch('app.api.routes.advanced_search_service', mock_search_service):
            response = await async_client.get("/api/cases/case_1")
            
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "case_1"
        assert data["case_name"] == "Test Contract Case"
        
    @pytest.mark.asyncio
    async def test_get_case_not_found(self, async_client):
        """Test case retrieval when case doesn't exist."""
        mock_service = AsyncMock()
        mock_service.get_case_by_id.return_value = None
        
        with patch('app.api.routes.advanced_search_service', mock_service):
            response = await async_client.get("/api/cases/nonexistent")
            
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
        
    @pytest.mark.asyncio
    async def test_get_case_service_error(self, async_client):
        """Test case retrieval when service throws an error."""
        mock_service = AsyncMock()
        mock_service.get_case_by_id.side_effect = Exception("Database error")
        
        with patch('app.api.routes.advanced_search_service', mock_service):
            response = await async_client.get("/api/cases/case_1")
            
        assert response.status_code == 500
        assert "Failed to retrieve case" in response.json()["detail"]

class TestFiltersAPI:
    """Test the filter options endpoint."""
    
    @pytest.mark.asyncio
    async def test_get_filters_success(self, async_client, mock_search_service):
        """Test successful filter options retrieval."""
        with patch('app.api.routes.advanced_search_service', mock_search_service):
            response = await async_client.get("/api/filters")
            
        assert response.status_code == 200
        data = response.json()
        assert "jurisdictions" in data
        assert "court_levels" in data
        assert "case_types" in data
        assert len(data["jurisdictions"]) > 0
        
    @pytest.mark.asyncio
    async def test_get_filters_service_error(self, async_client):
        """Test filter options when service throws an error."""
        mock_service = AsyncMock()
        mock_service.get_filter_options.side_effect = Exception("Service error")
        
        with patch('app.api.routes.advanced_search_service', mock_service):
            response = await async_client.get("/api/filters")
            
        assert response.status_code == 500
        assert "Failed to get filter options" in response.json()["detail"]

class TestHealthAPI:
    """Test the health check endpoint."""
    
    @pytest.mark.asyncio
    async def test_health_check_healthy(self, async_client, mock_advanced_qdrant_service):
        """Test health check when all services are healthy."""
        with patch('app.api.routes.advanced_qdrant_service', mock_advanced_qdrant_service):
            response = await async_client.get("/api/health")
            
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["qdrant_status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data
        
    @pytest.mark.asyncio
    async def test_health_check_unhealthy(self, async_client):
        """Test health check when Qdrant service is unhealthy."""
        mock_service = AsyncMock()
        mock_service.get_collection_info.return_value = {"status": "red"}
        
        with patch('app.api.routes.advanced_qdrant_service', mock_service):
            response = await async_client.get("/api/health")
            
        assert response.status_code == 200
        data = response.json()
        assert data["qdrant_status"] == "unhealthy"
        
    @pytest.mark.asyncio
    async def test_health_check_service_error(self, async_client):
        """Test health check when service throws an error."""
        mock_service = AsyncMock()
        mock_service.get_collection_info.side_effect = Exception("Connection error")
        
        with patch('app.api.routes.advanced_qdrant_service', mock_service):
            response = await async_client.get("/api/health")
            
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "unhealthy"
        assert data["qdrant_status"] == "error"

class TestStatsAPI:
    """Test the statistics endpoint."""
    
    @pytest.mark.asyncio
    async def test_get_stats_success(self, async_client, mock_advanced_qdrant_service):
        """Test successful stats retrieval."""
        with patch('app.api.routes.advanced_qdrant_service', mock_advanced_qdrant_service):
            response = await async_client.get("/api/stats")
            
        assert response.status_code == 200
        data = response.json()
        assert "collection_status" in data
        assert "total_cases" in data
        assert "search_type" in data
        assert "features" in data
        assert data["total_cases"] == 1000
        
    @pytest.mark.asyncio
    async def test_get_stats_service_error(self, async_client):
        """Test stats when service throws an error."""
        mock_service = AsyncMock()
        mock_service.get_collection_info.side_effect = Exception("Database error")
        
        with patch('app.api.routes.advanced_qdrant_service', mock_service):
            response = await async_client.get("/api/stats")
            
        assert response.status_code == 500
        assert "Failed to get stats" in response.json()["detail"]

class TestReindexAPI:
    """Test the collection reindexing endpoint."""
    
    @pytest.mark.asyncio
    async def test_reindex_success(self, async_client, mock_advanced_qdrant_service):
        """Test successful collection reindexing."""
        with patch('app.api.routes.advanced_qdrant_service', mock_advanced_qdrant_service):
            response = await async_client.post("/api/reindex")
            
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "features" in data
        mock_advanced_qdrant_service.initialize_collection.assert_called_once()
        
    @pytest.mark.asyncio
    async def test_reindex_service_error(self, async_client):
        """Test reindexing when service throws an error."""
        mock_service = AsyncMock()
        mock_service.initialize_collection.side_effect = Exception("Initialization error")
        
        with patch('app.api.routes.advanced_qdrant_service', mock_service):
            response = await async_client.post("/api/reindex")
            
        assert response.status_code == 500
        assert "Failed to reindex" in response.json()["detail"]

class TestRootAPI:
    """Test the root endpoint."""
    
    @pytest.mark.asyncio
    async def test_root_endpoint(self, async_client):
        """Test the root endpoint returns correct information."""
        response = await async_client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data
        assert "health" in data
        assert data["docs"] == "/docs"
        assert data["health"] == "/api/health" 