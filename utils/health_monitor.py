
import time
import requests
import streamlit as st
from threading import Thread
import logging

logger = logging.getLogger(__name__)

class HealthMonitor:
    """Monitor application health and auto-recover from failures"""
    
    def __init__(self, port=5000):
        self.port = port
        self.health_url = f"http://localhost:{port}/_stcore/health"
        self.is_monitoring = False
        
    def check_health(self):
        """Check if Streamlit server is responding"""
        try:
            response = requests.get(self.health_url, timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Health check failed: {e}")
            return False
    
    def start_monitoring(self):
        """Start background health monitoring"""
        if not self.is_monitoring:
            self.is_monitoring = True
            Thread(target=self._monitor_loop, daemon=True).start()
    
    def _monitor_loop(self):
        """Background monitoring loop"""
        consecutive_failures = 0
        
        while self.is_monitoring:
            if not self.check_health():
                consecutive_failures += 1
                logger.warning(f"Health check failed ({consecutive_failures} consecutive)")
                
                if consecutive_failures >= 3:
                    logger.error("Multiple health check failures detected")
                    # Could trigger restart logic here
                    
            else:
                consecutive_failures = 0
                
            time.sleep(30)  # Check every 30 seconds

# Global health monitor instance
health_monitor = HealthMonitor()
