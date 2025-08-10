import os
import logging
from typing import Dict, Any, Optional, List
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class GPTClient:
    """Abstraction layer for GPT API calls with error handling and rate limiting"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=self.api_key)
        self.default_model = "gpt-4o"
        self.default_max_tokens = 1000
        self.default_temperature = 0.7
        
        logger.info("GPT client initialized successfully")
    
    def generate_response(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        system_prompt: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a response using GPT
        
        Args:
            prompt: The user prompt
            model: GPT model to use
            max_tokens: Maximum tokens to generate
            temperature: Creativity level (0.0 to 1.0)
            system_prompt: System prompt for context
            metadata: Additional metadata for logging
            
        Returns:
            Dict containing response text and metadata
        """
        try:
            model = model or self.default_model
            max_tokens = max_tokens or self.default_max_tokens
            temperature = temperature or self.default_temperature
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=messages
            )
            
            result = {
                "text": response.choices[0].message.content,
                "model": model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                "metadata": metadata or {}
            }
            
            logger.info(f"GPT response generated successfully. Tokens: {result['usage']}")
            return result
            
        except Exception as e:
            logger.error(f"GPT API error: {str(e)}")
            return {
                "text": f"Error generating response: {str(e)}",
                "error": True,
                "metadata": metadata or {}
            }
    
    def generate_product_listing(
        self,
        product_data: Dict[str, Any],
        style: str = "professional"
    ) -> Dict[str, Any]:
        """
        Generate product listing copy using GPT
        
        Args:
            product_data: Product information
            style: Writing style (professional, casual, luxury, etc.)
            
        Returns:
            Generated product listing
        """
        system_prompt = f"""You are an expert e-commerce copywriter specializing in {style} product descriptions.
        Create compelling, SEO-optimized product listings that drive conversions.
        Focus on benefits, features, and emotional appeal while maintaining accuracy."""
        
        prompt = f"""Create a product listing for:

        Product Name: {product_data.get('name', 'Unknown Product')}
        Category: {product_data.get('category', 'General')}
        Price: ${product_data.get('price', 0)}
        Tags: {', '.join(product_data.get('tags', []))}
        Rating: {product_data.get('rating', 'Not rated')}

        Please create:
        1. A compelling product title (max 60 characters)
        2. A detailed product description (200-300 words)
        3. Key features and benefits (bullet points)
        4. SEO-optimized keywords
        5. A call-to-action

        Style: {style}"""
        
        return self.generate_response(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=500,
            temperature=0.8,
            metadata={"product_listing": True, "style": style}
        )
    
    def generate_ad_copy(
        self,
        product_data: Dict[str, Any],
        platform: str = "facebook",
        ad_type: str = "conversion"
    ) -> Dict[str, Any]:
        """
        Generate ad copy for different platforms
        
        Args:
            product_data: Product information
            platform: Ad platform (facebook, instagram, etc.)
            ad_type: Ad objective (conversion, awareness, traffic)
            
        Returns:
            Generated ad copy
        """
        platform_prompts = {
            "facebook": "Facebook ad copy should be conversational and benefit-focused",
            "instagram": "Instagram ad copy should be visual and lifestyle-oriented",

            "pinterest": "Pinterest ad copy should be aspirational and descriptive"
        }
        
        system_prompt = f"""You are an expert digital advertising copywriter specializing in {platform} ads.
        {platform_prompts.get(platform, 'Create compelling ad copy')}
        Focus on {ad_type} objectives and platform-specific best practices."""
        
        prompt = f"""Create {platform} ad copy for:

        Product: {product_data.get('name', 'Unknown Product')}
        Category: {product_data.get('category', 'General')}
        Price: ${product_data.get('price', 0)}
        Target Audience: General consumers

        Please create:
        1. Primary headline (platform-appropriate length)
        2. Secondary headline (if applicable)
        3. Ad description (platform-appropriate length)
        4. Call-to-action button text
        5. Key messaging points

        Ad Type: {ad_type}
        Platform: {platform}"""
        
        return self.generate_response(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=300,
            temperature=0.9,
            metadata={"ad_copy": True, "platform": platform, "ad_type": ad_type}
        )
    
    def research_product_trends(
        self,
        product_category: str,
        market: str = "global"
    ) -> Dict[str, Any]:
        """
        Research product trends and market insights
        
        Args:
            product_category: Product category to research
            market: Target market (global, US, Canada, etc.)
            
        Returns:
            Market research insights
        """
        system_prompt = """You are a market research expert specializing in e-commerce trends.
        Provide data-driven insights about product categories, market opportunities, and consumer behavior.
        Focus on actionable insights for dropshipping businesses."""
        
        prompt = f"""Research market trends for {product_category} in the {market} market.

        Please provide:
        1. Current market trends and opportunities
        2. Seasonal patterns and timing
        3. Target audience insights
        4. Competitive landscape analysis
        5. Pricing strategies and margins
        6. Marketing channel recommendations
        7. Risk factors and challenges

        Focus on insights relevant to dropshipping and e-commerce."""
        
        return self.generate_response(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=600,
            temperature=0.6,
            metadata={"market_research": True, "category": product_category, "market": market}
        )
    
    def optimize_pricing_strategy(
        self,
        product_data: Dict[str, Any],
        competitor_prices: List[float],
        market_conditions: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Optimize pricing strategy based on market data
        
        Args:
            product_data: Product information
            competitor_prices: List of competitor prices
            market_conditions: Current market conditions
            
        Returns:
            Pricing recommendations
        """
        system_prompt = """You are a pricing strategy expert specializing in e-commerce.
        Analyze market data to provide optimal pricing recommendations that maximize profit while remaining competitive."""
        
        prompt = f"""Analyze pricing strategy for:

        Product: {product_data.get('name', 'Unknown Product')}
        Current Price: ${product_data.get('price', 0)}
        Cost Price: ${product_data.get('cost_price', 0)}
        Competitor Prices: {competitor_prices}
        Market Conditions: {market_conditions}

        Please provide:
        1. Recommended price range
        2. Pricing strategy (premium, competitive, penetration)
        3. Profit margin analysis
        4. Competitive positioning
        5. Dynamic pricing recommendations
        6. Seasonal pricing adjustments

        Focus on maximizing profitability while maintaining market competitiveness."""
        
        return self.generate_response(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=400,
            temperature=0.5,
            metadata={"pricing_optimization": True}
        )

# Global instance for easy access
gpt_client = GPTClient() 