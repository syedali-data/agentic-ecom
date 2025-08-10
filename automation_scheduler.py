#!/usr/bin/env python3
"""
Agentic-Ecom Automation Scheduler
A simple Python-based alternative to n8n for automation workflows.
"""

import schedule
import time
import requests
import json
import logging
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/automation_scheduler.log'),
        logging.StreamHandler()
    ]
)

class AutomationScheduler:
    """Simple automation scheduler for Agentic-Ecom"""
    
    def __init__(self):
        self.api_base_url = "http://localhost:8000"
        self.logger = logging.getLogger(__name__)
        
        # Create logs directory
        Path("logs").mkdir(exist_ok=True)
        
    def check_system_health(self):
        """Check if the system is healthy"""
        try:
            response = requests.get(f"{self.api_base_url}/health", timeout=10)
            if response.status_code == 200:
                self.logger.info("✅ System health check passed")
                return True
            else:
                self.logger.error(f"❌ System health check failed: {response.status_code}")
                return False
        except Exception as e:
            self.logger.error(f"❌ System health check error: {e}")
            return False
    
    def trigger_sales_genie(self):
        """Trigger SalesGenie automation"""
        try:
            response = requests.post(
                f"{self.api_base_url}/trigger/sales-genie",
                params={"action": "generate_products", "count": 3},
                timeout=30
            )
            if response.status_code == 200:
                self.logger.info("✅ SalesGenie triggered successfully")
                return True
            else:
                self.logger.error(f"❌ SalesGenie trigger failed: {response.status_code}")
                return False
        except Exception as e:
            self.logger.error(f"❌ SalesGenie trigger error: {e}")
            return False
    
    def trigger_ad_optimization(self):
        """Trigger ad optimization"""
        try:
            response = requests.post(
                f"{self.api_base_url}/trigger/ad-optimization",
                params={"action": "optimize_campaigns", "platform": "meta_ads"},
                timeout=30
            )
            if response.status_code == 200:
                self.logger.info("✅ Ad optimization triggered successfully")
                return True
            else:
                self.logger.error(f"❌ Ad optimization trigger failed: {response.status_code}")
                return False
        except Exception as e:
            self.logger.error(f"❌ Ad optimization trigger error: {e}")
            return False
    
    def trigger_logibot(self):
        """Trigger LogiBot automation"""
        try:
            response = requests.post(
                f"{self.api_base_url}/trigger/logibot",
                params={"action": "process_support", "priority": "normal"},
                timeout=30
            )
            if response.status_code == 200:
                self.logger.info("✅ LogiBot triggered successfully")
                return True
            else:
                self.logger.error(f"❌ LogiBot trigger failed: {response.status_code}")
                return False
        except Exception as e:
            self.logger.error(f"❌ LogiBot trigger error: {e}")
            return False
    
    def get_analytics(self):
        """Get system analytics"""
        try:
            response = requests.get(f"{self.api_base_url}/analytics/performance", timeout=10)
            if response.status_code == 200:
                analytics = response.json()
                self.logger.info(f"📊 Analytics: {analytics}")
                return analytics
            else:
                self.logger.error(f"❌ Analytics fetch failed: {response.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"❌ Analytics fetch error: {e}")
            return None
    
    def emergency_stop(self):
        """Trigger emergency stop"""
        try:
            response = requests.post(
                f"{self.api_base_url}/trigger/emergency-stop",
                params={"reason": "Automated safety check", "threshold": "80%"},
                timeout=10
            )
            if response.status_code == 200:
                self.logger.warning("🚨 Emergency stop triggered")
                return True
            else:
                self.logger.error(f"❌ Emergency stop failed: {response.status_code}")
                return False
        except Exception as e:
            self.logger.error(f"❌ Emergency stop error: {e}")
            return False
    
    def daily_maintenance(self):
        """Daily maintenance routine"""
        self.logger.info("🔄 Starting daily maintenance routine")
        
        # Check system health
        if not self.check_system_health():
            self.logger.error("❌ System health check failed, skipping maintenance")
            return
        
        # Get analytics
        analytics = self.get_analytics()
        
        # Trigger optimizations based on analytics
        if analytics:
            # Example: Trigger ad optimization if performance is low
            if analytics.get('total_products', 0) < 10:
                self.trigger_sales_genie()
            
            # Example: Trigger ad optimization if spend is high
            if analytics.get('total_spend', 0) > 100:
                self.trigger_ad_optimization()
        
        # Always process support tickets
        self.trigger_logibot()
        
        self.logger.info("✅ Daily maintenance completed")
    
    def hourly_check(self):
        """Hourly system check"""
        self.logger.info("⏰ Hourly system check")
        
        if not self.check_system_health():
            self.logger.error("❌ System health check failed")
            # Could trigger emergency stop here if needed
            return
        
        # Get current analytics
        analytics = self.get_analytics()
        if analytics:
            self.logger.info(f"📈 Current stats: {analytics}")
    
    def setup_schedule(self):
        """Setup the automation schedule"""
        # Daily maintenance at 9 AM
        schedule.every().day.at("09:00").do(self.daily_maintenance)
        
        # Hourly health checks
        schedule.every().hour.do(self.hourly_check)
        
        # Weekly deep optimization on Sundays at 2 AM
        schedule.every().sunday.at("02:00").do(self.trigger_ad_optimization)
        
        self.logger.info("📅 Automation schedule configured:")
        self.logger.info("   - Daily maintenance: 9:00 AM")
        self.logger.info("   - Hourly health checks: Every hour")
        self.logger.info("   - Weekly optimization: Sundays 2:00 AM")
    
    def run(self):
        """Run the automation scheduler"""
        self.logger.info("🚀 Starting Agentic-Ecom Automation Scheduler")
        
        # Setup schedule
        self.setup_schedule()
        
        # Initial health check
        if not self.check_system_health():
            self.logger.error("❌ Initial health check failed. Please ensure the API server is running.")
            return
        
        self.logger.info("✅ Initial health check passed. Scheduler is running...")
        self.logger.info("💡 Press Ctrl+C to stop the scheduler")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            self.logger.info("🛑 Automation scheduler stopped by user")
        except Exception as e:
            self.logger.error(f"❌ Scheduler error: {e}")

def main():
    """Main function"""
    scheduler = AutomationScheduler()
    scheduler.run()

if __name__ == "__main__":
    main() 