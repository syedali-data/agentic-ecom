"""
Authentication and Authorization Module for Agentic-Ecom API
Provides JWT-based authentication, role-based access control, and security features.
"""

import os
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, List
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt
import hashlib
import secrets
from passlib.context import CryptContext
from starlette.requests import Request as StarletteRequest

logger = logging.getLogger(__name__)

# Password hashing - Fix for bcrypt __about__ attribute issue
try:
    # Monkey patch bcrypt to avoid __about__ attribute error
    import bcrypt
    if not hasattr(bcrypt, '__about__'):
        # Create a mock __about__ attribute if it doesn't exist
        class MockAbout:
            __version__ = getattr(bcrypt, '__version__', '4.0.1')
        bcrypt.__about__ = MockAbout()
    
    # Check if bcrypt is working by testing a simple hash
    test_password = b"test"
    test_hash = bcrypt.hashpw(test_password, bcrypt.gensalt())
    if bcrypt.checkpw(test_password, test_hash):
        # Use bcrypt with explicit configuration
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)
        logger.info("bcrypt initialized successfully with monkey patch")
    else:
        raise Exception("bcrypt test failed")
except Exception as e:
    # Fallback to sha256_crypt if bcrypt fails
    pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
    logger.warning(f"bcrypt not available, falling back to sha256_crypt: {e}")

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Security scheme
security = HTTPBearer()

class User(BaseModel):
    """User model for authentication"""
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    role: str = "user"

class UserInDB(User):
    """User model with hashed password"""
    hashed_password: str

class Token(BaseModel):
    """Token model for authentication"""
    access_token: str
    token_type: str
    expires_in: int
    user_role: str

class TokenData(BaseModel):
    """Token data model"""
    username: Optional[str] = None
    role: Optional[str] = None

# In-memory user store (replace with database in production)
def get_fake_users_db():
    """Get fake users database with properly hashed passwords"""
    return {
        "admin": {
            "username": "admin",
            "full_name": "Administrator",
            "email": "admin@agentic-ecom.com",
            "hashed_password": pwd_context.hash("admin123"),
            "disabled": False,
            "role": "admin"
        },
        "analyst": {
            "username": "analyst",
            "full_name": "Data Analyst",
            "email": "analyst@agentic-ecom.com",
            "hashed_password": pwd_context.hash("analyst123"),
            "disabled": False,
            "role": "analytics"
        },
        "support": {
            "username": "support",
            "full_name": "Support Agent",
            "email": "support@agentic-ecom.com",
            "hashed_password": pwd_context.hash("support123"),
            "disabled": False,
            "role": "support"
        },
        "sales": {
            "username": "sales",
            "full_name": "Sales Agent",
            "email": "sales@agentic-ecom.com",
            "hashed_password": pwd_context.hash("sales123"),
            "disabled": False,
            "role": "sales"
        }
    }

# Initialize fake users database
fake_users_db = get_fake_users_db()

class AuthManager:
    """Authentication and authorization manager"""
    
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM
        self.access_token_expire_minutes = ACCESS_TOKEN_EXPIRE_MINUTES
        self.logger = logging.getLogger(__name__)
        
        # Role-based permissions
        self.role_permissions = {
            "admin": ["*"],  # All permissions
            "analytics": [
                "read:products", "read:analytics", "read:performance", 
                "read:customers", "read:orders", "read:reports"
            ],
            "support": [
                "read:products", "read:customers", "read:orders", 
                "read:support_tickets", "write:support_tickets", "read:support", "write:support"
            ],
            "sales": [
                "read:products", "read:customers", "read:orders", 
                "write:products", "read:analytics"
            ],
            "user": [
                "read:products", "read:public_analytics"
            ]
        }
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Generate password hash"""
        return pwd_context.hash(password)
    
    def get_user(self, username: str) -> Optional[UserInDB]:
        """Get user from database"""
        users_db = get_fake_users_db()
        if username in users_db:
            user_dict = users_db[username]
            return UserInDB(**user_dict)
        return None
    
    def authenticate_user(self, username: str, password: str) -> Optional[UserInDB]:
        """Authenticate user with username and password"""
        user = self.get_user(username)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[TokenData]:
        """Verify JWT token and return token data"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            role: str = payload.get("role", "user")
            if username is None:
                return None
            token_data = TokenData(username=username, role=role)
            return token_data
        except jwt.PyJWTError:
            return None
    
    def has_permission(self, user_role: str, permission: str) -> bool:
        """Check if user has specific permission"""
        if user_role not in self.role_permissions:
            return False
        
        permissions = self.role_permissions[user_role]
        return "*" in permissions or permission in permissions
    
    def require_permission(self, permission: str):
        """Decorator to require specific permission"""
        def decorator(func):
            async def wrapper(*args, **kwargs):
                # Extract user from request or context
                request = None
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
                
                if not request:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Could not validate credentials"
                    )
                
                # Get user from request
                user = get_current_user(request)
                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Could not validate credentials"
                    )
                
                # Check permission
                if not self.has_permission(user.role, permission):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Not enough permissions"
                    )
                
                return await func(*args, **kwargs)
            return wrapper
        return decorator

# Global auth manager instance
auth_manager = AuthManager()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Optional[User]:
    """Get current user from JWT token"""
    try:
        token_data = auth_manager.verify_token(credentials.credentials)
        if token_data is None:
            return None
        
        user = auth_manager.get_user(username=token_data.username)
        if user is None:
            return None
        
        return user
    except Exception as e:
        logger.error(f"Error getting current user: {e}")
        return None

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def require_auth(permission: Optional[str] = None):
    """Decorator to require authentication and optionally specific permission"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Extract request from args
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if not request:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials"
                )
            
            # Get authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Extract token
            token = auth_header.split(" ")[1]
            token_data = auth_manager.verify_token(token)
            
            if token_data is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Get user
            user = auth_manager.get_user(username=token_data.username)
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Check permission if required
            if permission and not auth_manager.has_permission(user.role, permission):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough permissions"
                )
            
            # Add user to kwargs
            kwargs["current_user"] = user
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Rate limiting
class RateLimiter:
    """Simple rate limiter for API endpoints"""
    
    def __init__(self):
        self.requests = {}
        # Load rate limiting configuration
        self.max_requests = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", "10"))  # Default to 10 for testing
        self.window_minutes = int(os.getenv("RATE_LIMIT_WINDOW_MINUTES", "15"))
        
        # Try to load from config file
        try:
            import yaml
            config_path = "config/rate_limiting.yaml"
            if os.path.exists(config_path):
                with open(config_path, 'r') as file:
                    config = yaml.safe_load(file)
                    # Use login-specific limits if available
                    if 'endpoints' in config and 'auth' in config['endpoints'] and 'login' in config['endpoints']['auth']:
                        login_config = config['endpoints']['auth']['login']
                        self.max_requests = login_config.get('max_requests', self.max_requests)
                        self.window_minutes = login_config.get('window_minutes', self.window_minutes)
        except Exception as e:
            logging.warning(f"Could not load rate limiting config: {e}")
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if request is allowed for client"""
        now = datetime.utcnow()
        window_start = now - timedelta(minutes=self.window_minutes)
        
        # Clean old requests
        if client_id in self.requests:
            self.requests[client_id] = [
                req_time for req_time in self.requests[client_id]
                if req_time > window_start
            ]
        else:
            self.requests[client_id] = []
        
        # Check if under limit
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        
        # Add current request
        self.requests[client_id].append(now)
        return True

# Global rate limiter instance
rate_limiter = RateLimiter()

async def check_rate_limit(request: Request):
    """FastAPI dependency to check rate limiting"""
    try:
        # Extract client IP from request
        client_ip = request.client.host if request.client else "unknown"
        
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
        logger.warning(f"Rate limiting error: {e}")
        return True

def check_rate_limit_simple():
    """Simple rate limiting function that doesn't require any parameters"""
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
        logger.warning(f"Rate limiting error: {e}")
        return True
