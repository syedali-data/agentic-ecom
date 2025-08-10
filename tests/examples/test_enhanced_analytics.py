#!/usr/bin/env python3
"""
Enhanced Analytics System Test Script
Tests all analytics endpoints and functionality.
"""

import requests
import json
from datetime import datetime

def test_analytics_endpoints():
    """Test all analytics endpoints."""
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 Testing Enhanced Analytics System")
    print("=" * 50)
    
    # Test basic metrics
    print("\n1. Testing Basic Metrics...")
    try:
        response = requests.get(f"{base_url}/analytics/basic-metrics")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Basic Metrics: {data.get('products', {}).get('total', 0)} products, ${data.get('orders', {}).get('revenue', 0)} revenue")
        else:
            print(f"❌ Basic Metrics failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Basic Metrics error: {e}")
    
    # Test revenue analysis
    print("\n2. Testing Revenue Analysis...")
    try:
        response = requests.get(f"{base_url}/analytics/revenue-analysis?days=30")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Revenue Analysis: {len(data.get('daily_revenue', []))} days of data")
        else:
            print(f"❌ Revenue Analysis failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Revenue Analysis error: {e}")
    
    # Test customer insights
    print("\n3. Testing Customer Insights...")
    try:
        response = requests.get(f"{base_url}/analytics/customer-insights")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Customer Insights: {len(data.get('top_customers', []))} top customers")
        else:
            print(f"❌ Customer Insights failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Customer Insights error: {e}")
    
    # Test product performance
    print("\n4. Testing Product Performance...")
    try:
        response = requests.get(f"{base_url}/analytics/product-performance")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Product Performance: {len(data.get('top_products', []))} top products")
        else:
            print(f"❌ Product Performance failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Product Performance error: {e}")
    
    # Test KPI dashboard
    print("\n5. Testing KPI Dashboard...")
    try:
        response = requests.get(f"{base_url}/analytics/dashboard/kpi")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ KPI Dashboard: {len(data.get('kpis', {}))} KPIs generated")
        else:
            print(f"❌ KPI Dashboard failed: {response.status_code}")
    except Exception as e:
        print(f"❌ KPI Dashboard error: {e}")
    
    # Test daily report
    print("\n6. Testing Daily Report...")
    try:
        response = requests.get(f"{base_url}/analytics/reports/daily")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Daily Report: {data.get('report_type')} report generated")
        else:
            print(f"❌ Daily Report failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Daily Report error: {e}")
    
    # Test trends analysis
    print("\n7. Testing Sales Trends...")
    try:
        response = requests.get(f"{base_url}/analytics/trends/sales?days=30")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Sales Trends: {data.get('trend_analysis', {}).get('direction', 'unknown')} trend")
        else:
            print(f"❌ Sales Trends failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Sales Trends error: {e}")
    
    # Test forecasting
    print("\n8. Testing Revenue Forecasting...")
    try:
        response = requests.get(f"{base_url}/analytics/forecast/revenue?days=30")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Revenue Forecast: ${data.get('total_forecasted_revenue', 0)} forecasted")
        else:
            print(f"❌ Revenue Forecast failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Revenue Forecast error: {e}")
    
    # Test comprehensive analytics
    print("\n9. Testing Comprehensive Analytics...")
    try:
        response = requests.get(f"{base_url}/analytics/comprehensive")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Comprehensive Analytics: All modules working")
        else:
            print(f"❌ Comprehensive Analytics failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Comprehensive Analytics error: {e}")
    
    # Test embeddings
    print("\n10. Testing Embeddings...")
    try:
        response = requests.get(f"{base_url}/analytics/embeddings/customer-segments")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Customer Segments: {len(data)} segments analyzed")
        else:
            print(f"❌ Customer Segments failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Customer Segments error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Enhanced Analytics System Test Complete!")
    print(f"📅 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    test_analytics_endpoints() 