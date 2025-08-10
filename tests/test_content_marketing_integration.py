"""
Integration Tests for Content Marketing System

This test suite covers:
1. Complete content generation workflows
2. AI LLM optimization pipelines
3. End-to-end content marketing processes
4. Multi-component integration scenarios
5. Performance tracking integration
6. Schema markup generation workflows
7. Q&A content generation workflows
8. Product comparison workflows
9. Content calendar generation
10. Error handling in integrated workflows

These tests ensure that all components work together seamlessly
and that the complete content marketing pipeline functions correctly.
"""

import sys
import os
import unittest
import json
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from typing import Dict, Any, List

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from content_marketing.ai_llm_optimizer import AILLMOptimizer
from content_marketing.generator import ContentGenerator
from content_marketing.seo_optimizer import SEOOptimizer
from content_marketing.qa_engine import QAEngine
from content_marketing.schema_markup import SchemaMarkupGenerator
from content_marketing.performance_tracker import ContentPerformanceTracker
from db.models import Product, ProductStatus


class TestContentMarketingIntegration(unittest.TestCase):
    """Integration tests for complete content marketing workflows"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_db = Mock()
        self.ai_llm_optimizer = AILLMOptimizer(self.mock_db)

        # Create mock products for testing
        self.mock_product1 = Mock(spec=Product)
        self.mock_product1.id = "test_product_1"
        self.mock_product1.name = "Test Product 1"
        self.mock_product1.description = "A test product for integration testing"
        self.mock_product1.price = 99.99
        self.mock_product1.category = "ELECTRONICS"
        self.mock_product1.status = ProductStatus.ACTIVE
        self.mock_product1.product_metadata = {"features": ["Feature 1", "Feature 2"]}

        self.mock_product2 = Mock(spec=Product)
        self.mock_product2.id = "test_product_2"
        self.mock_product2.name = "Test Product 2"
        self.mock_product2.description = "Another test product for integration testing"
        self.mock_product2.price = 149.99
        self.mock_product2.category = "ELECTRONICS"
        self.mock_product2.status = ProductStatus.ACTIVE
        self.mock_product2.product_metadata = {"features": ["Feature 3", "Feature 4"]}

        # Set up mock database queries
        self.mock_db.query.return_value.filter.return_value.first.return_value = self.mock_product1
        self.mock_db.query.return_value.filter.return_value.all.return_value = [
            self.mock_product1, self.mock_product2
        ]

    def test_complete_blog_content_workflow(self):
        """Test complete blog content generation workflow"""
        print("\n🧪 Testing Complete Blog Content Workflow...")

        # ... (unchanged, as before)

    def test_complete_product_content_workflow(self):
        """Test complete product content generation workflow"""
        print("\n🧪 Testing Complete Product Content Workflow...")

        # ... (unchanged, as before)

    def test_content_calendar_generation_workflow(self):
        """Test content calendar generation workflow"""
        print("\n🧪 Testing Content Calendar Generation Workflow...")

        # ... (unchanged, as before)

    def test_complete_qa_content_workflow(self):
        """Test complete Q&A content generation workflow"""
        print("\n🧪 Testing Complete Q&A Content Workflow...")

        # ... (unchanged, as before)

    def test_product_comparison_workflow(self):
        """Test complete product comparison workflow"""
        print("\n🧪 Testing Complete Product Comparison Workflow...")

        # Use products from setUp
        mock_product1 = self.mock_product1
        mock_product2 = self.mock_product2

        # Mock the comparison content generation
        with patch.object(self.ai_llm_optimizer.content_generator, 'generate_comparison_content') as mock_generate:
            mock_generate.return_value = {
                "title": "Product Comparison",
                "content": "This is a comprehensive product comparison for integration testing.",
                "comparison": "Detailed comparison of products",
                "products": ["test_product_1", "test_product_2"],
                "ai_llm_optimized": False,
                "generated_at": datetime.now().isoformat()
            }

            # Mock the comparison Q&A generation
            with patch.object(self.ai_llm_optimizer.qa_engine, 'generate_comparison_qa') as mock_qa:
                mock_qa.return_value = {
                    "products": ["test_product_1", "test_product_2"],
                    "qa_pairs": [
                        {"question": "Which is better?", "answer": "Depends on your needs"},
                        {"question": "What are the differences?", "answer": "Price and features"}
                    ],
                    "ai_llm_optimized": True,
                    "generated_at": datetime.now().isoformat()
                }

                # Mock the schema generation
                with patch.object(self.ai_llm_optimizer.schema_generator, 'generate_comparison_schema') as mock_schema:
                    mock_schema.return_value = {
                        "comparison_id": "test_comparison",
                        "schema": {
                            "@context": "https://schema.org",
                            "@type": "ComparisonChart",
                            "name": "Product Comparison"
                        },
                        "generated_at": datetime.now().isoformat()
                    }

                    # Mock the SEO optimization
                    with patch.object(self.ai_llm_optimizer.seo_optimizer, 'optimize_for_ai_llm') as mock_optimize:
                        mock_optimize.return_value = {
                            "optimized_content": "Optimized comparison content",
                            "optimized_title": "Optimized Product Comparison",
                            "ai_llm_optimized": True
                        }

                        # Mock the database query for products - this is the key fix
                        with patch.object(self.ai_llm_optimizer.db, 'query') as mock_query:
                            # Create a mock that properly simulates the SQLAlchemy query chain
                            # The chain is: db.query(Product).filter(Product.id.in_(product_ids)).all()
                            
                            # Create mock products
                            mock_products = [mock_product1, mock_product2]
                            
                            # Set up the mock chain properly
                            # The chain is: query(Product).filter(Product.id.in_(product_ids)).all()
                            mock_filter_result = Mock()
                            mock_filter_result.all.return_value = mock_products
                            
                            mock_query.return_value.filter.return_value = mock_filter_result

                            # Execute the workflow
                            result = self.ai_llm_optimizer.generate_product_comparison_package([
                                "test_product_1", "test_product_2"
                            ])

                            # Assertions
                            self.assertNotIn("error", result)
                            self.assertIn("comparison_id", result)
                            self.assertIn("comparison_content", result)
                            self.assertIn("comparison_qa", result)
                            self.assertIn("comparison_schema", result)
                            self.assertTrue(result["ai_llm_optimized"])

                            print("✅ Complete product comparison workflow test passed")

    def test_performance_tracking_integration(self):
        """Test performance tracking integration"""
        print("\n🧪 Testing Performance Tracking Integration...")

        # ... (unchanged, as before)

    def test_schema_markup_integration(self):
        """Test schema markup integration"""
        print("\n🧪 Testing Schema Markup Integration...")

        # ... (unchanged, as before)

    def test_error_handling_in_integrated_workflow(self):
        """Test error handling in integrated workflows"""
        print("\n🧪 Testing Error Handling in Integrated Workflows...")

        # ... (unchanged, as before)

    def test_multi_component_integration(self):
        """Test multi-component integration scenarios"""
        print("\n🧪 Testing Multi-Component Integration...")

        # ... (unchanged, as before)


class TestContentMarketingEndToEnd(unittest.TestCase):
    """End-to-end tests for complete content marketing processes"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_db = Mock()
        self.ai_llm_optimizer = AILLMOptimizer(self.mock_db)

    def test_end_to_end_content_marketing_pipeline(self):
        """Test complete end-to-end content marketing pipeline"""
        print("\n🧪 Testing End-to-End Content Marketing Pipeline...")

        # ... (unchanged, as before)

    def test_content_optimization_workflow(self):
        """Test content optimization workflow"""
        print("\n🧪 Testing Content Optimization Workflow...")

        # ... (unchanged, as before)


if __name__ == "__main__":
    # Run the integration tests
    print("🚀 Starting Content Marketing Integration Tests...")
    unittest.main(verbosity=2)
