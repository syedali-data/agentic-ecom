"""
Analytics API for Agentic-Ecom
Provides endpoints for enhanced analytics and business intelligence.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from db.database import get_db
from analytics.engine import AnalyticsEngine
from analytics.embeddings import EmbeddingService
from analytics.trends import TrendAnalyzer
from analytics.forecasting import ForecastingEngine
from analytics.dashboards import DashboardService
from analytics.reports import ReportGenerator

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/basic-metrics")
async def get_basic_metrics(db: Session = Depends(get_db)):
    """Get basic business metrics."""
    try:
        engine = AnalyticsEngine(db)
        return engine.get_basic_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting basic metrics: {str(e)}")

@router.get("/revenue-analysis")
async def get_revenue_analysis(days: int = 30, db: Session = Depends(get_db)):
    """Get revenue analysis for specified period."""
    try:
        engine = AnalyticsEngine(db)
        return engine.get_revenue_analysis(days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting revenue analysis: {str(e)}")

@router.get("/customer-insights")
async def get_customer_insights(db: Session = Depends(get_db)):
    """Get customer behavior insights."""
    try:
        engine = AnalyticsEngine(db)
        return engine.get_customer_insights()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting customer insights: {str(e)}")

@router.get("/product-performance")
async def get_product_performance(db: Session = Depends(get_db)):
    """Get product performance metrics."""
    try:
        engine = AnalyticsEngine(db)
        return engine.get_product_performance()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting product performance: {str(e)}")

@router.get("/system-health")
async def get_system_health(db: Session = Depends(get_db)):
    """Get system health metrics."""
    try:
        engine = AnalyticsEngine(db)
        return engine.get_system_health_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting system health: {str(e)}")

@router.get("/comprehensive")
async def get_comprehensive_analytics(db: Session = Depends(get_db)):
    """Get comprehensive analytics report."""
    try:
        engine = AnalyticsEngine(db)
        return engine.generate_comprehensive_report()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating comprehensive report: {str(e)}")

# Trend Analysis Endpoints
@router.get("/trends/sales")
async def get_sales_trends(days: int = 30, db: Session = Depends(get_db)):
    """Get sales trends analysis."""
    try:
        analyzer = TrendAnalyzer(db)
        return analyzer.analyze_sales_trends(days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing sales trends: {str(e)}")

@router.get("/trends/products")
async def get_product_trends(db: Session = Depends(get_db)):
    """Get product trends analysis."""
    try:
        analyzer = TrendAnalyzer(db)
        return analyzer.analyze_product_trends()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing product trends: {str(e)}")

@router.get("/trends/customers")
async def get_customer_trends(db: Session = Depends(get_db)):
    """Get customer trends analysis."""
    try:
        analyzer = TrendAnalyzer(db)
        return analyzer.analyze_customer_trends()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing customer trends: {str(e)}")

@router.get("/trends/anomalies")
async def get_anomalies(db: Session = Depends(get_db)):
    """Get anomaly detection results."""
    try:
        analyzer = TrendAnalyzer(db)
        return analyzer.detect_anomalies()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error detecting anomalies: {str(e)}")

@router.get("/trends/seasonal")
async def get_seasonal_patterns(db: Session = Depends(get_db)):
    """Get seasonal patterns analysis."""
    try:
        analyzer = TrendAnalyzer(db)
        return analyzer.get_seasonal_patterns()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting seasonal patterns: {str(e)}")

# Forecasting Endpoints
@router.get("/forecast/revenue")
async def get_revenue_forecast(days: int = 30, db: Session = Depends(get_db)):
    """Get revenue forecast."""
    try:
        forecaster = ForecastingEngine(db)
        return forecaster.forecast_revenue(days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error forecasting revenue: {str(e)}")

@router.get("/forecast/demand")
async def get_demand_forecast(product_id: Optional[str] = None, db: Session = Depends(get_db)):
    """Get demand forecast."""
    try:
        forecaster = ForecastingEngine(db)
        return forecaster.forecast_demand(product_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error forecasting demand: {str(e)}")

@router.get("/forecast/customer-lifetime-value/{customer_id}")
async def get_customer_lifetime_value(customer_id: str, db: Session = Depends(get_db)):
    """Get customer lifetime value prediction."""
    try:
        forecaster = ForecastingEngine(db)
        return forecaster.predict_customer_lifetime_value(customer_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting CLV: {str(e)}")

@router.get("/forecast/inventory")
async def get_inventory_forecast(days: int = 30, db: Session = Depends(get_db)):
    """Get inventory needs forecast."""
    try:
        forecaster = ForecastingEngine(db)
        return forecaster.predict_inventory_needs(days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error forecasting inventory: {str(e)}")

@router.get("/forecast/market-trends")
async def get_market_trends(db: Session = Depends(get_db)):
    """Get market trends prediction."""
    try:
        forecaster = ForecastingEngine(db)
        return forecaster.predict_market_trends()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting market trends: {str(e)}")

# Dashboard Endpoints
@router.get("/dashboard/kpi")
async def get_kpi_dashboard(db: Session = Depends(get_db)):
    """Get KPI dashboard data."""
    try:
        engine = AnalyticsEngine(db)
        dashboard = DashboardService()
        data = engine.generate_comprehensive_report()
        return dashboard.generate_kpi_dashboard(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating KPI dashboard: {str(e)}")

@router.get("/dashboard/revenue-chart")
async def get_revenue_chart(db: Session = Depends(get_db)):
    """Get revenue chart data."""
    try:
        engine = AnalyticsEngine(db)
        dashboard = DashboardService()
        data = engine.get_revenue_analysis()
        return dashboard.generate_revenue_chart_data(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating revenue chart: {str(e)}")

@router.get("/dashboard/product-chart")
async def get_product_chart(db: Session = Depends(get_db)):
    """Get product performance chart data."""
    try:
        engine = AnalyticsEngine(db)
        dashboard = DashboardService()
        data = engine.get_product_performance()
        return dashboard.generate_product_performance_chart(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating product chart: {str(e)}")

@router.get("/dashboard/customer-chart")
async def get_customer_chart(db: Session = Depends(get_db)):
    """Get customer segments chart data."""
    try:
        engine = AnalyticsEngine(db)
        dashboard = DashboardService()
        data = engine.get_customer_insights()
        return dashboard.generate_customer_segments_chart(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating customer chart: {str(e)}")

@router.get("/dashboard/system-health")
async def get_system_health_widget(db: Session = Depends(get_db)):
    """Get system health widget data."""
    try:
        engine = AnalyticsEngine(db)
        dashboard = DashboardService()
        data = engine.get_system_health_metrics()
        return dashboard.generate_system_health_widget(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating system health widget: {str(e)}")

@router.get("/dashboard/comprehensive")
async def get_comprehensive_dashboard(db: Session = Depends(get_db)):
    """Get comprehensive dashboard with all widgets."""
    try:
        engine = AnalyticsEngine(db)
        dashboard = DashboardService()
        data = engine.generate_comprehensive_report()
        return dashboard.generate_comprehensive_dashboard(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating comprehensive dashboard: {str(e)}")

# Report Endpoints
@router.get("/reports/daily")
async def get_daily_report(db: Session = Depends(get_db)):
    """Get daily business report."""
    try:
        engine = AnalyticsEngine(db)
        reports = ReportGenerator()
        data = engine.generate_comprehensive_report()
        return reports.generate_daily_report(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating daily report: {str(e)}")

@router.get("/reports/weekly")
async def get_weekly_report(db: Session = Depends(get_db)):
    """Get weekly business report."""
    try:
        engine = AnalyticsEngine(db)
        reports = ReportGenerator()
        data = engine.generate_comprehensive_report()
        return reports.generate_weekly_report(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating weekly report: {str(e)}")

@router.get("/reports/monthly")
async def get_monthly_report(db: Session = Depends(get_db)):
    """Get monthly business report."""
    try:
        engine = AnalyticsEngine(db)
        reports = ReportGenerator()
        data = engine.generate_comprehensive_report()
        return reports.generate_monthly_report(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating monthly report: {str(e)}")

# Embedding Endpoints
@router.get("/embeddings/similar-products/{product_id}")
async def get_similar_products(product_id: str, limit: int = 5, db: Session = Depends(get_db)):
    """Get similar products using embeddings."""
    try:
        embedding_service = EmbeddingService(db)
        return embedding_service.find_similar_products(product_id, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding similar products: {str(e)}")

@router.get("/embeddings/recommendations/{customer_id}")
async def get_product_recommendations(customer_id: str, limit: int = 5, db: Session = Depends(get_db)):
    """Get product recommendations for customer."""
    try:
        embedding_service = EmbeddingService(db)
        return embedding_service.get_product_recommendations(customer_id, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting recommendations: {str(e)}")

@router.get("/embeddings/customer-segments")
async def get_customer_segments(db: Session = Depends(get_db)):
    """Get customer segments analysis."""
    try:
        embedding_service = EmbeddingService(db)
        return embedding_service.analyze_customer_segments()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing customer segments: {str(e)}")

# Viral Trend Analysis Endpoints
@router.get("/viral/discover")
async def discover_viral_products(
    categories: str = None,
    max_products: int = 20,
    min_viral_score: float = 0.6,
    db: Session = Depends(get_db)
):
    """Discover viral products using AI-powered trend analysis."""
    try:
        from analytics.viral_trend_analyzer import ViralTrendAnalyzer
        
        # Parse categories
        category_list = None
        if categories:
            category_list = [cat.strip() for cat in categories.split(",")]
        
        analyzer = ViralTrendAnalyzer(db)
        results = analyzer.discover_viral_products(
            categories=category_list,
            max_products=max_products,
            min_viral_score=min_viral_score,
            include_analysis=True
        )
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error discovering viral products: {str(e)}")

@router.get("/viral/analyze/{product_name}")
async def analyze_product_viral_potential(
    product_name: str,
    category: str = None,
    db: Session = Depends(get_db)
):
    """Analyze viral potential for a specific product."""
    try:
        from analytics.viral_trend_analyzer import ViralTrendAnalyzer
        
        analyzer = ViralTrendAnalyzer(db)
        results = analyzer.analyze_product_viral_potential(product_name, category)
        
        if "error" in results:
            raise HTTPException(status_code=400, detail=results["error"])
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing product viral potential: {str(e)}")

@router.get("/viral/categories")
async def get_trending_categories(
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get trending product categories based on viral analysis."""
    try:
        from analytics.viral_trend_analyzer import ViralTrendAnalyzer
        
        analyzer = ViralTrendAnalyzer(db)
        results = analyzer.get_trending_categories(days)
        
        if "error" in results:
            raise HTTPException(status_code=400, detail=results["error"])
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting trending categories: {str(e)}")

@router.post("/viral/batch-analyze")
async def batch_analyze_viral_potential(
    products: List[Dict[str, Any]],
    db: Session = Depends(get_db)
):
    """Batch analyze viral potential for multiple products."""
    try:
        from analytics.viral_trend_analyzer import ViralTrendAnalyzer
        
        analyzer = ViralTrendAnalyzer(db)
        results = []
        
        for product in products:
            product_name = product.get("name", "")
            category = product.get("category")
            
            if product_name:
                analysis = analyzer.analyze_product_viral_potential(product_name, category)
                results.append({
                    "product_name": product_name,
                    "category": category,
                    "analysis": analysis
                })
        
        return {
            "total_products": len(results),
            "analyses": results,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in batch analysis: {str(e)}") 