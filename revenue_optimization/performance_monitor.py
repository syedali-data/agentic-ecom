"""
Performance Monitor for Live Inventory Tracking System
Monitors system performance, gathers feedback, and provides insights.
"""

import logging
import time
import threading
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
import numpy as np

# Try to import psutil, fallback to mock if not available
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("ℹ️  psutil not available, using mock system metrics")

from db.models import EventLog, EventType, Product, InventoryItem
from revenue_optimization.inventory_prediction_engine import InventoryPredictionEngine

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Data class for performance metrics."""
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    response_time: float
    throughput: int
    error_rate: float
    active_connections: int
    inventory_changes: int
    sync_operations: int
    prediction_accuracy: float

@dataclass
class SystemFeedback:
    """Data class for system feedback."""
    timestamp: datetime
    feedback_type: str  # 'performance', 'accuracy', 'usability', 'reliability'
    rating: int  # 1-5 scale
    comment: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None

@dataclass
class PerformanceAlert:
    """Data class for performance alerts."""
    timestamp: datetime
    alert_type: str  # 'high_cpu', 'high_memory', 'slow_response', 'high_error_rate'
    severity: str  # 'low', 'medium', 'high', 'critical'
    message: str
    metrics: Dict[str, Any]
    resolved: bool = False

class LiveInventoryPerformanceMonitor:
    """
    Comprehensive performance monitoring system for Live Inventory Tracking.
    Monitors system performance, gathers feedback, and provides insights.
    """
    
    def __init__(self, db: Session, inventory_engine: InventoryPredictionEngine):
        self.db = db
        self.inventory_engine = inventory_engine
        self.logger = logging.getLogger(__name__)
        
        # Performance tracking
        self._performance_history: List[PerformanceMetrics] = []
        self._feedback_history: List[SystemFeedback] = []
        self._alerts: List[PerformanceAlert] = []
        
        # Monitoring settings
        self._monitoring_enabled = False
        self._monitoring_interval = 60  # seconds
        self._monitoring_thread = None
        self._monitoring_lock = threading.Lock()
        
        # Thresholds
        self._thresholds = {
            "cpu_usage": 80.0,  # 80% CPU usage
            "memory_usage": 85.0,  # 85% memory usage
            "response_time": 5.0,  # 5 seconds
            "error_rate": 5.0,  # 5% error rate
            "prediction_accuracy": 70.0  # 70% accuracy
        }
        
        # Callbacks
        self._alert_callbacks: List[Callable] = []
        self._feedback_callbacks: List[Callable] = []
        
    def start_monitoring(self, interval_seconds: int = 60) -> bool:
        """
        Start performance monitoring.
        
        Args:
            interval_seconds: Monitoring interval in seconds
            
        Returns:
            True if monitoring started successfully
        """
        try:
            if self._monitoring_enabled:
                self.logger.warning("Performance monitoring already enabled")
                return True
            
            self._monitoring_interval = interval_seconds
            self._monitoring_enabled = True
            self._monitoring_thread = threading.Thread(
                target=self._monitoring_loop,
                daemon=True
            )
            self._monitoring_thread.start()
            
            self.logger.info(f"✅ Performance monitoring started (interval: {interval_seconds}s)")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start performance monitoring: {e}")
            return False
    
    def stop_monitoring(self) -> bool:
        """
        Stop performance monitoring.
        
        Returns:
            True if monitoring stopped successfully
        """
        try:
            if not self._monitoring_enabled:
                return True
            
            self._monitoring_enabled = False
            if self._monitoring_thread:
                self._monitoring_thread.join(timeout=5)
            
            self.logger.info("🛑 Performance monitoring stopped")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop performance monitoring: {e}")
            return False
    
    def collect_performance_metrics(self) -> PerformanceMetrics:
        """
        Collect current performance metrics.
        
        Returns:
            PerformanceMetrics object
        """
        try:
            # System metrics
            if PSUTIL_AVAILABLE:
                cpu_usage = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                memory_usage = memory.percent
            else:
                # Mock values when psutil is not available
                cpu_usage = 25.0  # Mock 25% CPU usage
                memory_usage = 45.0  # Mock 45% memory usage
            
            # Application metrics
            response_time = self._measure_response_time()
            throughput = self._calculate_throughput()
            error_rate = self._calculate_error_rate()
            active_connections = self._count_active_connections()
            
            # Inventory-specific metrics
            inventory_changes = self._count_inventory_changes()
            sync_operations = self._count_sync_operations()
            prediction_accuracy = self._calculate_prediction_accuracy()
            
            metrics = PerformanceMetrics(
                timestamp=datetime.now(),
                cpu_usage=cpu_usage,
                memory_usage=memory_usage,
                response_time=response_time,
                throughput=throughput,
                error_rate=error_rate,
                active_connections=active_connections,
                inventory_changes=inventory_changes,
                sync_operations=sync_operations,
                prediction_accuracy=prediction_accuracy
            )
            
            # Store metrics
            with self._monitoring_lock:
                self._performance_history.append(metrics)
                
                # Keep only last 1000 metrics
                if len(self._performance_history) > 1000:
                    self._performance_history = self._performance_history[-1000:]
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error collecting performance metrics: {e}")
            return self._get_default_metrics()
    
    def add_feedback(self, feedback_type: str, rating: int, comment: str, 
                    user_id: str = None, session_id: str = None) -> Dict[str, Any]:
        """
        Add user feedback to the system.
        
        Args:
            feedback_type: Type of feedback (performance, accuracy, usability, reliability)
            rating: Rating from 1-5
            comment: User comment
            user_id: Optional user ID
            session_id: Optional session ID
            
        Returns:
            Feedback result
        """
        try:
            # Validate inputs
            if feedback_type not in ['performance', 'accuracy', 'usability', 'reliability']:
                return {"error": "Invalid feedback_type"}
            
            if not isinstance(rating, int) or rating < 1 or rating > 5:
                return {"error": "Rating must be between 1 and 5"}
            
            if not comment or not isinstance(comment, str):
                return {"error": "Comment is required"}
            
            feedback = SystemFeedback(
                timestamp=datetime.now(),
                feedback_type=feedback_type,
                rating=rating,
                comment=comment,
                user_id=user_id,
                session_id=session_id
            )
            
            # Store feedback
            with self._monitoring_lock:
                self._feedback_history.append(feedback)
                
                # Keep only last 1000 feedback entries
                if len(self._feedback_history) > 1000:
                    self._feedback_history = self._feedback_history[-1000:]
            
            # Notify callbacks
            self._notify_feedback_callbacks(feedback)
            
            # Log feedback
            self.logger.info(f"📝 Feedback received: {feedback_type} - {rating}/5")
            
            return {
                "feedback_id": len(self._feedback_history),
                "feedback_type": feedback_type,
                "rating": rating,
                "timestamp": feedback.timestamp.isoformat(),
                "status": "recorded"
            }
            
        except Exception as e:
            self.logger.error(f"Error adding feedback: {e}")
            return {"error": str(e)}
    
    def get_performance_report(self, hours: int = 24) -> Dict[str, Any]:
        """
        Get comprehensive performance report.
        
        Args:
            hours: Number of hours to analyze
            
        Returns:
            Performance report
        """
        try:
            # Get metrics for the specified time period
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            with self._monitoring_lock:
                recent_metrics = [
                    m for m in self._performance_history 
                    if m.timestamp >= cutoff_time
                ]
            
            if not recent_metrics:
                return {"error": "No performance data available for the specified period"}
            
            # Calculate statistics
            stats = self._calculate_performance_statistics(recent_metrics)
            
            # Get alerts
            alerts = self._get_recent_alerts(hours)
            
            # Get feedback summary
            feedback_summary = self._get_feedback_summary(hours)
            
            # Get recommendations
            recommendations = self._generate_recommendations(stats, alerts, feedback_summary)
            
            return {
                "report_period": f"Last {hours} hours",
                "generated_at": datetime.now().isoformat(),
                "performance_statistics": stats,
                "alerts": alerts,
                "feedback_summary": feedback_summary,
                "recommendations": recommendations,
                "system_health": self._assess_system_health(stats)
            }
            
        except Exception as e:
            self.logger.error(f"Error generating performance report: {e}")
            return {"error": str(e)}
    
    def subscribe_to_alerts(self, callback: Callable[[PerformanceAlert], None]) -> bool:
        """
        Subscribe to performance alerts.
        
        Args:
            callback: Function to call when alert is generated
            
        Returns:
            True if subscription successful
        """
        try:
            if callback not in self._alert_callbacks:
                self._alert_callbacks.append(callback)
                self.logger.info("✅ Alert subscription added")
            return True
        except Exception as e:
            self.logger.error(f"Error subscribing to alerts: {e}")
            return False
    
    def subscribe_to_feedback(self, callback: Callable[[SystemFeedback], None]) -> bool:
        """
        Subscribe to feedback notifications.
        
        Args:
            callback: Function to call when feedback is received
            
        Returns:
            True if subscription successful
        """
        try:
            if callback not in self._feedback_callbacks:
                self._feedback_callbacks.append(callback)
                self.logger.info("✅ Feedback subscription added")
            return True
        except Exception as e:
            self.logger.error(f"Error subscribing to feedback: {e}")
            return False
    
    def _monitoring_loop(self):
        """Main monitoring loop."""
        self.logger.info("🔄 Starting performance monitoring loop")
        
        while self._monitoring_enabled:
            try:
                # Collect metrics
                metrics = self.collect_performance_metrics()
                
                # Check for alerts
                alerts = self._check_for_alerts(metrics)
                for alert in alerts:
                    self._notify_alert_callbacks(alert)
                
                # Wait for next interval
                time.sleep(self._monitoring_interval)
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(self._monitoring_interval)
        
        self.logger.info("🛑 Performance monitoring loop stopped")
    
    def _measure_response_time(self) -> float:
        """Measure average response time for inventory operations."""
        try:
            start_time = time.time()
            
            # Test inventory status query
            self.inventory_engine.get_live_inventory_status()
            
            end_time = time.time()
            return round(end_time - start_time, 3)
            
        except Exception:
            return 0.0
    
    def _calculate_throughput(self) -> int:
        """Calculate operations per minute."""
        try:
            # Count recent events
            cutoff_time = datetime.now() - timedelta(minutes=1)
            recent_events = self.db.query(EventLog).filter(
                EventLog.created_at >= cutoff_time
            ).count()
            
            return recent_events
            
        except Exception:
            return 0
    
    def _calculate_error_rate(self) -> float:
        """Calculate error rate percentage."""
        try:
            # Count recent errors
            cutoff_time = datetime.now() - timedelta(hours=1)
            total_events = self.db.query(EventLog).filter(
                EventLog.created_at >= cutoff_time
            ).count()
            
            error_events = self.db.query(EventLog).filter(
                EventLog.created_at >= cutoff_time,
                EventLog.event_type == EventType.ERROR
            ).count()
            
            if total_events > 0:
                return round((error_events / total_events) * 100, 2)
            return 0.0
            
        except Exception:
            return 0.0
    
    def _count_active_connections(self) -> int:
        """Count active database connections."""
        try:
            # This is a simplified implementation
            # In a real system, you'd query the database for active connections
            return 1
        except Exception:
            return 0
    
    def _count_inventory_changes(self) -> int:
        """Count inventory changes in the last hour."""
        try:
            cutoff_time = datetime.now() - timedelta(hours=1)
            changes = self.db.query(EventLog).filter(
                EventLog.created_at >= cutoff_time,
                EventLog.event_type == EventType.INVENTORY_UPDATED
            ).count()
            
            return changes
            
        except Exception:
            return 0
    
    def _count_sync_operations(self) -> int:
        """Count sync operations in the last hour."""
        try:
            cutoff_time = datetime.now() - timedelta(hours=1)
            syncs = self.db.query(EventLog).filter(
                EventLog.created_at >= cutoff_time,
                EventLog.event_type == EventType.SYNC_COMPLETED
            ).count()
            
            return syncs
            
        except Exception:
            return 0
    
    def _calculate_prediction_accuracy(self) -> float:
        """Calculate prediction accuracy based on recent predictions vs actual."""
        try:
            # This is a simplified implementation
            # In a real system, you'd compare predicted vs actual inventory levels
            return 85.0  # Mock accuracy
        except Exception:
            return 0.0
    
    def _check_for_alerts(self, metrics: PerformanceMetrics) -> List[PerformanceAlert]:
        """Check for performance alerts based on metrics."""
        alerts = []
        
        try:
            # CPU usage alert
            if metrics.cpu_usage > self._thresholds["cpu_usage"]:
                alerts.append(PerformanceAlert(
                    timestamp=datetime.now(),
                    alert_type="high_cpu",
                    severity="high" if metrics.cpu_usage > 90 else "medium",
                    message=f"High CPU usage detected: {metrics.cpu_usage}%",
                    metrics={"cpu_usage": metrics.cpu_usage}
                ))
            
            # Memory usage alert
            if metrics.memory_usage > self._thresholds["memory_usage"]:
                alerts.append(PerformanceAlert(
                    timestamp=datetime.now(),
                    alert_type="high_memory",
                    severity="high" if metrics.memory_usage > 95 else "medium",
                    message=f"High memory usage detected: {metrics.memory_usage}%",
                    metrics={"memory_usage": metrics.memory_usage}
                ))
            
            # Response time alert
            if metrics.response_time > self._thresholds["response_time"]:
                alerts.append(PerformanceAlert(
                    timestamp=datetime.now(),
                    alert_type="slow_response",
                    severity="medium",
                    message=f"Slow response time detected: {metrics.response_time}s",
                    metrics={"response_time": metrics.response_time}
                ))
            
            # Error rate alert
            if metrics.error_rate > self._thresholds["error_rate"]:
                alerts.append(PerformanceAlert(
                    timestamp=datetime.now(),
                    alert_type="high_error_rate",
                    severity="high",
                    message=f"High error rate detected: {metrics.error_rate}%",
                    metrics={"error_rate": metrics.error_rate}
                ))
            
            # Store alerts
            with self._monitoring_lock:
                self._alerts.extend(alerts)
                
                # Keep only last 100 alerts
                if len(self._alerts) > 100:
                    self._alerts = self._alerts[-100:]
            
        except Exception as e:
            self.logger.error(f"Error checking for alerts: {e}")
        
        return alerts
    
    def _calculate_performance_statistics(self, metrics: List[PerformanceMetrics]) -> Dict[str, Any]:
        """Calculate performance statistics from metrics."""
        try:
            if not metrics:
                return {}
            
            # Calculate averages
            avg_cpu = np.mean([m.cpu_usage for m in metrics])
            avg_memory = np.mean([m.memory_usage for m in metrics])
            avg_response_time = np.mean([m.response_time for m in metrics])
            avg_error_rate = np.mean([m.error_rate for m in metrics])
            avg_prediction_accuracy = np.mean([m.prediction_accuracy for m in metrics])
            
            # Calculate totals
            total_inventory_changes = sum(m.inventory_changes for m in metrics)
            total_sync_operations = sum(m.sync_operations for m in metrics)
            total_throughput = sum(m.throughput for m in metrics)
            
            # Calculate trends
            if len(metrics) > 1:
                cpu_trend = self._calculate_trend([m.cpu_usage for m in metrics])
                memory_trend = self._calculate_trend([m.memory_usage for m in metrics])
                response_time_trend = self._calculate_trend([m.response_time for m in metrics])
            else:
                cpu_trend = memory_trend = response_time_trend = "stable"
            
            return {
                "averages": {
                    "cpu_usage": round(avg_cpu, 2),
                    "memory_usage": round(avg_memory, 2),
                    "response_time": round(avg_response_time, 3),
                    "error_rate": round(avg_error_rate, 2),
                    "prediction_accuracy": round(avg_prediction_accuracy, 2)
                },
                "totals": {
                    "inventory_changes": total_inventory_changes,
                    "sync_operations": total_sync_operations,
                    "throughput": total_throughput
                },
                "trends": {
                    "cpu_usage": cpu_trend,
                    "memory_usage": memory_trend,
                    "response_time": response_time_trend
                },
                "sample_size": len(metrics)
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating performance statistics: {e}")
            return {}
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend from a list of values."""
        try:
            if len(values) < 2:
                return "stable"
            
            # Simple linear regression
            x = np.arange(len(values))
            slope = np.polyfit(x, values, 1)[0]
            
            if slope > 0.1:
                return "increasing"
            elif slope < -0.1:
                return "decreasing"
            else:
                return "stable"
                
        except Exception:
            return "stable"
    
    def _get_recent_alerts(self, hours: int) -> List[Dict[str, Any]]:
        """Get recent alerts."""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            with self._monitoring_lock:
                recent_alerts = [
                    alert for alert in self._alerts 
                    if alert.timestamp >= cutoff_time
                ]
            
            return [asdict(alert) for alert in recent_alerts]
            
        except Exception as e:
            self.logger.error(f"Error getting recent alerts: {e}")
            return []
    
    def _get_feedback_summary(self, hours: int) -> Dict[str, Any]:
        """Get feedback summary."""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            with self._monitoring_lock:
                recent_feedback = [
                    f for f in self._feedback_history 
                    if f.timestamp >= cutoff_time
                ]
            
            if not recent_feedback:
                return {"total_feedback": 0, "average_rating": 0}
            
            # Calculate summary
            total_feedback = len(recent_feedback)
            average_rating = np.mean([f.rating for f in recent_feedback])
            
            # Group by feedback type
            feedback_by_type = {}
            for feedback in recent_feedback:
                if feedback.feedback_type not in feedback_by_type:
                    feedback_by_type[feedback.feedback_type] = []
                feedback_by_type[feedback.feedback_type].append(feedback.rating)
            
            # Calculate averages by type
            averages_by_type = {}
            for feedback_type, ratings in feedback_by_type.items():
                averages_by_type[feedback_type] = round(np.mean(ratings), 2)
            
            return {
                "total_feedback": total_feedback,
                "average_rating": round(average_rating, 2),
                "averages_by_type": averages_by_type,
                "feedback_distribution": {
                    "1_star": len([f for f in recent_feedback if f.rating == 1]),
                    "2_star": len([f for f in recent_feedback if f.rating == 2]),
                    "3_star": len([f for f in recent_feedback if f.rating == 3]),
                    "4_star": len([f for f in recent_feedback if f.rating == 4]),
                    "5_star": len([f for f in recent_feedback if f.rating == 5])
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error getting feedback summary: {e}")
            return {"total_feedback": 0, "average_rating": 0}
    
    def _generate_recommendations(self, stats: Dict[str, Any], alerts: List[Dict], 
                                feedback_summary: Dict[str, Any]) -> List[str]:
        """Generate performance recommendations."""
        recommendations = []
        
        try:
            # Performance recommendations
            if stats.get("averages", {}).get("cpu_usage", 0) > 70:
                recommendations.append("Consider scaling up CPU resources or optimizing code efficiency")
            
            if stats.get("averages", {}).get("memory_usage", 0) > 80:
                recommendations.append("Monitor memory usage and consider memory optimization")
            
            if stats.get("averages", {}).get("response_time", 0) > 3:
                recommendations.append("Optimize database queries and consider caching strategies")
            
            if stats.get("averages", {}).get("error_rate", 0) > 2:
                recommendations.append("Investigate error patterns and improve error handling")
            
            # Feedback-based recommendations
            if feedback_summary.get("average_rating", 0) < 3:
                recommendations.append("User satisfaction is low - review system usability and performance")
            
            # Alert-based recommendations
            if any(alert.get("severity") == "high" for alert in alerts):
                recommendations.append("Address high-severity alerts immediately")
            
            if not recommendations:
                recommendations.append("System performance is within acceptable parameters")
            
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {e}")
            recommendations.append("Unable to generate recommendations due to error")
        
        return recommendations
    
    def _assess_system_health(self, stats: Dict[str, Any]) -> str:
        """Assess overall system health."""
        try:
            averages = stats.get("averages", {})
            
            # Check critical metrics
            if (averages.get("cpu_usage", 0) > 90 or 
                averages.get("memory_usage", 0) > 95 or 
                averages.get("error_rate", 0) > 10):
                return "critical"
            
            # Check warning metrics
            if (averages.get("cpu_usage", 0) > 70 or 
                averages.get("memory_usage", 0) > 80 or 
                averages.get("error_rate", 0) > 5):
                return "warning"
            
            return "healthy"
            
        except Exception:
            return "unknown"
    
    def _notify_alert_callbacks(self, alert: PerformanceAlert):
        """Notify alert subscribers."""
        for callback in self._alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                self.logger.error(f"Error in alert callback: {e}")
    
    def _notify_feedback_callbacks(self, feedback: SystemFeedback):
        """Notify feedback subscribers."""
        for callback in self._feedback_callbacks:
            try:
                callback(feedback)
            except Exception as e:
                self.logger.error(f"Error in feedback callback: {e}")
    
    def _get_default_metrics(self) -> PerformanceMetrics:
        """Get default metrics when collection fails."""
        return PerformanceMetrics(
            timestamp=datetime.now(),
            cpu_usage=0.0,
            memory_usage=0.0,
            response_time=0.0,
            throughput=0,
            error_rate=0.0,
            active_connections=0,
            inventory_changes=0,
            sync_operations=0,
            prediction_accuracy=0.0
        ) 