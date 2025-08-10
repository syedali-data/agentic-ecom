#!/usr/bin/env python3
"""
Test script for content_marketing/generator.py functionality
Tests blog post generation, product descriptions, and comparison content.
"""

import requests
import json
from datetime import datetime

def test_generator_functionality():
    """Test the generator.py functionality through API endpoints."""
    base_url = "http://127.0.0.1:8000"
    print("📝 Testing Content Generator Functionality")
    print("=" * 50)
    
    # Test 1: Generate blog post
    print("\n1. Testing Blog Post Generation...")
    try:
        params = {
            "topic": "Best Wireless Earbuds for 2024",
            "product_id": "prod_001",
            "length": "medium"
        }
        response = requests.post(f"{base_url}/content-marketing/generate/blog", params=params)
        if response.status_code == 200:
            result = response.json()
            print("✅ Blog post generation successful!")
            print(f"   Title: {result.get('title', 'N/A')}")
            print(f"   Length: {len(result.get('content', ''))} characters")
            print(f"   Keywords: {len(result.get('keywords', []))} keywords")
            print(f"   Meta Description: {len(result.get('meta_description', ''))} characters")
        else:
            print(f"❌ Blog post generation failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Blog post generation error: {e}")
    
    # Test 2: Generate product description
    print("\n2. Testing Product Description Generation...")
    try:
        params = {
            "product_id": "prod_001"
        }
        response = requests.post(f"{base_url}/content-marketing/generate/product-description", params=params)
        if response.status_code == 200:
            result = response.json()
            print("✅ Product description generation successful!")
            print(f"   Product: {result.get('product_name', 'N/A')}")
            print(f"   Description Length: {len(result.get('description', ''))} characters")
            print(f"   Features: {len(result.get('features', []))} features")
            print(f"   Benefits: {len(result.get('benefits', []))} benefits")
        else:
            print(f"❌ Product description generation failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Product description generation error: {e}")
    
    # Test 3: Generate comparison content
    print("\n3. Testing Comparison Content Generation...")
    try:
        # For comparison, we need to send JSON data with product_ids list
        comparison_data = {
            "product_ids": ["prod_001", "prod_002", "prod_003"]
        }
        response = requests.post(f"{base_url}/content-marketing/generate/comparison", json=comparison_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Comparison content generation successful!")
            print(f"   Title: {result.get('title', 'N/A')}")
            print(f"   Products Compared: {len(result.get('products', []))}")
            print(f"   Content Length: {len(result.get('content', ''))} characters")
            print(f"   Comparison Table: {len(result.get('comparison_table', {}))} rows")
        else:
            print(f"❌ Comparison content generation failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Comparison content generation error: {e}")
    
    # Test 4: Test with different topics and lengths
    print("\n4. Testing Different Topics and Lengths...")
    test_cases = [
        {"topic": "Smart Home Security Systems", "length": "short"},
        {"topic": "Gaming Laptops Comparison", "length": "long"},
        {"topic": "Fitness Trackers for Beginners", "length": "medium"}
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            response = requests.post(f"{base_url}/content-marketing/generate/blog", params=test_case)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Test {i} successful: {test_case['topic']} ({test_case['length']})")
                print(f"   Content length: {len(result.get('content', ''))} characters")
            else:
                print(f"❌ Test {i} failed: {test_case['topic']} - {response.status_code}")
        except Exception as e:
            print(f"❌ Test {i} error: {test_case['topic']} - {e}")
    
    # Test 5: Test error handling
    print("\n5. Testing Error Handling...")
    try:
        # Test with invalid product ID
        params = {
            "product_id": "invalid_product_999"
        }
        response = requests.post(f"{base_url}/content-marketing/generate/product-description", params=params)
        if response.status_code == 404:
            print("✅ Error handling working correctly for invalid product ID")
        else:
            print(f"⚠️ Unexpected response for invalid product: {response.status_code}")
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
    
    # Test 6: Test health check
    print("\n6. Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/content-marketing/health")
        if response.status_code == 200:
            result = response.json()
            print("✅ Content marketing health check successful!")
            print(f"   Status: {result.get('status', 'N/A')}")
            print(f"   Service: {result.get('service', 'N/A')}")
            print(f"   Features: {len(result.get('features', []))} features")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Generator.py Functionality Test Complete!")
    print(f"📅 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def test_generator_direct():
    """Test generator.py directly without API."""
    print("\n🔧 Testing Generator.py Direct Import...")
    try:
        from content_marketing.generator import ContentGenerator
        from db.database import SessionLocal
        
        # Create database session
        db = SessionLocal()
        
        # Initialize generator
        generator = ContentGenerator(db)
        
        print("✅ ContentGenerator imported and initialized successfully!")
        print(f"   GPT Client: {generator.gpt_client}")
        print(f"   Claude Client: {generator.claude_client}")
        print(f"   Database Session: {generator.db}")
        
        # Test method availability
        methods = [
            'generate_blog_post',
            'generate_product_description', 
            'generate_comparison_content',
            '_create_blog_prompt',
            '_create_product_description_prompt',
            '_create_comparison_prompt',
            '_optimize_for_ai_llm',
            '_extract_title',
            '_generate_meta_description',
            '_extract_keywords'
        ]
        
        print("\n📋 Available Methods:")
        for method in methods:
            if hasattr(generator, method):
                print(f"   ✅ {method}")
            else:
                print(f"   ❌ {method} - MISSING")
        
        # Test direct method call
        print("\n🧪 Testing Direct Method Call...")
        try:
            result = generator.generate_blog_post("Test Topic", None, "short")
            print("✅ Direct blog generation successful!")
            print(f"   Title: {result.get('title', 'N/A')}")
            print(f"   Content Length: {len(result.get('content', ''))} characters")
        except Exception as e:
            print(f"❌ Direct blog generation failed: {e}")
        
        db.close()
        print("\n✅ Direct import test successful!")
        
    except Exception as e:
        print(f"❌ Direct import test failed: {e}")

if __name__ == "__main__":
    # Test API endpoints
    test_generator_functionality()
    
    # Test direct import
    test_generator_direct() 