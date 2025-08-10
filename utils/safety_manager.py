"""
Safety Manager for Agentic-Ecom
Enforces environment-specific safety measures and prevents accidental production actions.
"""

import os
import yaml
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SafetyManager:
    """Manages safety measures and environment-specific configurations"""
    
    def __init__(self):
        self.config = self._load_environment_config()
        self.current_env = self.config.get('current_environment', 'development')
        self.env_config = self.config['environments'][self.current_env]
        self.logger = self._setup_logger()
        
        # Safety state
        self.daily_spend = 0.0
        self.campaign_count = 0
        self.last_reset = datetime.now().date()
        
        self.logger.info(f"🔒 Safety Manager initialized for {self.current_env} environment")
        self.logger.info(f"💰 Max daily spend: ${self.env_config['features']['budget_limits']}")
        self.logger.info(f"🛡️ Dry run mode: {self.env_config['features']['dry_run']}")
    
    def _load_environment_config(self) -> Dict[str, Any]:
        """Load environment configuration"""
        config_path = "config/environments.yaml"
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            # Fallback to development mode
            return {
                'current_environment': 'development',
                'environments': {
                    'development': {
                        'features': {
                            'dry_run': True,
                            'budget_limits': 0.01,
                            'require_confirmation': True
                        }
                    }
                }
            }
    
    def _setup_logger(self) -> logging.Logger:
        """Setup safety logger"""
        logger = logging.getLogger('safety_manager')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '[%(asctime)s] [SAFETY] [%(levelname)s] %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def check_environment_safety(self, action: str, platform: str = None) -> Dict[str, Any]:
        """Check if an action is safe to perform in current environment"""
        self._reset_daily_counters()
        
        result = {
            'safe': True,
            'reason': None,
            'requires_approval': False,
            'dry_run': False,
            'budget_remaining': 0.0
        }
        
        # Check if kill switch is on
        if self._is_kill_switch_on():
            result['safe'] = False
            result['reason'] = "Kill switch is active"
            return result
        
        # Check budget limits
        max_budget = self.env_config['features']['budget_limits']
        budget_remaining = max_budget - self.daily_spend
        result['budget_remaining'] = budget_remaining
        
        if budget_remaining <= 0:
            result['safe'] = False
            result['reason'] = f"Daily budget limit exceeded (${self.daily_spend} >= ${max_budget})"
            return result
        
        # Check if dry run is required
        if self.env_config['features']['dry_run']:
            result['dry_run'] = True
            result['reason'] = "Dry run mode enabled"
        
        # Check if approval is required
        if self.env_config['features']['require_confirmation']:
            result['requires_approval'] = True
        
        # Platform-specific checks
        if platform and platform in self.config.get('platforms', {}):
            platform_config = self.config['platforms'][platform][self.current_env]
            if platform_config.get('require_approval', False):
                result['requires_approval'] = True
        
        self.logger.info(f"🔍 Safety check for {action}: {'✅ SAFE' if result['safe'] else '❌ BLOCKED'} - {result['reason']}")
        return result
    
    def approve_action(self, action: str, platform: str = None) -> bool:
        """Approve an action (for development/testing)"""
        if self.current_env == 'development':
            self.logger.info(f"✅ Auto-approved {action} in development mode")
            return True
        
        # In staging/production, require manual approval
        print(f"\n🚨 ACTION REQUIRES APPROVAL:")
        print(f"   Action: {action}")
        print(f"   Platform: {platform}")
        print(f"   Environment: {self.current_env}")
        print(f"   Current daily spend: ${self.daily_spend}")
        
        response = input("\n❓ Approve this action? (yes/no): ").lower().strip()
        approved = response in ['yes', 'y']
        
        if approved:
            self.logger.info(f"✅ Action approved by user: {action}")
        else:
            self.logger.warning(f"❌ Action rejected by user: {action}")
        
        return approved
    
    def track_spend(self, amount: float, platform: str = None):
        """Track spending and enforce limits"""
        self._reset_daily_counters()
        
        safety_check = self.check_environment_safety(f"spend_${amount}", platform)
        
        if not safety_check['safe']:
            self.logger.error(f"❌ Spend blocked: {safety_check['reason']}")
            return False
        
        if safety_check['requires_approval']:
            if not self.approve_action(f"spend_${amount}", platform):
                return False
        
        # Apply spend
        if not safety_check['dry_run']:
            self.daily_spend += amount
            self.logger.info(f"💰 Tracked spend: ${amount} (Total: ${self.daily_spend})")
        else:
            self.logger.info(f"🔍 DRY RUN: Would spend ${amount} (Total: ${self.daily_spend})")
        
        return True
    
    def track_campaign_creation(self, platform: str = None) -> bool:
        """Track campaign creation"""
        self.campaign_count += 1
        
        safety_check = self.check_environment_safety("create_campaign", platform)
        
        if not safety_check['safe']:
            self.logger.error(f"❌ Campaign creation blocked: {safety_check['reason']}")
            return False
        
        if safety_check['requires_approval']:
            if not self.approve_action("create_campaign", platform):
                return False
        
        if safety_check['dry_run']:
            self.logger.info(f"🔍 DRY RUN: Would create campaign #{self.campaign_count}")
        else:
            self.logger.info(f"📢 Created campaign #{self.campaign_count}")
        
        return True
    
    def _reset_daily_counters(self):
        """Reset daily counters if date changed"""
        today = datetime.now().date()
        if today != self.last_reset:
            self.daily_spend = 0.0
            self.campaign_count = 0
            self.last_reset = today
            self.logger.info("🔄 Daily counters reset")
    
    def _is_kill_switch_on(self) -> bool:
        """Check if kill switch is active"""
        try:
            with open('status.lock', 'r') as file:
                content = file.read().strip().lower()
                return content in ['stop', 'pause', 'halt']
        except FileNotFoundError:
            return False
    
    def get_safety_status(self) -> Dict[str, Any]:
        """Get current safety status"""
        return {
            'environment': self.current_env,
            'daily_spend': self.daily_spend,
            'max_budget': self.env_config['features']['budget_limits'],
            'budget_remaining': self.env_config['features']['budget_limits'] - self.daily_spend,
            'campaign_count': self.campaign_count,
            'dry_run_mode': self.env_config['features']['dry_run'],
            'kill_switch_active': self._is_kill_switch_on(),
            'requires_approval': self.env_config['features']['require_confirmation']
        }

# Global safety manager instance
safety_manager = SafetyManager()

def require_safety_check(action: str, platform: str = None):
    """Decorator to require safety check before function execution"""
    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            safety_check = safety_manager.check_environment_safety(action, platform)
            
            if not safety_check['safe']:
                from fastapi import HTTPException, status
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Safety check failed: {safety_check['reason']}"
                )
            
            if safety_check['requires_approval']:
                if not safety_manager.approve_action(action, platform):
                    from fastapi import HTTPException, status
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Action not approved by user"
                    )
            
            # Execute function with original arguments
            result = await func(*args, **kwargs)
            
            # Track if it was a dry run
            if safety_check['dry_run']:
                safety_manager.logger.info(f"🔍 DRY RUN completed for {action}")
            
            return result
        
        def sync_wrapper(*args, **kwargs):
            safety_check = safety_manager.check_environment_safety(action, platform)
            
            if not safety_check['safe']:
                raise Exception(f"Safety check failed: {safety_check['reason']}")
            
            if safety_check['requires_approval']:
                if not safety_manager.approve_action(action, platform):
                    raise Exception("Action not approved by user")
            
            # Execute function with original arguments
            result = func(*args, **kwargs)
            
            # Track if it was a dry run
            if safety_check['dry_run']:
                safety_manager.logger.info(f"🔍 DRY RUN completed for {action}")
            
            return result
        
        # Check if the function is async
        import inspect
        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    return decorator 