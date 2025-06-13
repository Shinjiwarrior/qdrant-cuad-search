#!/usr/bin/env python3
"""
Migration script to upgrade to the advanced multi-vector search system.

This script:
1. Sets up the new multi-vector Qdrant collection
2. Migrates existing data with new embedding types
3. Validates the new search system

Run with: python migrate_to_advanced_search.py
"""

import asyncio
import json
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append('..')

from app.services.fastembed_service import fastembed_service
from app.services.advanced_qdrant_service import advanced_qdrant_service
from app.services.advanced_search_service import advanced_search_service
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedSearchMigration:
    def __init__(self):
        self.fastembed_service = fastembed_service
        self.qdrant_service = advanced_qdrant_service
        self.search_service = advanced_search_service
    
    async def migrate(self):
        """
        Main migration function.
        """
        try:
            logger.info("="*60)
            logger.info("MIGRATING TO ADVANCED MULTI-VECTOR SEARCH SYSTEM")
            logger.info("="*60)
            
            # Step 1: Initialize FastEmbed models
            await self._initialize_models()
            
            # Step 2: Initialize new Qdrant collection
            await self._initialize_collection()
            
            # Step 3: Load and migrate existing data
            await self._migrate_data()
            
            # Step 4: Validate the new system
            await self._validate_system()
            
            logger.info("="*60)
            logger.info("MIGRATION COMPLETED SUCCESSFULLY!")
            logger.info("="*60)
            logger.info("\nNew Features:")
            logger.info("✅ FastEmbed local embeddings (no OpenAI dependency)")
            logger.info("✅ Multi-vector collection support")
            logger.info("✅ Byte vector prefetch (1000 candidates)")
            logger.info("✅ Dense vector reranking (100 candidates)")
            logger.info("✅ ColBERT multi-vector final ranking")
            logger.info("✅ 3-stage search optimization")
            
        except Exception as e:
            logger.error(f"Migration failed: {str(e)}")
            raise
    
    async def _initialize_models(self):
        """
        Initialize FastEmbed models.
        """
        logger.info("Step 1: Initializing FastEmbed models...")
        
        try:
            # Test model initialization
            test_text = "test embedding generation"
            
            dense_emb = await self.fastembed_service.get_dense_embedding(test_text)
            logger.info(f"✅ Dense model initialized: {len(dense_emb)} dimensions")
            
            rerank_emb = await self.fastembed_service.get_rerank_embedding(test_text)
            logger.info(f"✅ Rerank model initialized: {len(rerank_emb)} dimensions")
            
            colbert_embs = await self.fastembed_service.get_colbert_embeddings(test_text)
            logger.info(f"✅ ColBERT model initialized: {len(colbert_embs)} vectors of {len(colbert_embs[0])} dimensions")
            
            byte_emb = await self.fastembed_service.get_byte_vector(test_text)
            logger.info(f"✅ Byte vector generation: {len(byte_emb)} bytes")
            
            logger.info("All FastEmbed models initialized successfully!")
            
        except Exception as e:
            logger.error(f"Failed to initialize models: {str(e)}")
            raise
    
    async def _initialize_collection(self):
        """
        Initialize the new multi-vector Qdrant collection.
        """
        logger.info("Step 2: Initializing multi-vector Qdrant collection...")
        
        try:
            await self.qdrant_service.initialize_collection()
            
            # Get collection info
            info = await self.qdrant_service.get_collection_info()
            logger.info(f"✅ Collection created: {info}")
            
        except Exception as e:
            logger.error(f"Failed to initialize collection: {str(e)}")
            raise
    
    async def _migrate_data(self):
        """
        Load existing data and create new multi-vector embeddings.
        """
        logger.info("Step 3: Migrating data with multi-vector embeddings...")
        
        try:
            # Look for existing data files
            data_files = [
                "commercial_contracts_data.json",
                "cuad_processed_data.json", 
                "full_cuad_processed_data.json"
            ]
            
            contracts = []
            for data_file in data_files:
                file_path = Path(data_file)
                if file_path.exists():
                    logger.info(f"Loading data from {data_file}...")
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        if isinstance(data, list) and len(data) > 0:
                            contracts = data
                            logger.info(f"Loaded {len(contracts)} contracts from {data_file}")
                            break
            
            if not contracts:
                logger.warning("No existing contract data found. Creating sample data...")
                contracts = await self._create_sample_data()
            
            # Process contracts in batches with multi-vector embeddings
            logger.info(f"Processing {len(contracts)} contracts with multi-vector embeddings...")
            
            # Remove artificial demo limit - process all contracts
            # contracts = contracts[:50]  # Process first 50 for demo
            
            await self.search_service.add_cases_to_index(contracts)
            
            logger.info("Data migration completed successfully!")
            
        except Exception as e:
            logger.error(f"Failed to migrate data: {str(e)}")
            raise
    
    async def _create_sample_data(self):
        """
        Create sample contract data if none exists.
        """
        logger.info("Creating sample contract data...")
        
        sample_contracts = [
            {
                "id": "sample-1",
                "case_name": "Employment Agreement - Tech Startup",
                "citation": "SAMPLE-001",
                "court": "Commercial Transaction",
                "jurisdiction": "California",
                "case_type": "employment_agreement",
                "summary": "Employment agreement for software engineer at tech startup including equity compensation, non-compete clauses, and termination procedures.",
                "full_text": "This Employment Agreement is entered into between TechCorp Inc. and Employee for the position of Senior Software Engineer. The agreement includes base salary, equity compensation, benefits, confidentiality obligations, non-compete restrictions, and termination procedures. Employee agrees to develop software products and maintain confidentiality of proprietary information.",
                "industry": "Technology",
                "company_size": "Startup",
                "complexity_level": "Medium",
                "risk_level": "Medium",
                "contract_status": "Active",
                "renewal_terms": "Annual",
                "date_filed": "2024-01-01"
            },
            {
                "id": "sample-2", 
                "case_name": "Software License Agreement - Enterprise",
                "citation": "SAMPLE-002",
                "court": "Commercial Transaction",
                "jurisdiction": "New York",
                "case_type": "license_agreement",
                "summary": "Enterprise software licensing agreement with usage restrictions, support terms, and liability limitations.",
                "full_text": "This Software License Agreement grants Customer the right to use Software under specified terms. License includes installation rights, usage limitations, support services, maintenance updates, liability disclaimers, and termination conditions. Customer agrees to comply with usage restrictions and payment terms.",
                "industry": "Technology",
                "company_size": "Enterprise", 
                "complexity_level": "High",
                "risk_level": "Low",
                "contract_status": "Executed",
                "renewal_terms": "Fixed Term",
                "date_filed": "2024-01-02"
            },
            {
                "id": "sample-3",
                "case_name": "Service Agreement - Healthcare Provider",
                "citation": "SAMPLE-003", 
                "court": "Commercial Transaction",
                "jurisdiction": "Texas",
                "case_type": "service_agreement",
                "summary": "Healthcare service agreement including HIPAA compliance, service level agreements, and quality metrics.",
                "full_text": "This Service Agreement establishes terms for healthcare services including patient care standards, HIPAA compliance requirements, service level agreements, quality metrics, billing procedures, and regulatory compliance. Provider agrees to maintain professional standards and protect patient information.",
                "industry": "Healthcare",
                "company_size": "SME",
                "complexity_level": "High", 
                "risk_level": "High",
                "contract_status": "Active",
                "renewal_terms": "Annual",
                "date_filed": "2024-01-03"
            }
        ]
        
        return sample_contracts
    
    async def _validate_system(self):
        """
        Validate the new search system is working correctly.
        """
        logger.info("Step 4: Validating advanced search system...")
        
        try:
            # Test searches
            test_queries = [
                "employment termination",
                "software license",
                "healthcare services"
            ]
            
            for query in test_queries:
                logger.info(f"Testing search: '{query}'")
                
                # Create search request
                from app.models.schemas import SearchRequest
                request = SearchRequest(query=query, limit=3)
                
                # Perform search
                response = await self.search_service.semantic_search(request)
                
                logger.info(f"✅ Found {len(response.results)} results in {response.processing_time:.3f}s")
                
                if response.results:
                    best_result = response.results[0]
                    logger.info(f"   Best match: {best_result.case_name} (score: {best_result.score:.3f})")
            
            # Test collection stats
            stats = await self.qdrant_service.get_collection_info()
            logger.info(f"✅ Collection stats: {stats}")
            
            logger.info("System validation completed successfully!")
            
        except Exception as e:
            logger.error(f"System validation failed: {str(e)}")
            raise

async def main():
    """
    Run the migration.
    """
    migration = AdvancedSearchMigration()
    await migration.migrate()

if __name__ == "__main__":
    asyncio.run(main()) 