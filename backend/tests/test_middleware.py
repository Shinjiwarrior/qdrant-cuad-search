import pytest
from unittest.mock import patch
import time

class TestMiddleware:
    """Test middleware functionality."""
    
    @pytest.mark.asyncio
    async def test_cors_headers(self, async_client):
        """Test CORS headers are properly set."""
        response = await async_client.options("/api/health", headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET"
        })
        
        # Should allow the request
        assert response.status_code in [200, 204]
        
        # Test actual request with CORS
        response = await async_client.get("/api/health", headers={
            "Origin": "http://localhost:3000"
        })
        
        assert response.status_code == 200
        headers = response.headers
        assert "access-control-allow-origin" in headers
        
    @pytest.mark.asyncio
    async def test_process_time_header(self, async_client):
        """Test that process time header is added to responses."""
        response = await async_client.get("/")
        
        assert response.status_code == 200
        assert "x-process-time" in response.headers
        
        # Verify it's a valid float value
        process_time = float(response.headers["x-process-time"])
        assert process_time >= 0.0
        
    @pytest.mark.asyncio
    async def test_global_exception_handler(self, async_client):
        """Test global exception handler catches errors."""
        # This would require setting up a route that throws an exception
        # For now, we'll test with a route that doesn't exist
        response = await async_client.get("/api/nonexistent")
        
        # Should get 404, not 500 since this is handled by FastAPI
        assert response.status_code == 404

class TestErrorHandling:
    """Test error handling across the application."""
    
    @pytest.mark.asyncio
    async def test_invalid_json_request(self, async_client):
        """Test handling of invalid JSON in requests."""
        response = await async_client.post(
            "/api/search",
            content="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422  # Unprocessable Entity
        
    @pytest.mark.asyncio
    async def test_missing_required_fields(self, async_client):
        """Test handling of missing required fields."""
        response = await async_client.post("/api/search", json={})
        
        assert response.status_code == 422  # Validation error
        error_data = response.json()
        assert "detail" in error_data
        
    @pytest.mark.asyncio
    async def test_invalid_field_types(self, async_client):
        """Test handling of invalid field types."""
        response = await async_client.post("/api/search", json={
            "query": 123,  # Should be string
            "limit": "invalid"  # Should be integer
        })
        
        assert response.status_code == 422
        
    @pytest.mark.asyncio
    async def test_large_request_handling(self, async_client):
        """Test handling of very large requests."""
        large_query = "a" * 10000  # Very long query
        response = await async_client.post("/api/search", json={
            "query": large_query
        })
        
        # Should either process successfully or return appropriate error
        assert response.status_code in [200, 400, 413, 422] 