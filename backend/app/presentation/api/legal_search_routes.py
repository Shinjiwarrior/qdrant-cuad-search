from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import logging
from datetime import datetime

from app.domain.legal_search.schemas import (
    SearchRequest, SearchResponse, LegalCase, 
    FilterOptions, HealthResponse, ErrorResponse
)
from app.domain.legal_search.search_orchestrator import search_orchestrator
from app.infrastructure.vector_store.qdrant_client import qdrant_client
from app.infrastructure.configuration import settings

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/search", response_model=SearchResponse)
async def search_cuad_contracts(request: SearchRequest):
    """
    Perform advanced semantic search through CUAD commercial contracts.
    
    Flow:
    1. Generate multiple query embeddings (byte, dense, rerank, ColBERT)
    2. Stage 1: Fast prefetch with byte vectors (1000 candidates)
    3. Stage 2: Rerank with dense vectors (100 candidates)
    4. Stage 3: Final ranking with ColBERT multi-vectors (final results)
    """
    try:
        logger.info(f"CUAD contract search: '{request.query}' with {len(request.filters or {})} filters")
        
        # Validate request
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Search query cannot be empty")
        
        # Perform advanced multi-stage search
        result = await search_orchestrator.semantic_search(request)
        
        logger.info(f"CUAD search completed: {len(result.results)} results in {result.processing_time:.3f}s")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"CUAD search error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Contract search failed: {str(e)}")

@router.get("/cases/{case_id}", response_model=LegalCase)
async def get_cuad_contract(case_id: str):
    """
    Retrieve a specific CUAD commercial contract by ID.
    """
    try:
        contract = await search_orchestrator.get_case_by_id(case_id)
        
        if not contract:
            raise HTTPException(status_code=404, detail=f"CUAD contract {case_id} not found")
        
        return contract
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving CUAD contract {case_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve contract: {str(e)}")

@router.get("/filters", response_model=FilterOptions)
async def get_contract_filters():
    """
    Get available filter options for CUAD commercial contract search.
    """
    try:
        options = await search_orchestrator.get_filter_options()
        
        # Ensure we have all fields for the FilterOptions model
        filter_response = FilterOptions(
            jurisdictions=options.get("jurisdictions", []),
            court_levels=options.get("court_levels", []),
            case_types=options.get("case_types", []),
            industries=options.get("industries", []),
            company_sizes=options.get("company_sizes", []),
            contract_statuses=options.get("contract_statuses", []),
            complexity_levels=options.get("complexity_levels", []),
            risk_levels=options.get("risk_levels", []),
            renewal_terms=options.get("renewal_terms", [])
        )
        
        return filter_response
        
    except Exception as e:
        logger.error(f"Error getting filter options: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get filter options: {str(e)}")

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint for Qdrant CUAD Search.
    """
    try:
        # Check Qdrant connection
        qdrant_info = await qdrant_client.get_collection_info()
        qdrant_status = "healthy" if qdrant_info.get("status") == "green" else "unhealthy"
        
        return HealthResponse(
            status="healthy",
            timestamp=datetime.now(),
            version=f"{settings.app_version}",
            qdrant_status=qdrant_status
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthResponse(
            status="unhealthy",
            timestamp=datetime.now(),
            version=f"{settings.app_version}",
            qdrant_status="error"
        )

@router.get("/stats")
async def get_cuad_stats():
    """
    Get statistics about the CUAD contract collection.
    """
    try:
        info = await qdrant_client.get_collection_info()
        return {
            "collection_status": info.get("status", "unknown"),
            "total_contracts": info.get("points_count", 0),
            "vector_count": info.get("vectors_count", 0),
            "config": info.get("config", {}),
            "search_type": "Qdrant CUAD Contract Search",
            "dataset": "CUAD: Contract Understanding Atticus Dataset",
            "features": [
                "510 real commercial contracts",
                "13,000+ expert-labeled clauses",
                "Coarse-to-fine search pipeline",
                "ColBERT multi-vector refinement"
            ]
        }
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")

@router.post("/reindex")
async def reindex_cuad_collection():
    """
    Recreate the CUAD contract collection with multi-vector support.
    WARNING: This will delete and recreate the entire collection.
    """
    try:
        logger.info("Starting CUAD collection reindexing with Qdrant multi-vector support")
        
        # Initialize the advanced collection
        await qdrant_client.initialize_collection()
        
        return {
            "message": "CUAD collection reindexed with Qdrant multi-vector support",
            "status": "success",
            "dataset": "CUAD: Contract Understanding Atticus Dataset",
            "features": [
                "Dense vectors (BAAI/bge-small-en-v1.5)",
                "Rerank vectors (BAAI/bge-base-en-v1.5)",
                "ColBERT multi-vectors (all-MiniLM-L6-v2)",
                "Byte vectors for fast prefetch"
            ]
        }
        
    except Exception as e:
        logger.error(f"Error reindexing CUAD collection: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to reindex: {str(e)}") 