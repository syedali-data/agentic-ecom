from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel

from db.database import get_db
from content_marketing import AILLMOptimizer, ContentGenerator, QAEngine, SEOOptimizer, SchemaMarkupGenerator, ContentPerformanceTracker

class ComparisonRequest(BaseModel):
    product_ids: List[str]

router = APIRouter(prefix="/content-marketing", tags=["content-marketing"])

# Content Generation Endpoints
@router.post("/generate/blog")
async def generate_blog_post(
    topic: str,
    product_id: Optional[str] = None,
    length: str = "medium",
    db: Session = Depends(get_db)
):
    """Generate AI LLM optimized blog post."""
    try:
        generator = ContentGenerator(db)
        result = generator.generate_blog_post(topic, product_id, length)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Blog generation failed: {str(e)}")

@router.post("/generate/product-description")
async def generate_product_description(
    product_id: str,
    db: Session = Depends(get_db)
):
    """Generate AI LLM optimized product description."""
    try:
        generator = ContentGenerator(db)
        result = generator.generate_product_description(product_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Product description generation failed: {str(e)}")

@router.post("/generate/comparison")
async def generate_comparison_content(
    request: ComparisonRequest,
    db: Session = Depends(get_db)
):
    """Generate AI LLM optimized comparison content."""
    try:
        generator = ContentGenerator(db)
        result = generator.generate_comparison_content(request.product_ids)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison content generation failed: {str(e)}")

# Q&A Content Endpoints
@router.post("/generate/qa")
async def generate_qa_content(
    topic: str,
    product_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Generate Q&A content optimized for AI LLM apps."""
    try:
        qa_engine = QAEngine(db)
        result = qa_engine.generate_qa_content(topic, product_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Q&A generation failed: {str(e)}")

@router.post("/generate/product-qa")
async def generate_product_qa(
    product_id: str,
    db: Session = Depends(get_db)
):
    """Generate product-specific Q&A content."""
    try:
        qa_engine = QAEngine(db)
        result = qa_engine.generate_product_qa(product_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Product Q&A generation failed: {str(e)}")

# SEO Optimization Endpoints
@router.post("/optimize/content")
async def optimize_content_for_ai_llm(
    content: str,
    topic: str,
    content_type: str = "blog",
    db: Session = Depends(get_db)
):
    """Optimize content for AI LLM app discovery."""
    try:
        seo_optimizer = SEOOptimizer(db)
        result = seo_optimizer.optimize_for_ai_llm(content, topic, content_type)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Content optimization failed: {str(e)}")

@router.get("/optimize/keywords")
async def generate_ai_llm_keywords(
    topic: str,
    content_type: str = "blog",
    db: Session = Depends(get_db)
):
    """Generate AI LLM optimized keywords."""
    try:
        seo_optimizer = SEOOptimizer(db)
        keywords = seo_optimizer.generate_ai_llm_keywords(topic, content_type)
        return {"keywords": keywords}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Keyword generation failed: {str(e)}")

# Schema Markup Endpoints
@router.get("/schema/product/{product_id}")
async def generate_product_schema(
    product_id: str,
    db: Session = Depends(get_db)
):
    """Generate structured data markup for product."""
    try:
        schema_generator = SchemaMarkupGenerator(db)
        result = schema_generator.generate_product_schema(product_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Schema generation failed: {str(e)}")

@router.post("/schema/qa")
async def generate_qa_schema(
    qa_pairs: List[Dict[str, str]],
    topic: str,
    db: Session = Depends(get_db)
):
    """Generate structured data markup for Q&A content."""
    try:
        schema_generator = SchemaMarkupGenerator(db)
        result = schema_generator.generate_qa_schema(qa_pairs, topic)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Q&A schema generation failed: {str(e)}")

# Performance Tracking Endpoints
@router.post("/track/performance")
async def track_content_performance(
    content_id: str,
    content_type: str,
    metrics: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Track content performance metrics."""
    try:
        tracker = ContentPerformanceTracker(db)
        result = tracker.track_content_performance(content_id, content_type, metrics)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Performance tracking failed: {str(e)}")

@router.post("/track/ai-llm-mention")
async def track_ai_llm_mention(
    content_id: str,
    ai_llm_app: str,
    mention_type: str,
    details: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Track AI LLM app mentions and interactions."""
    try:
        tracker = ContentPerformanceTracker(db)
        result = tracker.track_ai_llm_mentions(content_id, ai_llm_app, mention_type, details)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI LLM mention tracking failed: {str(e)}")

# Analytics Endpoints
@router.get("/analytics/content")
async def get_content_analytics(
    content_id: Optional[str] = None,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get content performance analytics."""
    try:
        tracker = ContentPerformanceTracker(db)
        result = tracker.get_content_analytics(content_id, days)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Content analytics failed: {str(e)}")

@router.get("/analytics/ai-llm-performance")
async def get_ai_llm_performance_report(
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get AI LLM app performance report."""
    try:
        tracker = ContentPerformanceTracker(db)
        result = tracker.get_ai_llm_performance_report(days)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI LLM performance report failed: {str(e)}")

# Main AI LLM Optimizer Endpoints
@router.post("/create/optimized-content")
async def create_ai_llm_optimized_content(
    topic: str,
    content_type: str = "blog",
    product_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Create complete AI LLM optimized content package."""
    try:
        optimizer = AILLMOptimizer(db)
        result = optimizer.create_ai_llm_optimized_content(topic, content_type, product_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Optimized content creation failed: {str(e)}")

@router.post("/create/comparison-package")
async def create_product_comparison_package(
    product_ids: List[str],
    db: Session = Depends(get_db)
):
    """Create complete product comparison package for AI LLM optimization."""
    try:
        optimizer = AILLMOptimizer(db)
        result = optimizer.generate_product_comparison_package(product_ids)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison package creation failed: {str(e)}")

@router.get("/calendar/content")
async def create_content_calendar(
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Create AI LLM optimized content calendar."""
    try:
        optimizer = AILLMOptimizer(db)
        result = optimizer.create_ai_llm_content_calendar(days)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Content calendar creation failed: {str(e)}")

@router.get("/report/optimization")
async def get_optimization_report(
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get AI LLM optimization performance report."""
    try:
        optimizer = AILLMOptimizer(db)
        result = optimizer.get_ai_llm_optimization_report(days)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Optimization report failed: {str(e)}")

@router.post("/optimize/existing")
async def optimize_existing_content(
    content_id: str,
    content: str,
    topic: str,
    db: Session = Depends(get_db)
):
    """Optimize existing content for AI LLM apps."""
    try:
        optimizer = AILLMOptimizer(db)
        result = optimizer.optimize_existing_content(content_id, content, topic)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Content optimization failed: {str(e)}")

@router.get("/summary/content")
async def get_content_summary(
    db: Session = Depends(get_db)
):
    """Get AI LLM content marketing summary."""
    try:
        optimizer = AILLMOptimizer(db)
        result = optimizer.get_ai_llm_content_summary()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Content summary failed: {str(e)}")

# Health Check Endpoint
@router.get("/health")
async def content_marketing_health():
    return {
        "status": "healthy",
        "service": "AI LLM Content Marketing",
        "timestamp": datetime.now().isoformat(),
        "features": [
            "Content Generation",
            "Q&A Engine", 
            "SEO Optimization",
            "Schema Markup",
            "Performance Tracking",
            "AI LLM Optimization"
        ]
    } 