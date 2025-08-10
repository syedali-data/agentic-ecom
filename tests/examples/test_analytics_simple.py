#!/usr/bin/env python3
"""
Simple Analytics Test Script
Tests the enhanced analytics system endpoints
"""

import requests
import json
from datetime import datetime

def test_single_endpoint(endpoint, name):
    """Test a single analytics endpoint."""
    try:
        url = f"http://127.0.0.1:8000{endpoint}"
        print(f"Testing {name}...")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {name} - SUCCESS")
            print(f"   Response keys: {list(data.keys())}")
            return True
        else:
            print(f"❌ {name} - FAILED (Status: {response.status_code})")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ {name} - ERROR: {str(e)}")
        return False

def main():
    """Run all analytics tests."""
    print("🧪 Testing Enhanced Analytics System")
    print("=" * 50)
    
    # Test basic endpoints first
    endpoints = [
        ("/analytics/basic-metrics", "Basic Metrics"),
        ("/analytics/revenue-analysis", "Revenue Analysis"),
        ("/analytics/customer-insights", "Customer Insights"),
        ("/analytics/product-performance", "Product Performance"),
        ("/analytics/system-health", "System Health"),
        ("/analytics/trends/sales", "Sales Trends"),
        ("/analytics/embeddings/customer-segments", "Customer Segments"),
        ("/analytics/dashboard/kpi", "KPI Dashboard"),
        ("/analytics/reports/daily", "Daily Report"),
    ]
    
    success_count = 0
    total_count = len(endpoints)
    
    for endpoint, name in endpoints:
        if test_single_endpoint(endpoint, name):
            success_count += 1
        print()
    
    print("=" * 50)
    print(f"🎉 Test Results: {success_count}/{total_count} endpoints working")
    print(f"📅 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if success_count == total_count:
        print("✅ All analytics endpoints are working correctly!")
    else:
        print(f"⚠️  {total_count - success_count} endpoints need attention")

if __name__ == "__main__":
    main() 