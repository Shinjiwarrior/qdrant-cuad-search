import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from datetime import datetime

class TestSearchServiceIntegration:
    """Integration tests for search service functionality."""
    
    @pytest.mark.asyncio
    async def test_full_search_pipeline(self, async_client):
        """Test the complete search pipeline from API to service."""
        # Mock the search service with realistic data
        mock_service = AsyncMock()
        mock_service.semantic_search.return_value = MagicMock(
            results=[
                {
                    "id": "case_001",
                    "title": "Software License Agreement Dispute",
                    "content": "This case involves a commercial software license...",
                    "score": 0.92,
                    "metadata": {
                        "jurisdiction": "California",
                        "court_level": "Superior Court",
                        "case_type": "Contract Dispute",
                        "date": "2023-01-15",
                        "industry": "Technology"
                    }
                },
                {
                    "id": "case_002", 
                    "title": "Enterprise Service Agreement",
                    "content": "Commercial enterprise service agreement case...",
                    "score": 0.87,
                    "metadata": {
                        "jurisdiction": "New York",
                        "court_level": "Appeals Court",
                        "case_type": "Contract Dispute",
                        "date": "2023-03-22",
                        "industry": "Technology"
                    }
                }
            ],
            processing_time=0.234,
            total_count=2,
            search_metadata={
                "query_embeddings": "generated",
                "stage_1_candidates": 1000,
                "stage_2_candidates": 100,
                "final_results": 2
            }
        )
        
        with patch('app.api.routes.advanced_search_service', mock_service):
            response = await async_client.post("/api/search", json={
                "query": "commercial software license agreement",
                "limit": 10,
                "filters": {
                    "jurisdiction": ["California", "New York"],
                    "industry": ["Technology"]
                }
            })
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert len(data["results"]) == 2
        assert data["processing_time"] == 0.234
        assert data["total_count"] == 2
        
        # Verify first result
        first_result = data["results"][0]
        assert first_result["id"] == "case_001"
        assert first_result["score"] == 0.92
        assert first_result["metadata"]["jurisdiction"] == "California"
        
        # Verify service was called correctly
        mock_service.semantic_search.assert_called_once()
        call_args = mock_service.semantic_search.call_args[0][0]
        assert call_args.query == "commercial software license agreement"
        assert call_args.limit == 10
        
    @pytest.mark.asyncio
    async def test_case_detail_integration(self, async_client):
        """Test case detail retrieval integration."""
        mock_service = AsyncMock()
        mock_service.get_case_by_id.return_value = {
            "id": "case_detailed",
            "title": "Comprehensive Software License Case",
            "content": "This is the full content of the legal case...",
            "metadata": {
                "jurisdiction": "California",
                "court_level": "Superior Court",
                "case_type": "Contract Dispute",
                "date": "2023-01-15",
                "industry": "Technology",
                "company_size": "Large",
                "complexity_level": "High",
                "risk_level": "Medium"
            },
            "related_cases": ["case_001", "case_002"],
            "citations": ["Citation 1", "Citation 2"]
        }
        
        with patch('app.api.routes.advanced_search_service', mock_service):
            response = await async_client.get("/api/cases/case_detailed")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == "case_detailed"
        assert data["title"] == "Comprehensive Software License Case"
        assert "related_cases" in data
        assert len(data["related_cases"]) == 2

class TestQdrantServiceIntegration:
    """Integration tests for Qdrant service interactions."""
    
    @pytest.mark.asyncio
    async def test_qdrant_health_integration(self, async_client):
        """Test Qdrant health check integration."""
        mock_qdrant = AsyncMock()
        mock_qdrant.get_collection_info.return_value = {
            "status": "green",
            "points_count": 5000,
            "vectors_count": 5000,
            "config": {
                "params": {
                    "vectors": {
                        "dense": {"size": 384, "distance": "Cosine"},
                        "byte": {"size": 384, "distance": "Cosine"},
                        "rerank": {"size": 768, "distance": "Cosine"}
                    }
                }
            }
        }
        
        with patch('app.api.routes.advanced_qdrant_service', mock_qdrant):
            # Test health endpoint
            health_response = await async_client.get("/api/health")
            assert health_response.status_code == 200
            health_data = health_response.json()
            assert health_data["qdrant_status"] == "healthy"
            
            # Test stats endpoint
            stats_response = await async_client.get("/api/stats")
            assert stats_response.status_code == 200
            stats_data = stats_response.json()
            assert stats_data["total_cases"] == 5000
            assert stats_data["collection_status"] == "green"
    
    @pytest.mark.asyncio
    async def test_collection_reindex_integration(self, async_client):
        """Test collection reindexing integration."""
        mock_qdrant = AsyncMock()
        mock_qdrant.initialize_collection.return_value = True
        
        with patch('app.api.routes.advanced_qdrant_service', mock_qdrant):
            response = await async_client.post("/api/reindex")
            
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "features" in data
        assert len(data["features"]) > 0
        
        # Verify the service method was called
        mock_qdrant.initialize_collection.assert_called_once()

class TestFilterServiceIntegration:
    """Integration tests for filter service functionality."""
    
    @pytest.mark.asyncio
    async def test_filter_options_integration(self, async_client):
        """Test filter options retrieval integration."""
        mock_service = AsyncMock()
        mock_service.get_filter_options.return_value = {
            "jurisdictions": ["California", "New York", "Texas", "Florida"],
            "court_levels": ["Superior Court", "Appeals Court", "Supreme Court"],
            "case_types": ["Contract Dispute", "Intellectual Property", "Employment", "Real Estate"],
            "industries": ["Technology", "Healthcare", "Finance", "Manufacturing"],
            "company_sizes": ["Small", "Medium", "Large", "Enterprise"],
            "contract_statuses": ["Active", "Expired", "Pending", "Terminated"],
            "complexity_levels": ["Low", "Medium", "High", "Critical"],
            "risk_levels": ["Low", "Medium", "High", "Critical"],
            "renewal_terms": ["Monthly", "Quarterly", "Annual", "Multi-year"]
        }
        
        with patch('app.api.routes.advanced_search_service', mock_service):
            response = await async_client.get("/api/filters")
            
        assert response.status_code == 200
        data = response.json()
        
        # Verify all filter categories are present
        expected_categories = [
            "jurisdictions", "court_levels", "case_types", "industries",
            "company_sizes", "contract_statuses", "complexity_levels",
            "risk_levels", "renewal_terms"
        ]
        
        for category in expected_categories:
            assert category in data
            assert len(data[category]) > 0
        
        # Verify specific values
        assert "California" in data["jurisdictions"]
        assert "Technology" in data["industries"]
        assert "Contract Dispute" in data["case_types"]

class TestErrorScenarios:
    """Integration tests for error scenarios."""
    
    @pytest.mark.asyncio
    async def test_service_unavailable_scenarios(self, async_client):
        """Test behavior when services are unavailable."""
        
        # Test Qdrant service unavailable
        mock_qdrant = AsyncMock()
        mock_qdrant.get_collection_info.side_effect = Exception("Connection refused")
        
        with patch('app.api.routes.advanced_qdrant_service', mock_qdrant):
            health_response = await async_client.get("/api/health")
            assert health_response.status_code == 200
            health_data = health_response.json()
            assert health_data["status"] == "unhealthy"
            assert health_data["qdrant_status"] == "error"
    
    @pytest.mark.asyncio 
    async def test_search_service_timeout(self, async_client):
        """Test search service timeout handling."""
        mock_service = AsyncMock()
        mock_service.semantic_search.side_effect = TimeoutError("Search timeout")
        
        with patch('app.api.routes.advanced_search_service', mock_service):
            response = await async_client.post("/api/search", json={
                "query": "test query"
            })
            
        assert response.status_code == 500
        assert "search failed" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_partial_service_degradation(self, async_client):
        """Test behavior with partial service degradation."""
        # Mock search service working but Qdrant having issues
        mock_search = AsyncMock()
        mock_search.semantic_search.return_value = MagicMock(
            results=[],
            processing_time=0.5,
            total_count=0,
            search_metadata={}
        )
        
        mock_qdrant = AsyncMock()
        mock_qdrant.get_collection_info.return_value = {"status": "yellow"}
        
        with patch('app.api.routes.advanced_search_service', mock_search):
            with patch('app.api.routes.advanced_qdrant_service', mock_qdrant):
                # Search should still work
                search_response = await async_client.post("/api/search", json={
                    "query": "test"
                })
                assert search_response.status_code == 200
                
                # Health should show degraded status
                health_response = await async_client.get("/api/health")
                assert health_response.status_code == 200
                health_data = health_response.json()
                assert health_data["qdrant_status"] == "unhealthy" 