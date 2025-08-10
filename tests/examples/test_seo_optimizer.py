#!/usr/bin/env python3
"""
Test script for content_marketing/seo_optimizer.py functionality
Tests SEO optimization for AI LLM app discovery and search visibility.
"""

import requests
import json
from datetime import datetime

def test_seo_optimizer_functionality():
    """Test the SEO Optimizer functionality through API endpoints."""
    base_url = "http://127.0.0.1:8000"
    print("🔍 Testing SEO Optimizer Functionality")
    print("=" * 50)
    
    # Test 1: Optimize content for AI LLM
    print("\n1. Testing Content Optimization for AI LLM...")
    try:
        test_content = """
        Wireless earbuds are becoming increasingly popular for their convenience and portability. 
        They offer hands-free listening and are perfect for workouts, commuting, and daily use.
        """
        data = {
            "content": test_content,
            "topic": "Best Wireless Earbuds for 2024",
            "content_type": "blog"
        }
        response = requests.post(f"{base_url}/content-marketing/optimize/seo", json=data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Content optimization successful!")
            print(f"   Original Length: {len(test_content)} characters")
            print(f"   Optimized Length: {len(result.get('optimized_content', ''))} characters")
            print(f"   Keywords: {len(result.get('keywords', []))} keywords")
            print(f"   AI LLM Optimized: {result.get('ai_llm_optimized', False)}")
        else:
            print(f"❌ Content optimization failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Content optimization error: {e}")
    
    # Test 2: Generate AI LLM keywords
    print("\n2. Testing AI LLM Keyword Generation...")
    try:
        params = {
            "topic": "Smart Home Security Systems",
            "content_type": "product"
        }
        response = requests.post(f"{base_url}/content-marketing/generate/keywords", params=params)
        if response.status_code == 200:
            result = response.json()
            print("✅ Keyword generation successful!")
            print(f"   Keywords Generated: {len(result.get('keywords', []))} keywords")
            print(f"   Sample Keywords: {result.get('keywords', [])[:5]}")
        else:
            print(f"❌ Keyword generation failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Keyword generation error: {e}")
    
    # Test 3: Optimize title for AI LLM
    print("\n3. Testing Title Optimization...")
    try:
        data = {
            "content": "A comprehensive guide to wireless earbuds",
            "topic": "Wireless Earbuds Guide"
        }
        response = requests.post(f"{base_url}/content-marketing/optimize/title", json=data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Title optimization successful!")
            print(f"   Optimized Title: {result.get('optimized_title', 'N/A')}")
        else:
            print(f"❌ Title optimization failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Title optimization error: {e}")
    
    # Test 4: Generate meta description
    print("\n4. Testing Meta Description Generation...")
    try:
        data = {
            "content": "Discover the best wireless earbuds for 2024 with expert recommendations and comparisons.",
            "keywords": ["wireless earbuds", "best", "2024", "recommendations"]
        }
        response = requests.post(f"{base_url}/content-marketing/generate/meta-description", json=data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Meta description generation successful!")
            print(f"   Meta Description: {result.get('meta_description', 'N/A')}")
            print(f"   Length: {len(result.get('meta_description', ''))} characters")
        else:
            print(f"❌ Meta description generation failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Meta description generation error: {e}")
    
    # Test 5: Generate AI LLM schema
    print("\n5. Testing AI LLM Schema Generation...")
    try:
        data = {
            "title": "Best Wireless Earbuds for 2024",
            "content": "Expert guide to choosing the best wireless earbuds",
            "keywords": ["wireless earbuds", "best", "2024"],
            "content_type": "blog"
        }
        response = requests.post(f"{base_url}/content-marketing/generate/schema", json=data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Schema generation successful!")
            print(f"   Schema Type: {result.get('schema_type', 'N/A')}")
            print(f"   Has Q&A: {len(result.get('qa_section', [])) > 0}")
            print(f"   Has Expert Tips: {len(result.get('expert_tips', [])) > 0}")
        else:
            print(f"❌ Schema generation failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Schema generation error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 SEO Optimizer Test Complete!")
    print(f"📅 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def test_seo_optimizer_direct():
    """Test SEO Optimizer directly without API."""
    print("\n🔧 Testing SEO Optimizer Direct Import...")
    try:
        from content_marketing.seo_optimizer import SEOOptimizer
        from db.database import SessionLocal
        
        # Create database session
        db = SessionLocal()
        
        # Initialize SEO optimizer
        seo_optimizer = SEOOptimizer(db)
        
        print("✅ SEOOptimizer imported and initialized successfully!")
        print(f"   GPT Client: {seo_optimizer.gpt_client}")
        print(f"   Claude Client: {seo_optimizer.claude_client}")
        print(f"   Database Session: {seo_optimizer.db}")
        
        # Test method availability
        methods = [
            'optimize_for_ai_llm',
            'generate_ai_llm_keywords',
            'optimize_title_for_ai_llm',
            'generate_meta_description',
            'optimize_content_structure',
            'add_conversational_elements',
            'generate_ai_llm_schema',
            '_extract_key_information',
            '_generate_qa_section',
            '_generate_expert_tips',
            '_generate_comparison_table',
            '_parse_qa_pairs'
        ]
        
        print("\n📋 Available Methods:")
        for method in methods:
            if hasattr(seo_optimizer, method):
                print(f"   ✅ {method}")
            else:
                print(f"   ❌ {method} - MISSING")
        
        # Test direct method calls
        print("\n🧪 Testing Direct Method Calls...")
        
        # Test 1: Generate keywords
        try:
            keywords = seo_optimizer.generate_ai_llm_keywords("Wireless Earbuds", "blog")
            print("✅ Keyword generation successful!")
            print(f"   Keywords: {len(keywords)} keywords generated")
            print(f"   Sample: {keywords[:5]}")
        except Exception as e:
            print(f"❌ Keyword generation failed: {e}")
        
        # Test 2: Optimize title
        try:
            title = seo_optimizer.optimize_title_for_ai_llm("Guide to wireless earbuds", "Wireless Earbuds")
            print("✅ Title optimization successful!")
            print(f"   Optimized Title: {title}")
        except Exception as e:
            print(f"❌ Title optimization failed: {e}")
        
        # Test 3: Generate meta description
        try:
            meta_desc = seo_optimizer.generate_meta_description(
                "Comprehensive guide to wireless earbuds with expert recommendations",
                ["wireless earbuds", "guide", "recommendations"]
            )
            print("✅ Meta description generation successful!")
            print(f"   Meta Description: {meta_desc}")
        except Exception as e:
            print(f"❌ Meta description generation failed: {e}")
        
        # Test 4: Full content optimization
        try:
            test_content = "Wireless earbuds are great for daily use. They offer convenience and portability."
            result = seo_optimizer.optimize_for_ai_llm(test_content, "Wireless Earbuds", "blog")
            print("✅ Full content optimization successful!")
            print(f"   Original Length: {len(test_content)} characters")
            print(f"   Optimized Length: {len(result.get('optimized_content', ''))} characters")
            print(f"   Keywords: {len(result.get('keywords', []))} keywords")
        except Exception as e:
            print(f"❌ Full content optimization failed: {e}")
        
        db.close()
        print("\n✅ Direct import test successful!")
        
    except Exception as e:
        print(f"❌ Direct import test failed: {e}")

if __name__ == "__main__":
    # Test API endpoints
    test_seo_optimizer_functionality()
    
    # Test direct import
    test_seo_optimizer_direct() 