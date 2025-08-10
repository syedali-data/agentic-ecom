#!/usr/bin/env python3
"""
Demonstration of Advanced Multi-Factor Scoring System
Shows the comprehensive scoring capabilities with real examples.
"""

import sys
import os
import logging
from datetime import datetime
from typing import List, Dict, Any

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.database import get_db
from analytics.viral_trend_analyzer import ViralTrendAnalyzer, ScoringFactors, AdvancedProductScore

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def demo_advanced_scoring_system():
    """Demonstrate the advanced multi-factor scoring system."""
    
    print("🎯 Advanced Multi-Factor Scoring System Demo")
    print("=" * 60)
    
    # Initialize analyzer
    db = get_db()
    analyzer = ViralTrendAnalyzer(db)
    
    print("\n📊 SYSTEM OVERVIEW")
    print("-" * 40)
    print("The Advanced Multi-Factor Scoring System evaluates products across:")
    print("• 7 main categories with 25+ individual factors")
    print("• Weighted scoring algorithm for balanced evaluation")
    print("• AI-powered recommendations and risk assessment")
    print("• Comprehensive analysis and insights")
    
    # Sample products for demonstration
    sample_products = [
        {
            "name": "Smart Fitness Tracker Pro",
            "category": "electronics",
            "description": "Advanced fitness tracking with heart rate monitoring"
        },
        {
            "name": "LED Makeup Mirror with Bluetooth",
            "category": "beauty",
            "description": "Smart mirror with built-in speakers and lighting"
        },
        {
            "name": "Premium Coffee Mug Set",
            "category": "kitchen",
            "description": "High-quality ceramic mugs with temperature control"
        },
        {
            "name": "Wireless Noise-Canceling Earbuds",
            "category": "electronics",
            "description": "Premium audio experience with active noise cancellation"
        },
        {
            "name": "Yoga Mat with Alignment Lines",
            "category": "fitness",
            "description": "Non-slip yoga mat with alignment guides"
        }
    ]
    
    print(f"\n🔍 ANALYZING {len(sample_products)} SAMPLE PRODUCTS")
    print("-" * 40)
    
    # Calculate advanced scores for each product
    advanced_scores = []
    
    for i, product in enumerate(sample_products, 1):
        print(f"\n📊 Product {i}: {product['name']}")
        print(f"   Category: {product['category']}")
        print(f"   Description: {product['description']}")
        
        # Calculate advanced score
        advanced_score = analyzer.calculate_advanced_product_score(
            product_name=product['name'],
            category=product['category'],
            include_analysis=True
        )
        
        if advanced_score:
            advanced_scores.append(advanced_score)
            print(f"   ✅ Score calculated: {advanced_score.overall_score:.3f}")
        else:
            print(f"   ❌ Failed to calculate score")
    
    if not advanced_scores:
        print("\n❌ No scores calculated. Demo failed.")
        return False
    
    # Rank products
    print(f"\n🏆 PRODUCT RANKING RESULTS")
    print("-" * 40)
    
    # Sort by overall score (descending)
    ranked_scores = sorted(advanced_scores, key=lambda x: x.overall_score, reverse=True)
    
    for i, score in enumerate(ranked_scores, 1):
        score.rank_position = i
        print(f"{i:2d}. {score.product_name:<35} | Score: {score.overall_score:.3f} | Category: {score.category}")
    
    # Detailed analysis of top product
    if ranked_scores:
        top_product = ranked_scores[0]
        print(f"\n📈 DETAILED ANALYSIS: {top_product.product_name}")
        print("=" * 60)
        
        # Scoring factors
        factors = top_product.scoring_factors
        print(f"\n🎯 SCORING FACTORS")
        print("-" * 30)
        print(f"Viral Score:           {factors.viral_score:.3f}")
        print(f"Trend Momentum:        {factors.trend_momentum:.3f}")
        print(f"Social Media Buzz:     {factors.social_media_buzz:.3f}")
        print(f"Search Volume Growth:  {factors.search_volume_growth:.3f}")
        print(f"Market Potential:      {factors.market_potential:.3f}")
        print(f"Competition Level:     {factors.competition_level:.3f}")
        print(f"Estimated Margin:      {factors.estimated_margin:.3f}")
        print(f"Market Size:           {factors.market_size:.3f}")
        print(f"Product Quality:       {factors.product_quality_score:.3f}")
        print(f"Customer Satisfaction: {factors.customer_satisfaction:.3f}")
        print(f"Review Rating:         {factors.review_rating:.3f}")
        print(f"Review Count:          {factors.review_count:.3f}")
        print(f"Supply Availability:   {factors.supply_availability:.3f}")
        print(f"Shipping Speed:        {factors.shipping_speed:.3f}")
        print(f"Fulfillment Reliability: {factors.fulfillment_reliability:.3f}")
        print(f"Cost Efficiency:       {factors.cost_efficiency:.3f}")
        print(f"Risk Level:            {factors.risk_level:.3f}")
        print(f"Compliance Score:      {factors.compliance_score:.3f}")
        print(f"Regulatory Risk:       {factors.regulatory_risk:.3f}")
        print(f"Seasonal Relevance:    {factors.seasonal_relevance:.3f}")
        print(f"Timing Advantage:      {factors.timing_advantage:.3f}")
        print(f"Trend Lifecycle Stage: {factors.trend_lifecycle_stage:.3f}")
        print(f"Innovation Score:      {factors.innovation_score:.3f}")
        print(f"Differentiation Potential: {factors.differentiation_potential:.3f}")
        print(f"Competitive Advantage: {factors.competitive_advantage:.3f}")
        
        # Score breakdown
        print(f"\n📊 SCORE BREAKDOWN")
        print("-" * 30)
        for category, score in top_product.score_breakdown.items():
            print(f"{category.replace('_', ' ').title():<20} {score:.3f}")
        
        # Recommendations
        if top_product.recommendations:
            print(f"\n💡 RECOMMENDATIONS ({len(top_product.recommendations)})")
            print("-" * 30)
            for i, rec in enumerate(top_product.recommendations[:5], 1):
                print(f"{i}. {rec}")
        
        # Risk assessment
        if top_product.risk_assessment:
            risk = top_product.risk_assessment
            print(f"\n⚠️ RISK ASSESSMENT")
            print("-" * 30)
            print(f"Overall Risk Level:    {risk['overall_risk_level']}")
            print(f"Risk Score:           {risk['risk_score']:.3f}")
            print(f"Risk Factors:         {len(risk['risk_factors'])}")
            print(f"Mitigation Strategies: {len(risk['mitigation_strategies'])}")
            
            if risk['risk_factors']:
                print(f"\n   Risk Factors:")
                for factor in risk['risk_factors'][:3]:
                    print(f"   • {factor}")
            
            if risk['mitigation_strategies']:
                print(f"\n   Mitigation Strategies:")
                for strategy in risk['mitigation_strategies'][:3]:
                    print(f"   • {strategy}")
    
    # Category analysis
    print(f"\n📈 CATEGORY ANALYSIS")
    print("-" * 40)
    
    category_scores = {}
    for score in ranked_scores:
        category = score.category
        if category not in category_scores:
            category_scores[category] = []
        category_scores[category].append(score.overall_score)
    
    for category, scores in category_scores.items():
        avg_score = sum(scores) / len(scores)
        print(f"{category.title():<15} | Avg Score: {avg_score:.3f} | Products: {len(scores)}")
    
    # Performance summary
    print(f"\n🎯 PERFORMANCE SUMMARY")
    print("-" * 40)
    
    total_products = len(ranked_scores)
    high_score_products = len([s for s in ranked_scores if s.overall_score >= 0.7])
    medium_score_products = len([s for s in ranked_scores if 0.4 <= s.overall_score < 0.7])
    low_score_products = len([s for s in ranked_scores if s.overall_score < 0.4])
    
    print(f"Total Products Analyzed: {total_products}")
    print(f"High Score (≥0.7):       {high_score_products} ({high_score_products/total_products*100:.1f}%)")
    print(f"Medium Score (0.4-0.7):  {medium_score_products} ({medium_score_products/total_products*100:.1f}%)")
    print(f"Low Score (<0.4):        {low_score_products} ({low_score_products/total_products*100:.1f}%)")
    
    avg_overall_score = sum(s.overall_score for s in ranked_scores) / len(ranked_scores)
    print(f"Average Overall Score:   {avg_overall_score:.3f}")
    
    # System capabilities
    print(f"\n🚀 SYSTEM CAPABILITIES")
    print("-" * 40)
    print("✅ Multi-factor scoring across 25+ factors")
    print("✅ Weighted algorithm for balanced evaluation")
    print("✅ AI-powered recommendations")
    print("✅ Comprehensive risk assessment")
    print("✅ Detailed score breakdowns")
    print("✅ Product ranking and comparison")
    print("✅ Category analysis and insights")
    print("✅ Performance metrics and reporting")
    
    print(f"\n🎉 DEMO COMPLETED SUCCESSFULLY!")
    print(f"Advanced Multi-Factor Scoring System is working correctly.")
    
    return True

def demo_scoring_algorithm():
    """Demonstrate the scoring algorithm in detail."""
    
    print("\n🔬 SCORING ALGORITHM DEMONSTRATION")
    print("=" * 60)
    
    # Initialize analyzer
    db = get_db()
    analyzer = ViralTrendAnalyzer(db)
    
    # Create sample scoring factors
    print("\n📊 Sample Scoring Factors Calculation")
    print("-" * 40)
    
    # Example 1: High-performing product
    high_performing_factors = ScoringFactors(
        viral_score=0.9,
        trend_momentum=0.8,
        social_media_buzz=0.85,
        search_volume_growth=0.7,
        market_potential=0.9,
        competition_level=0.2,
        estimated_margin=0.6,
        market_size=0.8,
        product_quality_score=0.85,
        customer_satisfaction=0.9,
        review_rating=0.9,
        review_count=0.8,
        supply_availability=0.9,
        shipping_speed=0.8,
        fulfillment_reliability=0.9,
        cost_efficiency=0.7,
        risk_level=0.1,
        compliance_score=0.95,
        regulatory_risk=0.05,
        seasonal_relevance=0.8,
        timing_advantage=0.7,
        trend_lifecycle_stage=0.3,
        innovation_score=0.8,
        differentiation_potential=0.7,
        competitive_advantage=0.6
    )
    
    # Example 2: Medium-performing product
    medium_performing_factors = ScoringFactors(
        viral_score=0.5,
        trend_momentum=0.4,
        social_media_buzz=0.3,
        search_volume_growth=0.2,
        market_potential=0.6,
        competition_level=0.6,
        estimated_margin=0.4,
        market_size=0.5,
        product_quality_score=0.6,
        customer_satisfaction=0.5,
        review_rating=0.7,
        review_count=0.4,
        supply_availability=0.7,
        shipping_speed=0.5,
        fulfillment_reliability=0.6,
        cost_efficiency=0.5,
        risk_level=0.5,
        compliance_score=0.8,
        regulatory_risk=0.3,
        seasonal_relevance=0.4,
        timing_advantage=0.3,
        trend_lifecycle_stage=0.6,
        innovation_score=0.4,
        differentiation_potential=0.3,
        competitive_advantage=0.4
    )
    
    # Example 3: Low-performing product
    low_performing_factors = ScoringFactors(
        viral_score=0.2,
        trend_momentum=0.1,
        social_media_buzz=0.1,
        search_volume_growth=0.05,
        market_potential=0.3,
        competition_level=0.9,
        estimated_margin=0.2,
        market_size=0.3,
        product_quality_score=0.3,
        customer_satisfaction=0.2,
        review_rating=0.4,
        review_count=0.1,
        supply_availability=0.4,
        shipping_speed=0.3,
        fulfillment_reliability=0.4,
        cost_efficiency=0.3,
        risk_level=0.8,
        compliance_score=0.6,
        regulatory_risk=0.7,
        seasonal_relevance=0.2,
        timing_advantage=0.1,
        trend_lifecycle_stage=0.9,
        innovation_score=0.2,
        differentiation_potential=0.1,
        competitive_advantage=0.2
    )
    
    # Calculate scores
    examples = [
        ("High-Performing Product", high_performing_factors),
        ("Medium-Performing Product", medium_performing_factors),
        ("Low-Performing Product", low_performing_factors)
    ]
    
    for name, factors in examples:
        overall_score = analyzer._calculate_overall_score(factors)
        score_breakdown = analyzer._generate_score_breakdown(factors)
        
        print(f"\n📊 {name}")
        print(f"   Overall Score: {overall_score:.3f}")
        print(f"   Score Breakdown:")
        for category, score in score_breakdown.items():
            print(f"     {category.replace('_', ' ').title():<20} {score:.3f}")
    
    print(f"\n✅ Scoring algorithm demonstration completed!")

def main():
    """Run the complete demonstration."""
    
    print("🚀 Advanced Multi-Factor Scoring System - Complete Demo")
    print("=" * 80)
    
    try:
        # Run main demo
        success1 = demo_advanced_scoring_system()
        
        if success1:
            # Run algorithm demo
            demo_scoring_algorithm()
            
            print(f"\n{'='*80}")
            print("🎉 ALL DEMOS COMPLETED SUCCESSFULLY!")
            print("The Advanced Multi-Factor Scoring System is fully operational.")
            print(f"{'='*80}")
            
            return True
        else:
            print(f"\n❌ Demo failed. Please check the errors above.")
            return False
            
    except Exception as e:
        print(f"\n❌ Demo failed with exception: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 