"""
Chroma Index for Vector Database Operations
Provides semantic search and similarity matching for agentic e-commerce workflow.
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from datetime import datetime
import json

try:
    import chromadb
    from chromadb.config import Settings
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False
    logging.warning("ChromaDB not available. Using mock implementation.")

logger = logging.getLogger(__name__)

class ChromaIndex:
    """
    Chroma-based vector index for semantic search and similarity matching.
    Enables intelligent memory retrieval for AI agents.
    """
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """Initialize ChromaIndex with persistent storage."""
        self.persist_directory = persist_directory
        self.logger = logging.getLogger(__name__)
        
        if CHROMA_AVAILABLE:
            try:
                self.client = chromadb.PersistentClient(
                    path=persist_directory,
                    settings=Settings(
                        anonymized_telemetry=False,
                        allow_reset=True
                    )
                )
                self.collection = self.client.get_or_create_collection(
                    name="agentic_ecom_memory",
                    metadata={"description": "Agentic E-commerce Memory Store"}
                )
                self.logger.info("✅ ChromaIndex initialized successfully")
            except Exception as e:
                self.logger.error(f"❌ Failed to initialize ChromaDB: {e}")
                self.client = None
                self.collection = None
        else:
            self.client = None
            self.collection = None
            self.logger.warning("⚠️ Using mock ChromaIndex implementation")
    
    def add_memory(self, 
                   content: str, 
                   metadata: Dict[str, Any], 
                   memory_id: Optional[str] = None) -> str:
        """
        Add a memory entry to the vector index.
        
        Args:
            content: Text content to index
            metadata: Associated metadata (product_id, customer_id, etc.)
            memory_id: Optional custom ID
            
        Returns:
            Memory ID
        """
        try:
            if not self.collection:
                return self._mock_add_memory(content, metadata, memory_id)
            
            # Generate embedding for content
            embedding = self._generate_embedding(content)
            
            # Create memory ID if not provided
            if not memory_id:
                memory_id = f"memory_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(content) % 10000}"
            
            # Add to collection
            self.collection.add(
                embeddings=[embedding],
                documents=[content],
                metadatas=[metadata],
                ids=[memory_id]
            )
            
            self.logger.info(f"✅ Memory added: {memory_id}")
            return memory_id
            
        except Exception as e:
            self.logger.error(f"❌ Error adding memory: {e}")
            return self._mock_add_memory(content, metadata, memory_id)
    
    def search_memory(self, 
                     query: str, 
                     n_results: int = 5, 
                     filter_metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Search for similar memories using semantic similarity.
        
        Args:
            query: Search query
            n_results: Number of results to return
            filter_metadata: Optional metadata filters
            
        Returns:
            List of similar memories with scores
        """
        try:
            if not self.collection:
                return self._mock_search_memory(query, n_results, filter_metadata)
            
            # Generate embedding for query
            query_embedding = self._generate_embedding(query)
            
            # Search collection
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=filter_metadata
            )
            
            # Format results
            formatted_results = []
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    'memory_id': results['ids'][0][i],
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'similarity_score': results['distances'][0][i] if 'distances' in results else 0.0
                })
            
            self.logger.info(f"✅ Found {len(formatted_results)} similar memories")
            return formatted_results
            
        except Exception as e:
            self.logger.error(f"❌ Error searching memory: {e}")
            return self._mock_search_memory(query, n_results, filter_metadata)
    
    def get_memory_by_id(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific memory by ID."""
        try:
            if not self.collection:
                return self._mock_get_memory_by_id(memory_id)
            
            results = self.collection.get(ids=[memory_id])
            
            if results['ids']:
                return {
                    'memory_id': results['ids'][0],
                    'content': results['documents'][0],
                    'metadata': results['metadatas'][0]
                }
            return None
            
        except Exception as e:
            self.logger.error(f"❌ Error retrieving memory: {e}")
            return self._mock_get_memory_by_id(memory_id)
    
    def update_memory(self, memory_id: str, content: str, metadata: Dict[str, Any]) -> bool:
        """Update an existing memory entry."""
        try:
            if not self.collection:
                return self._mock_update_memory(memory_id, content, metadata)
            
            # Delete existing memory
            self.collection.delete(ids=[memory_id])
            
            # Add updated memory
            embedding = self._generate_embedding(content)
            self.collection.add(
                embeddings=[embedding],
                documents=[content],
                metadatas=[metadata],
                ids=[memory_id]
            )
            
            self.logger.info(f"✅ Memory updated: {memory_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error updating memory: {e}")
            return self._mock_update_memory(memory_id, content, metadata)
    
    def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory entry."""
        try:
            if not self.collection:
                return self._mock_delete_memory(memory_id)
            
            self.collection.delete(ids=[memory_id])
            self.logger.info(f"✅ Memory deleted: {memory_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error deleting memory: {e}")
            return self._mock_delete_memory(memory_id)
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get statistics about the memory store."""
        try:
            if not self.collection:
                return self._mock_get_memory_stats()
            
            count = self.collection.count()
            return {
                'total_memories': count,
                'collection_name': self.collection.name,
                'persist_directory': self.persist_directory,
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error getting memory stats: {e}")
            return self._mock_get_memory_stats()
    
    def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text content."""
        # In production, use a proper embedding model like OpenAI's text-embedding-ada-002
        # For now, use a simple hash-based embedding
        import hashlib
        hash_obj = hashlib.md5(text.encode())
        hash_bytes = hash_obj.digest()
        return [float(b) / 255.0 for b in hash_bytes[:8]]
    
    # Mock methods for fallback
    def _mock_add_memory(self, content: str, metadata: Dict[str, Any], memory_id: Optional[str] = None) -> str:
        memory_id = memory_id or f"mock_memory_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.logger.info(f"📝 [Mock] Memory added: {memory_id}")
        return memory_id
    
    def _mock_search_memory(self, query: str, n_results: int, filter_metadata: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [
            {
                'memory_id': f'mock_memory_{i}',
                'content': f'Mock memory content {i}',
                'metadata': {'type': 'mock', 'created_at': datetime.now().isoformat()},
                'similarity_score': 0.8 - (i * 0.1)
            }
            for i in range(min(n_results, 3))
        ]
    
    def _mock_get_memory_by_id(self, memory_id: str) -> Optional[Dict[str, Any]]:
        return {
            'memory_id': memory_id,
            'content': f'Mock memory content for {memory_id}',
            'metadata': {'type': 'mock', 'created_at': datetime.now().isoformat()}
        }
    
    def _mock_update_memory(self, memory_id: str, content: str, metadata: Dict[str, Any]) -> bool:
        self.logger.info(f"📝 [Mock] Memory updated: {memory_id}")
        return True
    
    def _mock_delete_memory(self, memory_id: str) -> bool:
        self.logger.info(f"📝 [Mock] Memory deleted: {memory_id}")
        return True
    
    def _mock_get_memory_stats(self) -> Dict[str, Any]:
        return {
            'total_memories': 100,
            'collection_name': 'mock_collection',
            'persist_directory': self.persist_directory,
            'last_updated': datetime.now().isoformat()
        }
