from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct, Filter, FieldCondition, 
    MatchValue, MatchAny, Range, PayloadSchemaType, CreateCollection,
    Prefetch, MultiVectorConfig
)
from typing import List, Dict, Any, Optional
import logging
import uuid
from app.core.config import settings

logger = logging.getLogger(__name__)

class AdvancedQdrantService:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )
        self.collection_name = settings.qdrant_collection_name
        
        # Vector configurations for multi-stage search
        self.vector_configs = {
            "dense": 384,      # BAAI/bge-small-en-v1.5 dimensions
            "rerank": 768,     # BAAI/bge-base-en-v1.5 dimensions  
            "colbert": 384,    # all-MiniLM-L6-v2 dimensions
            "byte": 384        # Quantized version of dense
        }
    
    async def initialize_collection(self):
        """
        Initialize the Qdrant collection with multi-vector configuration.
        """
        try:
            collections = self.client.get_collections()
            collection_names = [col.name for col in collections.collections]
            
            if self.collection_name not in collection_names:
                # Create collection with multiple vector configurations using latest API
                vectors_config = {
                    "dense": VectorParams(
                        size=self.vector_configs["dense"],
                        distance=Distance.COSINE
                    ),
                    "rerank": VectorParams(
                        size=self.vector_configs["rerank"], 
                        distance=Distance.COSINE
                    ),
                    "colbert": VectorParams(
                        size=self.vector_configs["colbert"],
                        distance=Distance.COSINE,
                        multivector_config=MultiVectorConfig(
                            comparator="max_sim"  # ColBERT-style max similarity
                        )
                    ),
                    "byte": VectorParams(
                        size=self.vector_configs["byte"],
                        distance=Distance.COSINE,
                        datatype="uint8"  # Byte vectors
                    )
                }
                
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=vectors_config
                )
                logger.info(f"Created multi-vector collection: {self.collection_name}")
                
                # Create indexes for filtering
                await self._create_filter_indexes()
            else:
                logger.info(f"Collection {self.collection_name} already exists")
                
        except Exception as e:
            logger.error(f"Error initializing collection: {str(e)}")
            raise
    
    async def _create_filter_indexes(self):
        """
        Create indexes for filtering fields.
        """
        try:
            filter_fields = [
                "jurisdiction", "court_level", "case_type", "industry",
                "company_size", "contract_status", "complexity_level",
                "risk_level", "renewal_terms", "contract_start_date",
                "contract_end_date", "date_filed"
            ]
            
            for field in filter_fields:
                try:
                    self.client.create_payload_index(
                        collection_name=self.collection_name,
                        field_name=field,
                        field_schema=PayloadSchemaType.KEYWORD
                    )
                except Exception as field_error:
                    logger.debug(f"Index for {field} may already exist: {str(field_error)}")
            
            logger.info("Created filter indexes for collection")
            
        except Exception as e:
            logger.info(f"Filter indexes may already exist: {str(e)}")
    
    async def add_multi_vector_points(self, cases: List[Dict[str, Any]], embeddings: Dict[str, Any]):
        """
        Add legal cases with multiple vector types to the collection.
        
        Args:
            cases: List of case data
            embeddings: Dict containing different embedding types:
                       {"dense": [...], "rerank": [...], "colbert": [...], "byte": [...]}
        """
        try:
            batch_size = 10
            total_points = 0
            
            for i in range(0, len(cases), batch_size):
                batch_cases = cases[i:i + batch_size]
                
                points = []
                for j, case in enumerate(batch_cases):
                    case_id = case.get('id', str(uuid.uuid4()))
                    
                    # Prepare vectors for this point
                    vectors = {}
                    
                    # Dense vector for fast initial search
                    if 'dense' in embeddings and i + j < len(embeddings['dense']):
                        vectors['dense'] = embeddings['dense'][i + j]
                    
                    # Rerank vector for better precision
                    if 'rerank' in embeddings and i + j < len(embeddings['rerank']):
                        vectors['rerank'] = embeddings['rerank'][i + j]
                    
                    # ColBERT multi-vectors for final ranking
                    if 'colbert' in embeddings and i + j < len(embeddings['colbert']):
                        vectors['colbert'] = embeddings['colbert'][i + j]
                    
                    # Byte vector for fastest prefetch
                    if 'byte' in embeddings and i + j < len(embeddings['byte']):
                        vectors['byte'] = embeddings['byte'][i + j]
                    
                    point = PointStruct(
                        id=case_id,
                        vector=vectors,
                        payload=case
                    )
                    points.append(point)
                
                # Upload this batch
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=points
                )
                
                total_points += len(points)
                logger.info(f"Uploaded batch {i//batch_size + 1}: {len(points)} points (Total: {total_points})")
            
            logger.info(f"Successfully added {total_points} multi-vector points to collection")
            
        except Exception as e:
            logger.error(f"Error adding multi-vector points to Qdrant: {str(e)}")
            raise
    
    async def advanced_search(
        self,
        query_embeddings: Dict[str, Any],
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 10,
        prefetch_limit: int = 1000,
        rerank_limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Perform advanced multi-stage search with prefetch and reranking.
        
        Args:
            query_embeddings: Dict with different query embedding types
            filters: Optional metadata filters
            limit: Final number of results
            prefetch_limit: Number of candidates from byte vector search
            rerank_limit: Number of candidates from dense vector rerank
        """
        try:
            # Build filters
            qdrant_filter = self._build_filter(filters) if filters else None
            
            # Stage 1: Fast prefetch with byte vectors (1000 candidates)
            prefetch_stage = Prefetch(
                query=query_embeddings.get('byte', query_embeddings.get('dense')),
                using="byte",
                limit=prefetch_limit,
                filter=qdrant_filter
            )
            
            # Stage 2: Rerank with dense vectors (100 candidates)
            if 'rerank' in query_embeddings:
                rerank_stage = Prefetch(
                    prefetch=prefetch_stage,
                    query=query_embeddings['rerank'],
                    using="rerank", 
                    limit=rerank_limit
                )
            else:
                rerank_stage = prefetch_stage
            
            # Stage 3: Final ranking with ColBERT multi-vectors (10 results)
            if 'colbert' in query_embeddings:
                search_result = self.client.query_points(
                    collection_name=self.collection_name,
                    prefetch=rerank_stage,
                    query=query_embeddings['colbert'],
                    using="colbert",
                    limit=limit,
                    with_payload=True
                )
            else:
                # Fallback to dense vector final search
                search_result = self.client.query_points(
                    collection_name=self.collection_name,
                    prefetch=rerank_stage,
                    query=query_embeddings.get('dense'),
                    using="dense",
                    limit=limit,
                    with_payload=True
                )
            
            # Format results
            formatted_results = []
            for result in search_result.points:
                case_data = result.payload
                case_data['score'] = result.score
                formatted_results.append(case_data)
            
            logger.info(f"Advanced search completed: {len(formatted_results)} results")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error in advanced search: {str(e)}")
            # Fallback to simple dense search
            return await self._fallback_search(query_embeddings, filters, limit)
    
    async def _fallback_search(
        self,
        query_embeddings: Dict[str, Any],
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Fallback to simple search if advanced search fails.
        """
        try:
            qdrant_filter = self._build_filter(filters) if filters else None
            
            # Use the best available query vector
            query_vector = (
                query_embeddings.get('dense') or 
                query_embeddings.get('rerank') or
                list(query_embeddings.values())[0]
            )
            
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                query_filter=qdrant_filter,
                limit=limit,
                score_threshold=settings.similarity_threshold,
                with_payload=True
            )
            
            formatted_results = []
            for result in search_result:
                case_data = result.payload
                case_data['score'] = result.score
                formatted_results.append(case_data)
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error in fallback search: {str(e)}")
            return []
    
    async def get_case_by_id(self, case_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific case by its ID.
        """
        try:
            result = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[case_id],
                with_payload=True
            )
            
            if result:
                return result[0].payload
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving case {case_id}: {str(e)}")
            return None
    
    async def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the multi-vector collection.
        """
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                "status": info.status,
                "points_count": info.points_count,
                "vectors_count": info.vectors_count,
                "config": {
                    "vector_configs": self.vector_configs,
                    "distance": "COSINE"
                }
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    def _build_filter(self, filters: Dict[str, Any]) -> Filter:
        """
        Build Qdrant filter from search filters.
        """
        conditions = []
        
        filterable_fields = [
            'jurisdiction', 'court_level', 'case_type', 'industry', 
            'company_size', 'contract_status', 'complexity_level', 
            'risk_level', 'renewal_terms'
        ]
        
        for field in filterable_fields:
            if filters.get(field):
                field_values = filters[field]
                if isinstance(field_values, list) and len(field_values) > 0:
                    if len(field_values) == 1:
                        conditions.append(
                            FieldCondition(
                                key=field,
                                match=MatchValue(value=field_values[0])
                            )
                        )
                    else:
                        conditions.append(
                            FieldCondition(
                                key=field,
                                match=MatchAny(any=field_values)
                            )
                        )
        
        # Date range filter
        if filters.get('date_from') or filters.get('date_to'):
            date_range = {}
            if filters.get('date_from'):
                date_range['gte'] = filters['date_from']
            if filters.get('date_to'):
                date_range['lte'] = filters['date_to']
            
            conditions.append(
                FieldCondition(
                    key="date_filed",
                    range=Range(**date_range)
                )
            )
        
        return Filter(must=conditions) if conditions else None
    
    async def get_unique_filter_values(self) -> Dict[str, List[str]]:
        """
        Get unique values for filter fields from the collection.
        """
        try:
            scroll_result = self.client.scroll(
                collection_name=self.collection_name,
                limit=1000,
                with_payload=True
            )
            
            unique_values = {
                "jurisdictions": set(),
                "court_levels": set(), 
                "case_types": set(),
                "industries": set(),
                "company_sizes": set(),
                "contract_statuses": set(),
                "complexity_levels": set(),
                "risk_levels": set(),
                "renewal_terms": set()
            }
            
            for point in scroll_result[0]:
                payload = point.payload
                
                if payload.get('jurisdiction'):
                    unique_values["jurisdictions"].add(payload['jurisdiction'])
                if payload.get('court_level'):
                    unique_values["court_levels"].add(payload['court_level'])
                if payload.get('case_type'):
                    unique_values["case_types"].add(payload['case_type'])
                if payload.get('industry'):
                    unique_values["industries"].add(payload['industry'])
                if payload.get('company_size'):
                    unique_values["company_sizes"].add(payload['company_size'])
                if payload.get('contract_status'):
                    unique_values["contract_statuses"].add(payload['contract_status'])
                if payload.get('complexity_level'):
                    unique_values["complexity_levels"].add(payload['complexity_level'])
                if payload.get('risk_level'):
                    unique_values["risk_levels"].add(payload['risk_level'])
                if payload.get('renewal_terms'):
                    unique_values["renewal_terms"].add(payload['renewal_terms'])
            
            return {
                key: sorted(list(values)) for key, values in unique_values.items()
            }
            
        except Exception as e:
            logger.error(f"Error getting unique filter values: {str(e)}")
            return {}

# Singleton instance
advanced_qdrant_service = AdvancedQdrantService() 