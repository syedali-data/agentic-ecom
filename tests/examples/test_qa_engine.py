#!/usr/bin/env python3
"""
Test script for content_marketing/qa_engine.py functionality
Tests Q&A content generation for AI LLM optimization.
"""

import requests
import json
from datetime import datetime

def test_qa_engine_functionality():
    """Test the Q&A Engine functionality through API endpoints."""
    base_url = "http://127.0.0.1:8000"
    print("❓ Testing Q&A Engine Functionality")
    print("=" * 50)
    
    # Test 1: Generate Q&A content
    print("\n1. Testing Q&A Content Generation...")
    try:
        params = {
            "topic": "Best Wireless Earbuds for 2024",
            "product_id": "prod_001"
        }
        response = requests.post(f"{base_url}/content-marketing/generate/qa", params=params)
        if response.status_code == 200:
            result = response.json()
            print("✅ Q&A content generation successful!")
            print(f"   Topic: {result.get('topic', 'N/A')}")
            print(f"   Q&A Pairs: {len(result.get('qa_pairs', []))} pairs")
            print(f"   Content Length: {len(result.get('content', ''))} characters")
            print(f"   AI LLM Optimized: {result.get('ai_llm_optimized', False)}")
        else:
            print(f"❌ Q&A content generation failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Q&A content generation error: {e}")
    
    # Test 2: Generate product-specific Q&A
    print("\n2. Testing Product Q&A Generation...")
    try:
        params = {
            "product_id": "prod_001"
        }
        response = requests.post(f"{base_url}/content-marketing/generate/product-qa", params=params)
        if response.status_code == 200:
            result = response.json()
            print("✅ Product Q&A generation successful!")
            print(f"   Product: {result.get('product_name', 'N/A')}")
            print(f"   Q&A Pairs: {len(result.get('qa_pairs', []))} pairs")
            print(f"   Content Length: {len(result.get('content', ''))} characters")
        else:
            print(f"❌ Product Q&A generation failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Product Q&A generation error: {e}")
    
    # Test 3: Test different topics
    print("\n3. Testing Different Topics...")
    test_topics = [
        "Smart Home Security Systems",
        "Gaming Laptops Comparison", 
        "Fitness Trackers for Beginners"
    ]
    
    for i, topic in enumerate(test_topics, 1):
        try:
            params = {"topic": topic}
            response = requests.post(f"{base_url}/content-marketing/generate/qa", params=params)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Test {i} successful: {topic}")
                print(f"   Q&A Pairs: {len(result.get('qa_pairs', []))} pairs")
            else:
                print(f"❌ Test {i} failed: {topic} - {response.status_code}")
        except Exception as e:
            print(f"❌ Test {i} error: {topic} - {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Q&A Engine Test Complete!")
    print(f"📅 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def test_qa_engine_direct():
    """Test Q&A Engine directly without API."""
    print("\n🔧 Testing Q&A Engine Direct Import...")
    try:
        from content_marketing.qa_engine import QAEngine
        from db.database import SessionLocal
        
        # Create database session
        db = SessionLocal()
        
        # Initialize Q&A engine
        qa_engine = QAEngine(db)
        
        print("✅ QAEngine imported and initialized successfully!")
        print(f"   GPT Client: {qa_engine.gpt_client}")
        print(f"   Claude Client: {qa_engine.claude_client}")
        print(f"   Database Session: {qa_engine.db}")
        
        # Test method availability
        methods = [
            'generate_qa_content',
            'generate_product_qa',
            'generate_comparison_qa',
            '_generate_qa_pairs',
            '_generate_product_qa_pairs',
            '_generate_comparison_qa_pairs',
            '_parse_qa_pairs',
            '_optimize_for_ai_llm'
        ]
        
        print("\n📋 Available Methods:")
        for method in methods:
            if hasattr(qa_engine, method):
                print(f"   ✅ {method}")
            else:
                print(f"   ❌ {method} - MISSING")
        
        # Test direct method call
        print("\n🧪 Testing Direct Method Call...")
        try:
            result = qa_engine.generate_qa_content("Test Topic", None)
            print("✅ Direct Q&A generation successful!")
            print(f"   Topic: {result.get('topic', 'N/A')}")
            print(f"   Q&A Pairs: {len(result.get('qa_pairs', []))} pairs")
        except Exception as e:
            print(f"❌ Direct Q&A generation failed: {e}")
        
        db.close()
        print("\n✅ Direct import test successful!")
        
    except Exception as e:
        print(f"❌ Direct import test failed: {e}")

if __name__ == "__main__":
    # Test API endpoints
    test_qa_engine_functionality()
    
    # Test direct import
    test_qa_engine_direct() 