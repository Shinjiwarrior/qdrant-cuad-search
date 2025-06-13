import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import json

class TestE2EWorkflows:
    """End-to-end workflow tests for the legal search platform."""
    
    @pytest.mark.asyncio
    async def test_complete_search_workflow(self, async_client, mock_search_service, mock_advanced_qdrant_service):
        """Test the complete search workflow from query to case detail."""
        
        # Step 1: Health check
        with patch('app.api.routes.advanced_qdrant_service', mock_advanced_qdrant_service):
            health_response = await async_client.get("/api/health")
            assert health_response.status_code == 200
            assert health_response.json()["status"] == "healthy"
        
        # Step 2: Get filter options
        with patch('app.api.routes.advanced_search_service', mock_search_service):
            filters_response = await async_client.get("/api/filters")
            assert filters_response.status_code == 200
            filters_data = filters_response.json()
            assert "jurisdictions" in filters_data
            assert "California" in filters_data["jurisdictions"]
        
        # Step 3: Perform search with filters
        search_request = {
            "query": "commercial software license agreement",
            "limit": 10,
            "filters": {
                "jurisdiction": ["California"],
                "case_type": ["Contract Dispute"],
                "industry": ["Technology"]
            }
        }
        
        with patch('app.api.routes.advanced_search_service', mock_search_service):
            search_response = await async_client.post("/api/search", json=search_request)
            assert search_response.status_code == 200
            search_data = search_response.json()
            assert len(search_data["results"]) > 0
            
            # Get the first case ID for detailed view
            first_case_id = search_data["results"][0]["id"]
        
        # Step 4: Get detailed case information
        with patch('app.api.routes.advanced_search_service', mock_search_service):
            case_response = await async_client.get(f"/api/cases/{first_case_id}")
            assert case_response.status_code == 200
            case_data = case_response.json()
            assert case_data["id"] == first_case_id
            assert "metadata" in case_data
    
    @pytest.mark.asyncio
    async def test_user_journey_discovery_to_analysis(self, async_client, mock_search_service, mock_advanced_qdrant_service):
        """Test a complete user journey from discovery to detailed analysis."""
        
        # User Journey: Legal researcher looking for software license precedents
        
        # 1. User starts by checking system health
        with patch('app.api.routes.advanced_qdrant_service', mock_advanced_qdrant_service):
            health_response = await async_client.get("/api/health")
            assert health_response.status_code == 200
        
        # 2. User explores available filter options
        with patch('app.api.routes.advanced_search_service', mock_search_service):
            filters_response = await async_client.get("/api/filters")
            filters_data = filters_response.json()
            available_jurisdictions = filters_data["jurisdictions"]
            available_case_types = filters_data["case_types"]
        
        # 3. User performs initial broad search
        broad_search = {
            "query": "software license",
            "limit": 20
        }
        
        with patch('app.api.routes.advanced_search_service', mock_search_service):
            broad_response = await async_client.post("/api/search", json=broad_search)
            assert broad_response.status_code == 200
            broad_results = broad_response.json()
        
        # 4. User refines search with specific filters
        refined_search = {
            "query": "commercial software license dispute termination",
            "limit": 10,
            "filters": {
                "jurisdiction": ["California"],
                "case_type": ["Contract Dispute"],
                "industry": ["Technology"],
                "complexity_level": ["High"]
            }
        }
        
        with patch('app.api.routes.advanced_search_service', mock_search_service):
            refined_response = await async_client.post("/api/search", json=refined_search)
            assert refined_response.status_code == 200
            refined_results = refined_response.json()
            
            # Verify refined search returns relevant results
            assert len(refined_results["results"]) > 0
            assert refined_results["processing_time"] > 0
        
        # 5. User examines specific cases
        for case in refined_results["results"][:3]:  # Look at top 3 cases
            with patch('app.api.routes.advanced_search_service', mock_search_service):
                case_response = await async_client.get(f"/api/cases/{case['id']}")
                assert case_response.status_code == 200
                case_detail = case_response.json()
                assert "content" in case_detail
                assert "metadata" in case_detail
    
    @pytest.mark.asyncio
    async def test_system_monitoring_workflow(self, async_client, mock_advanced_qdrant_service):
        """Test system monitoring and maintenance workflow."""
        
        # 1. System administrator checks health
        with patch('app.api.routes.advanced_qdrant_service', mock_advanced_qdrant_service):
            health_response = await async_client.get("/api/health")
            assert health_response.status_code == 200
            health_data = health_response.json()
            assert health_data["qdrant_status"] == "healthy"
        
        # 2. Administrator checks system statistics
        with patch('app.api.routes.advanced_qdrant_service', mock_advanced_qdrant_service):
            stats_response = await async_client.get("/api/stats")
            assert stats_response.status_code == 200
            stats_data = stats_response.json()
            assert "total_cases" in stats_data
            assert "collection_status" in stats_data
            assert stats_data["total_cases"] == 1000
        
        # 3. Administrator performs maintenance reindex
        with patch('app.api.routes.advanced_qdrant_service', mock_advanced_qdrant_service):
            reindex_response = await async_client.post("/api/reindex")
            assert reindex_response.status_code == 200
            reindex_data = reindex_response.json()
            assert reindex_data["status"] == "success"
            
            # Verify reindex was called
            mock_advanced_qdrant_service.initialize_collection.assert_called()
        
        # 4. Administrator verifies system is still healthy after reindex
        with patch('app.api.routes.advanced_qdrant_service', mock_advanced_qdrant_service):
            post_reindex_health = await async_client.get("/api/health")
            assert post_reindex_health.status_code == 200
    
    @pytest.mark.asyncio
    async def test_error_recovery_workflow(self, async_client):
        """Test system behavior during error conditions and recovery."""
        
        # 1. Test search with invalid parameters
        invalid_search = {
            "query": "",  # Empty query
            "limit": -1   # Invalid limit
        }
        
        search_response = await async_client.post("/api/search", json=invalid_search)
        assert search_response.status_code == 400
        
        # 2. Test case retrieval with non-existent ID
        mock_service = AsyncMock()
        mock_service.get_case_by_id.return_value = None
        
        with patch('app.api.routes.advanced_search_service', mock_service):
            case_response = await async_client.get("/api/cases/nonexistent")
            assert case_response.status_code == 404
        
        # 3. Test service error handling
        error_service = AsyncMock()
        error_service.semantic_search.side_effect = Exception("Service temporarily unavailable")
        
        with patch('app.api.routes.advanced_search_service', error_service):
            error_search_response = await async_client.post("/api/search", json={
                "query": "test query"
            })
            assert error_search_response.status_code == 500
            assert "search failed" in error_search_response.json()["detail"]
        
        # 4. Test recovery - service becomes available again
        recovery_service = AsyncMock()
        recovery_service.semantic_search.return_value = MagicMock(
            results=[],
            processing_time=0.1,
            total_count=0,
            search_metadata={}
        )
        
        with patch('app.api.routes.advanced_search_service', recovery_service):
            recovery_response = await async_client.post("/api/search", json={
                "query": "recovery test"
            })
            assert recovery_response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_performance_workflow(self, async_client, mock_search_service, mock_advanced_qdrant_service):
        """Test performance-related workflows and monitoring."""
        
        # 1. Test concurrent searches
        search_requests = [
            {"query": f"test query {i}", "limit": 5}
            for i in range(5)
        ]
        
        # Simulate concurrent requests
        with patch('app.api.routes.advanced_search_service', mock_search_service):
            responses = []
            for request in search_requests:
                response = await async_client.post("/api/search", json=request)
                responses.append(response)
            
            # All requests should succeed
            for response in responses:
                assert response.status_code == 200
                assert "processing_time" in response.json()
        
        # 2. Test processing time monitoring
        with patch('app.api.routes.advanced_search_service', mock_search_service):
            search_response = await async_client.post("/api/search", json={
                "query": "performance test"
            })
            
            # Check response time header
            assert "x-process-time" in search_response.headers
            process_time = float(search_response.headers["x-process-time"])
            assert process_time >= 0.0
        
        # 3. Test large result set handling
        mock_search_service.semantic_search.return_value = MagicMock(
            results=[{"id": f"case_{i}", "title": f"Case {i}", "score": 0.9} for i in range(100)],
            processing_time=0.5,
            total_count=100,
            search_metadata={}
        )
        
        with patch('app.api.routes.advanced_search_service', mock_search_service):
            large_search_response = await async_client.post("/api/search", json={
                "query": "large result test",
                "limit": 100
            })
            
            assert large_search_response.status_code == 200
            large_results = large_search_response.json()
            assert len(large_results["results"]) == 100
    
    @pytest.mark.asyncio
    async def test_api_integration_workflow(self, async_client, mock_search_service, mock_advanced_qdrant_service):
        """Test API integration patterns and data flow."""
        
        # 1. Test search -> filter -> refine workflow
        with patch('app.api.routes.advanced_search_service', mock_search_service):
            # Initial search
            initial_response = await async_client.post("/api/search", json={
                "query": "contract dispute"
            })
            initial_results = initial_response.json()
            
            # Extract metadata for filtering
            jurisdictions = set()
            for result in initial_results["results"]:
                if "jurisdiction" in result.get("metadata", {}):
                    jurisdictions.add(result["metadata"]["jurisdiction"])
            
            # Refined search with discovered filters
            refined_response = await async_client.post("/api/search", json={
                "query": "contract dispute",
                "filters": {
                    "jurisdiction": list(jurisdictions)
                }
            })
            assert refined_response.status_code == 200
        
        # 2. Test health monitoring integration
        with patch('app.api.routes.advanced_qdrant_service', mock_advanced_qdrant_service):
            # Check health status affects search availability
            health_response = await async_client.get("/api/health")
            health_data = health_response.json()
            
            if health_data["qdrant_status"] == "healthy":
                # Search should work when system is healthy
                with patch('app.api.routes.advanced_search_service', mock_search_service):
                    search_response = await async_client.post("/api/search", json={
                        "query": "integration test"
                    })
                    assert search_response.status_code == 200
        
        # 3. Test stats and search correlation
        with patch('app.api.routes.advanced_qdrant_service', mock_advanced_qdrant_service):
            stats_response = await async_client.get("/api/stats")
            stats_data = stats_response.json()
            
            # Verify stats reflect system capabilities
            assert stats_data["total_cases"] > 0
            assert "search_type" in stats_data
            assert "features" in stats_data 