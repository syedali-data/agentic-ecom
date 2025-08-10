#!/usr/bin/env python3
"""
Multi-Platform Marketing Strategy Test Script
Tests the comprehensive marketing strategy across Meta, Pinterest, and AI applications.
"""

import requests
import json
from datetime import datetime

def test_multi_platform_marketing():
    """Test the multi-platform marketing strategy system."""
    base_url = "http://127.0.0.1:8000"
    print("🎯 Testing Multi-Platform Marketing Strategy System")
    print("=" * 70)
    
    # Test health check
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/multi-platform-marketing/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check - SUCCESS")
            print(f"   Service: {data.get('service', 'Unknown')}")
            print(f"   Platforms: {len(data.get('platforms_supported', []))} platforms supported")
            print(f"   Features: {len(data.get('features', []))} features available")
        else:
            print(f"❌ Health Check - FAILED (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ Health Check - ERROR: {e}")
    
    # Test strategy creation
    print("\n2. Testing Strategy Creation...")
    try:
        strategy_request = {
            "product_id": "sample_product_123",
            "platforms": ["meta", "pinterest", "ai_apps"]
        }
        response = requests.post(
            f"{base_url}/multi-platform-marketing/strategy/create",
            json=strategy_request
        )
        if response.status_code == 200:
            data = response.json()
            strategy_id = data.get('data', {}).get('strategy_id', 'unknown')
            print(f"✅ Strategy Creation - SUCCESS")
            print(f"   Strategy ID: {strategy_id}")
            print(f"   Product: {data.get('data', {}).get('product_name', 'Unknown')}")
            print(f"   Platforms: {data.get('data', {}).get('platforms', [])}")
            print(f"   Status: {data.get('data', {}).get('status', 'Unknown')}")
        else:
            print(f"❌ Strategy Creation - FAILED (Status: {response.status_code})")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Strategy Creation - ERROR: {e}")
        strategy_id = "test_strategy_123"
    
    # Test Meta strategy
    print("\n3. Testing Meta Strategy...")
    try:
        response = requests.post(
            f"{base_url}/multi-platform-marketing/meta/strategy",
            params={"product_id": "sample_product_123"}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Meta Strategy - SUCCESS")
            meta_strategy = data.get('data', {})
            print(f"   Platform: {meta_strategy.get('platform', 'Unknown')}")
            print(f"   Campaigns: {len(meta_strategy.get('campaigns', []))} campaigns")
            print(f"   Budget: ${meta_strategy.get('budget_allocation', {}).get('daily_budget', 0)}/day")
            print(f"   Ad Formats: {meta_strategy.get('ad_formats', [])}")
        else:
            print(f"❌ Meta Strategy - FAILED (Status: {response.status_code})")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Meta Strategy - ERROR: {e}")
    
    # Test Pinterest strategy
    print("\n4. Testing Pinterest Strategy...")
    try:
        response = requests.post(
            f"{base_url}/multi-platform-marketing/pinterest/strategy",
            params={"product_id": "sample_product_123"}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Pinterest Strategy - SUCCESS")
            pinterest_strategy = data.get('data', {})
            print(f"   Platform: {pinterest_strategy.get('platform', 'Unknown')}")
            print(f"   Pins: {len(pinterest_strategy.get('pins', []))} pins")
            print(f"   Boards: {len(pinterest_strategy.get('boards', []))} boards")
            print(f"   Budget: ${pinterest_strategy.get('budget_allocation', {}).get('daily_budget', 0)}/day")
        else:
            print(f"❌ Pinterest Strategy - FAILED (Status: {response.status_code})")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Pinterest Strategy - ERROR: {e}")
    
    # Test AI Apps strategy
    print("\n5. Testing AI Apps Strategy...")
    try:
        response = requests.post(
            f"{base_url}/multi-platform-marketing/ai-apps/strategy",
            params={"product_id": "sample_product_123"}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ AI Apps Strategy - SUCCESS")
            ai_strategy = data.get('data', {})
            print(f"   Platform: {ai_strategy.get('platform', 'Unknown')}")
            print(f"   Target Apps: {ai_strategy.get('target_apps', [])}")
            print(f"   Content Types: {ai_strategy.get('content_types', [])}")
            print(f"   Optimization Features: {len(ai_strategy.get('optimization_features', {}))} features")
        else:
            print(f"❌ AI Apps Strategy - FAILED (Status: {response.status_code})")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ AI Apps Strategy - ERROR: {e}")
    
    # Test content generation
    print("\n6. Testing Multi-Platform Content Generation...")
    try:
        response = requests.post(
            f"{base_url}/multi-platform-marketing/content/generate",
            params={
                "product_id": "sample_product_123",
                "platforms": ["meta", "pinterest", "ai_apps"]
            }
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Content Generation - SUCCESS")
            content = data.get('data', {})
            print(f"   Meta Content: {'✅' if 'meta' in content else '❌'}")
            print(f"   Pinterest Content: {'✅' if 'pinterest' in content else '❌'}")
            print(f"   AI Apps Content: {'✅' if 'ai_apps' in content else '❌'}")
        else:
            print(f"❌ Content Generation - FAILED (Status: {response.status_code})")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Content Generation - ERROR: {e}")
    
    # Test platform performance analytics
    print("\n7. Testing Platform Performance Analytics...")
    try:
        response = requests.get(
            f"{base_url}/multi-platform-marketing/analytics/platform-performance",
            params={"days": 30}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Platform Performance - SUCCESS")
            performance = data.get('data', {}).get('platform_performance', {})
            
            for platform, metrics in performance.items():
                print(f"   {platform.upper()}:")
                print(f"     - Impressions: {metrics.get('impressions', 0):,}")
                print(f"     - Clicks: {metrics.get('clicks', 0):,}")
                print(f"     - Conversions: {metrics.get('conversions', 0)}")
                print(f"     - Revenue: ${metrics.get('revenue', 0):,}")
                print(f"     - ROAS: {metrics.get('roas', 0)}x")
        else:
            print(f"❌ Platform Performance - FAILED (Status: {response.status_code})")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Platform Performance - ERROR: {e}")
    
    # Test strategy optimization
    print("\n8. Testing Strategy Optimization...")
    try:
        response = requests.post(
            f"{base_url}/multi-platform-marketing/optimize/strategy",
            params={
                "strategy_id": strategy_id,
                "optimization_type": "performance"
            }
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Strategy Optimization - SUCCESS")
            optimization = data.get('data', {})
            print(f"   Strategy ID: {optimization.get('strategy_id', 'Unknown')}")
            print(f"   Optimization Type: {optimization.get('optimization_type', 'Unknown')}")
            print(f"   Optimizations Applied: {len(optimization.get('optimizations_applied', []))}")
            print(f"   Expected Improvements: {optimization.get('expected_improvement', {})}")
        else:
            print(f"❌ Strategy Optimization - FAILED (Status: {response.status_code})")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Strategy Optimization - ERROR: {e}")
    
    # Test strategy execution
    print("\n9. Testing Strategy Execution...")
    try:
        execution_request = {
            "strategy_id": strategy_id,
            "platforms": ["meta", "pinterest", "ai_apps"]
        }
        response = requests.post(
            f"{base_url}/multi-platform-marketing/strategy/execute",
            json=execution_request
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Strategy Execution - SUCCESS")
            execution = data.get('data', {})
            print(f"   Strategy ID: {execution.get('strategy_id', 'Unknown')}")
            print(f"   Status: {execution.get('execution_status', 'Unknown')}")
            print(f"   Platforms Executed: {execution.get('platforms_executed', [])}")
            print(f"   Campaigns Created: {execution.get('campaigns_created', 0)}")
            print(f"   Content Published: {execution.get('content_published', 0)}")
        else:
            print(f"❌ Strategy Execution - FAILED (Status: {response.status_code})")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Strategy Execution - ERROR: {e}")
    
    # Test strategy performance
    print("\n10. Testing Strategy Performance...")
    try:
        response = requests.get(
            f"{base_url}/multi-platform-marketing/strategy/{strategy_id}/performance"
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Strategy Performance - SUCCESS")
            performance = data.get('data', {})
            metrics = performance.get('performance_metrics', {})
            print(f"   Total Impressions: {metrics.get('total_impressions', 0):,}")
            print(f"   Total Clicks: {metrics.get('total_clicks', 0):,}")
            print(f"   Total Conversions: {metrics.get('total_conversions', 0)}")
            print(f"   Total Revenue: ${metrics.get('total_revenue', 0):,}")
            print(f"   ROAS: {metrics.get('total_roas', 0)}x")
            print(f"   CPA: ${metrics.get('total_cpa', 0)}")
            
            # Check if AI apps performance is integrated
            platform_perf = performance.get('platform_performance', {})
            ai_apps_perf = platform_perf.get('ai_apps', {})
            if ai_apps_perf:
                print("✅ AI apps performance data integrated")
                print(f"   - Mentions: {ai_apps_perf.get('mentions', 0)}")
                print(f"   - Content Engagement: {ai_apps_perf.get('content_engagement', 0)}")
                print(f"   - Content Visibility: {ai_apps_perf.get('content_visibility', 0)}")
            else:
                print("⚠️  AI apps performance data not found")
                
        else:
            print(f"❌ Strategy Performance - FAILED (Status: {response.status_code})")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Strategy Performance - ERROR: {e}")
    
    # Test performance tracking integration
    print("\n11. Testing Performance Tracking Integration...")
    try:
        # Create strategy service directly to test integration
        from services.multi_platform_marketing_strategy import MultiPlatformMarketingStrategy
        from db.database import get_db
        
        # Get database session
        db = next(get_db())
        strategy_service = MultiPlatformMarketingStrategy(db)
        
        # Create a test strategy
        strategy_result = strategy_service.create_product_marketing_strategy("test_product_1")
        
        if "error" in strategy_result:
            print(f"❌ Failed to create strategy: {strategy_result['error']}")
        else:
            strategy_id = strategy_result["strategy_id"]
            print(f"✅ Created strategy: {strategy_id}")
            
            # Get performance data
            performance_result = strategy_service.get_strategy_performance(strategy_id)
            
            if "error" in performance_result:
                print(f"❌ Failed to get performance: {performance_result['error']}")
            else:
                print("✅ Performance data retrieved successfully")
                print(f"   - Strategy ID: {performance_result['strategy_id']}")
                print(f"   - Product ID: {performance_result['product_id']}")
                print(f"   - Data Sources: {performance_result['data_sources']}")
                
                # Check if AI apps performance is included
                ai_apps_perf = performance_result.get("platform_performance", {}).get("ai_apps", {})
                if ai_apps_perf:
                    print("✅ AI apps performance data integrated")
                    print(f"   - Mentions: {ai_apps_perf.get('mentions', 0)}")
                    print(f"   - App Distribution: {ai_apps_perf.get('app_distribution', {})}")
                    print(f"   - Content Engagement: {ai_apps_perf.get('content_engagement', 0)}")
                else:
                    print("⚠️  AI apps performance data not found")
                
                # Check aggregated metrics
                total_metrics = performance_result.get("performance_metrics", {})
                if total_metrics:
                    print("✅ Aggregated performance metrics calculated")
                    print(f"   - Total Impressions: {total_metrics.get('total_impressions', 0)}")
                    print(f"   - Total Clicks: {total_metrics.get('total_clicks', 0)}")
                    print(f"   - Total Conversions: {total_metrics.get('total_conversions', 0)}")
                    print(f"   - Total Revenue: ${total_metrics.get('total_revenue', 0)}")
                else:
                    print("⚠️  Aggregated metrics not found")
                    
    except Exception as e:
        print(f"❌ Performance tracking integration test failed: {e}")
    
    print("\n" + "=" * 70)
    print("🎯 Multi-Platform Marketing Strategy Test Complete!")
    print("=" * 70)

if __name__ == "__main__":
    test_multi_platform_marketing() 