from fastembed import TextEmbedding, SparseTextEmbedding
from typing import List, Dict, Any, Tuple
import logging
import numpy as np
from app.core.config import settings

logger = logging.getLogger(__name__)

class FastEmbedService:
    def __init__(self):
        # Dense embedding models for different stages
        self.dense_model = TextEmbedding(
            model_name="BAAI/bge-small-en-v1.5",  # Lightweight, fast model
            max_length=512
        )
        
        self.rerank_model = TextEmbedding(
            model_name="BAAI/bge-base-en-v1.5",   # Better quality for reranking
            max_length=512
        )
        
        # ColBERT-style multi-vector model (simulated with chunking)
        self.colbert_model = TextEmbedding(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            max_length=256  # Smaller chunks for multi-vector
        )
        
        logger.info("FastEmbed models initialized")
    
    async def get_dense_embedding(self, text: str) -> List[float]:
        """
        Generate dense embedding for initial retrieval.
        """
        try:
            cleaned_text = self._clean_text(text)
            embeddings = list(self.dense_model.embed([cleaned_text]))
            return embeddings[0].tolist()
        except Exception as e:
            logger.error(f"Error generating dense embedding: {str(e)}")
            raise
    
    async def get_rerank_embedding(self, text: str) -> List[float]:
        """
        Generate higher-quality embedding for reranking.
        """
        try:
            cleaned_text = self._clean_text(text)
            embeddings = list(self.rerank_model.embed([cleaned_text]))
            return embeddings[0].tolist()
        except Exception as e:
            logger.error(f"Error generating rerank embedding: {str(e)}")
            raise
    
    async def get_colbert_embeddings(self, text: str) -> List[List[float]]:
        """
        Generate ColBERT-style multi-vector embeddings by chunking text.
        """
        try:
            cleaned_text = self._clean_text(text)
            
            # Split text into chunks for multi-vector representation
            chunks = self._chunk_text(cleaned_text, max_chunk_size=200)
            
            # Generate embedding for each chunk
            multi_vectors = []
            for chunk in chunks[:8]:  # Limit to 8 vectors for performance
                if chunk.strip():
                    embeddings = list(self.colbert_model.embed([chunk]))
                    multi_vectors.append(embeddings[0].tolist())
            
            # Ensure we have at least one vector
            if not multi_vectors:
                # Fallback to full text if no chunks
                embeddings = list(self.colbert_model.embed([cleaned_text]))
                multi_vectors = [embeddings[0].tolist()]
            
            return multi_vectors
            
        except Exception as e:
            logger.error(f"Error generating ColBERT embeddings: {str(e)}")
            raise
    
    async def get_byte_vector(self, text: str) -> List[int]:
        """
        Generate compressed byte vector for fast prefetch.
        """
        try:
            # Get dense embedding first
            dense_embedding = await self.get_dense_embedding(text)
            
            # Convert to byte representation (quantize to 0-255)
            dense_array = np.array(dense_embedding)
            
            # Normalize to [0, 1] range
            normalized = (dense_array - dense_array.min()) / (dense_array.max() - dense_array.min())
            
            # Convert to bytes (0-255)
            byte_vector = (normalized * 255).astype(np.uint8).tolist()
            
            return byte_vector
            
        except Exception as e:
            logger.error(f"Error generating byte vector: {str(e)}")
            raise
    
    async def get_all_embeddings(self, text: str) -> Dict[str, Any]:
        """
        Generate all embedding types for a single text.
        """
        try:
            results = {}
            
            # Generate all embedding types
            results['dense'] = await self.get_dense_embedding(text)
            results['rerank'] = await self.get_rerank_embedding(text)
            results['colbert'] = await self.get_colbert_embeddings(text)
            results['byte'] = await self.get_byte_vector(text)
            
            return results
            
        except Exception as e:
            logger.error(f"Error generating all embeddings: {str(e)}")
            raise
    
    async def get_batch_embeddings(self, texts: List[str], embedding_type: str = "dense") -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batch.
        """
        try:
            cleaned_texts = [self._clean_text(text) for text in texts]
            
            if embedding_type == "dense":
                embeddings = list(self.dense_model.embed(cleaned_texts))
            elif embedding_type == "rerank":
                embeddings = list(self.rerank_model.embed(cleaned_texts))
            elif embedding_type == "colbert":
                embeddings = list(self.colbert_model.embed(cleaned_texts))
            else:
                raise ValueError(f"Unknown embedding type: {embedding_type}")
            
            return [emb.tolist() for emb in embeddings]
            
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {str(e)}")
            raise
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and prepare text for embedding generation.
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = " ".join(text.split())
        
        # Truncate to reasonable length for embedding models
        max_chars = 2000
        if len(text) > max_chars:
            text = text[:max_chars] + "..."
        
        return text
    
    def _chunk_text(self, text: str, max_chunk_size: int = 200) -> List[str]:
        """
        Split text into chunks for multi-vector embeddings.
        """
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 > max_chunk_size and current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
            else:
                current_chunk.append(word)
                current_length += len(word) + 1
        
        # Add remaining chunk
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks

# Singleton instance
fastembed_service = FastEmbedService() 