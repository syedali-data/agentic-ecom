#!/usr/bin/env python3
"""
Content Marketing Unit Test Runner

This script runs all unit tests for the content marketing modules and provides
detailed reporting on test results, including:
- Test coverage
- Error details
- Performance metrics
- Summary statistics
"""

import sys
import os
import unittest
import time
import json
from datetime import datetime
from typing import Dict, List, Any

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the test modules
from test_content_marketing_unit import (
    TestContentGenerator,
    TestSEOOptimizer,
    TestQAEngine,
    TestSchemaMarkupGenerator,
    TestContentPerformanceTracker,
    TestAILLMOptimizer
)


class TestResultCollector:
    """Collects and formats test results"""
    
    def __init__(self):
        self.results = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "error_tests": 0,
            "skipped_tests": 0,
            "test_details": [],
            "start_time": None,
            "end_time": None,
            "duration": 0
        }
    
    def collect_results(self, test_result: unittest.TestResult):
        """Collect results from a test run"""
        self.results["total_tests"] = test_result.testsRun
        self.results["failed_tests"] = len(test_result.failures)
        self.results["error_tests"] = len(test_result.errors)
        self.results["skipped_tests"] = len(test_result.skipped) if hasattr(test_result, 'skipped') else 0
        self.results["passed_tests"] = self.results["total_tests"] - self.results["failed_tests"] - self.results["error_tests"] - self.results["skipped_tests"]
        
        # Collect failure details
        for test, traceback in test_result.failures:
            self.results["test_details"].append({
                "test_name": str(test),
                "status": "FAILED",
                "error": traceback,
                "type": "failure"
            })
        
        # Collect error details
        for test, traceback in test_result.errors:
            self.results["test_details"].append({
                "test_name": str(test),
                "status": "ERROR",
                "error": traceback,
                "type": "error"
            })
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate a comprehensive test report"""
        if self.results["total_tests"] > 0:
            success_rate = (self.results["passed_tests"] / self.results["total_tests"]) * 100
        else:
            success_rate = 0
        
        report = {
            "summary": {
                "total_tests": self.results["total_tests"],
                "passed_tests": self.results["passed_tests"],
                "failed_tests": self.results["failed_tests"],
                "error_tests": self.results["error_tests"],
                "skipped_tests": self.results["skipped_tests"],
                "success_rate": round(success_rate, 2),
                "duration_seconds": round(self.results["duration"], 2)
            },
            "test_details": self.results["test_details"],
            "timestamp": datetime.now().isoformat(),
            "test_suites": [
                "TestContentGenerator",
                "TestSEOOptimizer", 
                "TestQAEngine",
                "TestSchemaMarkupGenerator",
                "TestContentPerformanceTracker",
                "TestAILLMOptimizer"
            ]
        }
        
        return report


def run_unit_tests() -> Dict[str, Any]:
    """Run all unit tests and return results"""
    print("🚀 Starting Content Marketing Unit Tests...")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestContentGenerator,
        TestSEOOptimizer,
        TestQAEngine,
        TestSchemaMarkupGenerator,
        TestContentPerformanceTracker,
        TestAILLMOptimizer
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Create result collector
    collector = TestResultCollector()
    collector.results["start_time"] = datetime.now()
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    start_time = time.time()
    
    try:
        test_result = runner.run(test_suite)
        end_time = time.time()
        
        # Collect results
        collector.results["end_time"] = datetime.now()
        collector.results["duration"] = end_time - start_time
        collector.collect_results(test_result)
        
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        collector.results["error_tests"] += 1
        collector.results["test_details"].append({
            "test_name": "TestRunner",
            "status": "ERROR",
            "error": str(e),
            "type": "runner_error"
        })
    
    return collector.generate_report()


def print_report(report: Dict[str, Any]):
    """Print a formatted test report"""
    print("\n" + "=" * 60)
    print("📊 CONTENT MARKETING UNIT TEST REPORT")
    print("=" * 60)
    
    summary = report["summary"]
    
    # Print summary
    print(f"\n📈 SUMMARY:")
    print(f"   Total Tests: {summary['total_tests']}")
    print(f"   Passed: {summary['passed_tests']} ✅")
    print(f"   Failed: {summary['failed_tests']} ❌")
    print(f"   Errors: {summary['error_tests']} ⚠️")
    print(f"   Skipped: {summary['skipped_tests']} ⏭️")
    print(f"   Success Rate: {summary['success_rate']}%")
    print(f"   Duration: {summary['duration_seconds']}s")
    
    # Print test details if there are failures or errors
    if report["test_details"]:
        print(f"\n🔍 DETAILED RESULTS:")
        for detail in report["test_details"]:
            print(f"\n   {detail['status']}: {detail['test_name']}")
            if detail['error']:
                # Truncate long error messages
                error_msg = detail['error'][:200] + "..." if len(detail['error']) > 200 else detail['error']
                print(f"      Error: {error_msg}")
    
    # Print recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    if summary['success_rate'] == 100:
        print("   🎉 All tests passed! The content marketing system is working correctly.")
    elif summary['success_rate'] >= 90:
        print("   ✅ Most tests passed. Review the failed tests for minor issues.")
    elif summary['success_rate'] >= 70:
        print("   ⚠️  Several tests failed. Review the error details and fix issues.")
    else:
        print("   ❌ Many tests failed. Significant issues need to be addressed.")
    
    print("\n" + "=" * 60)


def save_report(report: Dict[str, Any], filename: str = None):
    """Save test report to a JSON file"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"content_marketing_unit_test_report_{timestamp}.json"
    
    # Ensure the tests/results directory exists
    results_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(results_dir, exist_ok=True)
    
    filepath = os.path.join(results_dir, filename)
    
    try:
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        print(f"\n💾 Test report saved to: {filepath}")
    except Exception as e:
        print(f"\n⚠️  Could not save test report: {e}")


def main():
    """Main function to run the unit tests"""
    try:
        # Run tests
        report = run_unit_tests()
        
        # Print report
        print_report(report)
        
        # Save report
        save_report(report)
        
        # Exit with appropriate code
        if report["summary"]["success_rate"] == 100:
            print("\n🎉 All tests passed successfully!")
            sys.exit(0)
        elif report["summary"]["success_rate"] >= 90:
            print("\n✅ Tests completed with minor issues.")
            sys.exit(0)
        else:
            print("\n❌ Tests completed with significant issues.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Test execution interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error during test execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 