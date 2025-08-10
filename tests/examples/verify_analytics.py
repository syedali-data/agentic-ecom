#!/usr/bin/env python3
"""
Analytics Verification Script
Tests the enhanced analytics system modules directly
"""

import sys
import traceback
from datetime import datetime

def test_imports():
    """Test if all analytics modules can be imported."""
    print("🔍 Testing Analytics Module Imports...")
    
    try:
        from analytics import AnalyticsEngine, EmbeddingService, TrendAnalyzer, ForecastingEngine, DashboardService, ReportGenerator
        print("✅ All analytics modules imported successfully")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        traceback.print_exc()
        return False

def test_analytics_engine():
    """Test AnalyticsEngine class."""
    print("\n🔍 Testing AnalyticsEngine...")
    
    try:
        from analytics.engine import AnalyticsEngine
        from db.database import get_db
        
        # Get a database session
        db = next(get_db())
        
        # Create analytics engine
        engine = AnalyticsEngine(db)
        print("✅ AnalyticsEngine created successfully")
        
        # Test basic metrics
        metrics = engine.get_basic_metrics()
        print(f"✅ Basic metrics generated: {list(metrics.keys())}")
        
        # Test revenue analysis
        revenue = engine.get_revenue_analysis(days=7)
        print(f"✅ Revenue analysis generated: {list(revenue.keys())}")
        
        # Test customer insights
        insights = engine.get_customer_insights()
        print(f"✅ Customer insights generated: {list(insights.keys())}")
        
        # Test product performance
        performance = engine.get_product_performance()
        print(f"✅ Product performance generated: {list(performance.keys())}")
        
        # Test system health
        health = engine.get_system_health_metrics()
        print(f"✅ System health generated: {list(health.keys())}")
        
        # Test comprehensive report
        report = engine.generate_comprehensive_report()
        print(f"✅ Comprehensive report generated: {list(report.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ AnalyticsEngine test failed: {e}")
        traceback.print_exc()
        return False

def test_embedding_service():
    """Test EmbeddingService class."""
    print("\n🔍 Testing EmbeddingService...")
    
    try:
        from analytics.embeddings import EmbeddingService
        from db.database import get_db
        
        # Get a database session
        db = next(get_db())
        
        # Create embedding service
        service = EmbeddingService(db)
        print("✅ EmbeddingService created successfully")
        
        # Test embedding generation
        embedding = service.generate_embedding("test product description")
        print(f"✅ Embedding generated: {len(embedding)} dimensions")
        
        # Test similarity calculation
        similarity = service.get_similarity("product A", "product B")
        print(f"✅ Similarity calculated: {similarity}")
        
        # Test batch embedding
        embeddings = service.batch_embed(["text1", "text2", "text3"])
        print(f"✅ Batch embeddings generated: {len(embeddings)}")
        
        # Test similar products
        similar = service.find_similar_products("test_product", limit=3)
        print(f"✅ Similar products found: {len(similar)}")
        
        # Test recommendations
        recommendations = service.get_product_recommendations("test_customer", limit=3)
        print(f"✅ Recommendations generated: {len(recommendations)}")
        
        # Test customer segments
        segments = service.analyze_customer_segments()
        print(f"✅ Customer segments analyzed: {list(segments.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ EmbeddingService test failed: {e}")
        traceback.print_exc()
        return False

def test_trend_analyzer():
    """Test TrendAnalyzer class."""
    print("\n🔍 Testing TrendAnalyzer...")
    
    try:
        from analytics.trends import TrendAnalyzer
        from db.database import get_db
        
        # Get a database session
        db = next(get_db())
        
        # Create trend analyzer
        analyzer = TrendAnalyzer(db)
        print("✅ TrendAnalyzer created successfully")
        
        # Test sales trends
        sales_trends = analyzer.analyze_sales_trends(days=7)
        print(f"✅ Sales trends analyzed: {list(sales_trends.keys())}")
        
        # Test product trends
        product_trends = analyzer.analyze_product_trends()
        print(f"✅ Product trends analyzed: {list(product_trends.keys())}")
        
        # Test customer trends
        customer_trends = analyzer.analyze_customer_trends()
        print(f"✅ Customer trends analyzed: {list(customer_trends.keys())}")
        
        # Test anomaly detection
        anomalies = analyzer.detect_anomalies()
        print(f"✅ Anomalies detected: {list(anomalies.keys())}")
        
        # Test seasonal patterns
        seasonal = analyzer.get_seasonal_patterns()
        print(f"✅ Seasonal patterns analyzed: {list(seasonal.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ TrendAnalyzer test failed: {e}")
        traceback.print_exc()
        return False

def test_forecasting_engine():
    """Test ForecastingEngine class."""
    print("\n🔍 Testing ForecastingEngine...")
    
    try:
        from analytics.forecasting import ForecastingEngine
        from db.database import get_db
        
        # Get a database session
        db = next(get_db())
        
        # Create forecasting engine
        engine = ForecastingEngine(db)
        print("✅ ForecastingEngine created successfully")
        
        # Test revenue forecasting
        revenue_forecast = engine.forecast_revenue(days=30)
        print(f"✅ Revenue forecast generated: {list(revenue_forecast.keys())}")
        
        # Test demand forecasting
        demand_forecast = engine.forecast_demand()
        print(f"✅ Demand forecast generated: {list(demand_forecast.keys())}")
        
        # Test inventory forecasting
        inventory_forecast = engine.predict_inventory_needs(days=30)
        print(f"✅ Inventory forecast generated: {list(inventory_forecast.keys())}")
        
        # Test market trends
        market_trends = engine.predict_market_trends()
        print(f"✅ Market trends predicted: {list(market_trends.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ ForecastingEngine test failed: {e}")
        traceback.print_exc()
        return False

def test_dashboard_service():
    """Test DashboardService class."""
    print("\n🔍 Testing DashboardService...")
    
    try:
        from analytics.dashboards import DashboardService
        
        # Create dashboard service
        service = DashboardService()
        print("✅ DashboardService created successfully")
        
        # Test KPI dashboard
        kpi_data = {"metrics": {"revenue": 1000, "orders": 50}}
        kpi_dashboard = service.generate_kpi_dashboard(kpi_data)
        print(f"✅ KPI dashboard generated: {list(kpi_dashboard.keys())}")
        
        # Test revenue chart
        revenue_data = {"daily_revenue": [100, 200, 300]}
        revenue_chart = service.generate_revenue_chart_data(revenue_data)
        print(f"✅ Revenue chart generated: {list(revenue_chart.keys())}")
        
        # Test product performance chart
        product_data = {"top_products": [{"name": "Product A", "sales": 100}]}
        product_chart = service.generate_product_performance_chart(product_data)
        print(f"✅ Product chart generated: {list(product_chart.keys())}")
        
        # Test customer segments chart
        customer_data = {"segments": [{"name": "High Value", "count": 100}]}
        customer_chart = service.generate_customer_segments_chart(customer_data)
        print(f"✅ Customer chart generated: {list(customer_chart.keys())}")
        
        # Test system health widget
        health_data = {"status": "healthy", "uptime": 99.9}
        health_widget = service.generate_system_health_widget(health_data)
        print(f"✅ Health widget generated: {list(health_widget.keys())}")
        
        # Test forecast widget
        forecast_data = {"revenue_forecast": [1000, 1100, 1200]}
        forecast_widget = service.generate_forecast_widget(forecast_data)
        print(f"✅ Forecast widget generated: {list(forecast_widget.keys())}")
        
        # Test comprehensive dashboard
        comprehensive_data = {"metrics": kpi_data, "revenue": revenue_data}
        comprehensive_dashboard = service.generate_comprehensive_dashboard(comprehensive_data)
        print(f"✅ Comprehensive dashboard generated: {list(comprehensive_dashboard.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ DashboardService test failed: {e}")
        traceback.print_exc()
        return False

def test_report_generator():
    """Test ReportGenerator class."""
    print("\n🔍 Testing ReportGenerator...")
    
    try:
        from analytics.reports import ReportGenerator
        
        # Create report generator
        generator = ReportGenerator()
        print("✅ ReportGenerator created successfully")
        
        # Test daily report
        daily_data = {"metrics": {"revenue": 1000, "orders": 50}}
        daily_report = generator.generate_daily_report(daily_data)
        print(f"✅ Daily report generated: {list(daily_report.keys())}")
        
        # Test weekly report
        weekly_data = {"metrics": {"revenue": 7000, "orders": 350}}
        weekly_report = generator.generate_weekly_report(weekly_data)
        print(f"✅ Weekly report generated: {list(weekly_report.keys())}")
        
        # Test monthly report
        monthly_data = {"metrics": {"revenue": 30000, "orders": 1500}}
        monthly_report = generator.generate_monthly_report(monthly_data)
        print(f"✅ Monthly report generated: {list(monthly_report.keys())}")
        
        # Test report export
        export_result = generator.export_report(daily_report, format="json")
        print(f"✅ Report exported: {len(export_result)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ ReportGenerator test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all analytics verification tests."""
    print("🧪 Enhanced Analytics System Verification")
    print("=" * 60)
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Module Imports", test_imports),
        ("Analytics Engine", test_analytics_engine),
        ("Embedding Service", test_embedding_service),
        ("Trend Analyzer", test_trend_analyzer),
        ("Forecasting Engine", test_forecasting_engine),
        ("Dashboard Service", test_dashboard_service),
        ("Report Generator", test_report_generator),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("📊 VERIFICATION RESULTS")
    print("=" * 60)
    
    success_count = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            success_count += 1
    
    print(f"\n🎉 Overall Result: {success_count}/{len(results)} tests passed")
    
    if success_count == len(results):
        print("✅ All analytics modules are working correctly!")
        print("🚀 The enhanced analytics system is ready for use.")
    else:
        print(f"⚠️  {len(results) - success_count} modules need attention.")
        print("🔧 Please check the error messages above for details.")
    
    print(f"\n📅 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 