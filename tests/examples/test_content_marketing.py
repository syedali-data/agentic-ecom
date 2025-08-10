#!/usr/bin/env python3
"""
AI LLM Content Marketing System Test Script
Tests all content marketing functionality for AI LLM optimization.
"""

import requests
import json
from datetime import datetime

def test_content_marketing_endpoints():
    """Test all content marketing endpoints."""
    base_url = "http://127.0.0.1:8000"
    print("🧠 Testing AI LLM Content Marketing System")
    print("=" * 60)
    
    # Test health check
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/content-marketing/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check - SUCCESS")
            print(f"   Service: {data.get('service', 'Unknown')}")
            print(f"   Features: {len(data.get('features', []))} features available")
        else:
            print(f"❌ Health Check - FAILED (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ Health Check - ERROR: {e}")
    
    # Test content generation
    print("\n2. Testing Content Generation...")
    try:
        response = requests.post(
            f"{base_url}/content-marketing/generate/blog",
            params={"topic": "wireless earbuds", "length": "medium"}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Blog Generation - SUCCESS")
            print(f"   Topic: {data.get('data', {}).get('topic', 'Unknown')}")
            print(f"   AI LLM Optimized: {data.get('data', {}).get('ai_llm_optimized', False)}")
        else:
            print(f"❌ Blog Generation - FAILED (Status: {response.status_code})")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Blog Generation - ERROR: {e}")
    
    # Test Q&A generation
    print("\n3. Testing Q&A Generation...")
    try:
        response = requests.post(
            f"{base_url}/content-marketing/generate/qa",
            params={"topic": "smartphone buying guide"}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Q&A Generation - SUCCESS")
            print(f"   Topic: {data.get('data', {}).get('topic', 'Unknown')}")
            print(f"   Q&A Pairs: {len(data.get('data', {}).get('qa_pairs', []))}")
        else:
            print(f"❌ Q&A Generation - FAILED (Status: {response.status_code})")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Q&A Generation - ERROR: {e}")
    
    # Test SEO optimization
    print("\n4. Testing SEO Optimization...")
    try:
        test_content = "Wireless earbuds are great for listening to music on the go."
        response = requests.post(
            f"{base_url}/content-marketing/optimize/content",
            params={
                "content": test_content,
                "topic": "wireless earbuds",
                "content_type": "blog"
            }
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SEO Optimization - SUCCESS")
            print(f"   Keywords: {len(data.get('data', {}).get('keywords', []))} keywords")
            print(f"   Optimized: {data.get('data', {}).get('ai_llm_optimized', False)}")
        else:
            print(f"❌ SEO Optimization - FAILED (Status: {response.status_code})")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ SEO Optimization - ERROR: {e}")
    
    # Test keyword generation
    print("\n5. Testing Keyword Generation...")
    try:
        response = requests.get(
            f"{base_url}/content-marketing/optimize/keywords",
            params={"topic": "wireless earbuds", "content_type": "blog"}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Keyword Generation - SUCCESS")
            print(f"   Keywords: {len(data.get('data', {}).get('keywords', []))} AI LLM optimized keywords")
        else:
            print(f"❌ Keyword Generation - FAILED (Status: {response.status_code})")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Keyword Generation - ERROR: {e}")
    
    # Test schema markup generation
    print("\n6. Testing Schema Markup Generation...")
    try:
        # Get first product ID from database
        products_response = requests.get(f"{base_url}/products")
        if products_response.status_code == 200:
            products = products_response.json()
            if products:
                product_id = products[0].get('id')
                response = requests.get(f"{base_url}/content-marketing/schema/product/{product_id}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Schema Markup - SUCCESS")
                    print(f"   Product ID: {product_id}")
                    print(f"   Schema Type: {data.get('data', {}).get('schema', {}).get('@type', 'Unknown')}")
                else:
                    print(f"❌ Schema Markup - FAILED (Status: {response.status_code})")
                    print(f"   Error: {response.text}")
            else:
                print("⚠️  Schema Markup - SKIPPED (No products available)")
        else:
            print(f"❌ Schema Markup - FAILED to get products (Status: {products_response.status_code})")
    except Exception as e:
        print(f"❌ Schema Markup - ERROR: {e}")
    
    # Test content calendar
    print("\n7. Testing Content Calendar...")
    try:
        response = requests.get(
            f"{base_url}/content-marketing/calendar/content",
            params={"days": 7}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Content Calendar - SUCCESS")
            print(f"   Ideas Generated: {data.get('data', {}).get('total_ideas', 0)}")
            print(f"   Days Covered: {data.get('data', {}).get('days_covered', 0)}")
        else:
            print(f"❌ Content Calendar - FAILED (Status: {response.status_code})")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Content Calendar - ERROR: {e}")
    
    # Test performance tracking
    print("\n8. Testing Performance Tracking...")
    try:
        test_metrics = {
            "views": 100,
            "clicks": 15,
            "conversions": 3
        }
        response = requests.post(
            f"{base_url}/content-marketing/track/performance",
            params={
                "content_id": "test_content_123",
                "content_type": "blog",
                "metrics": json.dumps(test_metrics)
            }
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Performance Tracking - SUCCESS")
            print(f"   Content ID: {data.get('data', {}).get('content_id', 'Unknown')}")
            print(f"   Insights: {len(data.get('data', {}).get('insights', []))} insights generated")
        else:
            print(f"❌ Performance Tracking - FAILED (Status: {response.status_code})")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Performance Tracking - ERROR: {e}")
    
    # Test AI LLM mention tracking
    print("\n9. Testing AI LLM Mention Tracking...")
    try:
        mention_details = {
            "featured": True,
            "user_engagement": 150,
            "position": "top"
        }
        response = requests.post(
            f"{base_url}/content-marketing/track/ai-llm-mention",
            params={
                "content_id": "test_content_123",
                "ai_llm_app": "ChatGPT",
                "mention_type": "recommendation",
                "details": json.dumps(mention_details)
            }
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ AI LLM Mention Tracking - SUCCESS")
            print(f"   App: {data.get('data', {}).get('mention_data', {}).get('ai_llm_app', 'Unknown')}")
            print(f"   Impact Score: {data.get('data', {}).get('impact', {}).get('impact_score', 0)}")
        else:
            print(f"❌ AI LLM Mention Tracking - FAILED (Status: {response.status_code})")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ AI LLM Mention Tracking - ERROR: {e}")
    
    # Test analytics
    print("\n10. Testing Analytics...")
    try:
        response = requests.get(
            f"{base_url}/content-marketing/analytics/content",
            params={"days": 7}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Content Analytics - SUCCESS")
            print(f"   Analysis Period: {data.get('data', {}).get('analysis_period', 'Unknown')}")
            print(f"   Insights: {len(data.get('data', {}).get('insights', []))} insights")
        else:
            print(f"❌ Content Analytics - FAILED (Status: {response.status_code})")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Content Analytics - ERROR: {e}")
    
    # Test AI LLM performance report
    print("\n11. Testing AI LLM Performance Report...")
    try:
        response = requests.get(
            f"{base_url}/content-marketing/analytics/ai-llm-performance",
            params={"days": 7}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ AI LLM Performance Report - SUCCESS")
            print(f"   Analysis Period: {data.get('data', {}).get('analysis_period', 'Unknown')}")
            print(f"   Recommendations: {len(data.get('data', {}).get('recommendations', []))} recommendations")
        else:
            print(f"❌ AI LLM Performance Report - FAILED (Status: {response.status_code})")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ AI LLM Performance Report - ERROR: {e}")
    
    # Test complete optimized content creation
    print("\n12. Testing Complete Optimized Content Creation...")
    try:
        response = requests.post(
            f"{base_url}/content-marketing/create/optimized-content",
            params={
                "topic": "best wireless earbuds 2025",
                "content_type": "blog"
            }
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Complete Optimized Content - SUCCESS")
            print(f"   Content ID: {data.get('data', {}).get('content_id', 'Unknown')}")
            print(f"   Content Type: {data.get('data', {}).get('content_type', 'Unknown')}")
            print(f"   Optimization Features: {len(data.get('data', {}).get('optimization_features', {}))} features")
        else:
            print(f"❌ Complete Optimized Content - FAILED (Status: {response.status_code})")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Complete Optimized Content - ERROR: {e}")
    
    # Test content summary
    print("\n13. Testing Content Summary...")
    try:
        response = requests.get(f"{base_url}/content-marketing/summary/content")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Content Summary - SUCCESS")
            summary = data.get('data', {}).get('summary', {})
            print(f"   Total Content: {summary.get('total_content', 0)}")
            print(f"   Total Mentions: {summary.get('total_mentions', 0)}")
            print(f"   Active Apps: {summary.get('active_apps', 0)}")
        else:
            print(f"❌ Content Summary - FAILED (Status: {response.status_code})")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Content Summary - ERROR: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 AI LLM Content Marketing System Test Complete!")
    print(f"📅 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    test_content_marketing_endpoints() 