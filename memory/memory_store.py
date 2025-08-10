"""
Memory Store for Agentic E-commerce Workflow
High-level memory management for AI agents with context awareness and persistence.
"""

import logging
from typing import List, Dict, Any, Optional, Union
from datetime import datetime, timedelta
import json
import hashlib

from .chroma_index import ChromaIndex
from .security_manager import SecurityManager
from .compliance_manager import ComplianceManager

logger = logging.getLogger(__name__)

class MemoryStore:
    """
    High-level memory store for agentic e-commerce workflow.
    Provides intelligent memory management with context awareness, security, and compliance.
    """
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """Initialize MemoryStore with ChromaIndex backend, security, and compliance."""
        self.chroma_index = ChromaIndex(persist_directory)
        self.security_manager = SecurityManager()
        self.compliance_manager = ComplianceManager()
        self.logger = logging.getLogger(__name__)
        self.memory_cache = {}
        self.cache_ttl = timedelta(hours=1)
        
    def store_customer_interaction(self, 
                                 customer_id: str, 
                                 interaction_type: str, 
                                 content: str, 
                                 metadata: Optional[Dict[str, Any]] = None,
                                 user_role: str = "system") -> str:
        """
        Store customer interaction for future reference with security and compliance.
        
        Args:
            customer_id: Customer identifier
            interaction_type: Type of interaction (chat, purchase, support, etc.)
            content: Interaction content
            metadata: Additional metadata
            user_role: Role of user storing the data
            
        Returns:
            Memory ID
        """
        try:
            # Validate access permissions
            if not self.security_manager.validate_data_access(user_role, "customer_data"):
                raise PermissionError(f"Access denied for role: {user_role}")
            
            # Sanitize customer data
            sanitized_metadata = self.security_manager.sanitize_customer_data(metadata or {})
            
            # Encrypt sensitive content if required
            if self.security_manager.encryption_required:
                encrypted_content = self.security_manager.encrypt_sensitive_data(content, "customer_data")
                content = json.dumps(encrypted_content)
            
            # Create memory metadata with compliance info
            memory_metadata = {
                'type': 'customer_interaction',
                'customer_id': customer_id,
                'interaction_type': interaction_type,
                'timestamp': datetime.now().isoformat(),
                'compliance_frameworks': list(self.compliance_manager.regulations.keys()),
                'data_categories': self._categorize_data(content, metadata),
                'retention_policy': self.compliance_manager._get_retention_policy(),
                **(sanitized_metadata or {})
            }
            
            # Store in vector index
            memory_id = self.chroma_index.add_memory(content, memory_metadata)
            
            # Audit the data access
            self.security_manager.audit_data_access(
                user_id=user_role,
                user_role=user_role,
                action="write",
                data_type="customer_data",
                data_id=memory_id
            )
            
            self.logger.info(f"✅ Customer interaction stored securely: {memory_id}")
            return memory_id
            
        except Exception as e:
            self.logger.error(f"❌ Error storing customer interaction: {e}")
            return f"error_memory_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def store_product_knowledge(self, 
                              product_id: str, 
                              knowledge_type: str, 
                              content: str, 
                              metadata: Optional[Dict[str, Any]] = None,
                              user_role: str = "system") -> str:
        """
        Store product-related knowledge for AI agents with security.
        
        Args:
            product_id: Product identifier
            knowledge_type: Type of knowledge (description, review, qa, etc.)
            content: Knowledge content
            metadata: Additional metadata
            user_role: Role of user storing the data
            
        Returns:
            Memory ID
        """
        try:
            # Validate access permissions
            if not self.security_manager.validate_data_access(user_role, "product_data"):
                raise PermissionError(f"Access denied for role: {user_role}")
            
            # Sanitize data
            sanitized_metadata = self.security_manager.sanitize_customer_data(metadata or {})
            
            # Create memory metadata
            memory_metadata = {
                'type': 'product_knowledge',
                'product_id': product_id,
                'knowledge_type': knowledge_type,
                'timestamp': datetime.now().isoformat(),
                'data_categories': self._categorize_data(content, metadata),
                **(sanitized_metadata or {})
            }
            
            # Store in vector index
            memory_id = self.chroma_index.add_memory(content, memory_metadata)
            
            # Audit the data access
            self.security_manager.audit_data_access(
                user_id=user_role,
                user_role=user_role,
                action="write",
                data_type="product_data",
                data_id=memory_id
            )
            
            self.logger.info(f"✅ Product knowledge stored securely: {memory_id}")
            return memory_id
            
        except Exception as e:
            self.logger.error(f"❌ Error storing product knowledge: {e}")
            return f"error_memory_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def store_agent_decision(self, 
                           agent_type: str, 
                           decision_type: str, 
                           content: str, 
                           metadata: Optional[Dict[str, Any]] = None,
                           user_role: str = "system") -> str:
        """
        Store AI agent decisions for learning and optimization with security.
        
        Args:
            agent_type: Type of agent (sales_genie, logibot, buybot)
            decision_type: Type of decision (product_selection, pricing, etc.)
            content: Decision content
            metadata: Additional metadata
            user_role: Role of user storing the data
            
        Returns:
            Memory ID
        """
        try:
            # Validate access permissions
            if not self.security_manager.validate_data_access(user_role, "agent_data"):
                raise PermissionError(f"Access denied for role: {user_role}")
            
            # Sanitize data
            sanitized_metadata = self.security_manager.sanitize_customer_data(metadata or {})
            
            # Create memory metadata
            memory_metadata = {
                'type': 'agent_decision',
                'agent_type': agent_type,
                'decision_type': decision_type,
                'timestamp': datetime.now().isoformat(),
                'data_categories': self._categorize_data(content, metadata),
                **(sanitized_metadata or {})
            }
            
            # Store in vector index
            memory_id = self.chroma_index.add_memory(content, memory_metadata)
            
            # Audit the data access
            self.security_manager.audit_data_access(
                user_id=user_role,
                user_role=user_role,
                action="write",
                data_type="agent_data",
                data_id=memory_id
            )
            
            self.logger.info(f"✅ Agent decision stored securely: {memory_id}")
            return memory_id
            
        except Exception as e:
            self.logger.error(f"❌ Error storing agent decision: {e}")
            return f"error_memory_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def get_customer_context(self, customer_id: str, limit: int = 10, user_role: str = "system") -> List[Dict[str, Any]]:
        """
        Get customer interaction history for context with security and compliance.
        
        Args:
            customer_id: Customer identifier
            limit: Maximum number of interactions to return
            user_role: Role of user accessing the data
            
        Returns:
            List of customer interactions
        """
        try:
            # Validate access permissions
            if not self.security_manager.validate_data_access(user_role, "customer_data"):
                raise PermissionError(f"Access denied for role: {user_role}")
            
            # Check data retention
            filter_metadata = {
                'type': 'customer_interaction',
                'customer_id': customer_id
            }
            
            memories = self.chroma_index.search_memory(
                query=f"customer {customer_id} interactions",
                n_results=limit,
                filter_metadata=filter_metadata
            )
            
            # Filter out expired data
            valid_memories = []
            for memory in memories:
                timestamp = memory['metadata'].get('timestamp', '')
                if timestamp and self.security_manager.check_data_retention(timestamp):
                    # Decrypt content if needed
                    if self.security_manager.encryption_required and memory.get('content'):
                        try:
                            # Check if content is already encrypted (JSON format)
                            if isinstance(memory['content'], str) and memory['content'].startswith('{'):
                                encrypted_content = json.loads(memory['content'])
                                if 'encrypted_data' in encrypted_content:
                                    memory['content'] = self.security_manager.decrypt_sensitive_data(encrypted_content)
                        except (json.JSONDecodeError, KeyError, Exception) as e:
                            # Content is not encrypted, use as-is
                            self.logger.debug(f"Content not encrypted, using as-is: {e}")
                    valid_memories.append(memory)
                else:
                    if timestamp:
                        self.logger.info(f"⚠️ Expired memory filtered out: {memory['memory_id']}")
            
            # Audit the data access
            self.security_manager.audit_data_access(
                user_id=user_role,
                user_role=user_role,
                action="read",
                data_type="customer_data",
                data_id=customer_id
            )
            
            self.logger.info(f"✅ Retrieved {len(valid_memories)} customer interactions securely")
            return valid_memories
            
        except PermissionError:
            # Re-raise PermissionError for proper access control testing
            raise
        except Exception as e:
            self.logger.error(f"❌ Error retrieving customer context: {e}")
            return []
    
    def get_product_knowledge(self, product_id: str, knowledge_type: Optional[str] = None, 
                            user_role: str = "system") -> List[Dict[str, Any]]:
        """
        Get product knowledge for AI agents with security.
        
        Args:
            product_id: Product identifier
            knowledge_type: Optional knowledge type filter
            user_role: Role of user accessing the data
            
        Returns:
            List of product knowledge entries
        """
        try:
            # Validate access permissions
            if not self.security_manager.validate_data_access(user_role, "product_data"):
                raise PermissionError(f"Access denied for role: {user_role}")
            
            filter_metadata = {
                'type': 'product_knowledge',
                'product_id': product_id
            }
            
            if knowledge_type:
                filter_metadata['knowledge_type'] = knowledge_type
            
            memories = self.chroma_index.search_memory(
                query=f"product {product_id} knowledge",
                n_results=20,
                filter_metadata=filter_metadata
            )
            
            # Audit the data access
            self.security_manager.audit_data_access(
                user_id=user_role,
                user_role=user_role,
                action="read",
                data_type="product_data",
                data_id=product_id
            )
            
            self.logger.info(f"✅ Retrieved {len(memories)} product knowledge entries securely")
            return memories
            
        except Exception as e:
            self.logger.error(f"❌ Error retrieving product knowledge: {e}")
            return []
    
    def get_agent_insights(self, agent_type: str, decision_type: Optional[str] = None, 
                          user_role: str = "system") -> List[Dict[str, Any]]:
        """
        Get agent decision history for insights and optimization with security.
        
        Args:
            agent_type: Type of agent
            decision_type: Optional decision type filter
            user_role: Role of user accessing the data
            
        Returns:
            List of agent decisions
        """
        try:
            # Validate access permissions
            if not self.security_manager.validate_data_access(user_role, "agent_data"):
                raise PermissionError(f"Access denied for role: {user_role}")
            
            filter_metadata = {
                'type': 'agent_decision',
                'agent_type': agent_type
            }
            
            if decision_type:
                filter_metadata['decision_type'] = decision_type
            
            memories = self.chroma_index.search_memory(
                query=f"agent {agent_type} decisions",
                n_results=20,
                filter_metadata=filter_metadata
            )
            
            # Audit the data access
            self.security_manager.audit_data_access(
                user_id=user_role,
                user_role=user_role,
                action="read",
                data_type="agent_data",
                data_id=agent_type
            )
            
            self.logger.info(f"✅ Retrieved {len(memories)} agent decisions securely")
            return memories
            
        except Exception as e:
            self.logger.error(f"❌ Error retrieving agent insights: {e}")
            return []
    
    def search_similar_experiences(self, query: str, context_type: Optional[str] = None, 
                                 user_role: str = "system") -> List[Dict[str, Any]]:
        """
        Search for similar past experiences across all memory types with security.
        
        Args:
            query: Search query
            context_type: Optional context type filter
            user_role: Role of user accessing the data
            
        Returns:
            List of similar experiences
        """
        try:
            # Validate access permissions for the context type
            if context_type and not self.security_manager.validate_data_access(user_role, f"{context_type}_data"):
                raise PermissionError(f"Access denied for role: {user_role}")
            
            filter_metadata = {}
            if context_type:
                filter_metadata['type'] = context_type
            
            memories = self.chroma_index.search_memory(
                query=query,
                n_results=10,
                filter_metadata=filter_metadata if filter_metadata else None
            )
            
            # Audit the data access
            self.security_manager.audit_data_access(
                user_id=user_role,
                user_role=user_role,
                action="read",
                data_type=context_type or "general",
                data_id="search"
            )
            
            self.logger.info(f"✅ Found {len(memories)} similar experiences securely")
            return memories
            
        except Exception as e:
            self.logger.error(f"❌ Error searching similar experiences: {e}")
            return []
    
    def get_memory_summary(self, memory_type: Optional[str] = None, user_role: str = "system") -> Dict[str, Any]:
        """
        Get summary statistics about stored memories with security.
        
        Args:
            memory_type: Optional memory type filter
            user_role: Role of user accessing the data
            
        Returns:
            Memory summary statistics
        """
        try:
            # Validate access permissions
            if not self.security_manager.validate_data_access(user_role, "system_data"):
                raise PermissionError(f"Access denied for role: {user_role}")
            
            stats = self.chroma_index.get_memory_stats()
            
            # Add type-specific statistics if requested
            if memory_type:
                filter_metadata = {'type': memory_type}
                memories = self.chroma_index.search_memory(
                    query=f"{memory_type} memories",
                    n_results=1000,
                    filter_metadata=filter_metadata
                )
                stats[f'{memory_type}_count'] = len(memories)
            
            # Audit the data access
            self.security_manager.audit_data_access(
                user_id=user_role,
                user_role=user_role,
                action="read",
                data_type="system_data",
                data_id="summary"
            )
            
            return stats
            
        except Exception as e:
            self.logger.error(f"❌ Error getting memory summary: {e}")
            return {'error': str(e)}
    
    def update_memory(self, memory_id: str, content: str, metadata: Dict[str, Any], 
                     user_role: str = "system") -> bool:
        """Update an existing memory entry with security."""
        try:
            # Validate access permissions
            if not self.security_manager.validate_data_access(user_role, "system_data"):
                raise PermissionError(f"Access denied for role: {user_role}")
            
            # Sanitize metadata
            sanitized_metadata = self.security_manager.sanitize_customer_data(metadata)
            
            # Encrypt content if required
            if self.security_manager.encryption_required:
                encrypted_content = self.security_manager.encrypt_sensitive_data(content, "customer_data")
                content = json.dumps(encrypted_content)
            
            success = self.chroma_index.update_memory(memory_id, content, sanitized_metadata)
            
            if success:
                # Audit the data access
                self.security_manager.audit_data_access(
                    user_id=user_role,
                    user_role=user_role,
                    action="update",
                    data_type="system_data",
                    data_id=memory_id
                )
                self.logger.info(f"✅ Memory updated securely: {memory_id}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"❌ Error updating memory: {e}")
            return False
    
    def delete_memory(self, memory_id: str, user_role: str = "system") -> bool:
        """Delete a memory entry with security."""
        try:
            # Validate access permissions
            if not self.security_manager.validate_data_access(user_role, "system_data"):
                raise PermissionError(f"Access denied for role: {user_role}")
            
            success = self.chroma_index.delete_memory(memory_id)
            
            if success:
                # Audit the data access
                self.security_manager.audit_data_access(
                    user_id=user_role,
                    user_role=user_role,
                    action="delete",
                    data_type="system_data",
                    data_id=memory_id
                )
                self.logger.info(f"✅ Memory deleted securely: {memory_id}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"❌ Error deleting memory: {e}")
            return False
    
    def get_memory_by_id(self, memory_id: str, user_role: str = "system") -> Optional[Dict[str, Any]]:
        """Retrieve a specific memory by ID with security."""
        try:
            # Validate access permissions - use customer_data for customer interactions
            if not self.security_manager.validate_data_access(user_role, "customer_data"):
                raise PermissionError(f"Access denied for role: {user_role}")
            
            memory = self.chroma_index.get_memory_by_id(memory_id)
            
            if memory:
                # Decrypt content if needed and if it's actually encrypted
                if self.security_manager.encryption_required and memory.get('content'):
                    try:
                        # Check if content is already encrypted (JSON format)
                        if isinstance(memory['content'], str) and memory['content'].startswith('{'):
                            encrypted_content = json.loads(memory['content'])
                            if 'encrypted_data' in encrypted_content:
                                memory['content'] = self.security_manager.decrypt_sensitive_data(encrypted_content)
                    except (json.JSONDecodeError, KeyError, Exception) as e:
                        # Content is not encrypted, use as-is
                        self.logger.debug(f"Content not encrypted, using as-is: {e}")
                
                # Audit the data access
                self.security_manager.audit_data_access(
                    user_id=user_role,
                    user_role=user_role,
                    action="read",
                    data_type="customer_data",
                    data_id=memory_id
                )
                self.logger.info(f"✅ Memory retrieved securely: {memory_id}")
            
            return memory
            
        except Exception as e:
            self.logger.error(f"❌ Error retrieving memory: {e}")
            return None
    
    def clear_old_memories(self, days_old: int = 90, user_role: str = "system") -> int:
        """
        Clear memories older than specified days with security and compliance.
        
        Args:
            days_old: Age threshold in days
            user_role: Role of user performing the operation
            
        Returns:
            Number of memories cleared
        """
        try:
            # Validate access permissions
            if not self.security_manager.validate_data_access(user_role, "system_data"):
                raise PermissionError(f"Access denied for role: {user_role}")
            
            cutoff_date = datetime.now() - timedelta(days=days_old)
            cutoff_iso = cutoff_date.isoformat()
            
            # This would require implementing date-based filtering in ChromaIndex
            # For now, return a placeholder
            self.logger.info(f"⚠️ Clear old memories not implemented yet")
            
            # Audit the operation
            self.security_manager.audit_data_access(
                user_id=user_role,
                user_role=user_role,
                action="delete",
                data_type="system_data",
                data_id="bulk_clear"
            )
            
            return 0
            
        except Exception as e:
            self.logger.error(f"❌ Error clearing old memories: {e}")
            return 0
    
    def _categorize_data(self, content: str, metadata: Optional[Dict[str, Any]]) -> List[str]:
        """Categorize data based on content and metadata."""
        categories = []
        
        # Check content for sensitive information
        sensitive_keywords = {
            "personal_data": ["email", "phone", "address", "name", "ssn", "credit"],
            "transactional_data": ["purchase", "order", "payment", "transaction"],
            "behavioral_data": ["preference", "browsing", "interaction", "click"],
            "technical_data": ["ip", "device", "cookie", "log", "session"]
        }
        
        content_lower = content.lower()
        for category, keywords in sensitive_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                categories.append(category)
        
        # Check metadata for additional categories
        if metadata:
            for key, value in metadata.items():
                if key in ["customer_id", "user_id"]:
                    categories.append("personal_data")
                elif key in ["order_id", "transaction_id"]:
                    categories.append("transactional_data")
        
        return list(set(categories)) if categories else ["general"]
