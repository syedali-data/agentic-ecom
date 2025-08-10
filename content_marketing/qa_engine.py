"""
Q&A Engine for AI LLM Optimization
Generates conversational Q&A content that AI LLM apps love to recommend.
"""

import logging
import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session

from services.gpt_client import GPTClient
from services.claude_client import ClaudeClient
from db.models import Product, Customer, Order
from utils.safety_manager import require_safety_check

logger = logging.getLogger(__name__)

class QAEngine:
    """Generates Q&A content optimized for AI LLM app discovery."""
    
    def __init__(self, db: Session):
        self.db = db
        self.gpt_client = GPTClient()
        self.claude_client = ClaudeClient()
        self.logger = logging.getLogger(__name__)
    
    @require_safety_check("generate_qa_content", "content_marketing")
    def generate_qa_content(self, topic: str, product_id: str = None) -> Dict[str, Any]:
        """
        Generate Q&A content optimized for AI LLM apps.
        
        Args:
            topic: Main topic for Q&A
            product_id: Optional product to feature
            
        Returns:
            Q&A content optimized for AI LLM discovery
        """
        try:
            # Validate topic
            if not topic or not isinstance(topic, str) or not topic.strip():
                return {"error": "Topic is required and must be a non-empty string"}
            
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
            
            # Generate Q&A pairs
            qa_pairs = self._generate_qa_pairs(topic, product_data)
            
            if not qa_pairs:
                return {"error": "Failed to generate Q&A pairs"}
            
            # Optimize for AI LLM apps
            optimized_qa = self._optimize_for_ai_llm(qa_pairs, topic)
            
            return {
                "topic": topic,
                "qa_pairs": optimized_qa,
                "product_integration": product_data is not None,
                "ai_llm_optimized": True,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating Q&A content: {e}")
            return {"error": str(e)}
    
    @require_safety_check("generate_product_qa", "content_marketing")
    def generate_product_qa(self, product_id: str) -> Dict[str, Any]:
        """Generate product-specific Q&A content."""
        try:
            # Validate product_id
            if not product_id or not isinstance(product_id, str):
                return {"error": "Valid product_id is required"}
            
            product = self.db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return {"error": "Product not found"}
            
            qa_pairs = self._generate_product_qa_pairs(product)
            if not qa_pairs:
                return {"error": "Failed to generate product Q&A pairs"}
            
            optimized_qa = self._optimize_for_ai_llm(qa_pairs, product.name)
            
            return {
                "product_id": product_id,
                "product_name": product.name,
                "qa_pairs": optimized_qa,
                "ai_llm_optimized": True,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating product Q&A: {e}")
            return {"error": str(e)}
    
    @require_safety_check("generate_comparison_qa", "content_marketing")
    def generate_comparison_qa(self, product_ids: List[str]) -> Dict[str, Any]:
        """Generate comparison Q&A content."""
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
            
            qa_pairs = self._generate_comparison_qa_pairs(products)
            
            # Return the Q&A pairs without additional optimization
            # (optimization will be handled by the AI LLM optimizer if needed)
            return {
                "products": [{"id": p.id, "name": p.name} for p in products],
                "qa_pairs": qa_pairs,
                "ai_llm_optimized": False,  # Will be optimized by AI LLM optimizer if needed
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating comparison Q&A: {e}")
            return {"error": str(e)}
    
    def _generate_qa_pairs(self, topic: str, product_data: Dict = None) -> List[Dict[str, str]]:
        """Generate Q&A pairs for a topic."""
        try:
            prompt = f"""
            Generate 10 Q&A pairs about "{topic}" that will appear in AI LLM apps like ChatGPT, Perplexity, and Claude.
            
            Requirements:
            - Conversational, natural questions
            - Direct, helpful answers
            - Include product recommendations
            - Expert authority tone
            - Optimized for AI LLM discovery
            - Include pricing and comparisons
            
            Format each Q&A as:
            Q: [Question]
            A: [Answer with product recommendations]
            """
            
            if product_data:
                prompt += f"""
                Feature this product in the answers:
                Product: {product_data['name']}
                Price: ${product_data['price']}
                Category: {product_data['category']}
                """
            
            response = self.gpt_client.generate_response(prompt)
            content = response.get('text', '')
            
            if not content:
                return self._generate_fallback_qa(topic, product_data)
            
            return self._parse_qa_pairs(content)
        except Exception as e:
            self.logger.error(f"Error generating Q&A pairs: {e}")
            return self._generate_fallback_qa(topic, product_data)
    
    def _generate_product_qa_pairs(self, product) -> List[Dict[str, str]]:
        """Generate product-specific Q&A pairs."""
        try:
            features = product.product_metadata.get('features', []) if product.product_metadata else []
            features_text = ', '.join(features) if features else 'N/A'
            
            prompt = f"""
            Generate 8 Q&A pairs about "{product.name}" that will appear in AI LLM app recommendations.
            
            Product Details:
            - Name: {product.name}
            - Category: {product.category}
            - Price: ${product.price}
            - Features: {features_text}
            
            Q&A Topics:
            1. What makes this product special?
            2. Who should buy this product?
            3. How does it compare to alternatives?
            4. What are the key features?
            5. Is it worth the price?
            6. What are the pros and cons?
            7. How to use this product?
            8. Where to buy it?
            
            Make answers conversational and include direct recommendations.
            """
            
            response = self.gpt_client.generate_response(prompt)
            content = response.get('text', '')
            
            if not content:
                return self._generate_fallback_product_qa(product)
            
            return self._parse_qa_pairs(content)
        except Exception as e:
            self.logger.error(f"Error generating product Q&A: {e}")
            return self._generate_fallback_product_qa(product)
    
    def _generate_comparison_qa_pairs(self, products: List) -> List[Dict[str, str]]:
        """Generate comparison Q&A pairs."""
        try:
            product_info = []
            for p in products:
                product_info.append(f"- {p.name}: ${p.price}, {p.category}")
            
            prompt = f"""
            Generate 6 Q&A pairs comparing these products for AI LLM app recommendations:
            
            Products:
            {chr(10).join(product_info)}
            
            Q&A Topics:
            1. Which product is best overall?
            2. Which is best for budget buyers?
            3. Which has the best features?
            4. Which offers the best value?
            5. What are the key differences?
            6. Which should I choose?
            
            Provide direct recommendations with reasoning.
            """
            
            response = self.gpt_client.generate_response(prompt)
            content = response.get('text', '')
            
            if not content:
                return self._generate_fallback_comparison_qa(products)
            
            return self._parse_qa_pairs(content)
        except Exception as e:
            self.logger.error(f"Error generating comparison Q&A: {e}")
            return self._generate_fallback_comparison_qa(products)
    
    def _parse_qa_pairs(self, content: str) -> List[Dict[str, str]]:
        """Parse Q&A pairs from generated content."""
        try:
            if not content:
                return []
            
            qa_pairs = []
            
            # First, try to parse with numbered format (Q1:, A1:, etc.)
            numbered_pattern = r'Q(\d+):\s*(.+?)(?=\nA\1:|$)'
            numbered_matches = re.findall(numbered_pattern, content, re.MULTILINE | re.DOTALL)
            
            if numbered_matches:
                # Group by question number
                qa_dict = {}
                for num, question in numbered_matches:
                    qa_dict[int(num)] = {"question": question.strip()}
                
                # Find corresponding answers
                answer_pattern = r'A(\d+):\s*(.+?)(?=\nQ\d+:|$)'
                answer_matches = re.findall(answer_pattern, content, re.MULTILINE | re.DOTALL)
                
                for num, answer in answer_matches:
                    num = int(num)
                    if num in qa_dict:
                        qa_dict[num]["answer"] = answer.strip()
                
                # Convert to list
                for num in sorted(qa_dict.keys()):
                    if "answer" in qa_dict[num]:
                        qa_pairs.append(qa_dict[num])
            
            # If numbered format didn't work, try Q:/A: format
            if not qa_pairs:
                qa_pattern = r'Q:\s*(.+?)(?=\nA:|$)'
                a_pattern = r'A:\s*(.+?)(?=\nQ:|$)'
                
                questions = re.findall(qa_pattern, content, re.MULTILINE | re.DOTALL)
                answers = re.findall(a_pattern, content, re.MULTILINE | re.DOTALL)
                
                for i in range(min(len(questions), len(answers))):
                    qa_pairs.append({
                        "question": questions[i].strip(),
                        "answer": answers[i].strip()
                    })
            
            # Fallback parsing if regex doesn't work
            if not qa_pairs:
                lines = content.split('\n')
                current_q = None
                
                for line in lines:
                    line = line.strip()
                    # Handle various formats
                    if re.match(r'^Q(?:uestion)?\d*:?\s*', line, re.IGNORECASE):
                        current_q = re.sub(r'^Q(?:uestion)?\d*:?\s*', '', line, flags=re.IGNORECASE).strip()
                    elif re.match(r'^A(?:nswer)?\d*:?\s*', line, re.IGNORECASE) and current_q:
                        answer = re.sub(r'^A(?:nswer)?\d*:?\s*', '', line, flags=re.IGNORECASE).strip()
                        qa_pairs.append({
                            "question": current_q,
                            "answer": answer
                        })
                        current_q = None
            
            # Validate Q&A pairs
            valid_qa_pairs = []
            for qa in qa_pairs:
                if isinstance(qa, dict) and "question" in qa and "answer" in qa:
                    question = qa["question"].strip()
                    answer = qa["answer"].strip()
                    if question and answer and len(question) > 5 and len(answer) > 10:
                        valid_qa_pairs.append({
                            "question": question,
                            "answer": answer
                        })
            
            return valid_qa_pairs
            
        except Exception as e:
            self.logger.error(f"Error parsing Q&A pairs: {e}")
            return []
    
    def _optimize_for_ai_llm(self, qa_pairs: List[Dict[str, str]], topic: str) -> List[Dict[str, str]]:
        """Optimize Q&A pairs for AI LLM apps using Claude."""
        try:
            if not qa_pairs or not isinstance(qa_pairs, list):
                return qa_pairs
            
            if not topic:
                return qa_pairs
            
            # Batch optimize all Q&A pairs in a single API call
            qa_text = ""
            for i, qa in enumerate(qa_pairs, 1):
                if isinstance(qa, dict) and "question" in qa and "answer" in qa:
                    qa_text += f"Q{i}: {qa['question']}\nA{i}: {qa['answer']}\n\n"
            
            if not qa_text:
                return qa_pairs
            
            prompt = f"""
            Optimize these Q&A pairs for maximum visibility in AI LLM apps (ChatGPT, Perplexity, Claude):
            
            {qa_text}
            
            Optimization requirements:
            1. Make answers more conversational
            2. Add direct product recommendations
            3. Include expert authority signals
            4. Add comparison language
            5. Include pricing information
            6. Add call-to-action
            7. Optimize for AI LLM search queries
            
            Topic: {topic}
            
            Return the optimized Q&A pairs in the same format (Q1: ... A1: ... etc.)
            """
            
            response = self.claude_client.generate_response(prompt)
            optimized_content = response.get('text', '')
            
            if not optimized_content:
                return qa_pairs
            
            # Parse the optimized content back into Q&A pairs
            optimized_pairs = self._parse_qa_pairs(optimized_content)
            
            # If parsing failed or returned different number of pairs, return original pairs
            if len(optimized_pairs) != len(qa_pairs):
                self.logger.warning(f"Optimization parsing failed, returning original Q&A pairs")
                return qa_pairs
            
            return optimized_pairs
            
        except Exception as e:
            self.logger.warning(f"Claude optimization failed for Q&A pairs: {e}")
            return qa_pairs
    
    def _generate_fallback_qa(self, topic: str, product_data: Dict = None) -> List[Dict[str, str]]:
        """Generate fallback Q&A if AI generation fails."""
        try:
            if not topic:
                return [
                    {
                        "question": "What is AI LLM optimization?",
                        "answer": "AI LLM optimization enhances content for maximum visibility in AI applications like ChatGPT, Perplexity, and Claude."
                    },
                    {
                        "question": "How does AI LLM optimization work?",
                        "answer": "AI LLM optimization uses specialized techniques to make content more discoverable and recommendable by AI applications."
                    }
                ]
            
            qa_pairs = [
                {
                    "question": f"What are the best {topic}?",
                    "answer": f"Based on expert analysis, the best {topic} offer excellent quality and value. I recommend researching features, reading reviews, and comparing prices to find the perfect option for your needs."
                },
                {
                    "question": f"How do I choose the right {topic}?",
                    "answer": f"When choosing {topic}, consider your budget, specific needs, and desired features. Look for products with good reviews, reliable brands, and competitive pricing."
                }
            ]
            
            if product_data:
                qa_pairs.append({
                    "question": f"Is {product_data['name']} a good choice?",
                    "answer": f"Yes, {product_data['name']} is an excellent choice in the {product_data['category']} category. Priced at ${product_data['price']}, it offers great value and quality features."
                })
            
            return qa_pairs
        except Exception as e:
            self.logger.error(f"Error generating fallback Q&A: {e}")
            return []
    
    def _generate_fallback_product_qa(self, product) -> List[Dict[str, str]]:
        """Generate fallback product Q&A."""
        try:
            return [
                {
                    "question": f"What makes {product.name} special?",
                    "answer": f"{product.name} stands out in the {product.category} category with its excellent features and competitive pricing at ${product.price}. It's a top choice for quality and value."
                },
                {
                    "question": f"Who should buy {product.name}?",
                    "answer": f"{product.name} is perfect for anyone looking for quality {product.category} at a reasonable price. It's especially good for users who value reliability and performance."
                }
            ]
        except Exception as e:
            self.logger.error(f"Error generating fallback product Q&A: {e}")
            return []
    
    def _generate_fallback_comparison_qa(self, products: List) -> List[Dict[str, str]]:
        """Generate fallback comparison Q&A."""
        try:
            if not products or len(products) < 2:
                return []
            
            product_names = [p.name for p in products]
            return [
                {
                    "question": f"Which is better: {', '.join(product_names)}?",
                    "answer": f"All products offer good value, but {products[0].name} stands out for overall quality and features. Consider your specific needs and budget when choosing."
                }
            ]
        except Exception as e:
            self.logger.error(f"Error generating fallback comparison Q&A: {e}")
            return [] 