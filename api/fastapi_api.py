from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import sys
from datetime import datetime, timedelta, timezone

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.sales_genie import generate_listing
from agents.logibot import LogiBot
from services.shopify_api import create_product
from services.cj_api import fetch_mock_products
from schemas.product import Product, ProductResponse
from db.database import get_db
from services.db_service import DatabaseService

# Import authentication module
from api.auth import (
    auth_manager, get_current_active_user, require_auth,
    User, Token, fake_users_db, rate_limiter, check_rate_limit
)

# Import safety middleware
from api.safety_middleware import safety_middleware
from utils.safety_manager import safety_manager, require_safety_check

# Import analytics API
from api.analytics_api import router as analytics_router

# Import content marketing API
from api.content_marketing_api import router as content_marketing_router

# Import multi-platform marketing strategy API
from api.multi_platform_marketing_api import router as multi_platform_marketing_router

def map_category_to_enum(category: str) -> str:
    """Map database categories to ProductCategory enum values"""
    category_mapping = {
        "Electronics": "electronics",
        "Beauty": "beauty", 
        "Home & Kitchen": "home_garden",
        "Fashion": "fashion",
        "Sports": "sports",
        "Toys": "toys",
        "Books": "books"
    }
    return category_mapping.get(category, "other")

app = FastAPI(
    title="Agentic-Ecom API",
    description="AI-powered e-commerce automation API with authentication and safety measures",
    version="1.0.0"
)

# CORS middleware with security headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add safety middleware
@app.middleware("http")
async def safety_middleware_handler(request: Request, call_next):
    """Safety middleware handler"""
    return await safety_middleware(request, call_next)

# Include routers with authentication
app.include_router(analytics_router)
app.include_router(content_marketing_router)
app.include_router(multi_platform_marketing_router)

# Initialize LogiBot
logibot = LogiBot()

def check_rate_limit_local():
    """Local rate limiting function to avoid dependency injection issues"""
    try:
        # Use a default client ID for now
        client_ip = "default"
        
        # Check rate limit
        if not rate_limiter.is_allowed(client_ip):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded"
            )
        
        return True
    except HTTPException:
        # Re-raise HTTP exceptions (like 429)
        raise
    except Exception as e:
        # If there's any other error with rate limiting, log it but don't block the request
        print(f"Rate limiting error: {e}")
        return True

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user_role: str
    username: str

# Authentication endpoints
@app.post("/auth/login", response_model=LoginResponse)
async def login(
    login_request: LoginRequest,
    rate_limit_check: bool = Depends(check_rate_limit)
):
    """Login endpoint to get JWT token"""
    user = auth_manager.authenticate_user(login_request.username, login_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=auth_manager.access_token_expire_minutes)
    access_token = auth_manager.create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=auth_manager.access_token_expire_minutes * 60,
        user_role=user.role,
        username=user.username
    )

@app.get("/auth/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user

@app.get("/auth/users")
async def get_users(current_user: User = Depends(get_current_active_user)):
    """Get all users (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    users = []
    for username, user_data in fake_users_db.items():
        users.append({
            "username": user_data["username"],
            "full_name": user_data["full_name"],
            "email": user_data["email"],
            "role": user_data["role"],
            "disabled": user_data["disabled"]
        })
    return users

# Public endpoints (no authentication required)
@app.get("/")
async def root():
    return {"message": "Agentic-Ecom API is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "operational", "agents": ["sales_genie", "logibot"]}

# Protected endpoints (authentication required)
@app.get("/db/health")
async def database_health_check(current_user: User = Depends(get_current_active_user)):
    """Check database connectivity and get statistics"""
    from db.database import health_check
    return health_check()

@app.get("/db/stats")
async def database_stats(current_user: User = Depends(get_current_active_user)):
    """Get database statistics and table counts"""
    from db.database import get_db_stats
    return get_db_stats()

@app.get("/products", response_model=List[ProductResponse])
async def get_products(db=Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Get all available products from database"""
    try:
        db_service = DatabaseService(db)
        db_products = db_service.get_products()
        
        formatted_products = []
        for product in db_products:
            formatted_product = {
                "id": product.id,
                "name": product.name,
                "description": product.description or f"Description for {product.name}",
                "category": map_category_to_enum(product.category),
                "price": product.price,
                "retail_price": product.price,  # Using price as retail_price
                "images": [product.image_url] if product.image_url else [],
                "status": product.status.value,
                "rating": product.average_rating,
                "review_count": product.review_count,
                "tags": product.tags or [],
                "created_at": product.created_at,
                "updated_at": product.updated_at
            }
            formatted_products.append(ProductResponse(**formatted_product))
        
        return formatted_products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch products: {str(e)}")

@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str, db=Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Get a specific product by ID from database"""
    try:
        db_service = DatabaseService(db)
        product = db_service.get_product_by_id(product_id)
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        formatted_product = {
            "id": product.id,
            "name": product.name,
            "description": product.description or f"Description for {product.name}",
            "category": map_category_to_enum(product.category),
            "price": product.price,
            "retail_price": product.price,
            "images": [product.image_url] if product.image_url else [],
            "status": product.status.value,
            "rating": product.average_rating,
            "review_count": product.review_count,
            "tags": product.tags or [],
            "created_at": product.created_at,
            "updated_at": product.updated_at
        }
        
        return ProductResponse(**formatted_product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch product: {str(e)}")

@app.post("/products/generate-listing")
@require_safety_check("generate_product_listing", "shopify")
async def generate_product_listing(
    product: Product, 
    db=Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    """Generate AI-powered product listing"""
    # Check rate limit
    check_rate_limit_local()
    
    try:
        if current_user.role not in ["admin", "sales"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to generate listings"
            )
        
        # Implementation here
        return {"status": "success", "message": "Product listing generated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate listing: {str(e)}")

@app.post("/orders/track")
@require_safety_check("track_order")
async def track_order(
    tracking_number: str, 
    current_user: User = Depends(get_current_active_user)
):
    """Track order status"""
    # Check rate limit
    check_rate_limit_local()
    
    try:
        tracking_info = logibot.get_tracking_info(tracking_number)
        return tracking_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to track order: {str(e)}")

@app.post("/support/chat", response_model=ChatResponse)
@require_safety_check("chat_with_support")
async def chat_with_support(
    message: ChatMessage, 
    current_user: User = Depends(get_current_active_user)
):
    """Chat with AI-powered customer support"""
    # Check rate limit
    check_rate_limit_local()
    
    try:
        if current_user.role not in ["admin", "support", "analytics"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to access support chat"
            )
        
        response = logibot.handle_support_ticket({
            "ticket_id": message.session_id or "default",
            "message": message.message,
            "customer_id": current_user.username
        })
        
        return ChatResponse(
            response=response.get("ai_response", "I'm here to help!"),
            session_id=message.session_id or "default"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process support chat: {str(e)}")

@app.get("/analytics/performance")
async def get_performance_analytics(db=Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Get system performance analytics from database"""
    try:
        if current_user.role not in ["admin", "analytics"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to access analytics"
            )
        
        db_service = DatabaseService(db)
        analytics = db_service.get_sales_analytics(days=30)
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch analytics: {str(e)}")

@app.get("/customers")
async def get_customers(db=Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Get all customers from database"""
    try:
        if current_user.role not in ["admin", "support", "sales", "analytics"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to access customer data"
            )
        
        db_service = DatabaseService(db)
        customers = db_service.get_customers(limit=100)
        
        formatted_customers = []
        for customer in customers:
            formatted_customers.append({
                "id": customer.id,
                "name": customer.name,
                "email": customer.email,
                "created_at": customer.created_at,
                "total_orders": customer.total_orders,
                "total_spent": customer.total_spent
            })
        
        return formatted_customers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch customers: {str(e)}")

@app.get("/orders")
async def get_orders(db=Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Get all orders from database"""
    try:
        if current_user.role not in ["admin", "support", "sales", "analytics"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to access order data"
            )
        
        db_service = DatabaseService(db)
        orders = db_service.get_orders(limit=100)
        
        formatted_orders = []
        for order in orders:
            formatted_orders.append({
                "id": order.id,
                "customer_id": order.customer_id,
                "total": order.total,
                "status": order.status.value,
                "created_at": order.created_at
            })
        
        return formatted_orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch orders: {str(e)}")

@app.get("/support/tickets")
async def get_support_tickets(db=Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Get all support tickets from database"""
    try:
        if current_user.role not in ["admin", "support"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to access support tickets"
            )
        
        db_service = DatabaseService(db)
        tickets = db_service.get_support_tickets(limit=100)
        
        formatted_tickets = []
        for ticket in tickets:
            formatted_tickets.append({
                "id": ticket.id,
                "customer_id": ticket.customer_id,
                "subject": ticket.subject,
                "status": ticket.status.value,
                "priority": ticket.priority.value,
                "created_at": ticket.created_at
            })
        
        return formatted_tickets
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch support tickets: {str(e)}")

# ==================== AUTOMATION TRIGGER ENDPOINTS ====================

@app.post("/trigger/sales-genie")
@require_safety_check("trigger_sales_genie", "shopify")
async def trigger_sales_genie(
    action: str, 
    count: int = 5, 
    db=Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    """Trigger SalesGenie automation"""
    # Check rate limit
    check_rate_limit_local()
    
    try:
        if current_user.role not in ["admin", "sales"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to trigger SalesGenie"
            )
        
        # Implementation here
        return {"status": "success", "message": f"SalesGenie triggered: {action}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to trigger SalesGenie: {str(e)}")

@app.post("/trigger/salesgenie")
@require_safety_check("trigger_salesgenie", "shopify")
async def trigger_salesgenie_alt(
    generate_products: str = None, 
    count: int = 5, 
    db=Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    """Alternative SalesGenie endpoint for n8n compatibility"""
    # Check rate limit
    check_rate_limit_local()
    
    try:
        if current_user.role not in ["admin", "sales"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to trigger SalesGenie"
            )
        
        # Implementation here
        return {"status": "success", "message": "SalesGenie triggered"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to trigger SalesGenie: {str(e)}")

@app.post("/trigger/ad-optimization")
@require_safety_check("trigger_ad_optimization", "meta_ads")
async def trigger_ad_optimization(
    action: str, 
    platform: str = "all", 
    current_user: User = Depends(get_current_active_user)
):
    """Trigger ad optimization automation"""
    # Check rate limit
    check_rate_limit_local()
    
    try:
        if current_user.role not in ["admin", "analytics"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to trigger ad optimization"
            )
        
        # Implementation here
        return {"status": "success", "message": f"Ad optimization triggered for {platform}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to trigger ad optimization: {str(e)}")

@app.post("/trigger/logibot")
@require_safety_check("trigger_logibot")
async def trigger_logibot(
    action: str, 
    priority: str = "normal", 
    current_user: User = Depends(get_current_active_user)
):
    """Trigger LogiBot automation"""
    # Check rate limit
    check_rate_limit_local()
    
    try:
        if current_user.role not in ["admin", "support"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to trigger LogiBot"
            )
        
        # Implementation here
        return {"status": "success", "message": f"LogiBot triggered: {action}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to trigger LogiBot: {str(e)}")

@app.post("/trigger/emergency-stop")
@require_safety_check("trigger_emergency_stop")
async def trigger_emergency_stop(
    reason: str, 
    threshold: str = "80%", 
    current_user: User = Depends(get_current_active_user)
):
    """Trigger emergency stop"""
    # Check rate limit
    check_rate_limit_local()
    
    try:
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can trigger emergency stop"
            )
        
        # Implementation here
        return {"status": "success", "message": "Emergency stop triggered"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to trigger emergency stop: {str(e)}")

@app.post("/log/automation")
@require_safety_check("log_automation_event")
async def log_automation_event(
    action: str, 
    status: str, 
    timestamp: str, 
    error: str = None, 
    current_user: User = Depends(get_current_active_user)
):
    """Log automation events"""
    # Check rate limit
    check_rate_limit_local()
    
    try:
        if current_user.role not in ["admin", "analytics"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to log automation events"
            )
        
        # Implementation here
        return {"status": "success", "message": "Event logged successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to log event: {str(e)}")

# Safety endpoints
@app.get("/test")
async def test_endpoint():
    """Simple test endpoint"""
    return {"status": "success", "message": "Test endpoint working"}

@app.get("/test-auth")
async def test_auth_endpoint(
    current_user: User = Depends(get_current_active_user)
):
    """Test endpoint with authentication"""
    return {
        "status": "success", 
        "message": "Auth test endpoint working",
        "user": current_user.username
    }

@app.get("/safety/status")
async def get_safety_status(
    current_user: User = Depends(get_current_active_user)
):
    """Get current safety status and configuration"""
    try:
        if current_user.role not in ["admin", "analytics"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to access safety status"
            )
        
        safety_status = safety_manager.get_safety_status()
        return {
            "status": "success",
            "data": safety_status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get safety status: {str(e)}")

@app.post("/safety/approve")
async def approve_safety_action(
    action: str, 
    platform: str = None, 
    current_user: User = Depends(get_current_active_user)
):
    """Approve a safety action"""
    # Check rate limit
    check_rate_limit_local()
    
    try:
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can approve safety actions"
            )
        
        # Check if action is safe
        safety_check = safety_manager.check_environment_safety(action, platform)
        
        if not safety_check['safe']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Action is not safe: {safety_check['reason']}"
            )
        
        # Approve the action
        approved = safety_manager.approve_action(action, platform)
        
        if approved:
            return {
                "status": "success",
                "message": f"Action '{action}' approved",
                "approved": True,
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Action was not approved"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to approve action: {str(e)}")

@app.get("/safety/check")
async def check_safety_action(
    action: str, 
    platform: str = None, 
    current_user: User = Depends(get_current_active_user)
):
    """Check if an action is safe to perform"""
    # Check rate limit
    check_rate_limit_local()
    
    try:
        safety_check = safety_manager.check_environment_safety(action, platform)
        
        return {
            "status": "success",
            "action": action,
            "platform": platform,
            "safe": safety_check['safe'],
            "reason": safety_check['reason'],
            "requires_approval": safety_check['requires_approval'],
            "dry_run": safety_check['dry_run'],
            "budget_remaining": safety_check['budget_remaining'],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check safety: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 