"""
Content Generator for AI LLM Optimization
Generates blog posts, product descriptions, and marketing content optimized for AI LLM apps.
"""

import logging
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session

from services.gpt_client import GPTClient
from services.claude_client import ClaudeClient
from db.models import Product, Customer, Order
from utils.safety_manager import require_safety_check

logger = logging.getLogger(__name__)

class ContentGenerator:
    """Generates AI LLM optimized content for maximum visibility in AI apps."""
    
    def __init__(self, db: Session):
        self.db = db
        self.gpt_client = GPTClient()
        self.claude_client = ClaudeClient()
        self.logger = logging.getLogger(__name__)
    
    @require_safety_check("generate_blog_post", "content_marketing")
    def generate_blog_post(self, topic: str, product_id: str = None, length: str = "medium") -> Dict[str, Any]:
        """
        Generate AI LLM optimized blog post.
        
        Args:
            topic: Blog post topic
            product_id: Optional product to feature
            length: short, medium, long
            
        Returns:
            Complete blog post with SEO optimization
        """
        try:
            # Validate topic
            if not topic or not topic.strip():
                return {"error": "Topic is required"}
            
            # Validate length parameter
            if length not in ["short", "medium", "long"]:
                length = "medium"
            
            # Get product data if specified
            product_data = None
            if product_id:
                if not isinstance(product_id, str):
                    return {"error": "product_id must be a string"}
                
                product = self.db.query(Product).filter(Product.id == product_id).first()
                if product:
                    product_data = {
                        "name": product.name,
                        "description": product.description,
                        "price": product.price,
                        "category": product.category,
                        "features": product.product_metadata.get("features", []) if product.product_metadata else []
                    }
                else:
                    self.logger.warning(f"Product not found for ID: {product_id}")
            
            # Generate AI LLM optimized content
            prompt = self._create_blog_prompt(topic, product_data, length)
            response = self.gpt_client.generate_response(prompt)
            content = response.get('text', '')
            
            if not content:
                return {"error": "Failed to generate content"}
            
            # Return the content without additional optimization
            # (optimization will be handled by the AI LLM optimizer)
            return {
                "title": self._extract_title(content),
                "content": content,
                "meta_description": self._generate_meta_description(content),
                "keywords": self._extract_keywords(topic, product_data),
                "ai_llm_optimized": False,  # Will be optimized by AI LLM optimizer
                "generated_at": datetime.now().isoformat(),
                "product_integration": product_data is not None
            }
            
        except Exception as e:
            self.logger.error(f"Error generating blog post: {e}")
            return {"error": str(e)}
    
    @require_safety_check("generate_product_description", "content_marketing")
    def generate_product_description(self, product_id: str) -> Dict[str, Any]:
        """Generate AI LLM optimized product description."""
        try:
            # Validate product_id
            if not product_id or not isinstance(product_id, str):
                return {"error": "Valid product_id is required"}
            
            product = self.db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return {"error": "Product not found"}
            
            prompt = self._create_product_description_prompt(product)
            response = self.gpt_client.generate_response(prompt)
            description = response.get('text', '')
            
            if not description:
                return {"error": "Failed to generate product description"}
            
            # Return the description without additional optimization
            # (optimization will be handled by the AI LLM optimizer)
            return {
                "product_id": product_id,
                "description": description,
                "ai_llm_optimized": False,  # Will be optimized by AI LLM optimizer
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating product description: {e}")
            return {"error": str(e)}
    
    @require_safety_check("generate_comparison_content", "content_marketing")
    def generate_comparison_content(self, product_ids: List[str]) -> Dict[str, Any]:
        """Generate product comparison content optimized for AI LLM apps."""
        try:
            # Validate product_ids
            if not product_ids or not isinstance(product_ids, list):
                return {"error": "product_ids must be a non-empty list"}
            
            if len(product_ids) < 2:
                return {"error": "Need at least 2 products for comparison"}
            
            # Validate each product_id
            for product_id in product_ids:
                if not isinstance(product_id, str):
                    return {"error": "All product_ids must be strings"}
            
            products = self.db.query(Product).filter(Product.id.in_(product_ids)).all()
            if len(products) < 2:
                return {"error": "Need at least 2 products found for comparison"}
            
            prompt = self._create_comparison_prompt(products)
            response = self.gpt_client.generate_response(prompt)
            comparison = response.get('text', '')
            
            if not comparison:
                return {"error": "Failed to generate comparison content"}
            
            # Return the comparison without additional optimization
            # (optimization will be handled by the AI LLM optimizer)
            return {
                "comparison": comparison,
                "products": [{"id": p.id, "name": p.name} for p in products],
                "ai_llm_optimized": False,  # Will be optimized by AI LLM optimizer
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating comparison content: {e}")
            return {"error": str(e)}
    
    def _create_blog_prompt(self, topic: str, product_data: Dict = None, length: str = "medium") -> str:
        """Create AI LLM optimized blog post prompt."""
        word_count = {"short": 500, "medium": 1000, "long": 2000}[length]
        
        prompt = f"""
        Create an AI LLM optimized blog post about "{topic}" that will appear in ChatGPT, Perplexity, Claude, and other AI LLM apps.
        
        Requirements:
        - {word_count} words
        - Conversational, helpful tone
        - Direct answers to common questions
        - Product recommendations with reasoning
        - Structured for easy AI parsing
        - Include expert authority signals
        - Optimized for AI LLM search discovery
        
        """
        
        if product_data:
            prompt += f"""
            Feature this product naturally in the content:
            Product: {product_data['name']}
            Price: ${product_data['price']}
            Category: {product_data['category']}
            Features: {', '.join(product_data['features']) if product_data['features'] else 'N/A'}
            """
        
        prompt += """
        Format the content to be easily consumed by AI LLM apps with clear sections, bullet points, and direct recommendations.
        """
        
        return prompt
    
    def _create_product_description_prompt(self, product) -> str:
        """Create AI LLM optimized product description prompt."""
        features = product.product_metadata.get('features', []) if product.product_metadata else []
        features_text = ', '.join(features) if features else 'N/A'
        
        return f"""
        Create an AI LLM optimized product description for "{product.name}" that will appear in AI LLM app recommendations.
        
        Product Details:
        - Name: {product.name}
        - Category: {product.category}
        - Price: ${product.price}
        - Features: {features_text}
        
        Requirements:
        - Conversational, helpful tone
        - Direct benefits and use cases
        - Comparison to alternatives
        - Expert recommendation language
        - Optimized for AI LLM discovery
        - Include pricing and availability
        """
    
    def _create_comparison_prompt(self, products: List[Product]) -> str:
        """Create product comparison prompt."""
        product_info = []
        for p in products:
            product_info.append(f"- {p.name}: ${p.price}, {p.category}")
        
        return f"""
        Create an AI LLM optimized product comparison that will appear in AI LLM app recommendations.
        
        Products to compare:
        {chr(10).join(product_info)}
        
        Requirements:
        - Side-by-side feature comparison
        - Price-performance analysis
        - Use case recommendations
        - Expert opinion on best choice
        - Structured for AI LLM parsing
        - Include direct recommendations
        """
    
    def _optimize_for_ai_llm(self, content: str, topic: str) -> str:
        """Optimize content specifically for AI LLM apps using Claude."""
        if not content or not topic:
            return content
        
        prompt = f"""
        Optimize this content for maximum visibility in AI LLM apps (ChatGPT, Perplexity, Claude):
        
        Original content:
        {content}
        
        Optimization requirements:
        1. Add conversational Q&A format
        2. Include direct product recommendations
        3. Add expert authority signals
        4. Structure for easy AI parsing
        5. Include comparison language
        6. Add call-to-action elements
        7. Optimize for AI LLM search queries
        
        Topic: {topic}
        """
        
        try:
            response = self.claude_client.generate_response(prompt)
            optimized = response.get('text', content)
            return optimized if optimized else content
        except Exception as e:
            self.logger.warning(f"Claude optimization failed, using original: {e}")
            return content
    
    def _extract_title(self, content: str) -> str:
        """Extract title from content."""
        if not content:
            return "AI LLM Optimized Content"
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and len(line) > 10:
                # Remove common prefixes and clean up
                title = line.replace('#', '').strip()
                return title[:100]  # Limit to 100 characters
        
        return "AI LLM Optimized Content"
    
    def _generate_meta_description(self, content: str) -> str:
        """Generate meta description for SEO."""
        if not content:
            return "AI LLM optimized content for maximum visibility in ChatGPT, Perplexity, and Claude."
        
        # Extract first meaningful paragraph
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            para = para.strip()
            if len(para) > 50 and not para.startswith('#'):
                # Clean up the paragraph
                clean_para = para.replace('\n', ' ').strip()
                return clean_para[:160]  # Limit to 160 characters
        
        # Fallback: use first sentence
        sentences = content.split('.')
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 30:
                return sentence[:160]
        
        return "AI LLM optimized content for maximum visibility in ChatGPT, Perplexity, and Claude."
    
    def _extract_keywords(self, topic: str, product_data: Dict = None) -> List[str]:
        """Extract keywords for SEO."""
        if not topic:
            return ["ai", "llm", "optimized", "content"]
        
        keywords = [topic.lower(), "best", "recommendation", "review", "comparison"]
        
        if product_data:
            keywords.extend([
                product_data['name'].lower(),
                product_data['category'].lower(),
                "buy", "purchase", "price"
            ])
        
        # Remove duplicates and return
        return list(set(keywords)) 