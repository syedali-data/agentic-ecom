#!/usr/bin/env python3
"""
Test Advanced Multi-Factor Scoring System
Tests the new advanced multi-factor scoring capabilities for product ranking.
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

def test_advanced_scoring_factors():
    """Test the ScoringFactors dataclass."""
    print("\n🧪 Testing ScoringFactors Dataclass")
    print("-" * 40)
    
    try:
        # Create a scoring factors instance
        factors = ScoringFactors(
            viral_score=0.8,
            trend_momentum=0.7,
            social_media_buzz=0.6,
            search_volume_growth=0.5,
            market_potential=0.75,
            competition_level=0.3,
            estimated_margin=0.4,
            market_size=0.8,
            product_quality_score=0.7,
            customer_satisfaction=0.8,
            review_rating=0.85,
            review_count=0.6,
            supply_availability=0.9,
            shipping_speed=0.7,
            fulfillment_reliability=0.8,
            cost_efficiency=0.6,
            risk_level=0.2,
            compliance_score=0.9,
            regulatory_risk=0.1,
            seasonal_relevance=0.6,
            timing_advantage=0.5,
            trend_lifecycle_stage=0.3,
            innovation_score=0.7,
            differentiation_potential=0.6,
            competitive_advantage=0.5
        )
        
        # Test that all fields are properly set
        assert factors.viral_score == 0.8, f"Expected viral_score 0.8, got {factors.viral_score}"
        assert factors.trend_momentum == 0.7, f"Expected trend_momentum 0.7, got {factors.trend_momentum}"
        assert factors.market_potential == 0.75, f"Expected market_potential 0.75, got {factors.market_potential}"
        
        print("✅ ScoringFactors dataclass test passed")
        return True
        
    except Exception as e:
        print(f"❌ ScoringFactors dataclass test failed: {e}")
        return False

def test_advanced_product_score():
    """Test the AdvancedProductScore dataclass."""
    print("\n🧪 Testing AdvancedProductScore Dataclass")
    print("-" * 40)
    
    try:
        # Create scoring factors
        factors = ScoringFactors(
            viral_score=0.8,
            trend_momentum=0.7,
            market_potential=0.75,
            competition_level=0.3
        )
        
        # Create an advanced product score
        score = AdvancedProductScore(
            product_name="Test Product",
            category="electronics",
            overall_score=0.75,
            scoring_factors=factors,
            rank_position=1
        )
        
        # Test that all fields are properly set
        assert score.product_name == "Test Product", f"Expected product_name 'Test Product', got {score.product_name}"
        assert score.category == "electronics", f"Expected category 'electronics', got {score.category}"
        assert score.overall_score == 0.75, f"Expected overall_score 0.75, got {score.overall_score}"
        assert score.rank_position == 1, f"Expected rank_position 1, got {score.rank_position}"
        assert score.timestamp is not None, "Expected timestamp to be set"
        assert score.score_breakdown is not None, "Expected score_breakdown to be initialized"
        assert score.recommendations is not None, "Expected recommendations to be initialized"
        assert score.risk_assessment is not None, "Expected risk_assessment to be initialized"
        
        print("✅ AdvancedProductScore dataclass test passed")
        return True
        
    except Exception as e:
        print(f"❌ AdvancedProductScore dataclass test failed: {e}")
        return False

def test_calculate_advanced_product_score():
    """Test the calculate_advanced_product_score method."""
    print("\n🧪 Testing calculate_advanced_product_score Method")
    print("-" * 40)
    
    try:
        # Initialize analyzer
        db = get_db()
        analyzer = ViralTrendAnalyzer(db)
        
        # Test with a sample product
        product_name = "Smart Fitness Tracker"
        category = "electronics"
        
        advanced_score = analyzer.calculate_advanced_product_score(
            product_name=product_name,
            category=category,
            include_analysis=True
        )
        
        # Verify the result
        assert advanced_score is not None, "Expected advanced_score to be returned"
        assert advanced_score.product_name == product_name, f"Expected product_name '{product_name}', got '{advanced_score.product_name}'"
        assert advanced_score.category == category, f"Expected category '{category}', got '{advanced_score.category}'"
        assert 0.0 <= advanced_score.overall_score <= 1.0, f"Expected overall_score between 0 and 1, got {advanced_score.overall_score}"
        assert advanced_score.scoring_factors is not None, "Expected scoring_factors to be set"
        assert advanced_score.score_breakdown is not None, "Expected score_breakdown to be set"
        assert advanced_score.recommendations is not None, "Expected recommendations to be set"
        assert advanced_score.risk_assessment is not None, "Expected risk_assessment to be set"
        
        # Print detailed results
        print(f"📊 Product: {advanced_score.product_name}")
        print(f"📊 Category: {advanced_score.category}")
        print(f"📊 Overall Score: {advanced_score.overall_score:.3f}")
        print(f"📊 Rank Position: {advanced_score.rank_position}")
        
        # Print score breakdown
        if advanced_score.score_breakdown:
            print("\n📈 Score Breakdown:")
            for factor, score in advanced_score.score_breakdown.items():
                print(f"   {factor}: {score:.3f}")
        
        # Print recommendations
        if advanced_score.recommendations:
            print(f"\n💡 Recommendations ({len(advanced_score.recommendations)}):")
            for i, rec in enumerate(advanced_score.recommendations[:3], 1):
                print(f"   {i}. {rec}")
        
        # Print risk assessment
        if advanced_score.risk_assessment:
            print(f"\n⚠️ Risk Assessment:")
            print(f"   Overall Risk: {advanced_score.risk_assessment.get('overall_risk_level', 'unknown')}")
            print(f"   Risk Score: {advanced_score.risk_assessment.get('risk_score', 0):.3f}")
        
        print("✅ calculate_advanced_product_score test passed")
        return True
        
    except Exception as e:
        print(f"❌ calculate_advanced_product_score test failed: {e}")
        return False

def test_rank_products_with_advanced_scoring():
    """Test the rank_products_with_advanced_scoring method."""
    print("\n🧪 Testing rank_products_with_advanced_scoring Method")
    print("-" * 40)
    
    try:
        # Initialize analyzer
        db = get_db()
        analyzer = ViralTrendAnalyzer(db)
        
        # Create sample products
        sample_products = [
            {"name": "Smart Fitness Tracker", "category": "electronics"},
            {"name": "LED Makeup Mirror", "category": "beauty"},
            {"name": "Basic Coffee Mug", "category": "kitchen"},
            {"name": "Wireless Earbuds", "category": "electronics"},
            {"name": "Yoga Mat", "category": "fitness"}
        ]
        
        # Rank products with advanced scoring
        ranked_scores = analyzer.rank_products_with_advanced_scoring(
            products=sample_products,
            max_products=3,
            min_score=0.3
        )
        
        # Verify the results
        assert len(ranked_scores) > 0, "Expected ranked_scores to be returned"
        assert len(ranked_scores) <= 3, f"Expected max 3 products, got {len(ranked_scores)}"
        
        # Check that products are ranked by overall score (descending)
        for i in range(len(ranked_scores) - 1):
            assert ranked_scores[i].overall_score >= ranked_scores[i + 1].overall_score, \
                f"Products not properly ranked: {ranked_scores[i].overall_score} < {ranked_scores[i + 1].overall_score}"
        
        # Print ranking results
        print(f"🏆 Top {len(ranked_scores)} Ranked Products:")
        for i, score in enumerate(ranked_scores, 1):
            print(f"   {i}. {score.product_name} ({score.category}) - Score: {score.overall_score:.3f}")
        
        # Verify rank positions are assigned correctly
        for i, score in enumerate(ranked_scores):
            assert score.rank_position == i + 1, f"Expected rank_position {i + 1}, got {score.rank_position}"
        
        print("✅ rank_products_with_advanced_scoring test passed")
        return True
        
    except Exception as e:
        print(f"❌ rank_products_with_advanced_scoring test failed: {e}")
        return False

def test_scoring_factors_calculation():
    """Test the calculation of individual scoring factors."""
    print("\n🧪 Testing Scoring Factors Calculation")
    print("-" * 40)
    
    try:
        # Initialize analyzer
        db = get_db()
        analyzer = ViralTrendAnalyzer(db)
        
        # Test individual scoring factor methods
        product_name = "Test Product"
        category = "electronics"
        
        # Test viral and trend factors
        trend_momentum = analyzer._calculate_trend_momentum(product_name, category)
        social_buzz = analyzer._calculate_social_media_buzz(product_name, category)
        search_growth = analyzer._calculate_search_volume_growth(product_name, category)
        
        # Test market and business factors
        market_size = analyzer._analyze_market_size(product_name, category)
        competition_level = analyzer._assess_competition_level_numeric(product_name, category)
        
        # Test product quality factors
        product_quality = analyzer._assess_product_quality(product_name, category)
        customer_satisfaction = analyzer._assess_customer_satisfaction(product_name, category)
        review_rating = analyzer._get_review_rating(product_name, category)
        review_count = analyzer._get_review_count(product_name, category)
        
        # Test operational factors
        supply_availability = analyzer._assess_supply_availability(product_name, category)
        shipping_speed = analyzer._assess_shipping_speed(product_name, category)
        fulfillment_reliability = analyzer._assess_fulfillment_reliability(product_name, category)
        cost_efficiency = analyzer._assess_cost_efficiency(product_name, category)
        
        # Test risk and compliance factors
        compliance_score = analyzer._assess_compliance_score(product_name, category)
        regulatory_risk = analyzer._assess_regulatory_risk(product_name, category)
        
        # Test seasonal and timing factors
        seasonal_relevance = analyzer._assess_seasonal_relevance(product_name, category)
        timing_advantage = analyzer._assess_timing_advantage(product_name, category)
        trend_lifecycle = analyzer._assess_trend_lifecycle_stage(product_name, category)
        
        # Test innovation factors
        innovation_score = analyzer._assess_innovation_score(product_name, category)
        differentiation_potential = analyzer._assess_differentiation_potential(product_name, category)
        competitive_advantage = analyzer._assess_competitive_advantage(product_name, category)
        
        # Verify all scores are within expected ranges
        factors_to_check = [
            ("trend_momentum", trend_momentum, 0.0, 1.0),
            ("social_buzz", social_buzz, 0.0, 1.0),
            ("search_growth", search_growth, 0.0, 1.0),
            ("market_size", market_size, 0.0, 1.0),
            ("competition_level", competition_level, 0.0, 1.0),
            ("product_quality", product_quality, 0.0, 1.0),
            ("customer_satisfaction", customer_satisfaction, 0.0, 1.0),
            ("review_rating", review_rating, 0.0, 1.0),
            ("review_count", review_count, 0.0, 1.0),
            ("supply_availability", supply_availability, 0.0, 1.0),
            ("shipping_speed", shipping_speed, 0.0, 1.0),
            ("fulfillment_reliability", fulfillment_reliability, 0.0, 1.0),
            ("cost_efficiency", cost_efficiency, 0.0, 1.0),
            ("compliance_score", compliance_score, 0.0, 1.0),
            ("regulatory_risk", regulatory_risk, 0.0, 1.0),
            ("seasonal_relevance", seasonal_relevance, 0.0, 1.0),
            ("timing_advantage", timing_advantage, 0.0, 1.0),
            ("trend_lifecycle", trend_lifecycle, 0.0, 1.0),
            ("innovation_score", innovation_score, 0.0, 1.0),
            ("differentiation_potential", differentiation_potential, 0.0, 1.0),
            ("competitive_advantage", competitive_advantage, 0.0, 1.0)
        ]
        
        for factor_name, score, min_val, max_val in factors_to_check:
            assert min_val <= score <= max_val, f"{factor_name}: Expected {min_val}-{max_val}, got {score}"
        
        print("✅ All scoring factors calculated successfully")
        print(f"📊 Sample factors: trend_momentum={trend_momentum:.3f}, social_buzz={social_buzz:.3f}, market_size={market_size:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Scoring factors calculation test failed: {e}")
        return False

def test_overall_score_calculation():
    """Test the overall score calculation."""
    print("\n🧪 Testing Overall Score Calculation")
    print("-" * 40)
    
    try:
        # Initialize analyzer
        db = get_db()
        analyzer = ViralTrendAnalyzer(db)
        
        # Create sample scoring factors
        scoring_factors = ScoringFactors(
            viral_score=0.8,
            trend_momentum=0.7,
            social_media_buzz=0.6,
            search_volume_growth=0.5,
            market_potential=0.75,
            competition_level=0.3,
            estimated_margin=0.4,
            market_size=0.8,
            product_quality_score=0.7,
            customer_satisfaction=0.8,
            review_rating=0.85,
            review_count=0.6,
            supply_availability=0.9,
            shipping_speed=0.7,
            fulfillment_reliability=0.8,
            cost_efficiency=0.6,
            risk_level=0.2,
            compliance_score=0.9,
            regulatory_risk=0.1,
            seasonal_relevance=0.6,
            timing_advantage=0.5,
            trend_lifecycle_stage=0.3,
            innovation_score=0.7,
            differentiation_potential=0.6,
            competitive_advantage=0.5
        )
        
        # Calculate overall score
        overall_score = analyzer._calculate_overall_score(scoring_factors)
        
        # Verify the result
        assert 0.0 <= overall_score <= 1.0, f"Expected overall_score between 0 and 1, got {overall_score}"
        
        # Generate score breakdown
        score_breakdown = analyzer._generate_score_breakdown(scoring_factors)
        
        # Verify score breakdown
        expected_categories = ["viral_trend", "market_business", "product_quality", "operational", "risk_compliance", "seasonal_timing", "innovation"]
        for category in expected_categories:
            assert category in score_breakdown, f"Expected {category} in score_breakdown"
            assert 0.0 <= score_breakdown[category] <= 1.0, f"Expected {category} score between 0 and 1, got {score_breakdown[category]}"
        
        print(f"✅ Overall score calculated: {overall_score:.3f}")
        print("📊 Score breakdown:")
        for category, score in score_breakdown.items():
            print(f"   {category}: {score:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Overall score calculation test failed: {e}")
        return False

def test_recommendations_and_risk_assessment():
    """Test the generation of recommendations and risk assessment."""
    print("\n🧪 Testing Recommendations and Risk Assessment")
    print("-" * 40)
    
    try:
        # Initialize analyzer
        db = get_db()
        analyzer = ViralTrendAnalyzer(db)
        
        # Create sample scoring factors with various scenarios
        scoring_factors = ScoringFactors(
            viral_score=0.3,  # Low viral score
            trend_momentum=0.2,  # Low trend momentum
            market_potential=0.8,  # High market potential
            competition_level=0.8,  # High competition
            estimated_margin=0.2,  # Low margin
            product_quality_score=0.4,  # Low quality
            customer_satisfaction=0.3,  # Low satisfaction
            supply_availability=0.3,  # Low availability
            shipping_speed=0.4,  # Low shipping speed
            risk_level=0.7,  # High risk
            compliance_score=0.6,  # Low compliance
            regulatory_risk=0.7,  # High regulatory risk
            seasonal_relevance=0.2,  # Low seasonal relevance
            trend_lifecycle_stage=0.9,  # Mature trend
            innovation_score=0.3,  # Low innovation
            differentiation_potential=0.2  # Low differentiation
        )
        
        # Generate recommendations
        recommendations = analyzer._generate_advanced_recommendations(scoring_factors)
        
        # Generate risk assessment
        risk_assessment = analyzer._generate_risk_assessment(scoring_factors)
        
        # Verify recommendations
        assert len(recommendations) > 0, "Expected recommendations to be generated"
        print(f"💡 Generated {len(recommendations)} recommendations:")
        for i, rec in enumerate(recommendations[:5], 1):
            print(f"   {i}. {rec}")
        
        # Verify risk assessment
        assert risk_assessment is not None, "Expected risk_assessment to be generated"
        assert "overall_risk_level" in risk_assessment, "Expected overall_risk_level in risk_assessment"
        assert "risk_factors" in risk_assessment, "Expected risk_factors in risk_assessment"
        assert "mitigation_strategies" in risk_assessment, "Expected mitigation_strategies in risk_assessment"
        
        print(f"⚠️ Risk Assessment:")
        print(f"   Overall Risk Level: {risk_assessment['overall_risk_level']}")
        print(f"   Risk Score: {risk_assessment['risk_score']:.3f}")
        print(f"   Risk Factors: {len(risk_assessment['risk_factors'])}")
        print(f"   Mitigation Strategies: {len(risk_assessment['mitigation_strategies'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Recommendations and risk assessment test failed: {e}")
        return False

def main():
    """Run all tests for the advanced multi-factor scoring system."""
    print("🚀 Advanced Multi-Factor Scoring System Tests")
    print("=" * 60)
    
    test_results = []
    
    # Run all tests
    tests = [
        ("ScoringFactors Dataclass", test_advanced_scoring_factors),
        ("AdvancedProductScore Dataclass", test_advanced_product_score),
        ("calculate_advanced_product_score Method", test_calculate_advanced_product_score),
        ("rank_products_with_advanced_scoring Method", test_rank_products_with_advanced_scoring),
        ("Scoring Factors Calculation", test_scoring_factors_calculation),
        ("Overall Score Calculation", test_overall_score_calculation),
        ("Recommendations and Risk Assessment", test_recommendations_and_risk_assessment)
    ]
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Running: {test_name}")
        print(f"{'='*60}")
        
        try:
            result = test_func()
            test_results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test {test_name} failed with exception: {e}")
            test_results.append((test_name, False))
    
    # Print summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    passed_tests = sum(1 for _, result in test_results if result)
    total_tests = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Overall Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Advanced multi-factor scoring system is working correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Please review the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 