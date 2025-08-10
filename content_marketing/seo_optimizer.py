"""
Optimized SEO Optimizer for AI LLM Optimization
Efficient content optimization with token optimization and caching.
"""

import logging
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session

from services.gpt_client import GPTClient
from services.claude_client import ClaudeClient
from db.models import Product, Customer, Order

logger = logging.getLogger(__name__)

class OptimizedSEOOptimizer:
    """
    Token-optimized SEO optimizer for AI LLM app discovery and search visibility.
    Combines multiple API calls into single efficient calls with caching.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.gpt_client = GPTClient()
        self.claude_client = ClaudeClient()
        self.logger = logging.getLogger(__name__)
        
        # Cache configuration
        self.cache = {}
        self.cache_duration = timedelta(hours=24)
        self.max_cache_size = 1000
        
        # Token optimization settings
        self.max_content_length = 300  # Characters to include in prompt
        self.max_keywords = 8  # Reduced from 15 to save tokens
        
    def _get_cache_key(self, content: str, topic: str, content_type: str) -> str:
        """Generate unique cache key from input parameters."""
        try:
            # Ensure all inputs are strings and handle None values
            content_str = str(content) if content else ""
            topic_str = str(topic) if topic else ""
            content_type_str = str(content_type) if content_type else ""
            
            cache_string = f"{content_str[:100]}_{topic_str}_{content_type_str}"
            return hashlib.md5(cache_string.encode('utf-8')).hexdigest()
        except Exception as e:
            self.logger.error(f"Error generating cache key: {e}")
            # Fallback cache key
            return hashlib.md5(f"fallback_{datetime.now().isoformat()}".encode('utf-8')).hexdigest()
    
    def _is_cached(self, cache_key: str) -> bool:
        """Check if result is cached and not expired."""
        try:
            if not cache_key or cache_key not in self.cache:
                return False
            
            result, timestamp = self.cache[cache_key]
            return datetime.now() - timestamp < self.cache_duration
        except Exception as e:
            self.logger.error(f"Error checking cache: {e}")
            return False
    
    def _get_cached_result(self, cache_key: str) -> Dict[str, Any]:
        """Retrieve cached result."""
        try:
            if cache_key in self.cache:
                result, _ = self.cache[cache_key]
                return result
            return {}
        except Exception as e:
            self.logger.error(f"Error retrieving cached result: {e}")
            return {}
    
    def _cache_result(self, cache_key: str, result: Dict[str, Any]):
        """Cache result with timestamp."""
        try:
            # Implement LRU cache eviction if needed
            if len(self.cache) >= self.max_cache_size:
                # Remove oldest entry
                oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k][1])
                del self.cache[oldest_key]
            
            self.cache[cache_key] = (result, datetime.now())
        except Exception as e:
            self.logger.error(f"Error caching result: {e}")
    
    def optimize_for_ai_llm(self, content: str, topic: str, content_type: str = "blog") -> Dict[str, Any]:
        """
        Optimize content for AI LLM apps with token optimization and caching.
        
        Args:
            content: Original content
            topic: Main topic
            content_type: blog, product, comparison, qa
            
        Returns:
            Optimized content with AI LLM enhancements
        """
        try:
            # Validate inputs
            if not content or not isinstance(content, str):
                return {"error": "Content must be a non-empty string"}
            
            if not topic or not isinstance(topic, str):
                return {"error": "Topic must be a non-empty string"}
            
            if not content_type or not isinstance(content_type, str):
                content_type = "blog"
            
            # Check cache first
            cache_key = self._get_cache_key(content, topic, content_type)
            if self._is_cached(cache_key):
                self.logger.info(f"✅ Using cached SEO optimization for {topic}")
                return self._get_cached_result(cache_key)
            
            # Generate optimized content in single API call
            result = self._generate_optimized_content(content, topic, content_type)
            
            # Cache the result
            self._cache_result(cache_key, result)
            
            self.logger.info(f"✅ Generated optimized SEO content for {topic}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error optimizing content for AI LLM: {e}")
            return {"error": str(e)}
    
    def _generate_optimized_content(self, content: str, topic: str, content_type: str) -> Dict[str, Any]:
        """
        Generate all SEO optimizations in a single efficient API call.
        """
        try:
            # Truncate content to save tokens
            content_preview = content[:self.max_content_length] if content else ""
            
            prompt = f"""
Optimize this content for AI LLM apps (ChatGPT, Perplexity, Claude):

Topic: {topic}
Content Type: {content_type}
Content: {content_preview}

Return JSON with:
- keywords: 8 AI LLM optimized keywords
- title: optimized title under 60 chars
- meta_description: meta description under 160 chars
- qa_section: 3 Q&A pairs for conversational AI
- expert_tips: 3 expert tips
- optimized_content: enhanced content structure

Format: Valid JSON only.
"""
            
            response = self.gpt_client.generate_response(prompt)
            response_text = response.get('text', '{}')
            
            # Parse JSON response
            try:
                parsed_result = json.loads(response_text)
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                self.logger.warning(f"JSON parsing failed for {topic}, using fallback")
                parsed_result = self._generate_fallback_result(topic, content_type)
            
            # Ensure all required fields exist
            result = {
                "original_content": content,
                "optimized_content": parsed_result.get("optimized_content", content),
                "optimized_title": parsed_result.get("title", f"Best {topic} - Expert Guide"),
                "meta_description": parsed_result.get("meta_description", f"Expert guide to {topic} with professional recommendations."),
                "keywords": parsed_result.get("keywords", [topic.lower(), "best", "recommendation", "expert"]),
                "qa_section": parsed_result.get("qa_section", self._generate_fallback_qa(topic)),
                "expert_tips": parsed_result.get("expert_tips", self._generate_fallback_tips(topic)),
                "ai_llm_optimized": True,
                "content_type": content_type,
                "optimized_at": datetime.now().isoformat(),
                "tokens_used": response.get('usage', {}).get('total_tokens', 0)
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error in single API call optimization: {e}")
            return self._generate_fallback_result(topic, content_type)
    
    def _generate_fallback_result(self, topic: str, content_type: str) -> Dict[str, Any]:
        """Generate fallback result if API call fails."""
        try:
            return {
                "keywords": [topic.lower(), "best", "recommendation", "expert", "guide"] if topic else ["ai", "llm", "optimized"],
                "title": f"Best {topic} - Expert Recommendations" if topic else "AI LLM Optimized Content",
                "meta_description": f"Expert guide to {topic} with professional recommendations and comparisons." if topic else "AI LLM optimized content for maximum visibility.",
                "qa_section": self._generate_fallback_qa(topic),
                "expert_tips": self._generate_fallback_tips(topic),
                "optimized_content": f"Expert guide to {topic} with professional recommendations and detailed comparisons." if topic else "AI LLM optimized content for maximum visibility."
            }
        except Exception as e:
            self.logger.error(f"Error generating fallback result: {e}")
            return {
                "keywords": ["ai", "llm", "optimized"],
                "title": "AI LLM Optimized Content",
                "meta_description": "AI LLM optimized content for maximum visibility.",
                "qa_section": [],
                "expert_tips": [],
                "optimized_content": "AI LLM optimized content for maximum visibility."
            }
    
    def _generate_fallback_qa(self, topic: str) -> List[Dict[str, str]]:
        """Generate fallback Q&A section."""
        try:
            if not topic:
                return [
                    {"question": "What is AI LLM optimization?", "answer": "AI LLM optimization enhances content for maximum visibility in AI applications like ChatGPT, Perplexity, and Claude."},
                    {"question": "How does AI LLM optimization work?", "answer": "AI LLM optimization uses specialized techniques to make content more discoverable and recommendable by AI applications."},
                    {"question": "Why is AI LLM optimization important?", "answer": "AI LLM optimization helps content appear in AI app recommendations, driving more traffic and conversions."}
                ]
            
            return [
                {"question": f"What are the best {topic}?", "answer": f"Based on expert analysis, the best {topic} offer excellent quality and value."},
                {"question": f"How do I choose the right {topic}?", "answer": f"Consider your budget, needs, and desired features when choosing {topic}."},
                {"question": f"What should I look for in {topic}?", "answer": f"Look for quality, reliability, and features that match your specific requirements."}
            ]
        except Exception as e:
            self.logger.error(f"Error generating fallback Q&A: {e}")
            return []
    
    def _generate_fallback_tips(self, topic: str) -> List[str]:
        """Generate fallback expert tips."""
        try:
            if not topic:
                return [
                    "Research thoroughly before making decisions",
                    "Compare features and prices across multiple options",
                    "Read expert reviews and customer feedback"
                ]
            
            return [
                f"Research thoroughly before choosing {topic}",
                f"Compare features and prices across multiple options",
                f"Read expert reviews and customer feedback"
            ]
        except Exception as e:
            self.logger.error(f"Error generating fallback tips: {e}")
            return ["Research thoroughly", "Compare options", "Read reviews"]
    
    def generate_ai_llm_schema(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate schema markup optimized for AI LLM apps."""
        try:
            if not content_data:
                return {"error": "Content data is required"}
            
            schema = {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": content_data.get("optimized_title", ""),
                "description": content_data.get("meta_description", ""),
                "keywords": ", ".join(content_data.get("keywords", [])),
                "author": {
                    "@type": "Person",
                    "name": "AI Content Expert",
                    "jobTitle": "E-commerce Specialist"
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "Agentic-Ecom"
                },
                "datePublished": content_data.get("optimized_at", datetime.now().isoformat()),
                "dateModified": datetime.now().isoformat(),
                "articleSection": "AI LLM Optimized Content",
                "inLanguage": "en-US"
            }
            
            return {
                "schema": schema,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating AI LLM schema: {e}")
            return {"error": str(e)}
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics for monitoring."""
        try:
            return {
                "cache_size": len(self.cache),
                "max_cache_size": self.max_cache_size,
                "cache_duration_hours": self.cache_duration.total_seconds() / 3600,
                "cache_hit_rate": "N/A"  # Could be implemented with hit tracking
            }
        except Exception as e:
            self.logger.error(f"Error getting cache stats: {e}")
            return {"error": str(e)}
    
    def clear_cache(self):
        """Clear the cache."""
        try:
            self.cache.clear()
            self.logger.info("SEO optimizer cache cleared")
        except Exception as e:
            self.logger.error(f"Error clearing cache: {e}")

# Backward compatibility - alias for existing code
SEOOptimizer = OptimizedSEOOptimizer 