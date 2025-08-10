#!/usr/bin/env python3
"""
Comprehensive AI LLM Optimizer Test
Tests all features with 120-second infinite loop detection.
"""

import sys
import os
import time
import threading
import uuid
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from db.database import SessionLocal
from content_marketing.ai_llm_optimizer import AILLMOptimizer
from db.models import Product, ProductStatus

# Global flags for loop detection
loop_detected = False
start_time = None
test_completed = False

def timeout_checker():
    """Background thread to check for timeouts."""
    global loop_detected, test_completed
    time.sleep(120)  # Wait 2 minutes
    if not test_completed:
        loop_detected = True
        print(f"\n⚠️  TIMEOUT DETECTED - Possible infinite loop!")
        print(f"   Test running for more than 120 seconds")
        print(f"   Stopping test immediately...")
        os._exit(1)

def test_ai_llm_comprehensive():
    """Comprehensive test for AI LLM Optimizer with loop detection."""
    
    global start_time, loop_detected, test_completed
    start_time = time.time()
    
    print("🔍 Comprehensive AI LLM Optimizer Test")
    print("=" * 50)
    print("⚠️  Test will stop if running longer than 120 seconds")
    print("🎯 Testing all features: blog, product, qa, comparison")
    
    # Start timeout checker thread
    timeout_thread = threading.Thread(target=timeout_checker, daemon=True)
    timeout_thread.start()
    
    # Initialize database session and optimizer
    db = SessionLocal()
    optimizer = AILLMOptimizer(db)
    
    try:
        # Test 1: Basic Initialization
        print("\n1. Testing Basic Initialization...")
        print(f"   ✅ AILLMOptimizer initialized successfully")
        print(f"   ✅ Database session: {type(db).__name__}")
        print(f"   ✅ Components loaded:")
        print(f"      • Content Generator: {type(optimizer.content_generator).__name__}")
        print(f"      • QA Engine: {type(optimizer.qa_engine).__name__}")
        print(f"      • SEO Optimizer: {type(optimizer.seo_optimizer).__name__}")
        print(f"      • Schema Generator: {type(optimizer.schema_generator).__name__}")
        print(f"      • Performance Tracker: {type(optimizer.performance_tracker).__name__}")
        
        # Test 2: Create Test Products
        print("\n2. Creating Test Products...")
        test_products = []
        
        for i in range(3):
            product = Product(
                name=f"Comprehensive Test Product {i+1}",
                description=f"Test product {i+1} for comprehensive testing",
                sku=f"COMPREHENSIVE-TEST-{i+1:03d}-{uuid.uuid4().hex[:8]}",
                category="Electronics",
                price=99.99 + (i * 50),
                status=ProductStatus.ACTIVE,
                image_url=f"https://example.com/comprehensive-test-{i+1}.jpg",
                tags=["test", "electronics", f"product-{i+1}"],
                product_metadata={
                    "features": [f"Feature {j+1}" for j in range(3)],
                    "brand": f"TestBrand{i+1}",
                    "warranty": "1 year"
                },
                review_count=50 + (i * 10),
                average_rating=4.0 + (i * 0.2)
            )
            db.add(product)
            test_products.append(product)
        
        db.commit()
        for product in test_products:
            db.refresh(product)
            print(f"   ✅ Test product created: {product.name} (ID: {product.id})")
        
        # Test 3: Test Blog Content Type
        print("\n3. Testing Blog Content Type...")
        print("   Testing create_ai_llm_optimized_content with content_type='blog'...")
        
        blog_start_time = time.time()
        
        blog_result = optimizer.create_ai_llm_optimized_content(
            "Comprehensive Blog Test Topic",
            "blog",
            str(test_products[0].id)
        )
        
        blog_end_time = time.time()
        blog_duration = blog_end_time - blog_start_time
        
        print(f"   Duration: {blog_duration:.2f} seconds")
        
        if "error" not in blog_result:
            print(f"   ✅ Blog content creation successful!")
            print(f"      - Content ID: {blog_result.get('content_id', 'N/A')}")
            print(f"      - Topic: {blog_result.get('topic', 'N/A')}")
            print(f"      - Content type: {blog_result.get('content_type', 'N/A')}")
            print(f"      - AI LLM optimized: {blog_result.get('ai_llm_optimized', False)}")
            
            # Check optimization features
            optimization_features = blog_result.get('optimization_features', {})
            print(f"      - Optimization features: {len(optimization_features)}")
            for feature, status in optimization_features.items():
                print(f"        • {feature}: {'✅' if status else '❌'}")
            
            # Check content structure
            base_content = blog_result.get('base_content', {})
            if base_content:
                print(f"      - Base content generated: ✅")
                content_length = len(base_content.get('content', ''))
                print(f"        • Content length: {content_length} chars")
            
            qa_content = blog_result.get('qa_content', {})
            if qa_content:
                qa_pairs = qa_content.get('qa_pairs', [])
                print(f"      - Q&A content generated: ✅ ({len(qa_pairs)} pairs)")
            
            schema_markup = blog_result.get('schema_markup', {})
            if schema_markup:
                print(f"      - Schema markup generated: ✅")
        else:
            print(f"   ❌ Blog content creation failed: {blog_result.get('error')}")
            return False
        
        # Test 4: Test Q&A Content Type
        print("\n4. Testing Q&A Content Type...")
        print("   Testing create_ai_llm_optimized_content with content_type='qa'...")
        
        qa_start_time = time.time()
        
        qa_result = optimizer.create_ai_llm_optimized_content(
            "Comprehensive Q&A Test Topic",
            "qa",
            str(test_products[1].id)
        )
        
        qa_end_time = time.time()
        qa_duration = qa_end_time - qa_start_time
        
        print(f"   Duration: {qa_duration:.2f} seconds")
        
        if "error" not in qa_result:
            print(f"   ✅ Q&A content creation successful!")
            print(f"      - Content ID: {qa_result.get('content_id', 'N/A')}")
            print(f"      - Topic: {qa_result.get('topic', 'N/A')}")
            print(f"      - Content type: {qa_result.get('content_type', 'N/A')}")
            
            # Check if Q&A content matches base content (should be for qa type)
            base_content = qa_result.get('base_content', {})
            qa_content = qa_result.get('qa_content', {})
            if base_content == qa_content:
                print(f"      - ✅ Q&A content matches base content (correct)")
            else:
                print(f"      - ⚠️ Q&A content differs from base content")
            
            qa_pairs = qa_content.get('qa_pairs', [])
            print(f"      - Q&A pairs generated: {len(qa_pairs)} pairs")
        else:
            print(f"   ❌ Q&A content creation failed: {qa_result.get('error')}")
            return False
        
        # Test 5: Test Product Content Type
        print("\n5. Testing Product Content Type...")
        print("   Testing create_ai_llm_optimized_content with content_type='product'...")
        
        product_start_time = time.time()
        
        product_result = optimizer.create_ai_llm_optimized_content(
            "Comprehensive Product Test",
            "product",
            str(test_products[2].id)
        )
        
        product_end_time = time.time()
        product_duration = product_end_time - product_start_time
        
        print(f"   Duration: {product_duration:.2f} seconds")
        
        if "error" not in product_result:
            print(f"   ✅ Product content creation successful!")
            print(f"      - Content ID: {product_result.get('content_id', 'N/A')}")
            print(f"      - Content type: {product_result.get('content_type', 'N/A')}")
            
            base_content = product_result.get('base_content', {})
            if base_content:
                print(f"      - Base content generated: ✅")
                content_length = len(base_content.get('content', ''))
                print(f"        • Content length: {content_length} chars")
        else:
            print(f"   ❌ Product content creation failed: {product_result.get('error')}")
            return False
        
        # Test 6: Test Product Comparison Package
        print("\n6. Testing Product Comparison Package...")
        print("   Testing generate_product_comparison_package...")
        
        comparison_start_time = time.time()
        
        comparison_result = optimizer.generate_product_comparison_package(
            [str(p.id) for p in test_products]
        )
        
        comparison_end_time = time.time()
        comparison_duration = comparison_end_time - comparison_start_time
        
        print(f"   Duration: {comparison_duration:.2f} seconds")
        
        if "error" not in comparison_result:
            print(f"   ✅ Product comparison creation successful!")
            print(f"      - Comparison ID: {comparison_result.get('comparison_id', 'N/A')}")
            print(f"      - Products compared: {len(comparison_result.get('products', []))}")
            
            comparison_content = comparison_result.get('comparison_content', {})
            if comparison_content:
                print(f"      - Comparison content generated: ✅")
            
            comparison_qa = comparison_result.get('comparison_qa', {})
            if comparison_qa:
                qa_pairs = comparison_qa.get('qa_pairs', [])
                print(f"      - Comparison Q&A: {len(qa_pairs)} pairs")
        else:
            print(f"   ❌ Product comparison creation failed: {comparison_result.get('error')}")
            return False
        
        # Test 7: Test Content Calendar
        print("\n7. Testing Content Calendar...")
        print("   Testing create_ai_llm_content_calendar...")
        
        calendar_start_time = time.time()
        
        calendar_result = optimizer.create_ai_llm_content_calendar(days=7)
        
        calendar_end_time = time.time()
        calendar_duration = calendar_end_time - calendar_start_time
        
        print(f"   Duration: {calendar_duration:.2f} seconds")
        
        if "error" not in calendar_result:
            print(f"   ✅ Content calendar creation successful!")
            content_ideas = calendar_result.get('content_calendar', [])
            print(f"      - Content ideas generated: {len(content_ideas)}")
            print(f"      - Days covered: {calendar_result.get('days_covered', 'N/A')}")
        else:
            print(f"   ❌ Content calendar creation failed: {calendar_result.get('error')}")
            return False
        
        # Test 8: Test Optimization Report
        print("\n8. Testing Optimization Report...")
        print("   Testing get_ai_llm_optimization_report...")
        
        report_start_time = time.time()
        
        report_result = optimizer.get_ai_llm_optimization_report(days=7)
        
        report_end_time = time.time()
        report_duration = report_end_time - report_start_time
        
        print(f"   Duration: {report_duration:.2f} seconds")
        
        if "error" not in report_result:
            print(f"   ✅ Optimization report generation successful!")
            print(f"      - Analysis period: {report_result.get('analysis_period', 'N/A')}")
            
            recommendations = report_result.get('recommendations', [])
            print(f"      - Recommendations generated: {len(recommendations)}")
        else:
            print(f"   ❌ Optimization report generation failed: {report_result.get('error')}")
            return False
        
        # Test 9: Test Content Summary
        print("\n9. Testing Content Summary...")
        print("   Testing get_ai_llm_content_summary...")
        
        summary_start_time = time.time()
        
        summary_result = optimizer.get_ai_llm_content_summary()
        
        summary_end_time = time.time()
        summary_duration = summary_end_time - summary_start_time
        
        print(f"   Duration: {summary_duration:.2f} seconds")
        
        if "error" not in summary_result:
            print(f"   ✅ Content summary generation successful!")
            summary = summary_result.get('summary', {})
            print(f"      - Total content: {summary.get('total_content', 'N/A')}")
            print(f"      - Total mentions: {summary.get('total_mentions', 'N/A')}")
            print(f"      - Active apps: {summary.get('active_apps', 'N/A')}")
        else:
            print(f"   ❌ Content summary generation failed: {summary_result.get('error')}")
            return False
        
        # Test 10: Check for Loops and Performance
        print("\n10. Checking for Loops and Performance...")
        
        total_duration = time.time() - start_time
        print(f"   Total test duration: {total_duration:.2f} seconds")
        
        if total_duration > 120:
            print(f"   ⚠️  WARNING: Total test duration is {total_duration:.2f} seconds")
            print(f"      This might indicate a loop")
        else:
            print(f"   ✅ Total test duration within acceptable limits")
        
        # Test 11: Final Loop Check
        print("\n11. Final Loop Detection Check...")
        
        if loop_detected:
            print("   ❌ INFINITE LOOP DETECTED!")
            print("   Stopping test immediately...")
            return False
        else:
            print("   ✅ No infinite loops detected")
            print("   ✅ All comprehensive tests passed")
        
        print(f"\n🎉 Comprehensive AI LLM Optimizer Test Completed Successfully!")
        print(f"   Total test time: {time.time() - start_time:.2f} seconds")
        print(f"   Features tested: 9")
        print(f"   Content types: blog, qa, product, comparison")
        print(f"   Additional features: calendar, report, summary")
        
        test_completed = True
        return True
        
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Cleanup
        try:
            if 'test_products' in locals():
                for product in test_products:
                    db.delete(product)
                db.commit()
                print("   ✅ Test products cleaned up")
        except Exception as e:
            print(f"   ⚠️ Cleanup warning: {e}")
        
        test_completed = True
        db.close()

if __name__ == "__main__":
    success = test_ai_llm_comprehensive()
    if success:
        print("\n✅ All comprehensive tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some comprehensive tests failed!")
        sys.exit(1) 