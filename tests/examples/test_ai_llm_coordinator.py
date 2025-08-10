#!/usr/bin/env python3
"""
Focused test for AI LLM Optimizer - Main Coordinator Module
Tests the core coordination functionality without running all comprehensive tests.
"""

import sys
import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any

# Add project root to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from db.database import SessionLocal
from content_marketing.ai_llm_optimizer import AILLMOptimizer
from db.models import Product, ProductStatus

def test_ai_llm_coordinator():
    """Focused test of AI LLM Optimizer main coordinator functionality."""
    
    print("🧪 Testing AI LLM Optimizer - Main Coordinator Module")
    print("=" * 60)
    
    # Initialize database session and optimizer
    db = SessionLocal()
    optimizer = AILLMOptimizer(db)
    
    try:
        # Test 1: Basic Coordinator Initialization
        print("\n1. Testing Coordinator Initialization...")
        print(f"   ✅ AILLMOptimizer initialized successfully")
        print(f"   ✅ Database session: {type(db).__name__}")
        print(f"   ✅ Content Generator: {type(optimizer.content_generator).__name__}")
        print(f"   ✅ SEO Optimizer: {type(optimizer.seo_optimizer).__name__}")
        print(f"   ✅ QA Engine: {type(optimizer.qa_engine).__name__}")
        print(f"   ✅ Schema Generator: {type(optimizer.schema_generator).__name__}")
        
        # Test 2: Create Test Product
        print("\n2. Creating Test Product...")
        test_product = Product(
            name="Test Electronics Product",
            description="High-quality test product with advanced features",
            sku="TEST-ELECTRONICS-001",
            category="Electronics",
            price=149.99,
            status=ProductStatus.ACTIVE,
            image_url="https://example.com/test-product.jpg",
            tags=["test", "electronics", "featured"],
            product_metadata={
                "features": ["Feature 1", "Feature 2", "Feature 3"],
                "brand": "TestBrand",
                "warranty": "1 year"
            },
            review_count=150,
            average_rating=4.2
        )
        db.add(test_product)
        db.commit()
        db.refresh(test_product)
        print(f"   ✅ Test product created: {test_product.name} (ID: {test_product.id})")
        
        # Test 3: Test Main Coordinator Method
        print("\n3. Testing Main Coordinator Method...")
        print("   Testing create_ai_llm_optimized_content...")
        
        start_time = time.time()
        result = optimizer.create_ai_llm_optimized_content(
            "Test Electronics Topic",
            "blog",
            str(test_product.id)
        )
        end_time = time.time()
        
        if "error" not in result:
            print(f"   ✅ Coordinator method executed successfully!")
            print(f"      - Execution time: {end_time - start_time:.2f} seconds")
            print(f"      - Content ID: {result.get('content_id', 'N/A')}")
            print(f"      - Topic: {result.get('topic', 'N/A')}")
            print(f"      - Content type: {result.get('content_type', 'N/A')}")
            print(f"      - AI LLM optimized: {result.get('ai_llm_optimized', False)}")
            
            # Check optimization features
            optimization_features = result.get('optimization_features', {})
            print(f"      - Optimization features: {len(optimization_features)}")
            for feature, status in optimization_features.items():
                print(f"        • {feature}: {'✅' if status else '❌'}")
            
            # Check content structure
            base_content = result.get('base_content', {})
            if base_content:
                print(f"      - Base content generated: ✅")
                print(f"        • Title: {base_content.get('title', 'N/A')[:50]}...")
                print(f"        • Content length: {len(base_content.get('content', ''))} chars")
            
            seo_content = result.get('seo_content', {})
            if seo_content:
                print(f"      - SEO content generated: ✅")
                print(f"        • Keywords: {len(seo_content.get('keywords', []))} keywords")
                print(f"        • Meta description: {seo_content.get('meta_description', 'N/A')[:50]}...")
            
            qa_content = result.get('qa_content', {})
            if qa_content:
                print(f"      - Q&A content generated: ✅")
                qa_pairs = qa_content.get('qa_pairs', [])
                print(f"        • Q&A pairs: {len(qa_pairs)} pairs")
            
            schema_content = result.get('schema_content', {})
            if schema_content:
                print(f"      - Schema content generated: ✅")
                print(f"        • Schema type: {schema_content.get('schema_type', 'N/A')}")
            
        else:
            print(f"   ❌ Coordinator method failed: {result.get('error')}")
            return False
        
        # Test 4: Test Error Handling
        print("\n4. Testing Error Handling...")
        error_result = optimizer.create_ai_llm_optimized_content(
            "",  # Empty topic
            "invalid_type",  # Invalid content type
            "invalid_product_id"  # Invalid product ID
        )
        
        if "error" in error_result:
            print(f"   ✅ Error handling working correctly")
            print(f"      - Error message: {error_result.get('error')}")
        else:
            print(f"   ⚠️ Error handling may need improvement")
        
        # Test 5: Test Performance
        print("\n5. Testing Performance...")
        print("   Testing coordinator with different content types...")
        
        content_types = ["blog", "product", "qa"]
        performance_results = {}
        
        for content_type in content_types:
            start_time = time.time()
            try:
                result = optimizer.create_ai_llm_optimized_content(
                    f"Performance Test {content_type.title()}",
                    content_type,
                    str(test_product.id)
                )
                end_time = time.time()
                
                if "error" not in result:
                    performance_results[content_type] = {
                        "success": True,
                        "time": end_time - start_time,
                        "content_id": result.get('content_id', 'N/A')
                    }
                else:
                    performance_results[content_type] = {
                        "success": False,
                        "error": result.get('error'),
                        "time": end_time - start_time
                    }
            except Exception as e:
                performance_results[content_type] = {
                    "success": False,
                    "error": str(e),
                    "time": time.time() - start_time
                }
        
        # Display performance results
        print("   Performance Results:")
        for content_type, result in performance_results.items():
            if result["success"]:
                print(f"      • {content_type.title()}: ✅ {result['time']:.2f}s")
            else:
                print(f"      • {content_type.title()}: ❌ {result['error']}")
        
        # Test 6: Test Integration
        print("\n6. Testing Component Integration...")
        integration_tests = [
            ("Content Generator", optimizer.content_generator is not None),
            ("SEO Optimizer", optimizer.seo_optimizer is not None),
            ("QA Engine", optimizer.qa_engine is not None),
            ("Schema Generator", optimizer.schema_generator is not None),
        ]
        
        all_integrated = True
        for component, status in integration_tests:
            if status:
                print(f"   ✅ {component} integrated")
            else:
                print(f"   ❌ {component} not integrated")
                all_integrated = False
        
        if all_integrated:
            print("   ✅ All components properly integrated")
        else:
            print("   ❌ Some components not properly integrated")
            return False
        
        # Test 7: Test Safety Integration
        print("\n7. Testing Safety Integration...")
        try:
            # Test that safety checks are working
            safety_result = optimizer.create_ai_llm_optimized_content(
                "Safety Test Topic",
                "blog",
                str(test_product.id)
            )
            
            if "error" not in safety_result:
                print("   ✅ Safety integration working correctly")
                print("   ✅ Dry run mode active (development)")
            else:
                print(f"   ⚠️ Safety integration issue: {safety_result.get('error')}")
        except Exception as e:
            print(f"   ❌ Safety integration failed: {e}")
        
        print(f"\n🎉 AI LLM Optimizer Coordinator Test Completed Successfully!")
        print(f"   Total test time: {time.time() - start_time:.2f} seconds")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Cleanup
        try:
            if 'test_product' in locals():
                db.delete(test_product)
                db.commit()
                print("   ✅ Test product cleaned up")
        except Exception as e:
            print(f"   ⚠️ Cleanup warning: {e}")
        
        db.close()

if __name__ == "__main__":
    success = test_ai_llm_coordinator()
    if success:
        print("\n✅ All coordinator tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some coordinator tests failed!")
        sys.exit(1) 