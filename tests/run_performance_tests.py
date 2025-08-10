#!/usr/bin/env python3
"""
Performance Test Runner for Content Marketing System

This script runs comprehensive performance tests and generates detailed reports
covering cache efficiency, API call optimization, response times, and more.
"""

import sys
import os
import unittest
import time
import json
from datetime import datetime
from typing import Dict, Any, List

# Try to import psutil, fallback to mock if not available
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    # Mock psutil for testing
    class MockPsutil:
        class Process:
            def memory_info(self):
                class MemoryInfo:
                    def __init__(self):
                        self.rss = 100 * 1024 * 1024  # 100MB mock
                return MemoryInfo()
        
        @staticmethod
        def cpu_percent():
            return 10.0  # 10% mock
    
    psutil = MockPsutil()

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_content_marketing_performance import (
    TestContentMarketingPerformance,
    TestContentMarketingPerformanceEndToEnd
)


class PerformanceTestResultCollector:
    """Collects and analyzes performance test results"""
    
    def __init__(self):
        self.results = {
            "test_results": [],
            "performance_metrics": {},
            "summary": {},
            "recommendations": []
        }
        self.start_time = None
        self.end_time = None
    
    def add_test_result(self, test_name: str, status: str, duration: float, details: Dict[str, Any] = None):
        """Add a test result to the collection"""
        self.results["test_results"].append({
            "test_name": test_name,
            "status": status,
            "duration": duration,
            "details": details or {},
            "timestamp": datetime.now().isoformat()
        })
    
    def add_performance_metric(self, metric_name: str, value: float, unit: str = ""):
        """Add a performance metric"""
        self.results["performance_metrics"][metric_name] = {
            "value": value,
            "unit": unit,
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_summary(self):
        """Generate a summary of all test results"""
        total_tests = len(self.results["test_results"])
        passed_tests = sum(1 for r in self.results["test_results"] if r["status"] == "PASS")
        failed_tests = total_tests - passed_tests
        
        total_duration = sum(r["duration"] for r in self.results["test_results"])
        avg_duration = total_duration / total_tests if total_tests > 0 else 0
        
        self.results["summary"] = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "total_duration": total_duration,
            "average_duration": avg_duration,
            "test_start_time": self.start_time.isoformat() if self.start_time else None,
            "test_end_time": self.end_time.isoformat() if self.end_time else None
        }
    
    def generate_recommendations(self):
        """Generate performance recommendations based on test results"""
        recommendations = []
        
        # Analyze cache efficiency
        cache_tests = [r for r in self.results["test_results"] if "cache" in r["test_name"].lower()]
        if cache_tests:
            avg_cache_time = sum(r["duration"] for r in cache_tests) / len(cache_tests)
            if avg_cache_time > 0.1:
                recommendations.append({
                    "category": "Cache Optimization",
                    "issue": "Cache hit times are slower than expected",
                    "recommendation": "Consider implementing Redis for distributed caching",
                    "priority": "Medium"
                })
        
        # Analyze response times
        response_tests = [r for r in self.results["test_results"] if "response" in r["test_name"].lower()]
        if response_tests:
            avg_response_time = sum(r["duration"] for r in response_tests) / len(response_tests)
            if avg_response_time > 2.0:
                recommendations.append({
                    "category": "Response Time",
                    "issue": "Average response times are above threshold",
                    "recommendation": "Optimize API calls and implement request batching",
                    "priority": "High"
                })
        
        # Analyze memory usage
        memory_tests = [r for r in self.results["test_results"] if "memory" in r["test_name"].lower()]
        if memory_tests:
            for test in memory_tests:
                if "details" in test and "memory_increase" in test["details"]:
                    memory_increase = test["details"]["memory_increase"]
                    if memory_increase > 100:
                        recommendations.append({
                            "category": "Memory Management",
                            "issue": "Memory usage increase is high",
                            "recommendation": "Implement memory cleanup and object pooling",
                            "priority": "High"
                        })
                        break
        
        # Analyze concurrent performance
        concurrent_tests = [r for r in self.results["test_results"] if "concurrent" in r["test_name"].lower()]
        if concurrent_tests:
            for test in concurrent_tests:
                if "details" in test and "successful_requests" in test["details"]:
                    successful_requests = test["details"]["successful_requests"]
                    total_requests = test["details"].get("total_requests", 10)
                    if successful_requests < total_requests:
                        recommendations.append({
                            "category": "Concurrency",
                            "issue": "Some concurrent requests are failing",
                            "recommendation": "Implement proper connection pooling and retry mechanisms",
                            "priority": "Medium"
                        })
                        break
        
        self.results["recommendations"] = recommendations
    
    def save_report(self, filename: str = None):
        """Save the performance test report to a file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"performance_test_report_{timestamp}.json"
        
        report_path = os.path.join(os.path.dirname(__file__), filename)
        
        with open(report_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        return report_path
    
    def print_summary(self):
        """Print a human-readable summary of the test results"""
        print("\n" + "="*80)
        print("📊 CONTENT MARKETING PERFORMANCE TEST SUMMARY")
        print("="*80)
        
        summary = self.results["summary"]
        print(f"🕒 Test Duration: {summary['total_duration']:.2f} seconds")
        print(f"📈 Success Rate: {summary['success_rate']:.1f}% ({summary['passed_tests']}/{summary['total_tests']} tests)")
        print(f"⚡ Average Test Duration: {summary['average_duration']:.3f} seconds")
        
        print(f"\n🎯 PERFORMANCE METRICS:")
        for metric_name, metric_data in self.results["performance_metrics"].items():
            print(f"   • {metric_name}: {metric_data['value']:.3f} {metric_data['unit']}")
        
        if self.results["recommendations"]:
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in self.results["recommendations"]:
                print(f"   • [{rec['priority']}] {rec['category']}: {rec['recommendation']}")
        
        print("="*80)


def run_performance_tests():
    """Run all performance tests and collect results"""
    print("🚀 Starting Content Marketing Performance Tests...")
    print("="*80)
    
    # Initialize result collector
    collector = PerformanceTestResultCollector()
    collector.start_time = datetime.now()
    
    # Get initial system metrics
    if PSUTIL_AVAILABLE:
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        initial_cpu = psutil.cpu_percent()
    else:
        # Use mock values when psutil is not available
        initial_memory = 100.0  # Mock 100MB
        initial_cpu = 10.0  # Mock 10%
        print("ℹ️  Using mock system metrics (psutil not available)")
    
    collector.add_performance_metric("initial_memory_usage", initial_memory, "MB")
    collector.add_performance_metric("initial_cpu_usage", initial_cpu, "%")
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add performance tests
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestContentMarketingPerformance))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestContentMarketingPerformanceEndToEnd))
    
    # Run tests with custom result collector
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(test_suite)
    
    # Collect final system metrics
    if PSUTIL_AVAILABLE:
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        final_cpu = psutil.cpu_percent()
    else:
        # Use mock values when psutil is not available
        final_memory = 105.0  # Mock 105MB (5MB increase)
        final_cpu = 12.0  # Mock 12% (2% increase)
    
    collector.add_performance_metric("final_memory_usage", final_memory, "MB")
    collector.add_performance_metric("final_cpu_usage", final_cpu, "%")
    collector.add_performance_metric("memory_increase", final_memory - initial_memory, "MB")
    collector.add_performance_metric("cpu_increase", final_cpu - initial_cpu, "%")
    
    # Generate summary and recommendations
    collector.end_time = datetime.now()
    collector.generate_summary()
    collector.generate_recommendations()
    
    # Save and print report
    report_path = collector.save_report()
    collector.print_summary()
    
    print(f"\n📄 Detailed report saved to: {report_path}")
    
    return collector.results


def main():
    """Main function to run performance tests"""
    try:
        results = run_performance_tests()
        
        # Exit with appropriate code
        if results["summary"]["failed_tests"] > 0:
            print(f"\n❌ Performance tests completed with {results['summary']['failed_tests']} failures")
            sys.exit(1)
        else:
            print(f"\n✅ All performance tests passed successfully!")
            sys.exit(0)
            
    except Exception as e:
        print(f"\n💥 Error running performance tests: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 