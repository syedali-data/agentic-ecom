"""
Safety Middleware for FastAPI
Integrates safety manager to gate external writes and ensure secure operations.
"""

import logging
from typing import Dict, Any, Optional, Callable
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from datetime import datetime

# Import safety manager
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.safety_manager import safety_manager, require_safety_check

logger = logging.getLogger(__name__)

class SafetyMiddleware:
    """Middleware to enforce safety measures on API endpoints"""
    
    def __init__(self):
        self.safety_manager = safety_manager
        self.logger = logging.getLogger(__name__)
        
        # Define write operations that require safety checks
        self.write_operations = {
            'POST': {
                '/products/generate-listing': 'generate_product_listing',
                '/trigger/sales-genie': 'trigger_sales_genie',
                '/trigger/salesgenie': 'trigger_salesgenie',
                '/trigger/ad-optimization': 'trigger_ad_optimization',
                '/trigger/logibot': 'trigger_logibot',
                '/trigger/emergency-stop': 'trigger_emergency_stop',
                '/log/automation': 'log_automation_event',
                '/orders/track': 'track_order',
                '/support/chat': 'chat_with_support'
            },
            'PUT': {
                '/products/{product_id}': 'update_product',
                '/orders/{order_id}': 'update_order',
                '/customers/{customer_id}': 'update_customer'
            },
            'DELETE': {
                '/products/{product_id}': 'delete_product',
                '/orders/{order_id}': 'delete_order',
                '/customers/{customer_id}': 'delete_customer'
            }
        }
        
        # Define read operations (for logging)
        self.read_operations = {
            'GET': {
                '/products': 'read_products',
                '/analytics/performance': 'read_analytics',
                '/customers': 'read_customers',
                '/orders': 'read_orders',
                '/support/tickets': 'read_support_tickets'
            }
        }
    
    async def __call__(self, request: Request, call_next: Callable):
        """Process request through safety middleware"""
        
        # Get request details
        method = request.method
        path = request.url.path
        client_ip = request.client.host if request.client else "unknown"
        
        # Log all requests
        self.logger.info(f"🔍 Safety check: {method} {path} from {client_ip}")
        
        # Check if this is a write operation
        if method in self.write_operations:
            for pattern, operation in self.write_operations[method].items():
                if self._path_matches(pattern, path):
                    return await self._handle_write_operation(request, call_next, operation, path)
        
        # Check if this is a read operation (for logging)
        if method in self.read_operations:
            for pattern, operation in self.read_operations[method].items():
                if self._path_matches(pattern, path):
                    self.logger.info(f"📖 Read operation: {operation} from {client_ip}")
                    break
        
        # Continue with normal request processing
        return await call_next(request)
    
    async def _handle_write_operation(self, request: Request, call_next: Callable, operation: str, path: str):
        """Handle write operations with safety checks"""
        
        try:
            # Get safety check result
            safety_check = self.safety_manager.check_environment_safety(operation, self._get_platform_from_path(path))
            
            if not safety_check['safe']:
                self.logger.warning(f"❌ Safety check failed for {operation}: {safety_check['reason']}")
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={
                        "error": "Safety check failed",
                        "reason": safety_check['reason'],
                        "operation": operation,
                        "requires_approval": safety_check['requires_approval'],
                        "dry_run": safety_check['dry_run']
                    }
                )
            
            # Check if approval is required
            if safety_check['requires_approval']:
                if not self._auto_approve_in_development(operation):
                    return JSONResponse(
                        status_code=status.HTTP_403_FORBIDDEN,
                        content={
                            "error": "Action requires approval",
                            "operation": operation,
                            "message": "This action requires manual approval. Please contact an administrator."
                        }
                    )
            
            # Log safety check passed
            self.logger.info(f"🔒 Safety check passed for {operation}")
            
            # Add dry run header if in dry run mode
            if safety_check['dry_run']:
                self.logger.info(f"🔍 DRY RUN MODE: {operation}")
                request.headers.__dict__['_list'].append((b'x-dry-run', b'true'))
            
            # Continue with request
            response = await call_next(request)
            
            # Log completion
            if safety_check['dry_run']:
                self.logger.info(f"🔍 DRY RUN completed for {operation}")
            else:
                self.logger.info(f"✅ Write operation completed: {operation}")
            
            return response
            
        except Exception as e:
            self.logger.error(f"❌ Safety middleware error for {operation}: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "Safety check error",
                    "message": str(e)
                }
            )
    
    def _path_matches(self, pattern: str, path: str) -> bool:
        """Check if path matches pattern (supports simple wildcards)"""
        if pattern == path:
            return True
        
        # Handle simple wildcard patterns like /products/{product_id}
        if '{' in pattern and '}' in pattern:
            # Convert pattern to regex-like matching
            import re
            pattern_regex = pattern.replace('{', '(?P<').replace('}', '>[^/]+)')
            return bool(re.match(pattern_regex, path))
        
        return False
    
    def _get_platform_from_path(self, path: str) -> Optional[str]:
        """Extract platform from path"""
        if 'shopify' in path.lower():
            return 'shopify'
        elif 'meta' in path.lower() or 'facebook' in path.lower():
            return 'meta_ads'
        elif 'pinterest' in path.lower():
            return 'pinterest_ads'
        elif 'google' in path.lower():
            return 'google_ads'
        return None
    
    def _auto_approve_in_development(self, operation: str) -> bool:
        """Auto-approve operations in development mode"""
        current_env = self.safety_manager.current_env
        if current_env == 'development':
            self.logger.info(f"✅ Auto-approved {operation} in development mode")
            return True
        return False

# Global safety middleware instance
safety_middleware = SafetyMiddleware()
