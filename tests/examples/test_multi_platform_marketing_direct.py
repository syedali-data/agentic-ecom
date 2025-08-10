#!/usr/bin/env python3
"""
Multi-Platform Marketing Strategy Direct Test Script
Tests the comprehensive marketing strategy service directly without requiring FastAPI server.
"""

import sys
import os
from datetime import datetime

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_multi_platform_marketing_direct():
    """Test the multi-platform marketing strategy system directly."""
    print("🎯 Testing Multi-Platform Marketing Strategy System (Direct)")
    print("=" * 70)
    
    try:
        # Import required modules
        from services.multi_platform_marketing_strategy import MultiPlatformMarketingStrategy
        from db.database import get_db
        from db.models import Product
        
        print("\n1. Testing Service Initialization...")
        
        # Get database session
        db = next(get_db())
        strategy_service = MultiPlatformMarketingStrategy(db)
        
        print("✅ Service initialized successfully")
        print(f"   - Meta API: {type(strategy_service.meta_api).__name__}")
        print(f"   - Pinterest API: {type(strategy_service.pinterest_api).__name__}")
        print(f"   - Content Optimizer: {type(strategy_service.content_optimizer).__name__}")
        print(f"   - Performance Tracker: {type(strategy_service.performance_tracker).__name__}")
        
        # Create a test product if it doesn't exist
        print("\n2. Testing Product Setup...")
        test_product_id = "test_product_multi_platform"
        
        # Check if product exists
        existing_product = db.query(Product).filter(Product.id == test_product_id).first()
        if not existing_product:
            # Create a test product
            test_product = Product(
                id=test_product_id,
                name="Test Multi-Platform Product",
                description="A test product for multi-platform marketing strategy testing",
                price=99.99,
                category="ELECTRONICS",
                sku=f"TEST-{datetime.now().strftime('%Y%m%d')}",
                status="ACTIVE"
            )
            db.add(test_product)
            db.commit()
            print(f"✅ Created test product: {test_product_id}")
        else:
            print(f"✅ Using existing test product: {test_product_id}")
        
        # Test strategy creation
        print("\n3. Testing Strategy Creation...")
        strategy_result = strategy_service.create_product_marketing_strategy(test_product_id)
        
        if "error" in strategy_result:
            print(f"❌ Strategy Creation - FAILED: {strategy_result['error']}")
            return
        else:
            print("✅ Strategy Creation - SUCCESS")
            strategy_id = strategy_result["strategy_id"]
            print(f"   - Strategy ID: {strategy_id}")
            print(f"   - Product Name: {strategy_result.get('product_name', 'Unknown')}")
            print(f"   - Platforms: {strategy_result.get('platforms', [])}")
            print(f"   - Status: {strategy_result.get('status', 'Unknown')}")
            
            # Check strategy components
            if "ai_content" in strategy_result:
                print("   - AI Content: ✅ Generated")
            if "meta_strategy" in strategy_result:
                print("   - Meta Strategy: ✅ Created")
            if "pinterest_strategy" in strategy_result:
                print("   - Pinterest Strategy: ✅ Created")
            if "ai_apps_strategy" in strategy_result:
                print("   - AI Apps Strategy: ✅ Created")
            if "optimization_strategy" in strategy_result:
                print("   - Optimization Strategy: ✅ Created")
        
        # Test strategy performance
        print("\n4. Testing Strategy Performance...")
        performance_result = strategy_service.get_strategy_performance(strategy_id)
        
        if "error" in performance_result:
            print(f"❌ Strategy Performance - FAILED: {performance_result['error']}")
        else:
            print("✅ Strategy Performance - SUCCESS")
            print(f"   - Strategy ID: {performance_result['strategy_id']}")
            print(f"   - Product ID: {performance_result['product_id']}")
            print(f"   - Last Updated: {performance_result['last_updated']}")
            
            # Check platform performance
            platform_performance = performance_result.get("platform_performance", {})
            print(f"   - Platforms Tracked: {list(platform_performance.keys())}")
            
            # Check AI apps performance integration
            ai_apps_perf = platform_performance.get("ai_apps", {})
            if ai_apps_perf:
                print("   - AI Apps Performance: ✅ Integrated")
                print(f"     * Mentions: {ai_apps_perf.get('mentions', 0)}")
                print(f"     * App Distribution: {ai_apps_perf.get('app_distribution', {})}")
                print(f"     * Content Engagement: {ai_apps_perf.get('content_engagement', 0)}")
                print(f"     * Content Visibility: {ai_apps_perf.get('content_visibility', 0)}")
            else:
                print("   - AI Apps Performance: ⚠️ Not found")
            
            # Check aggregated metrics
            total_metrics = performance_result.get("performance_metrics", {})
            if total_metrics:
                print("   - Aggregated Metrics: ✅ Calculated")
                print(f"     * Total Impressions: {total_metrics.get('total_impressions', 0):,}")
                print(f"     * Total Clicks: {total_metrics.get('total_clicks', 0):,}")
                print(f"     * Total Conversions: {total_metrics.get('total_conversions', 0)}")
                print(f"     * Total Revenue: ${total_metrics.get('total_revenue', 0):,}")
                print(f"     * Total ROAS: {total_metrics.get('total_roas', 0)}x")
                print(f"     * Total CPA: ${total_metrics.get('total_cpa', 0)}")
            else:
                print("   - Aggregated Metrics: ⚠️ Not found")
            
            # Check data sources
            data_sources = performance_result.get("data_sources", {})
            if data_sources:
                print("   - Data Sources: ✅ Configured")
                for source, description in data_sources.items():
                    print(f"     * {source}: {description}")
            else:
                print("   - Data Sources: ⚠️ Not found")
        
        # Test content generation
        print("\n5. Testing Content Generation...")
        try:
            # Test AI content generation
            ai_content = strategy_service._generate_ai_optimized_content(existing_product or test_product)
            if "error" in ai_content:
                print(f"❌ AI Content Generation - FAILED: {ai_content['error']}")
            else:
                print("✅ AI Content Generation - SUCCESS")
                print(f"   - Blog Content: {'✅' if 'blog_content' in ai_content else '❌'}")
                print(f"   - Product Content: {'✅' if 'product_content' in ai_content else '❌'}")
                print(f"   - Q&A Content: {'✅' if 'qa_content' in ai_content else '❌'}")
                print(f"   - SEO Content: {'✅' if 'seo_content' in ai_content else '❌'}")
        except Exception as e:
            print(f"❌ AI Content Generation - ERROR: {e}")
        
        # Test Meta strategy creation
        print("\n6. Testing Meta Strategy Creation...")
        try:
            meta_strategy = strategy_service._create_meta_strategy(existing_product or test_product, ai_content)
            if "error" in meta_strategy:
                print(f"❌ Meta Strategy - FAILED: {meta_strategy['error']}")
            else:
                print("✅ Meta Strategy - SUCCESS")
                print(f"   - Platform: {meta_strategy.get('platform', 'Unknown')}")
                print(f"   - Campaigns: {len(meta_strategy.get('campaigns', []))} campaigns")
                print(f"   - Budget: ${meta_strategy.get('budget_allocation', {}).get('daily_budget', 0)}/day")
                print(f"   - Ad Formats: {meta_strategy.get('ad_formats', [])}")
        except Exception as e:
            print(f"❌ Meta Strategy - ERROR: {e}")
        
        # Test Pinterest strategy creation
        print("\n7. Testing Pinterest Strategy Creation...")
        try:
            pinterest_strategy = strategy_service._create_pinterest_strategy(existing_product or test_product, ai_content)
            if "error" in pinterest_strategy:
                print(f"❌ Pinterest Strategy - FAILED: {pinterest_strategy['error']}")
            else:
                print("✅ Pinterest Strategy - SUCCESS")
                print(f"   - Platform: {pinterest_strategy.get('platform', 'Unknown')}")
                print(f"   - Pins: {len(pinterest_strategy.get('pins', []))} pins")
                print(f"   - Boards: {len(pinterest_strategy.get('boards', []))} boards")
                print(f"   - Budget: ${pinterest_strategy.get('budget_allocation', {}).get('daily_budget', 0)}/day")
        except Exception as e:
            print(f"❌ Pinterest Strategy - ERROR: {e}")
        
        # Test AI apps strategy creation
        print("\n8. Testing AI Apps Strategy Creation...")
        try:
            ai_apps_strategy = strategy_service._create_ai_apps_strategy(existing_product or test_product, ai_content)
            if "error" in ai_apps_strategy:
                print(f"❌ AI Apps Strategy - FAILED: {ai_apps_strategy['error']}")
            else:
                print("✅ AI Apps Strategy - SUCCESS")
                print(f"   - Platform: {ai_apps_strategy.get('platform', 'Unknown')}")
                print(f"   - Target Apps: {ai_apps_strategy.get('target_apps', [])}")
                print(f"   - Content Types: {ai_apps_strategy.get('content_types', [])}")
                print(f"   - Optimization Features: {len(ai_apps_strategy.get('optimization_features', {}))} features")
        except Exception as e:
            print(f"❌ AI Apps Strategy - ERROR: {e}")
        
        # Test performance tracking integration
        print("\n9. Testing Performance Tracking Integration...")
        try:
            # Test content performance tracking
            track_result = strategy_service.performance_tracker.track_content_performance(
                content_id=f"test_content_{test_product_id}",
                content_type="blog",
                metrics={
                    "views": 1000,
                    "clicks": 50,
                    "conversions": 5,
                    "engagement_rate": 0.05
                }
            )
            
            if "error" in track_result:
                print(f"❌ Content Performance Tracking - FAILED: {track_result['error']}")
            else:
                print("✅ Content Performance Tracking - SUCCESS")
                print(f"   - Content ID: {track_result.get('content_id', 'Unknown')}")
                print(f"   - Tracked At: {track_result.get('tracked_at', 'Unknown')}")
            
            # Test AI LLM mention tracking
            mention_result = strategy_service.performance_tracker.track_ai_llm_mentions(
                content_id=f"test_content_{test_product_id}",
                ai_llm_app="ChatGPT",
                mention_type="recommendation",
                details={
                    "user_engagement": "high",
                    "response_quality": "excellent",
                    "context_relevance": "perfect"
                }
            )
            
            if "error" in mention_result:
                print(f"❌ AI LLM Mention Tracking - FAILED: {mention_result['error']}")
            else:
                print("✅ AI LLM Mention Tracking - SUCCESS")
                print(f"   - AI App: {mention_result.get('ai_llm_app', 'Unknown')}")
                print(f"   - Mention Type: {mention_result.get('mention_type', 'Unknown')}")
                print(f"   - Impact Score: {mention_result.get('impact_score', 0)}")
                
        except Exception as e:
            print(f"❌ Performance Tracking Integration - ERROR: {e}")
        
        print("\n" + "=" * 70)
        print("🎯 Multi-Platform Marketing Strategy Direct Test Complete!")
        print("=" * 70)
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Please ensure all required modules are available.")
    except Exception as e:
        print(f"❌ Test Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_multi_platform_marketing_direct() 