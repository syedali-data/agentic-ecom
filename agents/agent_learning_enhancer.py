"""
Agent Learning Enhancer
Provides methods to improve agent intelligence through data enrichment and training.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from memory.memory_store import MemoryStore
from content_marketing.performance_tracker import ContentPerformanceTracker

logger = logging.getLogger(__name__)

class AgentLearningEnhancer:
    """
    Enhances agent intelligence through data enrichment, training, and optimization.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.memory_store = MemoryStore()
        self.performance_tracker = ContentPerformanceTracker(db)
        self.logger = logging.getLogger(__name__)
    
    def enrich_agent_training_data(self, agent_type: str, data_source: str = "performance") -> Dict[str, Any]:
        """
        Enrich agent training data with performance insights and historical decisions.
        
        Args:
            agent_type: Type of agent (sales_genie, logibot, buybot)
            data_source: Source of training data (performance, decisions, interactions)
            
        Returns:
            Enriched training data
        """
        try:
            enriched_data = {
                "agent_type": agent_type,
                "enrichment_date": datetime.now().isoformat(),
                "data_sources": [],
                "insights": [],
                "recommendations": []
            }
            
            # Get historical agent decisions
            if data_source in ["performance", "decisions"]:
                try:
                    decisions = self.memory_store.get_agent_insights(agent_type)
                    if isinstance(decisions, list):
                        enriched_data["data_sources"].append("agent_decisions")
                        enriched_data["insights"].extend(self._analyze_decisions(decisions))
                except Exception as e:
                    self.logger.warning(f"Could not retrieve agent decisions: {e}")
            
            # Get performance metrics
            if data_source in ["performance", "metrics"]:
                try:
                    performance = self.performance_tracker.get_content_analytics(days=30)
                    if isinstance(performance, list):
                        enriched_data["data_sources"].append("performance_metrics")
                        enriched_data["insights"].extend(self._analyze_performance(performance))
                except Exception as e:
                    self.logger.warning(f"Could not retrieve performance metrics: {e}")
            
            # Get customer interactions
            if data_source in ["interactions", "all"]:
                try:
                    interactions = self._get_customer_interactions(agent_type)
                    if isinstance(interactions, list):
                        enriched_data["data_sources"].append("customer_interactions")
                        enriched_data["insights"].extend(self._analyze_interactions(interactions))
                except Exception as e:
                    self.logger.warning(f"Could not retrieve customer interactions: {e}")
            
            # Generate recommendations
            enriched_data["recommendations"] = self._generate_recommendations(enriched_data["insights"])
            
            self.logger.info(f"✅ Enriched training data for {agent_type}")
            return enriched_data
            
        except Exception as e:
            self.logger.error(f"❌ Error enriching training data: {e}")
            return {"error": str(e)}
    
    def create_agent_training_dataset(self, agent_type: str, days: int = 30) -> Dict[str, Any]:
        """
        Create a comprehensive training dataset for agent improvement.
        
        Args:
            agent_type: Type of agent
            days: Number of days to include in dataset
            
        Returns:
            Training dataset
        """
        try:
            dataset = {
                "agent_type": agent_type,
                "created_at": datetime.now().isoformat(),
                "timeframe_days": days,
                "training_examples": [],
                "performance_metrics": {},
                "optimization_targets": []
            }
            
            # Get historical data
            try:
                decisions = self.memory_store.get_agent_insights(agent_type)
                if not isinstance(decisions, list):
                    decisions = []
            except Exception as e:
                self.logger.warning(f"Could not retrieve agent insights: {e}")
                decisions = []
            
            try:
                performance = self.performance_tracker.get_content_analytics(days=days)
                if not isinstance(performance, list):
                    performance = []
            except Exception as e:
                self.logger.warning(f"Could not retrieve performance data: {e}")
                performance = []
            
            # Create training examples
            for decision in decisions:
                example = self._create_training_example(decision, performance)
                if example:
                    dataset["training_examples"].append(example)
            
            # Calculate performance metrics
            dataset["performance_metrics"] = self._calculate_performance_metrics(performance)
            
            # Identify optimization targets
            dataset["optimization_targets"] = self._identify_optimization_targets(dataset)
            
            self.logger.info(f"✅ Created training dataset for {agent_type}: {len(dataset['training_examples'])} examples")
            return dataset
            
        except Exception as e:
            self.logger.error(f"❌ Error creating training dataset: {e}")
            return {"error": str(e)}
    
    def optimize_agent_prompts(self, agent_type: str, optimization_goal: str = "performance") -> Dict[str, Any]:
        """
        Optimize agent prompts based on historical performance and decisions.
        
        Args:
            agent_type: Type of agent
            optimization_goal: Goal for optimization (performance, accuracy, efficiency)
            
        Returns:
            Optimized prompts
        """
        try:
            # Get historical insights
            try:
                insights = self.memory_store.get_agent_insights(agent_type)
                if not isinstance(insights, list):
                    insights = []
            except Exception as e:
                self.logger.warning(f"Could not retrieve agent insights: {e}")
                insights = []
            
            try:
                performance = self.performance_tracker.get_content_analytics(days=30)
                if not isinstance(performance, list):
                    performance = []
            except Exception as e:
                self.logger.warning(f"Could not retrieve performance data: {e}")
                performance = []
            
            # Analyze patterns
            patterns = self._analyze_decision_patterns(insights)
            performance_patterns = self._analyze_performance_patterns(performance)
            
            # Generate optimized prompts
            optimized_prompts = self._generate_optimized_prompts(
                agent_type, patterns, performance_patterns, optimization_goal
            )
            
            self.logger.info(f"✅ Optimized prompts for {agent_type}")
            return optimized_prompts
            
        except Exception as e:
            self.logger.error(f"❌ Error optimizing prompts: {e}")
            return {"error": str(e)}
    
    def _analyze_decisions(self, decisions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze agent decisions for patterns and insights."""
        insights = []
        
        for decision in decisions:
            insight = {
                "decision_type": decision.get("decision_type"),
                "success_patterns": [],
                "failure_patterns": [],
                "recommendations": []
            }
            
            # Analyze decision patterns (simplified)
            if decision.get("content"):
                content = decision["content"]
                if "success" in content.lower() or "positive" in content.lower():
                    insight["success_patterns"].append("positive_outcome")
                elif "failure" in content.lower() or "negative" in content.lower():
                    insight["failure_patterns"].append("negative_outcome")
            
            insights.append(insight)
        
        return insights
    
    def _analyze_performance(self, performance: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze performance metrics for insights."""
        insights = []
        
        for metric in performance:
            insight = {
                "metric_type": metric.get("content_type"),
                "performance_score": metric.get("engagement_rate", 0),
                "trend": "improving" if metric.get("engagement_rate", 0) > 0.05 else "declining",
                "recommendations": []
            }
            
            if insight["performance_score"] < 0.03:
                insight["recommendations"].append("Consider content optimization")
            
            insights.append(insight)
        
        return insights
    
    def _analyze_interactions(self, interactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze customer interactions for insights."""
        insights = []
        
        for interaction in interactions:
            insight = {
                "interaction_type": interaction.get("interaction_type"),
                "customer_satisfaction": "positive",
                "improvement_areas": []
            }
            
            # Analyze interaction content for sentiment
            content = interaction.get("content", "")
            if any(word in content.lower() for word in ["problem", "issue", "complaint"]):
                insight["customer_satisfaction"] = "negative"
                insight["improvement_areas"].append("customer_support")
            
            insights.append(insight)
        
        return insights
    
    def _get_customer_interactions(self, agent_type: str) -> List[Dict[str, Any]]:
        """Get customer interactions related to agent type."""
        # This would query the memory store for customer interactions
        # For now, return empty list
        return []
    
    def _create_training_example(self, decision: Dict[str, Any], performance: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Create a training example from decision and performance data."""
        try:
            example = {
                "input": decision.get("content", ""),
                "output": decision.get("decision_type", ""),
                "metadata": decision.get("metadata", {}),
                "performance_score": 0.5  # Default score
            }
            
            # Calculate performance score based on related performance data
            # This is a simplified implementation
            return example
            
        except Exception as e:
            self.logger.error(f"Error creating training example: {e}")
            return None
    
    def _calculate_performance_metrics(self, performance: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate overall performance metrics."""
        if not performance:
            return {}
        
        total_views = sum(p.get("views", 0) for p in performance)
        total_clicks = sum(p.get("clicks", 0) for p in performance)
        total_conversions = sum(p.get("conversions", 0) for p in performance)
        
        return {
            "total_views": total_views,
            "total_clicks": total_clicks,
            "total_conversions": total_conversions,
            "overall_engagement_rate": total_clicks / total_views if total_views > 0 else 0,
            "conversion_rate": total_conversions / total_clicks if total_clicks > 0 else 0
        }
    
    def _identify_optimization_targets(self, dataset: Dict[str, Any]) -> List[str]:
        """Identify areas for optimization based on dataset analysis."""
        targets = []
        
        # Analyze performance metrics
        metrics = dataset.get("performance_metrics", {})
        if metrics.get("overall_engagement_rate", 0) < 0.05:
            targets.append("improve_engagement_rate")
        
        if metrics.get("conversion_rate", 0) < 0.02:
            targets.append("improve_conversion_rate")
        
        # Analyze training examples
        examples = dataset.get("training_examples", [])
        if len(examples) < 10:
            targets.append("increase_training_data")
        
        return targets
    
    def _analyze_decision_patterns(self, insights: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze patterns in agent decisions."""
        patterns = {
            "success_patterns": [],
            "failure_patterns": [],
            "common_decisions": []
        }
        
        # Simplified pattern analysis
        for insight in insights:
            decision_type = insight.get("decision_type")
            if decision_type:
                patterns["common_decisions"].append(decision_type)
        
        return patterns
    
    def _analyze_performance_patterns(self, performance: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze patterns in performance data."""
        patterns = {
            "high_performing_content": [],
            "low_performing_content": [],
            "trends": []
        }
        
        # Simplified pattern analysis
        for metric in performance:
            if metric.get("engagement_rate", 0) > 0.05:
                patterns["high_performing_content"].append(metric.get("content_type"))
            else:
                patterns["low_performing_content"].append(metric.get("content_type"))
        
        return patterns
    
    def _generate_optimized_prompts(self, agent_type: str, patterns: Dict[str, Any], 
                                  performance_patterns: Dict[str, Any], goal: str) -> Dict[str, Any]:
        """Generate optimized prompts based on analysis."""
        optimized_prompts = {
            "agent_type": agent_type,
            "optimization_goal": goal,
            "prompts": {}
        }
        
        # Generate prompts based on patterns and goals
        if goal == "performance":
            optimized_prompts["prompts"]["main"] = f"""
            Based on historical performance analysis for {agent_type}:
            - High-performing content types: {performance_patterns.get('high_performing_content', [])}
            - Success patterns: {patterns.get('success_patterns', [])}
            
            Focus on these areas for optimal performance.
            """
        
        return optimized_prompts 

    def _generate_recommendations(self, insights: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on insights analysis."""
        recommendations = []
        
        # Analyze insights for patterns
        success_count = 0
        failure_count = 0
        low_performance_count = 0
        
        for insight in insights:
            if insight.get("success_patterns"):
                success_count += 1
            if insight.get("failure_patterns"):
                failure_count += 1
            if insight.get("performance_score", 0) < 0.03:
                low_performance_count += 1
        
        # Generate recommendations based on patterns
        if failure_count > success_count:
            recommendations.append("Focus on improving decision accuracy")
        
        if low_performance_count > 0:
            recommendations.append("Optimize content for better engagement")
        
        if len(insights) < 5:
            recommendations.append("Increase training data collection")
        
        if not recommendations:
            recommendations.append("Continue current optimization strategies")
        
        return recommendations 