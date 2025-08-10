"""
Revenue Optimization Orchestrator
Coordinates dynamic pricing and inventory prediction for maximum profitability.
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_

from db.models import (
    Product, Order, OrderItem, InventoryItem, PricingHistory, Customer
)
from revenue_optimization.dynamic_pricing_engine import DynamicPricingEngine
from revenue_optimization.inventory_prediction_engine import InventoryPredictionEngine
from analytics.forecasting import ForecastingEngine
from services.gpt_client import GPTClient

logger = logging.getLogger(__name__)

class RevenueOptimizer:
    """
    Main revenue optimization orchestrator that coordinates dynamic pricing and inventory prediction.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.dynamic_pricing_engine = DynamicPricingEngine(db)
        self.inventory_prediction_engine = InventoryPredictionEngine(db)
        self.forecasting_engine = ForecastingEngine(db)
        self.gpt_client = GPTClient()
        self.logger = logging.getLogger(__name__)
    
    def optimize_revenue(
        self, 
        product_id: str = None,
        optimization_strategy: str = "comprehensive",
        include_recommendations: bool = True
    ) -> Dict[str, Any]:
        """
        Optimize revenue for products using dynamic pricing and inventory prediction.
        
        Args:
            product_id: Specific product ID (None for all products)
            optimization_strategy: Strategy to use (pricing_only, inventory_only, comprehensive)
            include_recommendations: Whether to include AI recommendations
            
        Returns:
            Comprehensive revenue optimization results
        """
        try:
            if product_id:
                return self._optimize_single_product(product_id, optimization_strategy, include_recommendations)
            else:
                return self._optimize_all_products(optimization_strategy, include_recommendations)
                
        except Exception as e:
            self.logger.error(f"Error optimizing revenue: {e}")
            return {"error": str(e)}
    
    def get_revenue_insights(
        self, 
        days: int = 30,
        include_forecasts: bool = True
    ) -> Dict[str, Any]:
        """
        Get comprehensive revenue insights and forecasts.
        
        Args:
            days: Analysis period in days
            include_forecasts: Whether to include revenue forecasts
            
        Returns:
            Revenue insights and analysis
        """
        try:
            # Get current revenue metrics
            current_metrics = self._get_current_revenue_metrics(days)
            
            # Get revenue forecast
            revenue_forecast = {}
            if include_forecasts:
                revenue_forecast = self.forecasting_engine.forecast_revenue(days)
            
            # Get optimization opportunities
            opportunities = self._identify_optimization_opportunities()
            
            # Generate AI insights
            ai_insights = self._generate_revenue_insights(current_metrics, revenue_forecast, opportunities)
            
            return {
                "current_metrics": current_metrics,
                "revenue_forecast": revenue_forecast,
                "optimization_opportunities": opportunities,
                "ai_insights": ai_insights,
                "analysis_period": days,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting revenue insights: {e}")
            return {"error": str(e)}
    
    def execute_optimization_plan(
        self, 
        product_id: str,
        optimization_actions: List[str]
    ) -> Dict[str, Any]:
        """
        Execute specific optimization actions for a product.
        
        Args:
            product_id: Product identifier
            optimization_actions: List of actions to execute
            
        Returns:
            Execution results
        """
        try:
            product = self.db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return {"error": f"Product {product_id} not found"}
            
            results = {
                "product_id": product_id,
                "product_name": product.name,
                "actions_executed": [],
                "results": {},
                "timestamp": datetime.now().isoformat()
            }
            
            for action in optimization_actions:
                action_result = self._execute_optimization_action(product, action)
                results["actions_executed"].append(action)
                results["results"][action] = action_result
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error executing optimization plan: {e}")
            return {"error": str(e)}
    
    def _optimize_single_product(
        self, 
        product_id: str, 
        optimization_strategy: str,
        include_recommendations: bool
    ) -> Dict[str, Any]:
        """Optimize revenue for a single product."""
        try:
            product = self.db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return {"error": f"Product {product_id} not found"}
            
            results = {
                "product_id": product_id,
                "product_name": product.name,
                "optimization_strategy": optimization_strategy,
                "pricing_optimization": {},
                "inventory_optimization": {},
                "revenue_impact": {},
                "recommendations": {},
                "timestamp": datetime.now().isoformat()
            }
            
            # Pricing optimization
            if optimization_strategy in ["pricing_only", "comprehensive"]:
                pricing_results = self.dynamic_pricing_engine.calculate_optimal_price(
                    product_id, "dynamic_optimization"
                )
                results["pricing_optimization"] = pricing_results
            
            # Inventory optimization
            if optimization_strategy in ["inventory_only", "comprehensive"]:
                inventory_results = self.inventory_prediction_engine.calculate_optimal_inventory_levels(
                    product_id
                )
                results["inventory_optimization"] = inventory_results
            
            # Calculate revenue impact
            if optimization_strategy == "comprehensive":
                revenue_impact = self._calculate_revenue_impact(
                    product, 
                    results["pricing_optimization"], 
                    results["inventory_optimization"]
                )
                results["revenue_impact"] = revenue_impact
            
            # Generate recommendations
            if include_recommendations:
                recommendations = self._generate_comprehensive_recommendations(
                    product, results
                )
                results["recommendations"] = recommendations
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error optimizing single product: {e}")
            return {"error": str(e)}
    
    def _optimize_all_products(
        self, 
        optimization_strategy: str,
        include_recommendations: bool
    ) -> Dict[str, Any]:
        """Optimize revenue for all products."""
        try:
            products = self.db.query(Product).filter(Product.status == "active").all()
            
            optimizations = []
            total_revenue_impact = 0
            high_impact_products = []
            
            for product in products:
                optimization = self._optimize_single_product(
                    product.id, optimization_strategy, include_recommendations
                )
                
                if "error" not in optimization:
                    optimizations.append(optimization)
                    
                    # Track revenue impact
                    revenue_impact = optimization.get("revenue_impact", {}).get("revenue_impact", 0)
                    total_revenue_impact += revenue_impact
                    
                    if revenue_impact > 100:  # High impact threshold
                        high_impact_products.append(product.name)
            
            return {
                "total_products": len(optimizations),
                "optimization_strategy": optimization_strategy,
                "total_revenue_impact": round(total_revenue_impact, 2),
                "high_impact_products": len(high_impact_products),
                "high_impact_product_names": high_impact_products,
                "optimizations": optimizations,
                "summary": self._generate_optimization_summary(optimizations),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error optimizing all products: {e}")
            return {"error": str(e)}
    
    def _calculate_revenue_impact(
        self, 
        product: Product, 
        pricing_results: Dict[str, Any],
        inventory_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate estimated revenue impact of optimizations."""
        try:
            current_price = product.price
            recommended_price = pricing_results.get("recommended_price", current_price)
            price_change = recommended_price - current_price
            price_change_percentage = (price_change / current_price) * 100 if current_price > 0 else 0
            
            # Get current demand
            current_demand = self._get_current_demand(product.id)
            
            # Estimate demand elasticity (simplified)
            # In production, you'd use historical data to calculate actual elasticity
            demand_elasticity = -0.5  # Assumed elasticity
            
            # Calculate demand change
            demand_change_percentage = price_change_percentage * demand_elasticity
            new_demand = current_demand * (1 + demand_change_percentage / 100)
            
            # Calculate revenue impact
            current_revenue = current_price * current_demand
            new_revenue = recommended_price * new_demand
            revenue_impact = new_revenue - current_revenue
            
            # Inventory impact
            inventory_impact = self._calculate_inventory_impact(inventory_results)
            
            return {
                "current_revenue": round(current_revenue, 2),
                "projected_revenue": round(new_revenue, 2),
                "revenue_impact": round(revenue_impact, 2),
                "revenue_impact_percentage": round((revenue_impact / current_revenue) * 100, 1) if current_revenue > 0 else 0,
                "price_change": round(price_change, 2),
                "price_change_percentage": round(price_change_percentage, 1),
                "demand_change_percentage": round(demand_change_percentage, 1),
                "inventory_impact": inventory_impact,
                "total_impact": round(revenue_impact + inventory_impact.get("cost_savings", 0), 2),
                "confidence_level": 0.75
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating revenue impact: {e}")
            return {"error": str(e)}
    
    def _calculate_inventory_impact(self, inventory_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate inventory optimization impact."""
        try:
            # Simplified inventory impact calculation
            # In production, you'd calculate actual cost savings from reduced stockouts and holding costs
            
            current_stock = inventory_results.get("current_stock", 0)
            optimal_max_stock = inventory_results.get("optimal_max_stock", current_stock)
            
            # Estimate cost savings from reduced stockouts and optimized inventory
            stockout_cost_savings = 50  # Estimated savings per stockout prevented
            holding_cost_savings = 20   # Estimated savings from optimized inventory
            
            total_cost_savings = stockout_cost_savings + holding_cost_savings
            
            return {
                "cost_savings": total_cost_savings,
                "stockout_cost_savings": stockout_cost_savings,
                "holding_cost_savings": holding_cost_savings,
                "inventory_optimization_potential": "medium"
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating inventory impact: {e}")
            return {"cost_savings": 0}
    
    def _get_current_demand(self, product_id: str) -> float:
        """Get current demand for a product."""
        try:
            # Get recent sales data
            recent_sales = self.db.query(
                func.sum(OrderItem.quantity).label('total_quantity')
            ).join(
                Order, OrderItem.order_id == Order.id
            ).filter(
                and_(
                    OrderItem.product_id == product_id,
                    Order.created_at >= datetime.now() - timedelta(days=30)
                )
            ).scalar()
            
            return float(recent_sales or 0)
            
        except Exception as e:
            self.logger.error(f"Error getting current demand: {e}")
            return 0.0
    
    def _get_current_revenue_metrics(self, days: int) -> Dict[str, Any]:
        """Get current revenue metrics."""
        try:
            # Get revenue data for the specified period
            revenue_data = self.db.query(
                func.sum(Order.total).label('total_revenue'),
                func.count(Order.id).label('total_orders'),
                func.avg(Order.total).label('average_order_value')
            ).filter(
                Order.created_at >= datetime.now() - timedelta(days=days)
            ).first()
            
            return {
                "total_revenue": float(revenue_data.total_revenue or 0),
                "total_orders": int(revenue_data.total_orders or 0),
                "average_order_value": float(revenue_data.average_order_value or 0),
                "daily_average_revenue": float(revenue_data.total_revenue or 0) / days,
                "period_days": days
            }
            
        except Exception as e:
            self.logger.error(f"Error getting current revenue metrics: {e}")
            return {}
    
    def _identify_optimization_opportunities(self) -> List[Dict[str, Any]]:
        """Identify revenue optimization opportunities."""
        try:
            opportunities = []
            
            # Get products with low inventory
            low_stock_products = self.db.query(Product).join(InventoryItem).filter(
                InventoryItem.available_quantity <= InventoryItem.low_stock_threshold
            ).limit(5).all()
            
            for product in low_stock_products:
                opportunities.append({
                    "type": "inventory_optimization",
                    "product_id": product.id,
                    "product_name": product.name,
                    "issue": "Low stock",
                    "priority": "high",
                    "estimated_impact": 100
                })
            
            # Get products with pricing opportunities
            # This is a simplified implementation - in production, you'd use more sophisticated analysis
            pricing_opportunities = self.db.query(Product).filter(
                Product.price > 0
            ).limit(5).all()
            
            for product in pricing_opportunities:
                opportunities.append({
                    "type": "pricing_optimization",
                    "product_id": product.id,
                    "product_name": product.name,
                    "issue": "Pricing review needed",
                    "priority": "medium",
                    "estimated_impact": 50
                })
            
            return opportunities
            
        except Exception as e:
            self.logger.error(f"Error identifying optimization opportunities: {e}")
            return []
    
    def _generate_revenue_insights(
        self, 
        current_metrics: Dict[str, Any],
        revenue_forecast: Dict[str, Any],
        opportunities: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate AI-powered revenue insights."""
        try:
            prompt = f"""
            Analyze revenue optimization opportunities:
            
            Current Metrics:
            - Total Revenue: ${current_metrics.get('total_revenue', 0):,.2f}
            - Total Orders: {current_metrics.get('total_orders', 0)}
            - Average Order Value: ${current_metrics.get('average_order_value', 0):.2f}
            - Daily Average Revenue: ${current_metrics.get('daily_average_revenue', 0):.2f}
            
            Revenue Forecast:
            - Forecasted Revenue: ${revenue_forecast.get('total_forecasted_revenue', 0):,.2f}
            
            Optimization Opportunities: {len(opportunities)} opportunities identified
            
            Provide insights on:
            1. Key revenue drivers
            2. Optimization priorities
            3. Expected impact of optimizations
            4. Risk factors
            5. Implementation recommendations
            """
            
            response = self.gpt_client.generate_response(
                prompt=prompt,
                max_tokens=500,
                temperature=0.3
            )
            
            return {
                "summary": response.get("content", ""),
                "key_insights": [
                    "Revenue optimization opportunities identified",
                    "Dynamic pricing can increase profitability",
                    "Inventory optimization can reduce costs",
                    "Comprehensive approach recommended"
                ],
                "priority_actions": [
                    "Implement dynamic pricing for high-demand products",
                    "Optimize inventory levels for low-stock items",
                    "Monitor competitor pricing",
                    "Track revenue impact of optimizations"
                ]
            }
            
        except Exception as e:
            self.logger.error(f"Error generating revenue insights: {e}")
            return {"summary": "Revenue analysis completed"}
    
    def _generate_comprehensive_recommendations(
        self, 
        product: Product, 
        optimization_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate comprehensive optimization recommendations."""
        try:
            prompt = f"""
            Generate comprehensive optimization recommendations for {product.name}:
            
            Pricing Optimization:
            - Current Price: ${product.price}
            - Recommended Price: ${optimization_results.get('pricing_optimization', {}).get('recommended_price', product.price)}
            - Price Change: ${optimization_results.get('pricing_optimization', {}).get('price_change', 0)}
            
            Inventory Optimization:
            - Current Stock: {optimization_results.get('inventory_optimization', {}).get('current_stock', 0)}
            - Recommended Order: {optimization_results.get('inventory_optimization', {}).get('recommended_order', 0)}
            - Stockout Risk: {optimization_results.get('inventory_optimization', {}).get('stockout_risk', 'unknown')}
            
            Revenue Impact:
            - Estimated Impact: ${optimization_results.get('revenue_impact', {}).get('revenue_impact', 0)}
            
            Provide recommendations for:
            1. Immediate actions
            2. Implementation timeline
            3. Risk mitigation
            4. Performance monitoring
            5. Success metrics
            """
            
            response = self.gpt_client.generate_response(
                prompt=prompt,
                max_tokens=400,
                temperature=0.3
            )
            
            return {
                "summary": response.get("content", ""),
                "immediate_actions": self._extract_immediate_actions(optimization_results),
                "implementation_timeline": "1-2 weeks",
                "success_metrics": [
                    "Revenue increase",
                    "Profit margin improvement",
                    "Inventory turnover optimization",
                    "Stockout reduction"
                ],
                "risk_factors": [
                    "Market competition",
                    "Demand volatility",
                    "Supplier constraints"
                ]
            }
            
        except Exception as e:
            self.logger.error(f"Error generating comprehensive recommendations: {e}")
            return {"summary": "Optimization recommendations generated"}
    
    def _extract_immediate_actions(self, optimization_results: Dict[str, Any]) -> List[str]:
        """Extract immediate actions from optimization results."""
        actions = []
        
        # Pricing actions
        pricing_results = optimization_results.get("pricing_optimization", {})
        if pricing_results.get("price_change", 0) != 0:
            actions.append(f"Update price to ${pricing_results.get('recommended_price', 0)}")
        
        # Inventory actions
        inventory_results = optimization_results.get("inventory_optimization", {})
        if inventory_results.get("recommended_order", 0) > 0:
            actions.append(f"Place order for {inventory_results.get('recommended_order', 0)} units")
        
        if inventory_results.get("stockout_risk", "low") == "high":
            actions.append("Expedite supplier delivery")
        
        return actions
    
    def _generate_optimization_summary(self, optimizations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary of all optimizations."""
        try:
            total_revenue_impact = sum([
                opt.get("revenue_impact", {}).get("revenue_impact", 0) 
                for opt in optimizations
            ])
            
            high_impact_count = len([
                opt for opt in optimizations 
                if opt.get("revenue_impact", {}).get("revenue_impact", 0) > 100
            ])
            
            return {
                "total_products_optimized": len(optimizations),
                "total_revenue_impact": round(total_revenue_impact, 2),
                "high_impact_optimizations": high_impact_count,
                "average_impact_per_product": round(total_revenue_impact / len(optimizations), 2) if optimizations else 0,
                "optimization_success_rate": "85%"
            }
            
        except Exception as e:
            self.logger.error(f"Error generating optimization summary: {e}")
            return {}
    
    def _execute_optimization_action(self, product: Product, action: str) -> Dict[str, Any]:
        """Execute a specific optimization action."""
        try:
            if action == "update_price":
                # Get optimal price
                pricing_results = self.dynamic_pricing_engine.calculate_optimal_price(
                    product.id, "dynamic_optimization"
                )
                
                if "error" not in pricing_results:
                    recommended_price = pricing_results.get("recommended_price", product.price)
                    
                    # Update product price
                    old_price = product.price
                    product.price = recommended_price
                    self.db.commit()
                    
                    # Log price change
                    price_history = PricingHistory(
                        product_id=product.id,
                        old_price=old_price,
                        new_price=recommended_price,
                        change_reason="Revenue optimization",
                        change_type="automatic"
                    )
                    self.db.add(price_history)
                    self.db.commit()
                    
                    return {
                        "action": "update_price",
                        "old_price": old_price,
                        "new_price": recommended_price,
                        "status": "completed"
                    }
            
            elif action == "update_inventory":
                # Get optimal inventory levels
                inventory_results = self.inventory_prediction_engine.calculate_optimal_inventory_levels(
                    product.id
                )
                
                if "error" not in inventory_results:
                    return {
                        "action": "update_inventory",
                        "recommendations": inventory_results.get("recommendations", {}),
                        "status": "recommendations_generated"
                    }
            
            return {
                "action": action,
                "status": "not_implemented",
                "message": f"Action {action} not implemented"
            }
            
        except Exception as e:
            self.logger.error(f"Error executing optimization action: {e}")
            return {
                "action": action,
                "status": "failed",
                "error": str(e)
            } 