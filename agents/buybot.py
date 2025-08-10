import sys
import os
import uuid
import logging
from dotenv import load_dotenv
from typing import Dict, Any, Optional, List

# Add project root for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.log_rotation import get_rotating_file_handler
from services.gpt_client import gpt_client
from services.shopify_api import get_products
from schemas.product import ProductSearch

# --- Session ID Formatter for Logging ---
class SessionIDLogFormatter(logging.Formatter):
    def __init__(self, session_id, fmt=None, datefmt=None, style='%'):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        self.session_id = session_id

    def format(self, record):
        record.session_id = self.session_id
        return super().format(record)

# --- Generate a Unique Session/Run ID ---
SESSION_ID = str(uuid.uuid4())

# --- Logging Setup with Rotation ---
log_format = "%(asctime)s [%(levelname)s] [Session:%(session_id)s] %(message)s"
formatter = SessionIDLogFormatter(SESSION_ID, fmt=log_format)

os.makedirs("logs/buybot", exist_ok=True)
file_handler = get_rotating_file_handler("logs/buybot/buybot.log", when="midnight", backup_count=14)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger = logging.getLogger("buybot")
logger.setLevel(logging.INFO)
logger.handlers = []
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# --- Load Environment Variables ---
load_dotenv()

class BuyBot:
    """AI-powered customer assistant for product Q&A and recommendations"""
    
    def __init__(self):
        self.session_id = SESSION_ID
        self.conversation_history = []
        logger.info("BuyBot initialized successfully")
    
    def handle_customer_query(
        self,
        query: str,
        customer_context: Optional[Dict[str, Any]] = None,
        product_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Handle customer queries and provide helpful responses
        
        Args:
            query: Customer's question or request
            customer_context: Customer information (preferences, history, etc.)
            product_context: Product information if query is product-specific
            
        Returns:
            Response with answer and recommendations
        """
        try:
            logger.info(f"Processing customer query: {query[:100]}...")
            
            # Analyze query intent
            intent = self._analyze_query_intent(query)
            
            # Generate response based on intent
            if intent == "product_search":
                response = self._handle_product_search(query, customer_context)
            elif intent == "product_info":
                response = self._handle_product_info(query, product_context)
            elif intent == "pricing":
                response = self._handle_pricing_query(query, product_context)
            elif intent == "shipping":
                response = self._handle_shipping_query(query)
            elif intent == "general":
                response = self._handle_general_query(query)
            else:
                response = self._handle_general_query(query)
            
            # Add to conversation history
            self.conversation_history.append({
                "query": query,
                "response": response,
                "timestamp": "now"
            })
            
            logger.info("Customer query processed successfully")
            return response
            
        except Exception as e:
            logger.error(f"Error processing customer query: {e}")
            return {
                "answer": "I apologize, but I'm having trouble processing your request right now. Please try again or contact our support team.",
                "confidence": 0.0,
                "error": True
            }
    
    def _analyze_query_intent(self, query: str) -> str:
        """Analyze customer query to determine intent"""
        try:
            prompt = f"""Analyze this customer query and determine the intent:

            Query: "{query}"

            Possible intents:
            - product_search: Looking for products, recommendations, or browsing
            - product_info: Asking about specific product details, features, or specifications
            - pricing: Questions about prices, discounts, or payment
            - shipping: Questions about delivery, shipping times, or tracking
            - general: General questions about the store, policies, or support

            Return only the intent category."""
            
            result = gpt_client.generate_response(
                prompt=prompt,
                max_tokens=50,
                temperature=0.3
            )
            
            intent = result.get("text", "general").strip().lower()
            return intent
            
        except Exception as e:
            logger.error(f"Error analyzing query intent: {e}")
            return "general"
    
    def _handle_product_search(self, query: str, customer_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Handle product search and recommendations"""
        try:
            # Get available products
            products = get_products()
            
            prompt = f"""A customer is looking for products. Help them find what they need.

            Customer Query: "{query}"
            Customer Context: {customer_context or 'No specific context'}
            Available Products: {[p.get('name', 'Unknown') for p in products[:10]]}

            Please provide:
            1. A helpful response acknowledging their search
            2. Product recommendations based on their query
            3. Any relevant tips or information
            4. A friendly call-to-action

            Keep the response conversational and helpful."""
            
            result = gpt_client.generate_response(
                prompt=prompt,
                max_tokens=300,
                temperature=0.7
            )
            
            return {
                "answer": result.get("text", "I'd be happy to help you find products!"),
                "recommendations": products[:5],
                "confidence": 0.8,
                "intent": "product_search"
            }
            
        except Exception as e:
            logger.error(f"Error handling product search: {e}")
            return {
                "answer": "I'd be happy to help you find products! Let me search our inventory for you.",
                "confidence": 0.5,
                "intent": "product_search"
            }
    
    def _handle_product_info(self, query: str, product_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Handle product-specific questions"""
        try:
            prompt = f"""A customer is asking about a specific product. Provide helpful information.

            Customer Query: "{query}"
            Product Context: {product_context or 'No specific product context'}

            Please provide:
            1. A clear, informative answer about the product
            2. Relevant features and benefits
            3. Any important specifications or details
            4. A helpful call-to-action if appropriate

            Be accurate and helpful while maintaining a friendly tone."""
            
            result = gpt_client.generate_response(
                prompt=prompt,
                max_tokens=250,
                temperature=0.6
            )
            
            return {
                "answer": result.get("text", "I'd be happy to provide more information about this product!"),
                "confidence": 0.9,
                "intent": "product_info"
            }
            
        except Exception as e:
            logger.error(f"Error handling product info: {e}")
            return {
                "answer": "I'd be happy to provide more information about this product!",
                "confidence": 0.5,
                "intent": "product_info"
            }
    
    def _handle_pricing_query(self, query: str, product_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Handle pricing-related questions"""
        try:
            prompt = f"""A customer is asking about pricing. Provide helpful information.

            Customer Query: "{query}"
            Product Context: {product_context or 'No specific product context'}

            Please provide:
            1. Clear pricing information
            2. Any available discounts or promotions
            3. Payment options if relevant
            4. A helpful call-to-action

            Be transparent about pricing and any additional costs."""
            
            result = gpt_client.generate_response(
                prompt=prompt,
                max_tokens=200,
                temperature=0.5
            )
            
            return {
                "answer": result.get("text", "I'd be happy to help with pricing information!"),
                "confidence": 0.8,
                "intent": "pricing"
            }
            
        except Exception as e:
            logger.error(f"Error handling pricing query: {e}")
            return {
                "answer": "I'd be happy to help with pricing information!",
                "confidence": 0.5,
                "intent": "pricing"
            }
    
    def _handle_shipping_query(self, query: str) -> Dict[str, Any]:
        """Handle shipping and delivery questions"""
        try:
            prompt = f"""A customer is asking about shipping and delivery. Provide helpful information.

            Customer Query: "{query}"

            Please provide:
            1. Shipping options and timeframes
            2. Delivery information
            3. Tracking capabilities
            4. Any relevant policies

            Be clear about shipping times and any restrictions."""
            
            result = gpt_client.generate_response(
                prompt=prompt,
                max_tokens=200,
                temperature=0.5
            )
            
            return {
                "answer": result.get("text", "I'd be happy to help with shipping information!"),
                "confidence": 0.8,
                "intent": "shipping"
            }
            
        except Exception as e:
            logger.error(f"Error handling shipping query: {e}")
            return {
                "answer": "I'd be happy to help with shipping information!",
                "confidence": 0.5,
                "intent": "shipping"
            }
    
    def _handle_general_query(self, query: str) -> Dict[str, Any]:
        """Handle general questions about the store or policies"""
        try:
            prompt = f"""A customer is asking a general question about the store. Provide helpful information.

            Customer Query: "{query}"

            Please provide:
            1. A helpful, accurate answer
            2. Relevant information about policies or procedures
            3. A friendly, professional tone
            4. A call-to-action if appropriate

            Be helpful and informative while maintaining a positive customer experience."""
            
            result = gpt_client.generate_response(
                prompt=prompt,
                max_tokens=200,
                temperature=0.6
            )
            
            return {
                "answer": result.get("text", "I'd be happy to help with your question!"),
                "confidence": 0.7,
                "intent": "general"
            }
            
        except Exception as e:
            logger.error(f"Error handling general query: {e}")
            return {
                "answer": "I'd be happy to help with your question!",
                "confidence": 0.5,
                "intent": "general"
            }
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get conversation history for this session"""
        return self.conversation_history
    
    def clear_conversation_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")

# --- Script Entrypoint ---
if __name__ == "__main__":
    logger.info("BuyBot session started.")
    
    bot = BuyBot()
    
    # Test queries
    test_queries = [
        "Do you have any fitness trackers?",
        "What's the shipping time to Canada?",
        "How much does the LED makeup mirror cost?",
        "What's your return policy?",
        "Can you recommend a good coffee mug?"
    ]
    
    for query in test_queries:
        print(f"\nCustomer: {query}")
        response = bot.handle_customer_query(query)
        print(f"BuyBot: {response['answer']}")
        print(f"Confidence: {response['confidence']}")
    
    logger.info("BuyBot session finished.") 