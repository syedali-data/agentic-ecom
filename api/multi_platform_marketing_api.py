"""
Multi-Platform Marketing Strategy API
API endpoints for coordinating product marketing across Meta, Pinterest, and AI applications.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel

from db.database import get_db
from services.multi_platform_marketing_strategy import MultiPlatformMarketingStrategy

class StrategyRequest(BaseModel):
    product_id: str
    platforms: Optional[List[str]] = ["meta", "pinterest", "ai_apps"]

class ExecutionRequest(BaseModel):
    strategy_id: str
    platforms: Optional[List[str]] = ["meta", "pinterest", "ai_apps"]

router = APIRouter(prefix="/multi-platform-marketing", tags=["multi-platform-marketing"])

# Strategy Creation Endpoints
@router.post("/strategy/create")
async def create_marketing_strategy(
    request: StrategyRequest,
    db: Session = Depends(get_db)
):
    """Create comprehensive marketing strategy for a product across all platforms."""
    try:
        strategy_service = MultiPlatformMarketingStrategy(db)
        result = strategy_service.create_product_marketing_strategy(request.product_id)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "status": "success",
            "data": result,
            "message": f"Marketing strategy created for product {request.product_id}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Strategy creation failed: {str(e)}")

@router.get("/strategy/{strategy_id}")
async def get_marketing_strategy(
    strategy_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific marketing strategy by ID."""
    try:
        strategy_service = MultiPlatformMarketingStrategy(db)
        # This would implement actual strategy retrieval
        # For now, return a mock response
        return {
            "status": "success",
            "data": {
                "strategy_id": strategy_id,
                "product_id": "sample_product",
                "platforms": ["meta", "pinterest", "ai_apps"],
                "status": "ready_for_execution",
                "created_at": datetime.now().isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Strategy retrieval failed: {str(e)}")

# Strategy Execution Endpoints
@router.post("/strategy/execute")
async def execute_marketing_strategy(
    request: ExecutionRequest,
    db: Session = Depends(get_db)
):
    """Execute a marketing strategy across specified platforms."""
    try:
        strategy_service = MultiPlatformMarketingStrategy(db)
        result = strategy_service.execute_marketing_strategy(request.strategy_id)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "status": "success",
            "data": result,
            "message": f"Marketing strategy executed for {request.strategy_id}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Strategy execution failed: {str(e)}")

@router.get("/strategy/{strategy_id}/performance")
async def get_strategy_performance(
    strategy_id: str,
    db: Session = Depends(get_db)
):
    """Get performance metrics for a marketing strategy."""
    try:
        strategy_service = MultiPlatformMarketingStrategy(db)
        result = strategy_service.get_strategy_performance(strategy_id)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "status": "success",
            "data": result,
            "message": f"Performance metrics retrieved for {strategy_id}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Performance retrieval failed: {str(e)}")

# Platform-Specific Endpoints
@router.post("/meta/strategy")
async def create_meta_strategy(
    product_id: str,
    db: Session = Depends(get_db)
):
    """Create Meta-specific marketing strategy."""
    try:
        strategy_service = MultiPlatformMarketingStrategy(db)
        result = strategy_service.create_product_marketing_strategy(product_id)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "status": "success",
            "data": result.get("meta_strategy", {}),
            "message": f"Meta strategy created for product {product_id}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Meta strategy creation failed: {str(e)}")

@router.post("/pinterest/strategy")
async def create_pinterest_strategy(
    product_id: str,
    db: Session = Depends(get_db)
):
    """Create Pinterest-specific marketing strategy."""
    try:
        strategy_service = MultiPlatformMarketingStrategy(db)
        result = strategy_service.create_product_marketing_strategy(product_id)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "status": "success",
            "data": result.get("pinterest_strategy", {}),
            "message": f"Pinterest strategy created for product {product_id}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pinterest strategy creation failed: {str(e)}")

@router.post("/ai-apps/strategy")
async def create_ai_apps_strategy(
    product_id: str,
    db: Session = Depends(get_db)
):
    """Create AI applications-specific marketing strategy."""
    try:
        strategy_service = MultiPlatformMarketingStrategy(db)
        result = strategy_service.create_product_marketing_strategy(product_id)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "status": "success",
            "data": result.get("ai_apps_strategy", {}),
            "message": f"AI apps strategy created for product {product_id}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI apps strategy creation failed: {str(e)}")

# Content Generation Endpoints
@router.post("/content/generate")
async def generate_multi_platform_content(
    product_id: str,
    platforms: Optional[List[str]] = ["meta", "pinterest", "ai_apps"],
    db: Session = Depends(get_db)
):
    """Generate content optimized for multiple platforms."""
    try:
        strategy_service = MultiPlatformMarketingStrategy(db)
        result = strategy_service.create_product_marketing_strategy(product_id)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        # Filter content based on requested platforms
        content = {}
        if "meta" in platforms:
            content["meta"] = result.get("meta_strategy", {}).get("content", {})
        if "pinterest" in platforms:
            content["pinterest"] = result.get("pinterest_strategy", {}).get("content", {})
        if "ai_apps" in platforms:
            content["ai_apps"] = result.get("ai_apps_strategy", {}).get("content", {})
        
        return {
            "status": "success",
            "data": content,
            "message": f"Content generated for platforms: {', '.join(platforms)}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Content generation failed: {str(e)}")

# Performance Analytics Endpoints
@router.get("/analytics/platform-performance")
async def get_platform_performance(
    strategy_id: Optional[str] = None,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get performance analytics across all platforms."""
    try:
        strategy_service = MultiPlatformMarketingStrategy(db)
        
        if strategy_id:
            result = strategy_service.get_strategy_performance(strategy_id)
        else:
            # Return mock data for general platform performance
            result = {
                "platform_performance": {
                    "meta": {
                        "impressions": 150000,
                        "clicks": 7500,
                        "conversions": 450,
                        "revenue": 22500,
                        "roas": 3.2
                    },
                    "pinterest": {
                        "impressions": 75000,
                        "clicks": 4000,
                        "conversions": 225,
                        "revenue": 11250,
                        "roas": 2.8
                    },
                    "ai_apps": {
                        "mentions": 2500,
                        "clicks": 1000,
                        "conversions": 75,
                        "revenue": 3750,
                        "roas": 4.1
                    }
                },
                "analysis_period": f"Last {days} days"
            }
        
        return {
            "status": "success",
            "data": result,
            "message": "Platform performance analytics retrieved"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics retrieval failed: {str(e)}")

# Optimization Endpoints
@router.post("/optimize/strategy")
async def optimize_marketing_strategy(
    strategy_id: str,
    optimization_type: str = "performance",
    db: Session = Depends(get_db)
):
    """Optimize an existing marketing strategy."""
    try:
        strategy_service = MultiPlatformMarketingStrategy(db)
        
        # This would implement actual optimization logic
        result = {
            "strategy_id": strategy_id,
            "optimization_type": optimization_type,
            "optimizations_applied": [
                "budget_reallocation",
                "targeting_refinement",
                "content_optimization"
            ],
            "expected_improvement": {
                "conversion_rate": "+15%",
                "cost_per_acquisition": "-20%",
                "return_on_ad_spend": "+25%"
            },
            "optimized_at": datetime.now().isoformat()
        }
        
        return {
            "status": "success",
            "data": result,
            "message": f"Strategy optimized with {optimization_type} focus"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Strategy optimization failed: {str(e)}")

# Health Check Endpoint
@router.get("/health")
async def multi_platform_marketing_health():
    """Health check for multi-platform marketing service."""
    return {
        "status": "healthy",
        "service": "Multi-Platform Marketing Strategy",
        "timestamp": datetime.now().isoformat(),
        "platforms_supported": [
            "Meta (Facebook/Instagram)",
            "Pinterest",
            "AI Applications (GPT/Claude/Perplexity)"
        ],
        "features": [
            "Strategy Creation",
            "Content Generation",
            "Campaign Management",
            "Performance Tracking",
            "Cross-Platform Optimization"
        ]
    } 