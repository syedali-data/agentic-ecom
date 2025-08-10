import logging
import random
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

def get_tracking_info(tracking_number: str) -> Dict[str, Any]:
    """
    Mock tracking API for package tracking information.
    
    Args:
        tracking_number: Package tracking number
        
    Returns:
        Dict containing tracking status, ETA, and history
    """
    # Input Validation with detailed error messages
    if not tracking_number or not isinstance(tracking_number, str):
        return {"status": "error", "message": "Invalid or missing tracking_number", "code": "INVALID_TRACKING_NUMBER"}
    
    # Validate tracking number format (basic validation)
    if len(tracking_number) < 8:
        return {"status": "error", "message": "Invalid tracking number format", "code": "INVALID_TRACKING_FORMAT"}

    # Simulate API Failure (10% chance)
    if random.random() < 0.1:
        logging.error("[MOCK] Simulated API failure in tracking")
        return {"status": "error", "message": "Simulated API failure: tracking service is down", "code": "SERVICE_UNAVAILABLE"}

    # Simulate processing delay (0.1-0.3 seconds)
    processing_time = random.uniform(0.1, 0.3)
    
    # Generate realistic tracking status based on tracking number
    status_options = [
        "In Transit", "Delivered", "Out for Delivery", "Package Received", 
        "In Transit to Next Facility", "Arrived at Destination"
    ]
    status = random.choice(status_options)
    
    # Generate realistic ETA based on status
    if status == "Delivered":
        eta_date = datetime.now() - timedelta(days=random.randint(0, 2))
        eta_status = "Delivered"
    elif status == "Out for Delivery":
        eta_date = datetime.now()
        eta_status = "Today"
    else:
        eta_date = datetime.now() + timedelta(days=random.randint(1, 5))
        eta_status = eta_date.strftime("%Y-%m-%d")
    
    # Generate realistic tracking history
    history = _generate_tracking_history(tracking_number, status)
    
    logging.info(f"[MOCK] Getting tracking info for {tracking_number} (Status: {status}) - Processing time: {processing_time:.2f}s")
    
    return {
        "tracking_number": tracking_number,
        "status": status,
        "eta": eta_status,
        "eta_date": eta_date.strftime("%Y-%m-%d"),
        "carrier": random.choice(["MockCarrier", "MockExpress", "MockShipping"]),
        "history": history,
        "processing_time": processing_time,
        "last_updated": datetime.now().isoformat(),
        "package_weight": f"{random.uniform(0.5, 15.0):.1f} lbs",
        "package_dimensions": f"{random.randint(6, 24)}x{random.randint(4, 18)}x{random.randint(2, 12)} inches"
    }

def _generate_tracking_history(tracking_number: str, current_status: str) -> List[Dict[str, Any]]:
    """
    Generate realistic tracking history based on current status.
    
    Args:
        tracking_number: Package tracking number
        current_status: Current package status
        
    Returns:
        List of tracking history events
    """
    history = []
    base_time = datetime.now() - timedelta(days=random.randint(1, 7))
    
    # Always start with package received
    history.append({
        "timestamp": (base_time - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S"),
        "location": "Origin Facility",
        "status": "Package received",
        "description": "Package received at origin facility"
    })
    
    # Add in-transit events
    if current_status in ["In Transit", "Out for Delivery", "Delivered"]:
        history.append({
            "timestamp": (base_time - timedelta(hours=12)).strftime("%Y-%m-%dT%H:%M:%S"),
            "location": "Sorting Facility",
            "status": "In transit",
            "description": "Package in transit to next facility"
        })
        
        history.append({
            "timestamp": (base_time - timedelta(hours=6)).strftime("%Y-%m-%dT%H:%M:%S"),
            "location": "Destination Facility",
            "status": "Arrived at destination",
            "description": "Package arrived at destination facility"
        })
    
    # Add delivery events
    if current_status in ["Out for Delivery", "Delivered"]:
        history.append({
            "timestamp": (base_time - timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S"),
            "location": "Local Facility",
            "status": "Out for delivery",
            "description": "Package out for delivery"
        })
    
    if current_status == "Delivered":
        history.append({
            "timestamp": base_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "location": "Destination",
            "status": "Delivered",
            "description": "Package delivered to recipient"
        })
    
    return sorted(history, key=lambda x: x["timestamp"])
