import asyncio
import json
import logging
from typing import Dict, Any, List, Callable, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)

class EventType(str, Enum):
    # SalesGenie events
    PRODUCT_RESEARCHED = "product_researched"
    LISTING_GENERATED = "listing_generated"
    AD_CREATED = "ad_created"
    COMPLIANCE_CHECKED = "compliance_checked"
    
    # LogiBot events
    ORDER_FULFILLED = "order_fulfilled"
    TRACKING_UPDATED = "tracking_updated"
    SUPPORT_TICKET_CREATED = "support_ticket_created"
    FRAUD_DETECTED = "fraud_detected"
    
    # BuyBot events
    CUSTOMER_QUERY = "customer_query"
    PRODUCT_RECOMMENDATION = "product_recommendation"
    
    # System events
    AGENT_STARTED = "agent_started"
    AGENT_STOPPED = "agent_stopped"
    ERROR_OCCURRED = "error_occurred"
    KILL_SWITCH_ENGAGED = "kill_switch_engaged"

@dataclass
class Event:
    id: str
    type: EventType
    source: str
    data: Dict[str, Any]
    timestamp: datetime
    session_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class EventBus:
    """Central event bus for cross-agent communication"""
    
    def __init__(self):
        self.subscribers: Dict[EventType, List[Callable]] = {}
        self.event_history: List[Event] = []
        self.max_history = 1000
        logger.info("Event bus initialized")
    
    def subscribe(self, event_type: EventType, callback: Callable[[Event], None]):
        """Subscribe to an event type"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
        logger.info(f"Subscribed to {event_type}")
    
    def unsubscribe(self, event_type: EventType, callback: Callable[[Event], None]):
        """Unsubscribe from an event type"""
        if event_type in self.subscribers:
            if callback in self.subscribers[event_type]:
                self.subscribers[event_type].remove(callback)
                logger.info(f"Unsubscribed from {event_type}")
    
    def publish(self, event: Event):
        """Publish an event to all subscribers"""
        try:
            # Add to history
            self.event_history.append(event)
            if len(self.event_history) > self.max_history:
                self.event_history.pop(0)
            
            # Notify subscribers
            if event.type in self.subscribers:
                for callback in self.subscribers[event.type]:
                    try:
                        callback(event)
                    except Exception as e:
                        logger.error(f"Error in event callback: {e}")
            
            logger.info(f"Published event: {event.type} from {event.source}")
            
        except Exception as e:
            logger.error(f"Error publishing event: {e}")
    
    def publish_simple(self, event_type: EventType, source: str, data: Dict[str, Any], session_id: Optional[str] = None):
        """Publish a simple event with auto-generated ID and timestamp"""
        import uuid
        event = Event(
            id=str(uuid.uuid4()),
            type=event_type,
            source=source,
            data=data,
            timestamp=datetime.utcnow(),
            session_id=session_id
        )
        self.publish(event)
    
    def get_events_by_type(self, event_type: EventType, limit: int = 100) -> List[Event]:
        """Get recent events of a specific type"""
        events = [e for e in self.event_history if e.type == event_type]
        return events[-limit:]
    
    def get_events_by_source(self, source: str, limit: int = 100) -> List[Event]:
        """Get recent events from a specific source"""
        events = [e for e in self.event_history if e.source == source]
        return events[-limit:]
    
    def get_events_by_session(self, session_id: str, limit: int = 100) -> List[Event]:
        """Get recent events from a specific session"""
        events = [e for e in self.event_history if e.session_id == session_id]
        return events[-limit:]
    
    def clear_history(self):
        """Clear event history"""
        self.event_history.clear()
        logger.info("Event history cleared")

# Global event bus instance
event_bus = EventBus()

# Convenience functions for common events
def publish_product_researched(product_data: Dict[str, Any], source: str, session_id: Optional[str] = None):
    """Publish product research event"""
    event_bus.publish_simple(
        EventType.PRODUCT_RESEARCHED,
        source,
        {"product": product_data},
        session_id
    )

def publish_listing_generated(product_name: str, listing: str, source: str, session_id: Optional[str] = None):
    """Publish listing generation event"""
    event_bus.publish_simple(
        EventType.LISTING_GENERATED,
        source,
        {"product_name": product_name, "listing": listing},
        session_id
    )

def publish_order_fulfilled(order_id: str, tracking_number: str, source: str, session_id: Optional[str] = None):
    """Publish order fulfillment event"""
    event_bus.publish_simple(
        EventType.ORDER_FULFILLED,
        source,
        {"order_id": order_id, "tracking_number": tracking_number},
        session_id
    )

def publish_support_ticket(ticket_id: str, customer_message: str, source: str, session_id: Optional[str] = None):
    """Publish support ticket event"""
    event_bus.publish_simple(
        EventType.SUPPORT_TICKET_CREATED,
        source,
        {"ticket_id": ticket_id, "customer_message": customer_message},
        session_id
    )

def publish_fraud_detected(order_data: Dict[str, Any], risk_level: str, source: str, session_id: Optional[str] = None):
    """Publish fraud detection event"""
    event_bus.publish_simple(
        EventType.FRAUD_DETECTED,
        source,
        {"order_data": order_data, "risk_level": risk_level},
        session_id
    )

def publish_customer_query(query: str, response: str, source: str, session_id: Optional[str] = None):
    """Publish customer query event"""
    event_bus.publish_simple(
        EventType.CUSTOMER_QUERY,
        source,
        {"query": query, "response": response},
        session_id
    )

def publish_error(error_message: str, source: str, session_id: Optional[str] = None):
    """Publish error event"""
    event_bus.publish_simple(
        EventType.ERROR_OCCURRED,
        source,
        {"error_message": error_message},
        session_id
    ) 