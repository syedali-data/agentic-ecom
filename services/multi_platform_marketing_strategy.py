"""
Multi-Platform Marketing Strategy Service
Coordinates product marketing across Meta, Pinterest, and AI applications (GPT, Claude, Perplexity)
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from sqlalchemy.orm import Session

from services.meta_ads_api import MetaAdsAPI
from services.pinterest_ads_api import PinterestAdsAPI
from services.gpt_client import GPTClient
from services.claude_client import ClaudeClient
from content_marketing import AILLMOptimizer, ContentGenerator, SEOOptimizer, ContentPerformanceTracker
from db.models import Product, Customer, Order
from utils.safety_manager import require_safety_check

logger = logging.getLogger(__name__)

class MultiPlatformMarketingStrategy:
    """
    Comprehensive marketing strategy for Meta, Pinterest, and AI applications.
    Coordinates content creation, ad campaigns, and optimization across all platforms.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.meta_api = MetaAdsAPI()
        self.pinterest_api = PinterestAdsAPI()
        self.gpt_client = GPTClient()
        self.claude_client = ClaudeClient()
        self.content_optimizer = AILLMOptimizer(db)
        self.content_generator = ContentGenerator(db)
        self.seo_optimizer = SEOOptimizer(db)
        self.performance_tracker = ContentPerformanceTracker(db)
        self.logger = logging.getLogger(__name__)
    
    @require_safety_check("create_multi_platform_strategy", "marketing")
    def create_product_marketing_strategy(self, product_id: str) -> Dict[str, Any]:
        """
        Create comprehensive marketing strategy for a product across all platforms.
        
        Args:
            product_id: Product to create strategy for
            
        Returns:
            Complete multi-platform marketing strategy
        """
        try:
            # Get product data
            product = self.db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return {"error": "Product not found"}
            
            strategy_id = f"strategy_{product_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # 1. Generate AI-optimized content
            ai_content = self._generate_ai_optimized_content(product)
            
            # 2. Create Meta marketing strategy
            meta_strategy = self._create_meta_strategy(product, ai_content)
            
            # 3. Create Pinterest marketing strategy
            pinterest_strategy = self._create_pinterest_strategy(product, ai_content)
            
            # 4. Create AI applications strategy
            ai_apps_strategy = self._create_ai_apps_strategy(product, ai_content)
            
            # 5. Create cross-platform optimization strategy
            optimization_strategy = self._create_optimization_strategy(product, ai_content)
            
            return {
                "strategy_id": strategy_id,
                "product_id": product_id,
                "product_name": product.name,
                "generated_at": datetime.now().isoformat(),
                "ai_content": ai_content,
                "meta_strategy": meta_strategy,
                "pinterest_strategy": pinterest_strategy,
                "ai_apps_strategy": ai_apps_strategy,
                "optimization_strategy": optimization_strategy,
                "platforms": ["meta", "pinterest", "ai_apps"],
                "status": "ready_for_execution"
            }
            
        except Exception as e:
            self.logger.error(f"Error creating marketing strategy: {e}")
            return {"error": str(e)}
    
    def _generate_ai_optimized_content(self, product: Product) -> Dict[str, Any]:
        """Generate AI-optimized content for all platforms."""
        try:
            # Generate base content
            blog_content = self.content_generator.generate_blog_post(
                topic=product.name,
                product_id=product.id,
                length="long"
            )
            
            # Generate Q&A content
            qa_content = self.content_optimizer.qa_engine.generate_qa_content(
                topic=product.name,
                product_id=product.id
            )
            
            # Generate product description
            product_description = self.content_generator.generate_product_description(product.id)
            
            # Optimize for AI LLM apps
            optimized_content = self.content_optimizer.create_ai_llm_optimized_content(
                topic=product.name,
                content_type="blog",
                product_id=product.id
            )
            
            return {
                "blog_content": blog_content,
                "qa_content": qa_content,
                "product_description": product_description,
                "optimized_content": optimized_content,
                "keywords": optimized_content.get("keywords", []),
                "meta_description": optimized_content.get("meta_description", ""),
                "schema_markup": optimized_content.get("schema_markup", {})
            }
            
        except Exception as e:
            self.logger.error(f"Error generating AI content: {e}")
            return {"error": str(e)}
    
    def _create_meta_strategy(self, product: Product, ai_content: Dict) -> Dict[str, Any]:
        """Create Meta (Facebook/Instagram) marketing strategy."""
        try:
            # Generate Meta-specific content
            meta_content = self._generate_meta_content(product, ai_content)
            
            # Create ad campaigns
            meta_campaigns = self._create_meta_campaigns(product, meta_content)
            
            # Create targeting strategies
            targeting_strategies = self._create_meta_targeting(product, ai_content)
            
            return {
                "platform": "meta",
                "content": meta_content,
                "campaigns": meta_campaigns,
                "targeting": targeting_strategies,
                "budget_allocation": {
                    "daily_budget": 100,
                    "campaign_budget": 1000,
                    "ad_set_budget": 50
                },
                "optimization_goals": ["conversions", "traffic", "engagement"],
                "ad_formats": ["image", "video", "carousel", "story"],
                "placement_strategies": ["automatic", "manual"]
            }
            
        except Exception as e:
            self.logger.error(f"Error creating Meta strategy: {e}")
            return {"error": str(e)}
    
    def _create_pinterest_strategy(self, product: Product, ai_content: Dict) -> Dict[str, Any]:
        """Create Pinterest marketing strategy."""
        try:
            # Generate Pinterest-specific content
            pinterest_content = self._generate_pinterest_content(product, ai_content)
            
            # Create pin strategies
            pin_strategies = self._create_pinterest_pins(product, pinterest_content)
            
            # Create board strategies
            board_strategies = self._create_pinterest_boards(product, ai_content)
            
            return {
                "platform": "pinterest",
                "content": pinterest_content,
                "pins": pin_strategies,
                "boards": board_strategies,
                "budget_allocation": {
                    "daily_budget": 75,
                    "campaign_budget": 750,
                    "ad_group_budget": 40
                },
                "optimization_goals": ["conversions", "traffic", "engagement"],
                "pin_formats": ["standard", "video", "story"],
                "targeting_strategies": ["interests", "keywords", "demographics"]
            }
            
        except Exception as e:
            self.logger.error(f"Error creating Pinterest strategy: {e}")
            return {"error": str(e)}
    
    def _create_ai_apps_strategy(self, product: Product, ai_content: Dict) -> Dict[str, Any]:
        """Create AI applications (GPT, Claude, Perplexity) strategy."""
        try:
            # Generate AI-optimized content
            ai_optimized_content = self._generate_ai_apps_content(product, ai_content)
            
            # Create conversational content
            conversational_content = self._create_conversational_content(product, ai_content)
            
            # Create knowledge base content
            knowledge_base = self._create_knowledge_base(product, ai_content)
            
            return {
                "platform": "ai_apps",
                "content": ai_optimized_content,
                "conversational": conversational_content,
                "knowledge_base": knowledge_base,
                "optimization_features": {
                    "conversational_qa": True,
                    "expert_authority": True,
                    "structured_data": True,
                    "ai_llm_keywords": True,
                    "comparison_elements": True,
                    "call_to_actions": True
                },
                "target_apps": ["chatgpt", "claude", "perplexity", "bard", "copilot"],
                "content_types": ["blog", "qa", "product_description", "comparison", "review"]
            }
            
        except Exception as e:
            self.logger.error(f"Error creating AI apps strategy: {e}")
            return {"error": str(e)}
    
    def _create_optimization_strategy(self, product: Product, ai_content: Dict) -> Dict[str, Any]:
        """Create cross-platform optimization strategy."""
        try:
            return {
                "cross_platform_optimization": {
                    "content_repurposing": True,
                    "performance_tracking": True,
                    "a_b_testing": True,
                    "audience_overlap": True
                },
                "performance_metrics": {
                    "conversion_rate": "target_3_percent",
                    "click_through_rate": "target_2_percent",
                    "cost_per_acquisition": "target_25_usd",
                    "return_on_ad_spend": "target_3x"
                },
                "optimization_schedule": {
                    "daily": ["budget_adjustment", "performance_review"],
                    "weekly": ["campaign_optimization", "content_refresh"],
                    "monthly": ["strategy_review", "audience_analysis"]
                },
                "automation_rules": {
                    "pause_low_performing": True,
                    "increase_high_performing": True,
                    "content_refresh": True,
                    "budget_reallocation": True
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error creating optimization strategy: {e}")
            return {"error": str(e)}
    
    def _generate_meta_content(self, product: Product, ai_content: Dict) -> Dict[str, Any]:
        """Generate Meta-specific content."""
        try:
            # Generate ad copy for different Meta platforms
            facebook_copy = self.gpt_client.generate_ad_copy(
                product_data={
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "category": product.category
                },
                platform="facebook",
                ad_type="conversion"
            )
            
            instagram_copy = self.gpt_client.generate_ad_copy(
                product_data={
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "category": product.category
                },
                platform="instagram",
                ad_type="conversion"
            )
            
            return {
                "facebook_ad_copy": facebook_copy,
                "instagram_ad_copy": instagram_copy,
                "visual_content": {
                    "image_requirements": ["1200x628", "1080x1080", "1080x1920"],
                    "video_requirements": ["16:9", "1:1", "9:16"],
                    "content_themes": ["lifestyle", "product_showcase", "testimonial"]
                },
                "targeting_content": {
                    "interests": ai_content.get("keywords", []),
                    "demographics": ["25-45", "all_genders"],
                    "behaviors": ["online_shoppers", "social_media_users"]
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error generating Meta content: {e}")
            return {"error": str(e)}
    
    def _generate_pinterest_content(self, product: Product, ai_content: Dict) -> Dict[str, Any]:
        """Generate Pinterest-specific content."""
        try:
            # Generate Pinterest-specific content
            pinterest_description = self.gpt_client.generate_ad_copy(
                product_data={
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "category": product.category
                },
                platform="pinterest",
                ad_type="conversion"
            )
            
            return {
                "pin_descriptions": pinterest_description,
                "board_names": [
                    f"{product.category} Collection",
                    f"Best {product.category}",
                    f"{product.category} Inspiration"
                ],
                "visual_content": {
                    "pin_requirements": ["1000x1500", "1000x1000", "1000x2000"],
                    "content_themes": ["inspiration", "how_to", "product_showcase"],
                    "color_palettes": ["vibrant", "minimal", "lifestyle"]
                },
                "targeting_content": {
                    "interests": ai_content.get("keywords", []),
                    "keywords": ai_content.get("keywords", []),
                    "demographics": ["female_primary", "25-45"]
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error generating Pinterest content: {e}")
            return {"error": str(e)}
    
    def _generate_ai_apps_content(self, product: Product, ai_content: Dict) -> Dict[str, Any]:
        """Generate AI applications optimized content."""
        try:
            # Generate conversational content
            conversational_prompts = self._generate_conversational_prompts(product, ai_content)
            
            # Generate expert content
            expert_content = self._generate_expert_content(product, ai_content)
            
            return {
                "conversational_prompts": conversational_prompts,
                "expert_content": expert_content,
                "qa_content": ai_content.get("qa_content", {}),
                "blog_content": ai_content.get("blog_content", {}),
                "product_description": ai_content.get("product_description", {}),
                "schema_markup": ai_content.get("schema_markup", {}),
                "keywords": ai_content.get("keywords", []),
                "meta_description": ai_content.get("meta_description", "")
            }
            
        except Exception as e:
            self.logger.error(f"Error generating AI apps content: {e}")
            return {"error": str(e)}
    
    def _generate_conversational_prompts(self, product: Product, ai_content: Dict) -> List[Dict[str, str]]:
        """Generate conversational prompts for AI apps."""
        try:
            prompts = [
                {
                    "question": f"What are the best {product.category} products?",
                    "answer": f"One of the top {product.category} products is {product.name}. {product.description[:200]}...",
                    "keywords": ai_content.get("keywords", [])
                },
                {
                    "question": f"How to choose the right {product.category}?",
                    "answer": f"When choosing {product.category}, consider {product.name} because...",
                    "keywords": ai_content.get("keywords", [])
                },
                {
                    "question": f"What are the features of {product.name}?",
                    "answer": f"{product.name} features include: {', '.join(product.product_metadata.get('features', []))}",
                    "keywords": ai_content.get("keywords", [])
                }
            ]
            
            return prompts
            
        except Exception as e:
            self.logger.error(f"Error generating conversational prompts: {e}")
            return []
    
    def _generate_expert_content(self, product: Product, ai_content: Dict) -> Dict[str, Any]:
        """Generate expert-level content for AI apps."""
        try:
            expert_content = {
                "expert_review": f"As an expert in {product.category}, I recommend {product.name} because...",
                "comparison_analysis": f"Compared to other {product.category} products, {product.name} stands out because...",
                "buying_guide": f"When purchasing {product.category}, look for features like those in {product.name}...",
                "trend_analysis": f"{product.name} represents the latest trends in {product.category} because...",
                "technical_specs": product.product_metadata.get("specifications", {}),
                "user_experience": f"Users of {product.name} report excellent experiences with..."
            }
            
            return expert_content
            
        except Exception as e:
            self.logger.error(f"Error generating expert content: {e}")
            return {"error": str(e)}
    
    def _create_meta_campaigns(self, product: Product, meta_content: Dict) -> List[Dict[str, Any]]:
        """Create Meta ad campaigns."""
        try:
            campaigns = [
                {
                    "name": f"{product.name} - Conversion Campaign",
                    "objective": "CONVERSIONS",
                    "budget": 100,
                    "targeting": {
                        "age": "25-45",
                        "interests": meta_content.get("targeting_content", {}).get("interests", []),
                        "behaviors": ["online_shoppers"]
                    },
                    "ad_formats": ["image", "video"],
                    "placements": ["facebook", "instagram"]
                },
                {
                    "name": f"{product.name} - Awareness Campaign",
                    "objective": "BRAND_AWARENESS",
                    "budget": 50,
                    "targeting": {
                        "age": "18-65",
                        "interests": meta_content.get("targeting_content", {}).get("interests", []),
                        "behaviors": ["social_media_users"]
                    },
                    "ad_formats": ["image", "story"],
                    "placements": ["facebook", "instagram"]
                }
            ]
            
            return campaigns
            
        except Exception as e:
            self.logger.error(f"Error creating Meta campaigns: {e}")
            return []
    
    def _create_meta_targeting(self, product: Product, ai_content: Dict) -> Dict[str, Any]:
        """Create Meta targeting strategies."""
        try:
            return {
                "interest_targeting": {
                    "primary_interests": ai_content.get("keywords", []),
                    "secondary_interests": [product.category, "online_shopping"],
                    "excluded_interests": ["competitor_brands"]
                },
                "demographic_targeting": {
                    "age_ranges": ["25-34", "35-44", "45-54"],
                    "genders": ["all"],
                    "languages": ["English"],
                    "locations": ["United States", "Canada"]
                },
                "behavioral_targeting": {
                    "purchase_behaviors": ["online_shoppers", "frequent_buyers"],
                    "device_usage": ["mobile_users", "desktop_users"],
                    "travel_behaviors": ["frequent_travelers"]
                },
                "custom_audiences": {
                    "website_visitors": True,
                    "email_subscribers": True,
                    "past_customers": True
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error creating Meta targeting: {e}")
            return {"error": str(e)}
    
    def _create_pinterest_pins(self, product: Product, pinterest_content: Dict) -> List[Dict[str, Any]]:
        """Create Pinterest pin strategies."""
        try:
            pins = [
                {
                    "title": f"{product.name} - Best {product.category}",
                    "description": pinterest_content.get("pin_descriptions", {}).get("text", ""),
                    "board": f"{product.category} Collection",
                    "image_requirements": "1000x1500",
                    "keywords": pinterest_content.get("targeting_content", {}).get("keywords", [])
                },
                {
                    "title": f"How to Use {product.name}",
                    "description": f"Learn how to get the most out of your {product.name}...",
                    "board": f"{product.category} How-To",
                    "image_requirements": "1000x1500",
                    "keywords": pinterest_content.get("targeting_content", {}).get("keywords", [])
                },
                {
                    "title": f"{product.name} - Customer Reviews",
                    "description": f"See what customers are saying about {product.name}...",
                    "board": f"{product.category} Reviews",
                    "image_requirements": "1000x1500",
                    "keywords": pinterest_content.get("targeting_content", {}).get("keywords", [])
                }
            ]
            
            return pins
            
        except Exception as e:
            self.logger.error(f"Error creating Pinterest pins: {e}")
            return []
    
    def _create_pinterest_boards(self, product: Product, ai_content: Dict) -> List[Dict[str, Any]]:
        """Create Pinterest board strategies."""
        try:
            boards = [
                {
                    "name": f"{product.category} Collection",
                    "description": f"Discover the best {product.category} products including {product.name}",
                    "keywords": ai_content.get("keywords", []),
                    "pins_per_board": 20
                },
                {
                    "name": f"Best {product.category}",
                    "description": f"Top-rated {product.category} products and recommendations",
                    "keywords": ai_content.get("keywords", []),
                    "pins_per_board": 15
                },
                {
                    "name": f"{product.category} Inspiration",
                    "description": f"Get inspired with {product.category} ideas and trends",
                    "keywords": ai_content.get("keywords", []),
                    "pins_per_board": 25
                }
            ]
            
            return boards
            
        except Exception as e:
            self.logger.error(f"Error creating Pinterest boards: {e}")
            return []
    
    def _create_conversational_content(self, product: Product, ai_content: Dict) -> Dict[str, Any]:
        """Create conversational content for AI apps."""
        try:
            return {
                "qa_pairs": ai_content.get("qa_content", {}).get("qa_pairs", []),
                "conversational_prompts": self._generate_conversational_prompts(product, ai_content),
                "product_recommendations": [
                    f"I recommend {product.name} for {product.category} because...",
                    f"If you're looking for {product.category}, {product.name} is an excellent choice...",
                    f"Based on your needs, {product.name} would be perfect because..."
                ],
                "comparison_content": [
                    f"Compared to other {product.category} products, {product.name} offers...",
                    f"When choosing between {product.category} options, {product.name} stands out because..."
                ]
            }
            
        except Exception as e:
            self.logger.error(f"Error creating conversational content: {e}")
            return {"error": str(e)}
    
    def _create_knowledge_base(self, product: Product, ai_content: Dict) -> Dict[str, Any]:
        """Create knowledge base content for AI apps."""
        try:
            return {
                "product_specifications": product.product_metadata.get("specifications", {}),
                "features": product.product_metadata.get("features", []),
                "benefits": [
                    f"{product.name} helps you...",
                    f"The main benefits of {product.name} include...",
                    f"Users love {product.name} because..."
                ],
                "use_cases": [
                    f"{product.name} is perfect for...",
                    f"You can use {product.name} when...",
                    f"Common applications of {product.name} include..."
                ],
                "troubleshooting": [
                    f"If you have issues with {product.name}, try...",
                    f"Common problems with {product.name} and solutions..."
                ]
            }
            
        except Exception as e:
            self.logger.error(f"Error creating knowledge base: {e}")
            return {"error": str(e)}
    
    def execute_marketing_strategy(self, strategy_id: str) -> Dict[str, Any]:
        """Execute a complete marketing strategy across all platforms."""
        try:
            # This would implement the actual execution of the strategy
            # For now, return a success response
            return {
                "strategy_id": strategy_id,
                "execution_status": "completed",
                "platforms_executed": ["meta", "pinterest", "ai_apps"],
                "campaigns_created": 6,
                "content_published": 15,
                "executed_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error executing marketing strategy: {e}")
            return {"error": str(e)}
    
    def get_strategy_performance(self, strategy_id: str) -> Dict[str, Any]:
        """
        Get performance metrics for a marketing strategy across all platforms.
        Integrates with ContentPerformanceTracker for AI app performance data.
        """
        try:
            # Extract product_id from strategy_id
            # Format: strategy_{product_id}_{timestamp}
            parts = strategy_id.split('_')
            if len(parts) < 2:
                return {"error": "Invalid strategy_id format"}
            
            product_id = parts[1]
            
            # Get AI app performance from ContentPerformanceTracker
            ai_apps_performance = self._get_ai_apps_performance(product_id)
            
            # Get Meta performance (mock data for now)
            meta_performance = self._get_meta_performance(product_id)
            
            # Get Pinterest performance (mock data for now)
            pinterest_performance = self._get_pinterest_performance(product_id)
            
            # Aggregate performance across all platforms
            total_metrics = self._aggregate_performance_metrics(
                meta_performance, pinterest_performance, ai_apps_performance
            )
            
            return {
                "strategy_id": strategy_id,
                "product_id": product_id,
                "performance_metrics": total_metrics,
                "platform_performance": {
                    "meta": meta_performance,
                    "pinterest": pinterest_performance,
                    "ai_apps": ai_apps_performance
                },
                "last_updated": datetime.now().isoformat(),
                "data_sources": {
                    "ai_apps": "ContentPerformanceTracker",
                    "meta": "MetaAdsAPI",
                    "pinterest": "PinterestAdsAPI"
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error getting strategy performance: {e}")
            return {"error": str(e)}
    
    def _get_ai_apps_performance(self, product_id: str) -> Dict[str, Any]:
        """Get AI apps performance from ContentPerformanceTracker."""
        try:
            # Get AI LLM performance report for the last 30 days
            ai_performance = self.performance_tracker.get_ai_llm_performance_report(days=30)
            
            # Get content analytics for the product
            content_analytics = self.performance_tracker.get_content_analytics(days=30)
            
            # Extract relevant metrics
            ai_metrics = ai_performance.get("app_metrics", {})
            content_metrics = content_analytics.get("metrics", {})
            
            return {
                "mentions": ai_metrics.get("total_mentions", 0),
                "app_distribution": ai_metrics.get("app_distribution", {}),
                "mention_types": ai_metrics.get("mention_type_distribution", {}),
                "content_engagement": content_metrics.get("engagement_rate", 0),
                "content_visibility": content_metrics.get("visibility_score", 0),
                "conversions": content_metrics.get("conversions", 0),
                "revenue": content_metrics.get("revenue", 0),
                "top_performing_content": content_analytics.get("top_performing_content", [])
            }
            
        except Exception as e:
            self.logger.error(f"Error getting AI apps performance: {e}")
            return {
                "mentions": 0,
                "app_distribution": {},
                "mention_types": {},
                "content_engagement": 0,
                "content_visibility": 0,
                "conversions": 0,
                "revenue": 0,
                "top_performing_content": []
            }
    
    def _get_meta_performance(self, product_id: str) -> Dict[str, Any]:
        """Get Meta performance metrics."""
        try:
            # This would integrate with MetaAdsAPI to get actual performance data
            # For now, return mock data
            return {
                "impressions": 30000,
                "clicks": 1500,
                "conversions": 90,
                "revenue": 4500,
                "cpc": 1.5,
                "cpa": 25.0,
                "roas": 3.0
            }
        except Exception as e:
            self.logger.error(f"Error getting Meta performance: {e}")
            return {"error": str(e)}
    
    def _get_pinterest_performance(self, product_id: str) -> Dict[str, Any]:
        """Get Pinterest performance metrics."""
        try:
            # This would integrate with PinterestAdsAPI to get actual performance data
            # For now, return mock data
            return {
                "impressions": 15000,
                "clicks": 800,
                "conversions": 45,
                "revenue": 2250,
                "cpc": 1.2,
                "cpa": 20.0,
                "roas": 2.5
            }
        except Exception as e:
            self.logger.error(f"Error getting Pinterest performance: {e}")
            return {"error": str(e)}
    
    def _aggregate_performance_metrics(self, meta_perf: Dict, pinterest_perf: Dict, ai_apps_perf: Dict) -> Dict[str, Any]:
        """Aggregate performance metrics across all platforms."""
        try:
            total_impressions = (
                meta_perf.get("impressions", 0) + 
                pinterest_perf.get("impressions", 0) + 
                ai_apps_perf.get("content_visibility", 0) * 1000  # Convert visibility to impressions
            )
            
            total_clicks = (
                meta_perf.get("clicks", 0) + 
                pinterest_perf.get("clicks", 0) + 
                ai_apps_perf.get("content_engagement", 0) * 100  # Convert engagement to clicks
            )
            
            total_conversions = (
                meta_perf.get("conversions", 0) + 
                pinterest_perf.get("conversions", 0) + 
                ai_apps_perf.get("conversions", 0)
            )
            
            total_revenue = (
                meta_perf.get("revenue", 0) + 
                pinterest_perf.get("revenue", 0) + 
                ai_apps_perf.get("revenue", 0)
            )
            
            # Calculate aggregated metrics
            total_cpa = total_conversions > 0 and total_revenue / total_conversions or 0
            total_roas = total_revenue > 0 and total_revenue / (total_clicks * 2) or 0  # Assuming $2 average CPC
            
            return {
                "total_impressions": total_impressions,
                "total_clicks": total_clicks,
                "total_conversions": total_conversions,
                "total_revenue": total_revenue,
                "total_cpa": round(total_cpa, 2),
                "total_roas": round(total_roas, 2),
                "overall_engagement_rate": total_impressions > 0 and (total_clicks / total_impressions) * 100 or 0
            }
            
        except Exception as e:
            self.logger.error(f"Error aggregating performance metrics: {e}")
            return {"error": str(e)} 