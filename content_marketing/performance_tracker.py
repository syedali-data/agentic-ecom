"""
Content Performance Tracker for AI LLM Optimization
Tracks content performance in AI LLM apps and provides optimization insights.
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session

from db.models import Product, Customer, Order, EventLog, EventType

logger = logging.getLogger(__name__)

class ContentPerformanceTracker:
    """Tracks content performance in AI LLM apps and provides optimization insights."""
    
    def __init__(self, db: Session):
        self.db = db
        self.logger = logging.getLogger(__name__)
    
    def track_content_performance(self, content_id: str, content_type: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Track content performance metrics.
        
        Args:
            content_id: Unique content identifier
            content_type: blog, product, comparison, qa
            metrics: Performance metrics
            
        Returns:
            Tracking result with insights
        """
        try:
            # Validate inputs
            if not content_id or not isinstance(content_id, str):
                return {"error": "content_id must be a non-empty string"}
            
            if not content_type or not isinstance(content_type, str):
                return {"error": "content_type must be a non-empty string"}
            
            if not metrics or not isinstance(metrics, dict):
                metrics = {}
            
            # Store performance data
            performance_data = {
                "content_id": content_id,
                "content_type": content_type,
                "metrics": metrics,
                "tracked_at": datetime.now().isoformat()
            }
            
            # Log performance event
            self._log_performance_event(content_id, content_type, metrics)
            
            # Generate insights
            insights = self._generate_performance_insights(content_id, content_type, metrics)
            
            return {
                "content_id": content_id,
                "performance_data": performance_data,
                "insights": insights,
                "tracked_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error tracking content performance: {e}")
            return {"error": str(e)}
    
    def get_content_analytics(self, content_id: str = None, days: int = 30) -> Dict[str, Any]:
        """
        Get content analytics and performance insights.
        
        Args:
            content_id: Optional specific content ID
            days: Number of days to analyze
            
        Returns:
            Analytics data with insights
        """
        try:
            # Validate inputs
            if content_id and not isinstance(content_id, str):
                return {"error": "content_id must be a string if provided"}
            
            if not isinstance(days, int) or days <= 0:
                days = 30
            
            # Get performance data
            performance_data = self._get_performance_data(content_id, days)
            
            # Calculate metrics
            metrics = self._calculate_performance_metrics(performance_data)
            
            # Generate insights
            insights = self._generate_analytics_insights(metrics)
            
            # Get AI LLM app performance
            ai_llm_performance = self._get_ai_llm_performance(content_id, days)
            
            return {
                "performance_data": performance_data,
                "metrics": metrics,
                "insights": insights,
                "ai_llm_performance": ai_llm_performance,
                "analysis_period": f"Last {days} days",
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting content analytics: {e}")
            return {"error": str(e)}
    
    def track_ai_llm_mentions(self, content_id: str, ai_llm_app: str, mention_type: str, details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Track mentions of content in AI LLM apps.
        
        Args:
            content_id: Content identifier
            ai_llm_app: ChatGPT, Perplexity, Claude, etc.
            mention_type: recommendation, citation, answer
            details: Mention details
            
        Returns:
            Tracking result
        """
        try:
            # Validate inputs
            if not content_id or not isinstance(content_id, str):
                return {"error": "content_id must be a non-empty string"}
            
            if not ai_llm_app or not isinstance(ai_llm_app, str):
                return {"error": "ai_llm_app must be a non-empty string"}
            
            if not mention_type or not isinstance(mention_type, str):
                return {"error": "mention_type must be a non-empty string"}
            
            if not details or not isinstance(details, dict):
                details = {}
            
            mention_data = {
                "content_id": content_id,
                "ai_llm_app": ai_llm_app,
                "mention_type": mention_type,
                "details": details,
                "tracked_at": datetime.now().isoformat()
            }
            
            # Log mention event
            self._log_mention_event(content_id, ai_llm_app, mention_type, details)
            
            # Calculate mention impact
            impact = self._calculate_mention_impact(ai_llm_app, mention_type, details)
            
            return {
                "content_id": content_id,
                "mention_data": mention_data,
                "impact": impact,
                "tracked_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error tracking AI LLM mention: {e}")
            return {"error": str(e)}
    
    def get_ai_llm_performance_report(self, days: int = 30) -> Dict[str, Any]:
        """
        Get comprehensive AI LLM performance report.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Comprehensive performance report
        """
        try:
            # Validate days parameter
            if not isinstance(days, int) or days <= 0:
                days = 30
            
            # Get AI LLM app data
            ai_llm_data = self._get_ai_llm_data(days)
            
            # Calculate app-specific metrics
            app_metrics = self._calculate_app_metrics(ai_llm_data)
            
            # Generate recommendations
            recommendations = self._generate_ai_llm_recommendations(app_metrics)
            
            # Get top performing content
            top_content = self._get_top_performing_content(days)
            
            return {
                "ai_llm_data": ai_llm_data,
                "app_metrics": app_metrics,
                "recommendations": recommendations,
                "top_content": top_content,
                "analysis_period": f"Last {days} days",
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting AI LLM performance report: {e}")
            return {"error": str(e)}
    
    def _log_performance_event(self, content_id: str, content_type: str, metrics: Dict[str, Any]):
        """Log performance event to database."""
        try:
            event_data = {
                "event_type": EventType.PRODUCT_UPDATED,  # Using existing event type
                "source": "performance_tracker",
                "data": {
                    "content_id": content_id,
                    "content_type": content_type,
                    "metrics": metrics,
                    "timestamp": datetime.now().isoformat()
                },
                "processed": False
            }
            
            # Create event log entry
            event_log = EventLog(**event_data)
            self.db.add(event_log)
            self.db.commit()
            
        except Exception as e:
            self.logger.error(f"Error logging performance event: {e}")
    
    def _log_mention_event(self, content_id: str, ai_llm_app: str, mention_type: str, details: Dict[str, Any]):
        """Log AI LLM mention event to database."""
        try:
            event_data = {
                "event_type": EventType.PRODUCT_UPDATED,  # Using existing event type
                "source": "ai_llm_tracker",
                "data": {
                    "content_id": content_id,
                    "ai_llm_app": ai_llm_app,
                    "mention_type": mention_type,
                    "details": details,
                    "timestamp": datetime.now().isoformat()
                },
                "processed": False
            }
            
            # Create event log entry
            event_log = EventLog(**event_data)
            self.db.add(event_log)
            self.db.commit()
            
        except Exception as e:
            self.logger.error(f"Error logging mention event: {e}")
    
    def _get_performance_data(self, content_id: str = None, days: int = 30) -> List[Dict[str, Any]]:
        """Get performance data from database."""
        try:
            start_date = datetime.now() - timedelta(days=days)
            
            query = self.db.query(EventLog).filter(
                EventLog.source == "performance_tracker",
                EventLog.created_at >= start_date
            )
            
            if content_id:
                query = query.filter(EventLog.data.contains({"content_id": content_id}))
            
            events = query.all()
            
            performance_data = []
            for event in events:
                try:
                    if event.data and isinstance(event.data, dict) and "content_id" in event.data:
                        performance_data.append({
                            "content_id": event.data.get("content_id"),
                            "content_type": event.data.get("content_type"),
                            "metrics": event.data.get("metrics", {}),
                            "timestamp": event.data.get("timestamp", event.created_at.isoformat())
                        })
                except Exception:
                    continue
            
            return performance_data
            
        except Exception as e:
            self.logger.error(f"Error getting performance data: {e}")
            return []
    
    def _get_ai_llm_data(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get AI LLM mention data from database."""
        try:
            start_date = datetime.now() - timedelta(days=days)
            
            events = self.db.query(EventLog).filter(
                EventLog.source == "ai_llm_tracker",
                EventLog.created_at >= start_date
            ).all()
            
            ai_llm_data = []
            for event in events:
                try:
                    if event.data and isinstance(event.data, dict) and "content_id" in event.data:
                        ai_llm_data.append({
                            "content_id": event.data.get("content_id"),
                            "ai_llm_app": event.data.get("ai_llm_app"),
                            "mention_type": event.data.get("mention_type"),
                            "details": event.data.get("details", {}),
                            "timestamp": event.data.get("timestamp", event.created_at.isoformat())
                        })
                except Exception:
                    continue
            
            return ai_llm_data
            
        except Exception as e:
            self.logger.error(f"Error getting AI LLM data: {e}")
            return []
    
    def _get_ai_llm_performance(self, content_id: str, days: int) -> Dict[str, Any]:
        """Get AI LLM performance data for specific content."""
        try:
            ai_llm_data = self._get_ai_llm_data(days)
            
            if content_id:
                ai_llm_data = [item for item in ai_llm_data if item.get("content_id") == content_id]
            
            app_metrics = self._calculate_app_metrics(ai_llm_data)
            
            return {
                "ai_llm_data": ai_llm_data,
                "app_metrics": app_metrics,
                "analysis_period": f"Last {days} days"
            }
            
        except Exception as e:
            self.logger.error(f"Error getting AI LLM performance: {e}")
            return {"ai_llm_data": [], "app_metrics": self._get_default_app_metrics()}
    
    def _calculate_performance_metrics(self, performance_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate performance metrics from data."""
        try:
            if not performance_data or not isinstance(performance_data, list):
                return self._get_default_metrics()
            
            total_content = len(set(item.get("content_id", "") for item in performance_data if item.get("content_id")))
            total_views = sum(item.get("metrics", {}).get("views", 0) for item in performance_data)
            total_clicks = sum(item.get("metrics", {}).get("clicks", 0) for item in performance_data)
            total_conversions = sum(item.get("metrics", {}).get("conversions", 0) for item in performance_data)
            
            avg_views = total_views / len(performance_data) if performance_data else 0
            avg_clicks = total_clicks / len(performance_data) if performance_data else 0
            avg_conversions = total_conversions / len(performance_data) if performance_data else 0
            
            ctr = (total_clicks / total_views * 100) if total_views > 0 else 0
            conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
            
            return {
                "total_content": total_content,
                "total_views": total_views,
                "total_clicks": total_clicks,
                "total_conversions": total_conversions,
                "avg_views": round(avg_views, 2),
                "avg_clicks": round(avg_clicks, 2),
                "avg_conversions": round(avg_conversions, 2),
                "ctr": round(ctr, 2),
                "conversion_rate": round(conversion_rate, 2)
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating performance metrics: {e}")
            return self._get_default_metrics()
    
    def _calculate_app_metrics(self, ai_llm_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate AI LLM app-specific metrics."""
        try:
            if not ai_llm_data or not isinstance(ai_llm_data, list):
                return self._get_default_app_metrics()
            
            app_counts = {}
            mention_type_counts = {}
            content_mentions = {}
            
            for item in ai_llm_data:
                if not isinstance(item, dict):
                    continue
                
                app = item.get("ai_llm_app", "")
                mention_type = item.get("mention_type", "")
                content_id = item.get("content_id", "")
                
                if app:
                    app_counts[app] = app_counts.get(app, 0) + 1
                
                if mention_type:
                    mention_type_counts[mention_type] = mention_type_counts.get(mention_type, 0) + 1
                
                if content_id:
                    content_mentions[content_id] = content_mentions.get(content_id, 0) + 1
            
            return {
                "app_distribution": app_counts,
                "mention_type_distribution": mention_type_counts,
                "content_mentions": content_mentions,
                "total_mentions": len(ai_llm_data),
                "unique_content": len(content_mentions),
                "unique_apps": len(app_counts)
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating app metrics: {e}")
            return self._get_default_app_metrics()
    
    def _generate_performance_insights(self, content_id: str, content_type: str, metrics: Dict[str, Any]) -> List[str]:
        """Generate performance insights."""
        insights = []
        
        try:
            if not metrics or not isinstance(metrics, dict):
                return ["Performance analysis completed"]
            
            views = metrics.get("views", 0)
            clicks = metrics.get("clicks", 0)
            conversions = metrics.get("conversions", 0)
            
            if views > 0:
                ctr = (clicks / views) * 100
                if ctr > 5:
                    insights.append("High click-through rate indicates strong content appeal")
                elif ctr < 1:
                    insights.append("Low click-through rate - consider optimizing title and meta description")
            
            if clicks > 0:
                conversion_rate = (conversions / clicks) * 100
                if conversion_rate > 10:
                    insights.append("Excellent conversion rate - content is driving sales effectively")
                elif conversion_rate < 2:
                    insights.append("Low conversion rate - consider adding stronger call-to-actions")
            
            if views > 1000:
                insights.append("High visibility content - consider expanding on this topic")
            elif views < 100:
                insights.append("Low visibility - consider SEO optimization and promotion")
            
            return insights if insights else ["Performance analysis completed"]
            
        except Exception as e:
            self.logger.error(f"Error generating performance insights: {e}")
            return ["Performance analysis completed"]
    
    def _generate_analytics_insights(self, metrics: Dict[str, Any]) -> List[str]:
        """Generate analytics insights."""
        insights = []
        
        try:
            if not metrics or not isinstance(metrics, dict):
                return ["Analytics analysis completed"]
            
            ctr = metrics.get("ctr", 0)
            conversion_rate = metrics.get("conversion_rate", 0)
            total_views = metrics.get("total_views", 0)
            
            if ctr > 3:
                insights.append("Overall CTR is strong - content is engaging users effectively")
            elif ctr < 1:
                insights.append("Low overall CTR - focus on improving content titles and descriptions")
            
            if conversion_rate > 5:
                insights.append("Good conversion rate - content is driving sales")
            elif conversion_rate < 1:
                insights.append("Low conversion rate - review call-to-actions and product integration")
            
            if total_views > 10000:
                insights.append("High content visibility - excellent reach")
            elif total_views < 1000:
                insights.append("Limited visibility - focus on content promotion and SEO")
            
            return insights if insights else ["Analytics analysis completed"]
            
        except Exception as e:
            self.logger.error(f"Error generating analytics insights: {e}")
            return ["Analytics analysis completed"]
    
    def _generate_ai_llm_recommendations(self, app_metrics: Dict[str, Any]) -> List[str]:
        """Generate AI LLM optimization recommendations."""
        recommendations = []
        
        try:
            if not app_metrics or not isinstance(app_metrics, dict):
                return ["AI LLM optimization analysis completed"]
            
            app_distribution = app_metrics.get("app_distribution", {})
            
            # Check app performance
            for app, count in app_distribution.items():
                if count > 100:
                    recommendations.append(f"Strong performance in {app} - continue optimizing for this platform")
                elif count < 10:
                    recommendations.append(f"Limited presence in {app} - focus on platform-specific optimization")
            
            # Check mention types
            mention_types = app_metrics.get("mention_type_distribution", {})
            if mention_types.get("recommendation", 0) > mention_types.get("citation", 0):
                recommendations.append("Strong recommendation mentions - focus on maintaining quality")
            else:
                recommendations.append("More citations than recommendations - work on becoming the go-to source")
            
            return recommendations if recommendations else ["AI LLM optimization analysis completed"]
            
        except Exception as e:
            self.logger.error(f"Error generating AI LLM recommendations: {e}")
            return ["AI LLM optimization analysis completed"]
    
    def _get_top_performing_content(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get top performing content."""
        try:
            performance_data = self._get_performance_data(days=days)
            
            if not performance_data:
                return []
            
            # Group by content ID and calculate total metrics
            content_metrics = {}
            for item in performance_data:
                if not isinstance(item, dict):
                    continue
                
                content_id = item.get("content_id", "")
                if not content_id:
                    continue
                
                if content_id not in content_metrics:
                    content_metrics[content_id] = {
                        "views": 0,
                        "clicks": 0,
                        "conversions": 0,
                        "content_type": item.get("content_type", "unknown")
                    }
                
                metrics = item.get("metrics", {})
                content_metrics[content_id]["views"] += metrics.get("views", 0)
                content_metrics[content_id]["clicks"] += metrics.get("clicks", 0)
                content_metrics[content_id]["conversions"] += metrics.get("conversions", 0)
            
            # Sort by total views
            sorted_content = sorted(
                content_metrics.items(),
                key=lambda x: x[1]["views"],
                reverse=True
            )
            
            return [
                {
                    "content_id": content_id,
                    "metrics": metrics,
                    "ctr": round((metrics["clicks"] / metrics["views"] * 100), 2) if metrics["views"] > 0 else 0
                }
                for content_id, metrics in sorted_content[:10]
            ]
            
        except Exception as e:
            self.logger.error(f"Error getting top performing content: {e}")
            return []
    
    def _calculate_mention_impact(self, ai_llm_app: str, mention_type: str, details: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate impact of AI LLM mention."""
        try:
            impact_score = 0
            
            # Base impact by app
            app_impact = {
                "ChatGPT": 10,
                "Perplexity": 8,
                "Claude": 7,
                "Google AI": 9,
                "Bing AI": 6
            }
            impact_score += app_impact.get(ai_llm_app, 5)
            
            # Impact by mention type
            type_impact = {
                "recommendation": 10,
                "citation": 5,
                "answer": 7,
                "comparison": 8
            }
            impact_score += type_impact.get(mention_type, 3)
            
            # Additional impact factors
            if details.get("featured", False):
                impact_score += 5
            
            user_engagement = details.get("user_engagement", 0)
            if isinstance(user_engagement, (int, float)) and user_engagement > 100:
                impact_score += 3
            
            return {
                "impact_score": impact_score,
                "app_impact": app_impact.get(ai_llm_app, 5),
                "type_impact": type_impact.get(mention_type, 3),
                "total_impact": impact_score
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating mention impact: {e}")
            return {"impact_score": 0, "total_impact": 0}
    
    def _get_default_metrics(self) -> Dict[str, Any]:
        """Get default metrics when no data is available."""
        return {
            "total_content": 0,
            "total_views": 0,
            "total_clicks": 0,
            "total_conversions": 0,
            "avg_views": 0,
            "avg_clicks": 0,
            "avg_conversions": 0,
            "ctr": 0,
            "conversion_rate": 0
        }
    
    def _get_default_app_metrics(self) -> Dict[str, Any]:
        """Get default app metrics when no data is available."""
        return {
            "app_distribution": {},
            "mention_type_distribution": {},
            "content_mentions": {},
            "total_mentions": 0,
            "unique_content": 0,
            "unique_apps": 0
        } 