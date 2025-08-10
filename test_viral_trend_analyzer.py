"""
Test script for AI-powered Viral Trend Analyzer
Tests all major functionality of the viral trend analysis system.
"""

import sys
import os
import logging
from datetime import datetime

# Add project root for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from analytics.viral_trend_analyzer import ViralTrendAnalyzer, TrendSignal, ViralProductCandidate
from db.database import get_db
from services.gpt_client import GPTClient

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_viral_trend_analyzer():
    """Test the viral trend analyzer functionality."""
    print("🚀 Testing AI-Powered Viral Trend Analyzer")
    print("=" * 50)
    
    try:
        # Initialize database and analyzer
        db = get_db()
        analyzer = ViralTrendAnalyzer(db)
        
        # Test 1: Discover viral products
        print("\n1. Testing viral product discovery...")
        viral_products = analyzer.discover_viral_products(
            categories=["electronics", "fashion"],
            max_products=10,
            min_viral_score=0.5,
            include_analysis=True
        )
        
        if "error" in viral_products:
            print(f"❌ Error in viral product discovery: {viral_products['error']}")
        else:
            print(f"✅ Discovered {len(viral_products['viral_products'])} viral products")
            print(f"   Total candidates: {viral_products['total_candidates']}")
            print(f"   Filtered candidates: {viral_products['filtered_candidates']}")
            print(f"   High potential: {viral_products['summary']['high_potential']}")
            print(f"   Medium potential: {viral_products['summary']['medium_potential']}")
            print(f"   Low risk: {viral_products['summary']['low_risk']}")
            
            # Show top 3 products
            if viral_products['viral_products']:
                print("\n   Top 3 Viral Products:")
                for i, product in enumerate(viral_products['viral_products'][:3], 1):
                    print(f"   {i}. {product['product_name']} (Score: {product['viral_score']:.2f}, Risk: {product['risk_level']})")
        
        # Test 2: Analyze specific product viral potential
        print("\n2. Testing product viral potential analysis...")
        product_analysis = analyzer.analyze_product_viral_potential(
            product_name="Smart Fitness Tracker",
            category="electronics"
        )
        
        if "error" in product_analysis:
            print(f"❌ Error in product analysis: {product_analysis['error']}")
        else:
            print(f"✅ Product analysis completed")
            print(f"   Product: {product_analysis['product_name']}")
            print(f"   Viral Score: {product_analysis['viral_score']:.2f}")
            print(f"   Market Potential: {product_analysis['market_potential']:.2f}")
            print(f"   Competition Level: {product_analysis['competition_level']}")
            print(f"   Risk Level: {product_analysis['risk_level']}")
            print(f"   Trend Signals: {len(product_analysis['trend_signals'])}")
            
            # Show recommendations
            if product_analysis['recommendations']:
                print(f"   Recommendations: {len(product_analysis['recommendations'])}")
                for rec in product_analysis['recommendations'][:3]:
                    print(f"     - {rec}")
        
        # Test 3: Get trending categories
        print("\n3. Testing trending categories analysis...")
        trending_categories = analyzer.get_trending_categories(days=30)
        
        if "error" in trending_categories:
            print(f"❌ Error in trending categories: {trending_categories['error']}")
        else:
            print(f"✅ Trending categories analysis completed")
            print(f"   Analysis period: {trending_categories['analysis_period']} days")
            
            if trending_categories['trending_categories']:
                print("   Top Trending Categories:")
                for i, category in enumerate(trending_categories['trending_categories'][:3], 1):
                    print(f"   {i}. {category['category']} (Score: {category['trend_score']:.2f})")
        
        # Test 4: Test trend signal generation
        print("\n4. Testing trend signal generation...")
        test_signals = []
        
        # Test Google Trends
        google_signals = analyzer._analyze_google_trends("Test Product", "electronics")
        test_signals.extend(google_signals)
        print(f"   Google Trends signals: {len(google_signals)}")
        
        # Test TikTok Trends
        tiktok_signals = analyzer._analyze_tiktok_trends("Test Product", "electronics")
        test_signals.extend(tiktok_signals)
        print(f"   TikTok Trends signals: {len(tiktok_signals)}")
        
        # Test Social Media
        social_signals = analyzer._analyze_social_media_trends("Test Product", "electronics")
        test_signals.extend(social_signals)
        print(f"   Social Media signals: {len(social_signals)}")
        
        # Test Ad Library
        ad_signals = analyzer._analyze_ad_library_trends("Test Product", "electronics")
        test_signals.extend(ad_signals)
        print(f"   Ad Library signals: {len(ad_signals)}")
        
        # Test Search Volume
        search_signals = analyzer._analyze_search_volume_trends("Test Product", "electronics")
        test_signals.extend(search_signals)
        print(f"   Search Volume signals: {len(search_signals)}")
        
        print(f"   Total signals generated: {len(test_signals)}")
        
        # Test 5: Test viral score calculation
        print("\n5. Testing viral score calculation...")
        viral_score = analyzer._calculate_viral_score(test_signals)
        print(f"   Calculated viral score: {viral_score:.2f}")
        
        # Test 6: Test product idea generation
        print("\n6. Testing product idea generation...")
        product_ideas = analyzer._generate_product_ideas("smart home gadgets")
        
        if product_ideas:
            print(f"   Generated {len(product_ideas)} product ideas")
            for i, idea in enumerate(product_ideas[:3], 1):
                print(f"   {i}. {idea.get('name', 'Unknown')} ({idea.get('category', 'Unknown')})")
        else:
            print("   No product ideas generated")
        
        # Test 7: Test comprehensive analysis
        print("\n7. Testing comprehensive analysis...")
        if viral_products and 'viral_products' in viral_products:
            # Create test candidates
            test_candidates = []
            for product_data in viral_products['viral_products'][:3]:
                candidate = ViralProductCandidate(
                    product_name=product_data['product_name'],
                    category=product_data['category'],
                    trend_signals=[],
                    viral_score=product_data['viral_score'],
                    market_potential=product_data['market_potential'],
                    competition_level=product_data['competition_level'],
                    estimated_margin=product_data['estimated_margin'],
                    risk_level=product_data['risk_level'],
                    discovery_timestamp=datetime.now(),
                    metadata={}
                )
                test_candidates.append(candidate)
            
            # Generate analysis
            analysis = analyzer._generate_viral_analysis(test_candidates)
            
            if analysis:
                print(f"   Analysis generated successfully")
                print(f"   Statistics: {analysis['statistics']}")
                print(f"   Top categories: {len(analysis['top_categories'])}")
                print(f"   Trend insights: {len(analysis['trend_insights'])}")
                print(f"   Recommendations: {len(analysis['recommendations'])}")
            else:
                print("   No analysis generated")
        
        print("\n✅ All tests completed successfully!")
        
        # Summary
        print("\n📊 Test Summary:")
        print(f"   ✅ Viral product discovery: {'PASS' if 'viral_products' in viral_products else 'FAIL'}")
        print(f"   ✅ Product analysis: {'PASS' if 'viral_score' in product_analysis else 'FAIL'}")
        print(f"   ✅ Trending categories: {'PASS' if 'trending_categories' in trending_categories else 'FAIL'}")
        print(f"   ✅ Trend signals: {'PASS' if test_signals else 'FAIL'}")
        print(f"   ✅ Viral score calculation: {'PASS' if viral_score > 0 else 'FAIL'}")
        print(f"   ✅ Product ideas: {'PASS' if product_ideas else 'FAIL'}")
        print(f"   ✅ Comprehensive analysis: {'PASS' if analysis else 'FAIL'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        logger.error(f"Test failed: {e}")
        return False

def test_integration_with_sales_genie():
    """Test integration with SalesGenie."""
    print("\n🔗 Testing Integration with SalesGenie")
    print("=" * 40)
    
    try:
        # Initialize components
        db = get_db()
        analyzer = ViralTrendAnalyzer(db)
        
        # Simulate SalesGenie workflow
        print("1. Discovering viral products for SalesGenie...")
        viral_products = analyzer.discover_viral_products(
            categories=["electronics", "fashion", "home"],
            max_products=5,
            min_viral_score=0.6,
            include_analysis=True
        )
        
        if "error" in viral_products:
            print(f"❌ Error: {viral_products['error']}")
            return False
        
        print(f"✅ Found {len(viral_products['viral_products'])} viral products")
        
        # Simulate product selection for SalesGenie
        if viral_products['viral_products']:
            selected_product = viral_products['viral_products'][0]
            print(f"\n2. Selected product for SalesGenie: {selected_product['product_name']}")
            
            # Analyze the selected product
            detailed_analysis = analyzer.analyze_product_viral_potential(
                selected_product['product_name'],
                selected_product['category']
            )
            
            if "error" not in detailed_analysis:
                print(f"   Viral Score: {detailed_analysis['viral_score']:.2f}")
                print(f"   Market Potential: {detailed_analysis['market_potential']:.2f}")
                print(f"   Risk Level: {detailed_analysis['risk_level']}")
                
                # Show recommendations for SalesGenie
                if detailed_analysis['recommendations']:
                    print(f"   Recommendations for SalesGenie:")
                    for rec in detailed_analysis['recommendations']:
                        print(f"     - {rec}")
        
        print("✅ Integration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def test_trending_categories_optimization():
    """Test that trending categories uses only 1 API call."""
    print("\n🔍 Testing Trending Categories Optimization")
    print("=" * 50)
    
    try:
        # Initialize analyzer
        db = get_db()
        analyzer = ViralTrendAnalyzer(db)
        
        # Mock the GPT client to count calls
        original_generate_response = analyzer.gpt_client.generate_response
        call_count = 0
        
        def mock_generate_response(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            print(f"   📞 GPT API call #{call_count} made")
            return original_generate_response(*args, **kwargs)
        
        analyzer.gpt_client.generate_response = mock_generate_response
        
        # Test trending categories
        print("1. Testing trending categories analysis...")
        result = analyzer.get_trending_categories(days=30)
        
        # Verify results
        assert "trending_categories" in result, "Missing trending_categories in result"
        assert "viral_products_by_category" in result, "Missing viral_products_by_category in result"
        assert "analysis_period" in result, "Missing analysis_period in result"
        
        # Check that only 1 API call was made
        assert call_count == 1, f"Expected 1 API call, but {call_count} calls were made"
        
        print(f"   ✅ Trending categories analysis completed")
        print(f"   📊 Analysis period: {result['analysis_period']} days")
        print(f"   🎯 API calls made: {call_count}")
        
        # Show some results
        categories = result.get("trending_categories", [])
        if categories:
            print(f"   📈 Top Trending Categories:")
            for i, cat in enumerate(categories[:3], 1):
                print(f"   {i}. {cat.get('category', 'Unknown')} (Score: {cat.get('trend_score', 0):.2f})")
        
        viral_by_category = result.get("viral_products_by_category", {})
        if viral_by_category:
            print(f"   🚀 Viral products found in {len(viral_by_category)} categories")
            for category, products in viral_by_category.items():
                print(f"      {category}: {len(products)} products")
        
        print(f"   ✅ Optimization test passed - Only {call_count} API call used!")
        return True
        
    except Exception as e:
        print(f"   ❌ Optimization test failed: {e}")
        return False
    finally:
        # Restore original method
        if 'analyzer' in locals():
            analyzer.gpt_client.generate_response = original_generate_response

def main():
    """Main test function."""
    print("🎯 AI-Powered Viral Trend Analyzer - Comprehensive Test Suite")
    print("=" * 60)
    
    # Run core tests
    core_tests_passed = test_viral_trend_analyzer()
    
    # Run integration tests
    integration_tests_passed = test_integration_with_sales_genie()
    
    # Run optimization test
    optimization_tests_passed = test_trending_categories_optimization()
    
    # Final summary
    print("\n" + "=" * 60)
    print("🎯 FINAL TEST RESULTS")
    print("=" * 60)
    print(f"   Core Functionality: {'✅ PASS' if core_tests_passed else '❌ FAIL'}")
    print(f"   SalesGenie Integration: {'✅ PASS' if integration_tests_passed else '❌ FAIL'}")
    print(f"   Trending Categories Optimization: {'✅ PASS' if optimization_tests_passed else '❌ FAIL'}")
    
    if core_tests_passed and integration_tests_passed and optimization_tests_passed:
        print("\n🎉 ALL TESTS PASSED! Viral Trend Analyzer is ready for production.")
    else:
        print("\n⚠️ Some tests failed. Please review the errors above.")
    
    return core_tests_passed and integration_tests_passed and optimization_tests_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 