"""
AI LLM Optimizer - Main Coordinator
Coordinates all content marketing components for maximum AI LLM app visibility.
"""

import logging
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session

from .generator import ContentGenerator
from .qa_engine import QAEngine
from .seo_optimizer import SEOOptimizer
from .schema_markup import SchemaMarkupGenerator
from .performance_tracker import ContentPerformanceTracker
from db.models import Product, Customer, Order
from utils.safety_manager import require_safety_check

logger = logging.getLogger(__name__)

class AILLMOptimizer:
    """Main coordinator for AI LLM content optimization."""
    
    def __init__(self, db: Session):
        self.db = db
        self.content_generator = ContentGenerator(db)
        self.qa_engine = QAEngine(db)
        self.seo_optimizer = SEOOptimizer(db)
        self.schema_generator = SchemaMarkupGenerator(db)
        self.performance_tracker = ContentPerformanceTracker(db)
        self.logger = logging.getLogger(__name__)
    
    @require_safety_check("create_ai_llm_optimized_content", "content_marketing")
    def create_ai_llm_optimized_content(self, topic: str, content_type: str = "blog", product_id: str = None) -> Dict[str, Any]:
        """
        Create complete AI LLM optimized content package.
        
        Args:
            topic: Main content topic
            content_type: blog, product, comparison, qa
            product_id: Optional product to feature
            
        Returns:
            Complete AI LLM optimized content package
        """
        try:
            # Validate inputs
            if not topic or not isinstance(topic, str) or not topic.strip():
                return {"error": "Topic is required and must be a non-empty string"}
            
            if not content_type or not isinstance(content_type, str):
                content_type = "blog"
            
            if content_type not in ["blog", "product", "comparison", "qa"]:
                return {"error": f"Unsupported content type: {content_type}"}
            
            if product_id and not isinstance(product_id, str):
                return {"error": "product_id must be a string if provided"}
            
            content_id = f"{content_type}_{topic}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Generate base content
            if content_type == "blog":
                base_content = self.content_generator.generate_blog_post(topic, product_id)
            elif content_type == "product":
                if not product_id:
                    return {"error": "product_id is required for product content type"}
                base_content = self.content_generator.generate_product_description(product_id)
            elif content_type == "qa":
                base_content = self.qa_engine.generate_qa_content(topic, product_id)
            else:
                return {"error": f"Unsupported content type: {content_type}"}
            
            if "error" in base_content:
                return base_content
            
            # Get content for optimization
            content_to_optimize = base_content.get("content", "")
            if not content_to_optimize:
                content_to_optimize = base_content.get("description", "")
            
            if not content_to_optimize:
                return {"error": "No content generated for optimization"}
            
            # Optimize for AI LLM apps
            optimized_content = self.seo_optimizer.optimize_for_ai_llm(
                content_to_optimize,
                topic,
                content_type
            )
            
            if "error" in optimized_content:
                return optimized_content
            
            # Generate schema markup
            schema_data = self.schema_generator.generate_article_schema({
                "id": content_id,
                "title": optimized_content.get("optimized_title", base_content.get("title", "")),
                "meta_description": optimized_content.get("meta_description", ""),
                "keywords": optimized_content.get("keywords", []),
                "generated_at": datetime.now().isoformat()
            })
            
            # Generate Q&A content for conversational optimization (only for blog content type)
            if content_type == "blog":
                qa_content = self.qa_engine.generate_qa_content(topic, product_id)
                if "error" in qa_content:
                    # Use fallback Q&A content
                    qa_content = {
                        "topic": topic,
                        "qa_pairs": [],
                        "ai_llm_optimized": False,
                        "generated_at": datetime.now().isoformat()
                    }
            elif content_type == "qa":
                qa_content = base_content  # Use the already generated QA content
            else:
                # For other content types (product, comparison), skip Q&A generation to avoid loops
                qa_content = {
                    "topic": topic,
                    "qa_pairs": [],
                    "ai_llm_optimized": False,
                    "generated_at": datetime.now().isoformat()
                }
            
            # Create complete package
            complete_package = {
                "content_id": content_id,
                "topic": topic,
                "content_type": content_type,
                "base_content": base_content,
                "optimized_content": optimized_content,
                "qa_content": qa_content,
                "schema_markup": schema_data,
                "ai_llm_optimized": True,
                "generated_at": datetime.now().isoformat(),
                "optimization_features": {
                    "conversational_qa": True,
                    "expert_authority": True,
                    "structured_data": True,
                    "ai_llm_keywords": True,
                    "comparison_elements": True,
                    "call_to_actions": True
                }
            }
            
            # Track performance
            try:
                self.performance_tracker.track_content_performance(
                    content_id,
                    content_type,
                    {"views": 0, "clicks": 0, "conversions": 0}
                )
            except Exception as e:
                self.logger.warning(f"Failed to track performance: {e}")
            
            return complete_package
            
        except Exception as e:
            self.logger.error(f"Error creating AI LLM optimized content: {e}")
            return {"error": str(e)}
    
    @require_safety_check("generate_product_comparison_package", "content_marketing")
    def generate_product_comparison_package(self, product_ids: List[str]) -> Dict[str, Any]:
        """Generate complete product comparison package optimized for AI LLM apps."""
        try:
            # Validate inputs
            if not product_ids or not isinstance(product_ids, list):
                return {"error": "product_ids must be a non-empty list"}
            
            if len(product_ids) < 2:
                return {"error": "Need at least 2 products for comparison"}
            
            # Validate each product_id
            for product_id in product_ids:
                if not isinstance(product_id, str):
                    return {"error": "All product_ids must be strings"}
            
            comparison_id = f"comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Generate comparison content
            comparison_content = self.content_generator.generate_comparison_content(product_ids)
            if "error" in comparison_content:
                return comparison_content
            
            # Generate comparison Q&A
            comparison_qa = self.qa_engine.generate_comparison_qa(product_ids)
            if "error" in comparison_qa:
                # Use fallback Q&A content
                comparison_qa = {
                    "products": [],
                    "qa_pairs": [],
                    "ai_llm_optimized": False,
                    "generated_at": datetime.now().isoformat()
                }
            
            # Get product data for schema
            products = self.db.query(Product).filter(Product.id.in_(product_ids)).all()
            if len(products) < 2:
                return {"error": "Need at least 2 products found for comparison"}
            
            product_data = [
                {
                    "name": p.name or "Unknown Product",
                    "category": p.category or "General",
                    "price": float(p.price) if p.price else 0.0,
                    "id": p.id
                }
                for p in products
            ]
            
            # Generate comparison schema
            comparison_schema = self.schema_generator.generate_comparison_schema(
                product_data,
                {
                    "id": comparison_id,
                    "title": f"Product Comparison - {', '.join([p['name'] for p in product_data])}",
                    "description": "Expert comparison of products with recommendations",
                    "generated_at": datetime.now().isoformat()
                }
            )
            
            # Optimize for AI LLM
            comparison_text = comparison_content.get("comparison", "")
            if comparison_text:
                optimized_comparison = self.seo_optimizer.optimize_for_ai_llm(
                    comparison_text,
                    "product comparison",
                    "comparison"
                )
            else:
                optimized_comparison = {"error": "No comparison content to optimize"}
            
            return {
                "comparison_id": comparison_id,
                "products": product_data,
                "comparison_content": comparison_content,
                "comparison_qa": comparison_qa,
                "optimized_comparison": optimized_comparison,
                "comparison_schema": comparison_schema,
                "ai_llm_optimized": True,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating product comparison package: {e}")
            return {"error": str(e)}
    
    @require_safety_check("create_ai_llm_content_calendar", "content_marketing")
    def create_ai_llm_content_calendar(self, days: int = 30) -> Dict[str, Any]:
        """Create AI LLM optimized content calendar."""
        try:
            # Validate days parameter
            if not isinstance(days, int) or days <= 0:
                days = 30
            
            # Get products for content ideas
            products = self.db.query(Product).filter(Product.status == "ACTIVE").all()
            
            if not products:
                return {"error": "No active products found for content calendar"}
            
            content_ideas = []
            
            # Generate content ideas for each product
            for product in products:
                if not product.name or not product.category:
                    continue
                
                # Blog post ideas
                blog_ideas = [
                    f"Best {product.category} for 2025",
                    f"How to Choose the Right {product.category}",
                    f"{product.name} vs Competitors",
                    f"Complete Guide to {product.category}",
                    f"Expert Review: {product.name}"
                ]
                
                for idea in blog_ideas:
                    content_ideas.append({
                        "type": "blog",
                        "topic": idea,
                        "product_id": product.id,
                        "priority": "high" if product.price and product.price > 100 else "medium",
                        "estimated_impact": "high"
                    })
                
                # Q&A content ideas
                qa_ideas = [
                    f"Frequently Asked Questions about {product.category}",
                    f"Expert Q&A: {product.name}",
                    f"Buying Guide: {product.category}"
                ]
                
                for idea in qa_ideas:
                    content_ideas.append({
                        "type": "qa",
                        "topic": idea,
                        "product_id": product.id,
                        "priority": "medium",
                        "estimated_impact": "medium"
                    })
            
            # Generate comparison ideas
            categories = list(set([p.category for p in products if p.category]))
            for category in categories:
                category_products = [p for p in products if p.category == category]
                if len(category_products) >= 2:
                    content_ideas.append({
                        "type": "comparison",
                        "topic": f"Best {category} Comparison",
                        "product_ids": [p.id for p in category_products[:3]],
                        "priority": "high",
                        "estimated_impact": "high"
                    })
            
            return {
                "content_calendar": content_ideas,
                "total_ideas": len(content_ideas),
                "days_covered": days,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error creating content calendar: {e}")
            return {"error": str(e)}
    
    def get_ai_llm_optimization_report(self, days: int = 30) -> Dict[str, Any]:
        """Get comprehensive AI LLM optimization report."""
        try:
            # Validate days parameter
            if not isinstance(days, int) or days <= 0:
                days = 30
            
            # Get performance data
            performance_report = self.performance_tracker.get_ai_llm_performance_report(days)
            if "error" in performance_report:
                performance_report = {"error": "Failed to get performance report"}
            
            # Get content analytics
            content_analytics = self.performance_tracker.get_content_analytics(days=days)
            if "error" in content_analytics:
                content_analytics = {"error": "Failed to get content analytics"}
            
            # Generate optimization recommendations
            recommendations = self._generate_optimization_recommendations(performance_report, content_analytics)
            
            return {
                "performance_report": performance_report,
                "content_analytics": content_analytics,
                "recommendations": recommendations,
                "analysis_period": f"Last {days} days",
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting AI LLM optimization report: {e}")
            return {"error": str(e)}
    
    def optimize_existing_content(self, content_id: str, content: str, topic: str) -> Dict[str, Any]:
        """Optimize existing content for AI LLM apps."""
        try:
            # Validate inputs
            if not content_id or not isinstance(content_id, str):
                return {"error": "content_id must be a non-empty string"}
            
            if not content or not isinstance(content, str):
                return {"error": "content must be a non-empty string"}
            
            if not topic or not isinstance(topic, str):
                return {"error": "topic must be a non-empty string"}
            
            # Optimize content
            optimized_content = self.seo_optimizer.optimize_for_ai_llm(content, topic, "blog")
            if "error" in optimized_content:
                return optimized_content
            
            # Generate Q&A content
            qa_content = self.qa_engine.generate_qa_content(topic)
            if "error" in qa_content:
                qa_content = {
                    "topic": topic,
                    "qa_pairs": [],
                    "ai_llm_optimized": False,
                    "generated_at": datetime.now().isoformat()
                }
            
            # Generate schema markup
            schema_data = self.schema_generator.generate_article_schema({
                "id": content_id,
                "title": optimized_content.get("optimized_title", ""),
                "meta_description": optimized_content.get("meta_description", ""),
                "keywords": optimized_content.get("keywords", []),
                "generated_at": datetime.now().isoformat()
            })
            
            return {
                "content_id": content_id,
                "original_content": content,
                "optimized_content": optimized_content,
                "qa_content": qa_content,
                "schema_markup": schema_data,
                "ai_llm_optimized": True,
                "optimized_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error optimizing existing content: {e}")
            return {"error": str(e)}
    
    def _generate_optimization_recommendations(self, performance_report: Dict, content_analytics: Dict) -> List[str]:
        """Generate optimization recommendations based on performance data."""
        recommendations = []
        
        try:
            # Check AI LLM app performance
            app_metrics = performance_report.get("app_metrics", {})
            app_distribution = app_metrics.get("app_distribution", {})
            
            # Recommend focus on underperforming apps
            for app, count in app_distribution.items():
                if count < 10:
                    recommendations.append(f"Focus on {app} optimization - currently low presence")
                elif count > 100:
                    recommendations.append(f"Maintain strong {app} performance - continue current strategy")
            
            # Check content performance
            metrics = content_analytics.get("metrics", {})
            if metrics.get("ctr", 0) < 2:
                recommendations.append("Improve click-through rates by optimizing titles and meta descriptions")
            
            if metrics.get("conversion_rate", 0) < 3:
                recommendations.append("Enhance conversion rates with stronger call-to-actions and product integration")
            
            # Check content types
            mention_types = app_metrics.get("mention_type_distribution", {})
            if mention_types.get("recommendation", 0) < mention_types.get("citation", 0):
                recommendations.append("Focus on becoming the go-to recommendation source rather than just citations")
            
            return recommendations if recommendations else ["Continue current AI LLM optimization strategy"]
            
        except Exception as e:
            self.logger.error(f"Error generating optimization recommendations: {e}")
            return ["Continue current AI LLM optimization strategy"]
    
    def get_ai_llm_content_summary(self) -> Dict[str, Any]:
        """Get summary of AI LLM optimized content."""
        try:
            # Get recent content
            recent_content = self.performance_tracker.get_content_analytics(days=7)
            if "error" in recent_content:
                recent_content = {"metrics": {"total_content": 0}}
            
            # Get AI LLM mentions
            ai_llm_data = self.performance_tracker.get_ai_llm_performance_report(days=7)
            if "error" in ai_llm_data:
                ai_llm_data = {"app_metrics": {"total_mentions": 0, "app_distribution": {}}}
            
            return {
                "recent_content": recent_content,
                "ai_llm_mentions": ai_llm_data,
                "summary": {
                    "total_content": recent_content.get("metrics", {}).get("total_content", 0),
                    "total_mentions": ai_llm_data.get("app_metrics", {}).get("total_mentions", 0),
                    "active_apps": len(ai_llm_data.get("app_metrics", {}).get("app_distribution", {})),
                    "optimization_status": "active"
                },
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting AI LLM content summary: {e}")
            return {"error": str(e)} 