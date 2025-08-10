#!/usr/bin/env python3
"""
Integration Test Runner for Content Marketing System

This script runs comprehensive integration tests to verify that all
content marketing components work together seamlessly.
"""

import sys
import os
import unittest
from datetime import datetime

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_integration_tests():
    """Run all integration tests"""
    print("🚀 Starting Content Marketing Integration Tests...")
    print("=" * 60)
    
    # Import the integration test module
    from test_content_marketing_integration import (
        TestContentMarketingIntegration,
        TestContentMarketingEndToEnd
    )
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add integration tests
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestContentMarketingIntegration))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestContentMarketingEndToEnd))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 Integration Test Results Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print("\n⚠️ Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('Exception:')[-1].strip()}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1) 