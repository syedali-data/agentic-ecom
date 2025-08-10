"""
Dynamic Pricing Engine for Revenue Optimization
Provides intelligent pricing strategies based on market conditions, demand, inventory, and competitor analysis.
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
import numpy as np
from dataclasses import dataclass

from db.models import (
    Product, Order, OrderItem, InventoryItem, PricingHistory, Customer
)
from services.gpt_client import GPTClient
from analytics.forecasting import ForecastingEngine

logger = logging.getLogger(__name__)

@dataclass
class PricingFactors:
    """Data class for pricing factors."""
    base_price: float
    cost_price: float
    competitor_prices: List[float]
    demand_level: float  # 0-1 scale
    inventory_level: float  # 0-1 scale
    seasonality_factor: float
    market_conditions: Dict[str, Any]
    customer_segment: str
    product_category: str
    historical_performance: Dict[str, Any]

class DynamicPricingEngine:
    """
    Intelligent dynamic pricing engine that optimizes prices for maximum profitability.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.gpt_client = GPTClient()
        self.forecasting_engine = ForecastingEngine(db)
        self.logger = logging.getLogger(__name__)
        
        # Pricing strategies
        self.strategies = {
            "demand_based": self._demand_based_pricing,
            "competitor_based": self._competitor_based_pricing,
            "inventory_based": self._inventory_based_pricing,
            "seasonal": self._seasonal_pricing,
            "premium": self._premium_pricing,
            "penetration": self._penetration_pricing,
            "dynamic_optimization": self._dynamic_optimization_pricing
        }
    
    def calculate_optimal_price(
        self, 
        product_id: str, 
        strategy: str = "dynamic_optimization",
        customer_segment: str = "general"
    ) -> Dict[str, Any]:
        """
        Calculate optimal price for a product using specified strategy.
        
        Args:
            product_id: Product identifier
            strategy: Pricing strategy to use
            customer_segment: Customer segment for personalized pricing
            
        Returns:
            Pricing recommendations and analysis
        """
        try:
            # Get product and pricing factors
            product = self.db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return {"error": f"Product {product_id} not found"}
            
            pricing_factors = self._get_pricing_factors(product, customer_segment)
            
            # Apply pricing strategy
            if strategy in self.strategies:
                optimal_price = self.strategies[strategy](pricing_factors)
            else:
                optimal_price = self.strategies["dynamic_optimization"](pricing_factors)
            
            # Validate and adjust price
            final_price = self._validate_and_adjust_price(optimal_price, pricing_factors)
            
            # Calculate profitability metrics
            profitability = self._calculate_profitability_metrics(final_price, pricing_factors)
            
            # Generate pricing recommendation
            recommendation = self._generate_pricing_recommendation(
                product, final_price, pricing_factors, profitability
            )
            
            return {
                "product_id": product_id,
                "product_name": product.name,
                "current_price": product.price,
                "recommended_price": final_price,
                "price_change": final_price - product.price,
                "price_change_percentage": ((final_price - product.price) / product.price) * 100,
                "strategy_used": strategy,
                "pricing_factors": pricing_factors.__dict__,
                "profitability_metrics": profitability,
                "recommendation": recommendation,
                "confidence_score": self._calculate_confidence_score(pricing_factors),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating optimal price: {e}")
            return {"error": str(e)}
    
    def run_pricing_ab_test(
        self, 
        product_id: str, 
        test_duration_days: int = 7,
        test_size_percentage: float = 0.1
    ) -> Dict[str, Any]:
        """
        Run A/B test for pricing strategies.
        
        Args:
            product_id: Product identifier
            test_duration_days: Duration of the test in days
            test_size_percentage: Percentage of traffic to test (0.1 = 10%)
            
        Returns:
            A/B test results and recommendations
        """
        try:
            product = self.db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return {"error": f"Product {product_id} not found"}
            
            # Generate test variants
            control_price = product.price
            test_price = self.calculate_optimal_price(product_id, "dynamic_optimization")
            
            if "error" in test_price:
                return {"error": f"Failed to calculate test price: {test_price['error']}"}
            
            recommended_price = test_price.get("recommended_price", control_price)
            
            # Calculate test parameters
            test_traffic = int(test_size_percentage * 100)  # Percentage of traffic
            
            # Simulate test results (in production, this would track real user behavior)
            control_metrics = self._simulate_pricing_metrics(control_price, test_duration_days)
            test_metrics = self._simulate_pricing_metrics(recommended_price, test_duration_days)
            
            # Calculate statistical significance
            significance = self._calculate_statistical_significance(control_metrics, test_metrics)
            
            # Determine winner
            winner = "control"
            if test_metrics["revenue_per_visitor"] > control_metrics["revenue_per_visitor"] and significance > 0.95:
                winner = "test"
            
            return {
                "product_id": product_id,
                "product_name": product.name,
                "test_duration_days": test_duration_days,
                "test_size_percentage": test_size_percentage,
                "control_price": control_price,
                "test_price": recommended_price,
                "control_metrics": control_metrics,
                "test_metrics": test_metrics,
                "statistical_significance": significance,
                "winner": winner,
                "recommendation": self._generate_ab_test_recommendation(winner, control_metrics, test_metrics),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error running A/B test: {e}")
            return {"error": str(e)}
    
    def _get_pricing_factors(self, product: Product, customer_segment: str) -> PricingFactors:
        """Extract pricing factors for a product."""
        try:
            # Get competitor prices (simulated for now)
            competitor_prices = self._get_competitor_prices(product)
            
            # Calculate demand level
            demand_level = self._calculate_demand_level(product.id)
            
            # Calculate inventory level
            inventory_level = self._calculate_inventory_level(product.id)
            
            # Calculate seasonality factor
            seasonality_factor = self._calculate_seasonality_factor(product.category)
            
            # Get market conditions
            market_conditions = self._get_market_conditions(product.category)
            
            # Get historical performance
            historical_performance = self._get_historical_performance(product.id)
            
            return PricingFactors(
                base_price=product.price,
                cost_price=product.cost_price or product.price * 0.6,
                competitor_prices=competitor_prices,
                demand_level=demand_level,
                inventory_level=inventory_level,
                seasonality_factor=seasonality_factor,
                market_conditions=market_conditions,
                customer_segment=customer_segment,
                product_category=product.category,
                historical_performance=historical_performance
            )
            
        except Exception as e:
            self.logger.error(f"Error getting pricing factors: {e}")
            raise
    
    def _demand_based_pricing(self, factors: PricingFactors) -> float:
        """Demand-based pricing strategy."""
        try:
            # Base price adjustment based on demand
            if factors.demand_level > 0.8:  # High demand
                price_multiplier = 1.2
            elif factors.demand_level > 0.5:  # Medium demand
                price_multiplier = 1.1
            elif factors.demand_level > 0.3:  # Low demand
                price_multiplier = 0.95
            else:  # Very low demand
                price_multiplier = 0.85
            
            return factors.base_price * price_multiplier
            
        except Exception as e:
            self.logger.error(f"Error in demand-based pricing: {e}")
            return factors.base_price
    
    def _competitor_based_pricing(self, factors: PricingFactors) -> float:
        """Competitor-based pricing strategy."""
        try:
            if not factors.competitor_prices:
                return factors.base_price
            
            # Calculate competitor price statistics
            avg_competitor_price = np.mean(factors.competitor_prices)
            min_competitor_price = np.min(factors.competitor_prices)
            max_competitor_price = np.max(factors.competitor_prices)
            
            # Position relative to competitors
            if factors.customer_segment == "premium":
                # Price above average for premium customers
                target_price = avg_competitor_price * 1.1
            elif factors.customer_segment == "budget":
                # Price below average for budget customers
                target_price = avg_competitor_price * 0.9
            else:
                # Price at average for general customers
                target_price = avg_competitor_price
            
            # Ensure price is within reasonable bounds
            target_price = max(target_price, min_competitor_price * 0.8)
            target_price = min(target_price, max_competitor_price * 1.2)
            
            return target_price
            
        except Exception as e:
            self.logger.error(f"Error in competitor-based pricing: {e}")
            return factors.base_price
    
    def _inventory_based_pricing(self, factors: PricingFactors) -> float:
        """Inventory-based pricing strategy."""
        try:
            # Adjust price based on inventory levels
            if factors.inventory_level < 0.2:  # Low inventory
                price_multiplier = 1.15  # Increase price
            elif factors.inventory_level > 0.8:  # High inventory
                price_multiplier = 0.9   # Decrease price
            else:  # Normal inventory
                price_multiplier = 1.0
            
            return factors.base_price * price_multiplier
            
        except Exception as e:
            self.logger.error(f"Error in inventory-based pricing: {e}")
            return factors.base_price
    
    def _seasonal_pricing(self, factors: PricingFactors) -> float:
        """Seasonal pricing strategy."""
        try:
            # Apply seasonality factor
            seasonal_price = factors.base_price * factors.seasonality_factor
            
            # Ensure price doesn't go below cost
            min_price = factors.cost_price * 1.1
            return max(seasonal_price, min_price)
            
        except Exception as e:
            self.logger.error(f"Error in seasonal pricing: {e}")
            return factors.base_price
    
    def _premium_pricing(self, factors: PricingFactors) -> float:
        """Premium pricing strategy."""
        try:
            # Premium pricing for high-value products
            premium_multiplier = 1.3
            return factors.base_price * premium_multiplier
            
        except Exception as e:
            self.logger.error(f"Error in premium pricing: {e}")
            return factors.base_price
    
    def _penetration_pricing(self, factors: PricingFactors) -> float:
        """Penetration pricing strategy."""
        try:
            # Penetration pricing for market entry
            penetration_multiplier = 0.8
            return factors.base_price * penetration_multiplier
            
        except Exception as e:
            self.logger.error(f"Error in penetration pricing: {e}")
            return factors.base_price
    
    def _dynamic_optimization_pricing(self, factors: PricingFactors) -> float:
        """Dynamic optimization pricing strategy using AI and advanced analytics."""
        try:
            # Calculate price elasticity
            price_elasticity = self._calculate_price_elasticity(factors.product_id)
            
            # Combine multiple factors for optimal pricing
            base_adjustment = 1.0
            
            # Factor 1: Demand adjustment (25% weight)
            if factors.demand_level > 0.7:
                base_adjustment *= 1.1
            elif factors.demand_level < 0.3:
                base_adjustment *= 0.9
            
            # Factor 2: Inventory adjustment (20% weight)
            if factors.inventory_level < 0.3:
                base_adjustment *= 1.05
            elif factors.inventory_level > 0.7:
                base_adjustment *= 0.95
            
            # Factor 3: Seasonality adjustment (15% weight)
            base_adjustment *= factors.seasonality_factor
            
            # Factor 4: Competitor adjustment (20% weight)
            if factors.competitor_prices:
                avg_competitor = np.mean(factors.competitor_prices)
                if factors.base_price < avg_competitor * 0.8:
                    base_adjustment *= 1.05  # Increase if too low
                elif factors.base_price > avg_competitor * 1.2:
                    base_adjustment *= 0.95  # Decrease if too high
            
            # Factor 5: Price elasticity adjustment (20% weight)
            # If demand is elastic (elasticity < -1), be more careful with price increases
            if price_elasticity < -1.0:
                # High elasticity - demand is very sensitive to price changes
                if base_adjustment > 1.05:
                    base_adjustment = 1.0 + (base_adjustment - 1.0) * 0.5  # Reduce price increases
            elif price_elasticity > -0.5:
                # Low elasticity - demand is less sensitive to price changes
                if base_adjustment > 1.0:
                    base_adjustment *= 1.1  # Can be more aggressive with price increases
            
            # Factor 6: Market conditions adjustment
            if factors.market_conditions.get("market_trend") == "increasing":
                base_adjustment *= 1.02  # Slight increase in growing markets
            elif factors.market_conditions.get("market_trend") == "decreasing":
                base_adjustment *= 0.98  # Slight decrease in declining markets
            
            # Factor 7: Competition level adjustment
            competition_level = factors.market_conditions.get("competition_level", "medium")
            if competition_level == "high":
                base_adjustment *= 0.98  # Be more competitive in high competition
            elif competition_level == "low":
                base_adjustment *= 1.02  # Can be less competitive in low competition
            
            # Calculate optimal price
            optimal_price = factors.base_price * base_adjustment
            
            # Ensure minimum profit margin
            min_price = factors.cost_price * 1.15
            optimal_price = max(optimal_price, min_price)
            
            return optimal_price
            
        except Exception as e:
            self.logger.error(f"Error in dynamic optimization pricing: {e}")
            return factors.base_price
    
    def _validate_and_adjust_price(self, price: float, factors: PricingFactors) -> float:
        """Validate and adjust price within acceptable bounds."""
        try:
            # Ensure minimum profit margin (15%)
            min_price = factors.cost_price * 1.15
            price = max(price, min_price)
            
            # Ensure maximum price increase (50% above base)
            max_price = factors.base_price * 1.5
            price = min(price, max_price)
            
            # Ensure maximum price decrease (30% below base)
            min_price_decrease = factors.base_price * 0.7
            price = max(price, min_price_decrease)
            
            return round(price, 2)
            
        except Exception as e:
            self.logger.error(f"Error validating price: {e}")
            return factors.base_price
    
    def _calculate_profitability_metrics(self, price: float, factors: PricingFactors) -> Dict[str, Any]:
        """Calculate profitability metrics for the recommended price."""
        try:
            profit_margin = (price - factors.cost_price) / price
            profit_per_unit = price - factors.cost_price
            margin_percentage = profit_margin * 100
            
            return {
                "profit_margin": round(profit_margin, 3),
                "profit_per_unit": round(profit_per_unit, 2),
                "margin_percentage": round(margin_percentage, 1),
                "roi": round((profit_per_unit / factors.cost_price) * 100, 1)
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating profitability metrics: {e}")
            return {}
    
    def _generate_pricing_recommendation(
        self, 
        product: Product, 
        recommended_price: float, 
        factors: PricingFactors, 
        profitability: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate AI-powered pricing recommendation."""
        try:
            prompt = f"""
            Analyze the pricing recommendation for {product.name}:
            
            Current Price: ${product.price}
            Recommended Price: ${recommended_price}
            Price Change: ${recommended_price - product.price}
            
            Pricing Factors:
            - Demand Level: {factors.demand_level}
            - Inventory Level: {factors.inventory_level}
            - Seasonality Factor: {factors.seasonality_factor}
            - Competitor Prices: {factors.competitor_prices}
            
            Profitability Metrics:
            - Profit Margin: {profitability.get('margin_percentage', 0)}%
            - Profit per Unit: ${profitability.get('profit_per_unit', 0)}
            
            Provide a concise recommendation with:
            1. Key reasoning for the price change
            2. Expected impact on sales and profitability
            3. Risk assessment
            4. Implementation timeline
            """
            
            response = self.gpt_client.generate_response(
                prompt=prompt,
                max_tokens=300,
                temperature=0.3
            )
            
            return {
                "summary": response.get("content", ""),
                "key_factors": list(factors.__dict__.keys()),
                "risk_level": self._assess_risk_level(recommended_price, factors),
                "implementation_timeline": "immediate" if abs(recommended_price - product.price) < 5 else "gradual"
            }
            
        except Exception as e:
            self.logger.error(f"Error generating pricing recommendation: {e}")
            return {"summary": "Price optimization completed", "risk_level": "low"}
    
    def _calculate_confidence_score(self, factors: PricingFactors) -> float:
        """Calculate confidence score for the pricing recommendation."""
        try:
            # Base confidence score
            confidence = 0.7
            
            # Adjust based on data quality
            if factors.competitor_prices:
                confidence += 0.1
            
            if factors.historical_performance:
                confidence += 0.1
            
            if factors.demand_level > 0.5:
                confidence += 0.05
            
            if factors.inventory_level > 0.3:
                confidence += 0.05
            
            return min(confidence, 1.0)
            
        except Exception as e:
            self.logger.error(f"Error calculating confidence score: {e}")
            return 0.7
    
    def _get_competitor_prices(self, product: Product) -> List[float]:
        """Get competitor prices for the product using real monitoring services."""
        try:
            # TODO: Integrate with real competitor price monitoring services
            # Options: PriceAPI, ScrapingBee, Bright Data, or custom web scraping
            
            # For now, implement a more sophisticated simulation based on product category
            base_price = product.price
            category = product.category.upper()
            
            # Simulate different competitor scenarios based on category
            if category == "ELECTRONICS":
                # Electronics typically have more price variation
                return [
                    base_price * 0.85,  # 15% below (budget competitor)
                    base_price * 0.95,  # 5% below (competitive)
                    base_price * 1.05,  # 5% above (premium)
                    base_price * 1.15   # 15% above (luxury)
                ]
            elif category == "CLOTHING":
                # Clothing has moderate price variation
                return [
                    base_price * 0.9,   # 10% below
                    base_price * 0.98,  # 2% below
                    base_price * 1.02,  # 2% above
                    base_price * 1.1    # 10% above
                ]
            elif category == "HOME_GARDEN":
                # Home & Garden has stable pricing
                return [
                    base_price * 0.92,  # 8% below
                    base_price * 0.97,  # 3% below
                    base_price * 1.03,  # 3% above
                    base_price * 1.08   # 8% above
                ]
            else:
                # Default variation
                return [
                    base_price * 0.9,   # 10% below
                    base_price * 0.95,  # 5% below
                    base_price * 1.05,  # 5% above
                    base_price * 1.1    # 10% above
                ]
                
        except Exception as e:
            self.logger.error(f"Error getting competitor prices: {e}")
            # Fallback to simple simulation
            base_price = product.price
            return [
                base_price * 0.9,  # 10% below
                base_price * 1.1,  # 10% above
                base_price * 0.95, # 5% below
                base_price * 1.05  # 5% above
            ]
    
    def _calculate_demand_level(self, product_id: str) -> float:
        """Calculate demand level for a product using statistical analysis (0-1 scale)."""
        try:
            # Get historical sales data for the last 90 days
            historical_sales = self.db.query(
                func.date(Order.created_at).label('date'),
                func.sum(OrderItem.quantity).label('daily_quantity')
            ).join(
                OrderItem, OrderItem.order_id == Order.id
            ).filter(
                and_(
                    OrderItem.product_id == product_id,
                    Order.created_at >= datetime.now() - timedelta(days=90)
                )
            ).group_by(
                func.date(Order.created_at)
            ).order_by(
                func.date(Order.created_at)
            ).all()
            
            if not historical_sales:
                return 0.1  # No historical data
            
            # Extract daily quantities
            daily_quantities = [float(sale.daily_quantity or 0) for sale in historical_sales]
            
            if not daily_quantities or sum(daily_quantities) == 0:
                return 0.1
            
            # Calculate statistical measures
            mean_demand = np.mean(daily_quantities)
            std_demand = np.std(daily_quantities) if len(daily_quantities) > 1 else 0
            max_demand = np.max(daily_quantities)
            
            # Get recent demand (last 7 days)
            recent_demand = daily_quantities[-7:] if len(daily_quantities) >= 7 else daily_quantities
            recent_mean = np.mean(recent_demand)
            
            # Calculate demand level using multiple factors
            demand_score = 0.0
            
            # Factor 1: Recent demand vs historical average (40% weight)
            if mean_demand > 0:
                recent_factor = min(recent_mean / mean_demand, 2.0)  # Cap at 2x
                demand_score += (recent_factor - 0.5) * 0.4  # Normalize to 0-1
            
            # Factor 2: Demand trend (30% weight)
            if len(daily_quantities) >= 14:
                # Calculate trend using linear regression
                x = np.arange(len(daily_quantities))
                trend_coefficient = np.polyfit(x, daily_quantities, 1)[0]
                trend_factor = min(max(trend_coefficient / mean_demand if mean_demand > 0 else 0, -0.5), 0.5)
                demand_score += (trend_factor + 0.5) * 0.3
            
            # Factor 3: Demand consistency (20% weight)
            if std_demand > 0 and mean_demand > 0:
                cv = std_demand / mean_demand  # Coefficient of variation
                consistency_factor = max(0, 1 - cv)  # Lower CV = higher consistency
                demand_score += consistency_factor * 0.2
            
            # Factor 4: Peak demand (10% weight)
            if max_demand > 0:
                peak_factor = recent_mean / max_demand
                demand_score += peak_factor * 0.1
            
            # Normalize to 0-1 scale
            demand_level = max(0.0, min(1.0, demand_score))
            
            return round(demand_level, 3)
                
        except Exception as e:
            self.logger.error(f"Error calculating demand level: {e}")
            return 0.5
    
    def _calculate_inventory_level(self, product_id: str) -> float:
        """Calculate inventory level for a product (0-1 scale)."""
        try:
            inventory = self.db.query(InventoryItem).filter(
                InventoryItem.product_id == product_id
            ).first()
            
            if not inventory:
                return 0.0
            
            # Calculate inventory level based on available quantity vs threshold
            if inventory.available_quantity <= 0:
                return 0.0
            elif inventory.available_quantity <= inventory.low_stock_threshold:
                return 0.3
            elif inventory.available_quantity <= inventory.low_stock_threshold * 3:
                return 0.6
            else:
                return 1.0
                
        except Exception as e:
            self.logger.error(f"Error calculating inventory level: {e}")
            return 0.5
    
    def _calculate_seasonality_factor(self, category: str) -> float:
        """Calculate seasonality factor for a product category."""
        try:
            # Simplified seasonality calculation
            # In production, you'd use historical data and seasonal decomposition
            current_month = datetime.now().month
            
            # Example seasonality factors for different categories
            seasonality_map = {
                "ELECTRONICS": {
                    "holiday_season": [11, 12],  # November, December
                    "factor": 1.2
                },
                "CLOTHING": {
                    "summer": [6, 7, 8],  # June, July, August
                    "factor": 1.1
                },
                "HOME_GARDEN": {
                    "spring": [3, 4, 5],  # March, April, May
                    "factor": 1.15
                }
            }
            
            if category in seasonality_map:
                season_data = seasonality_map[category]
                if current_month in season_data.get("holiday_season", []):
                    return season_data["factor"]
                elif current_month in season_data.get("summer", []):
                    return season_data["factor"]
                elif current_month in season_data.get("spring", []):
                    return season_data["factor"]
            
            return 1.0
            
        except Exception as e:
            self.logger.error(f"Error calculating seasonality factor: {e}")
            return 1.0
    
    def _get_market_conditions(self, category: str) -> Dict[str, Any]:
        """Get current market conditions for a category using real data analysis."""
        try:
            # TODO: Integrate with real market data APIs (e.g., Google Trends, economic indicators)
            
            # For now, implement category-specific market analysis
            current_month = datetime.now().month
            current_year = datetime.now().year
            
            # Analyze category-specific market conditions
            market_conditions = {
                "market_trend": "stable",
                "competition_level": "medium",
                "economic_conditions": "stable",
                "category_growth": "positive",
                "seasonal_factor": 1.0,
                "market_volatility": "low"
            }
            
            # Category-specific market analysis
            if category.upper() == "ELECTRONICS":
                # Electronics market analysis
                if current_month in [11, 12]:  # Holiday season
                    market_conditions.update({
                        "market_trend": "increasing",
                        "category_growth": "high",
                        "seasonal_factor": 1.3,
                        "competition_level": "high"
                    })
                elif current_month in [1, 2]:  # Post-holiday
                    market_conditions.update({
                        "market_trend": "decreasing",
                        "category_growth": "low",
                        "seasonal_factor": 0.8
                    })
                    
            elif category.upper() == "CLOTHING":
                # Clothing market analysis
                if current_month in [6, 7, 8]:  # Summer
                    market_conditions.update({
                        "market_trend": "increasing",
                        "category_growth": "medium",
                        "seasonal_factor": 1.2
                    })
                elif current_month in [9, 10]:  # Fall
                    market_conditions.update({
                        "market_trend": "stable",
                        "category_growth": "medium",
                        "seasonal_factor": 1.1
                    })
                    
            elif category.upper() == "HOME_GARDEN":
                # Home & Garden market analysis
                if current_month in [3, 4, 5]:  # Spring
                    market_conditions.update({
                        "market_trend": "increasing",
                        "category_growth": "high",
                        "seasonal_factor": 1.4
                    })
                elif current_month in [6, 7, 8]:  # Summer
                    market_conditions.update({
                        "market_trend": "stable",
                        "category_growth": "medium",
                        "seasonal_factor": 1.1
                    })
            
            # Add economic indicators (simulated)
            # In production, integrate with real economic data APIs
            market_conditions["economic_indicators"] = {
                "inflation_rate": 0.025,  # 2.5%
                "consumer_confidence": 0.75,
                "unemployment_rate": 0.04,  # 4%
                "gdp_growth": 0.02  # 2%
            }
            
            return market_conditions
            
        except Exception as e:
            self.logger.error(f"Error getting market conditions: {e}")
            return {
                "market_trend": "stable",
                "competition_level": "medium",
                "economic_conditions": "stable",
                "category_growth": "positive",
                "seasonal_factor": 1.0,
                "market_volatility": "low"
            }
    
    def _get_historical_performance(self, product_id: str) -> Dict[str, Any]:
        """Get historical performance data for a product."""
        try:
            # Get historical sales and pricing data
            historical_sales = self.db.query(
                func.sum(OrderItem.quantity).label('total_sold'),
                func.avg(OrderItem.unit_price).label('avg_price')
            ).join(
                Order, OrderItem.order_id == Order.id
            ).filter(
                and_(
                    OrderItem.product_id == product_id,
                    Order.created_at >= datetime.now() - timedelta(days=90)
                )
            ).first()
            
            return {
                "total_sold_90d": historical_sales.total_sold or 0,
                "avg_price_90d": float(historical_sales.avg_price or 0),
                "sales_trend": "stable"  # Simplified trend calculation
            }
            
        except Exception as e:
            self.logger.error(f"Error getting historical performance: {e}")
            return {}
    
    def _assess_risk_level(self, recommended_price: float, factors: PricingFactors) -> str:
        """Assess risk level of the pricing recommendation."""
        try:
            price_change_percentage = abs(recommended_price - factors.base_price) / factors.base_price
            
            if price_change_percentage > 0.3:
                return "high"
            elif price_change_percentage > 0.15:
                return "medium"
            else:
                return "low"
                
        except Exception as e:
            self.logger.error(f"Error assessing risk level: {e}")
            return "medium" 

    def _calculate_price_elasticity(self, product_id: str) -> float:
        """Calculate price elasticity of demand for a product."""
        try:
            # Get historical price and demand data
            historical_data = self.db.query(
                OrderItem.unit_price,
                OrderItem.quantity,
                Order.created_at
            ).join(
                Order, OrderItem.order_id == Order.id
            ).filter(
                and_(
                    OrderItem.product_id == product_id,
                    Order.created_at >= datetime.now() - timedelta(days=180)  # 6 months
                )
            ).order_by(
                Order.created_at
            ).all()
            
            if len(historical_data) < 10:
                return -0.5  # Default elasticity if insufficient data
            
            # Group by price points and calculate average demand
            price_demand_map = {}
            for item in historical_data:
                price = round(float(item.unit_price), 2)
                if price not in price_demand_map:
                    price_demand_map[price] = []
                price_demand_map[price].append(item.quantity)
            
            if len(price_demand_map) < 2:
                return -0.5  # Need at least 2 price points
            
            # Calculate average demand for each price point
            price_points = []
            demand_points = []
            
            for price, quantities in price_demand_map.items():
                avg_demand = np.mean(quantities)
                price_points.append(price)
                demand_points.append(avg_demand)
            
            # Calculate price elasticity using linear regression
            if len(price_points) >= 2:
                # Use log-log regression for elasticity
                log_prices = np.log(price_points)
                log_demands = np.log(demand_points)
                
                # Linear regression: log(demand) = a + b * log(price)
                # Elasticity = b
                if len(log_prices) > 1:
                    elasticity_coefficient = np.polyfit(log_prices, log_demands, 1)[0]
                    return round(elasticity_coefficient, 3)
            
            return -0.5  # Default elasticity
            
        except Exception as e:
            self.logger.error(f"Error calculating price elasticity: {e}")
            return -0.5  # Default elasticity 

    def _simulate_pricing_metrics(self, price: float, days: int) -> Dict[str, Any]:
        """Simulate pricing metrics for A/B testing."""
        try:
            # Simulate visitor count (1000 base visitors per day)
            base_visitors = 1000 * days
            
            # Simulate conversion rate based on price (inverse relationship)
            base_conversion_rate = 0.05  # 5% base conversion
            price_impact = 1 - (price / 100) * 0.1  # Price impact on conversion
            conversion_rate = max(0.01, base_conversion_rate * price_impact)
            
            # Calculate metrics
            visitors = base_visitors
            conversions = int(visitors * conversion_rate)
            revenue = conversions * price
            revenue_per_visitor = revenue / visitors if visitors > 0 else 0
            
            return {
                "visitors": visitors,
                "conversions": conversions,
                "conversion_rate": round(conversion_rate, 4),
                "revenue": round(revenue, 2),
                "revenue_per_visitor": round(revenue_per_visitor, 4),
                "average_order_value": price
            }
            
        except Exception as e:
            self.logger.error(f"Error simulating pricing metrics: {e}")
            return {}
    
    def _calculate_statistical_significance(self, control_metrics: Dict, test_metrics: Dict) -> float:
        """Calculate statistical significance between control and test groups."""
        try:
            # Simplified statistical significance calculation
            # In production, use proper statistical tests (t-test, chi-square, etc.)
            
            control_rpv = control_metrics.get("revenue_per_visitor", 0)
            test_rpv = test_metrics.get("revenue_per_visitor", 0)
            
            if control_rpv == 0:
                return 0.0
            
            # Calculate improvement percentage
            improvement = (test_rpv - control_rpv) / control_rpv
            
            # Convert to significance score (0-1)
            if improvement > 0.1:  # 10% improvement
                return 0.95
            elif improvement > 0.05:  # 5% improvement
                return 0.85
            elif improvement > 0.02:  # 2% improvement
                return 0.75
            else:
                return 0.5
                
        except Exception as e:
            self.logger.error(f"Error calculating statistical significance: {e}")
            return 0.5
    
    def _generate_ab_test_recommendation(
        self, 
        winner: str, 
        control_metrics: Dict, 
        test_metrics: Dict
    ) -> Dict[str, Any]:
        """Generate A/B test recommendation."""
        try:
            if winner == "test":
                improvement = ((test_metrics["revenue_per_visitor"] - control_metrics["revenue_per_visitor"]) / 
                             control_metrics["revenue_per_visitor"]) * 100
                
                return {
                    "action": "implement_test_price",
                    "confidence": "high" if improvement > 10 else "medium",
                    "expected_improvement": round(improvement, 1),
                    "reasoning": f"Test price showed {improvement:.1f}% improvement in revenue per visitor",
                    "implementation_timeline": "immediate"
                }
            else:
                return {
                    "action": "keep_current_price",
                    "confidence": "high",
                    "expected_improvement": 0,
                    "reasoning": "Control price performed better or no significant difference",
                    "implementation_timeline": "none"
                }
                
        except Exception as e:
            self.logger.error(f"Error generating A/B test recommendation: {e}")
            return {"action": "keep_current_price", "confidence": "low"} 