import logging
import random
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

def fulfill_order(order_id: str, items: List[Dict[str, Any]], shipping_address: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mock fulfillment API for order processing.
    
    Args:
        order_id: Unique order identifier
        items: List of items to fulfill
        shipping_address: Shipping address dictionary
        
    Returns:
        Dict containing fulfillment status and tracking information
    """
    # Input Validation with detailed error messages
    if not order_id or not isinstance(order_id, str):
        return {"status": "error", "message": "Invalid or missing order_id", "code": "INVALID_ORDER_ID"}
    
    if not items or not isinstance(items, list):
        return {"status": "error", "message": "Invalid or missing items", "code": "INVALID_ITEMS"}
    
    if not shipping_address or not isinstance(shipping_address, dict):
        return {"status": "error", "message": "Invalid or missing shipping_address", "code": "INVALID_ADDRESS"}
    
    # Validate required address fields
    required_fields = ['address1', 'city', 'state', 'zip_code', 'country']
    missing_fields = [field for field in required_fields if not shipping_address.get(field)]
    if missing_fields:
        return {"status": "error", "message": f"Missing required address fields: {', '.join(missing_fields)}", "code": "INCOMPLETE_ADDRESS"}

    # Simulate API Failure (10% chance)
    if random.random() < 0.1:
        logging.error("[MOCK] Simulated API failure in fulfillment")
        return {"status": "error", "message": "Simulated API failure: fulfillment service is down", "code": "SERVICE_UNAVAILABLE"}

    # Simulate processing delay (0.1-0.5 seconds)
    processing_time = random.uniform(0.1, 0.5)
    
    # Generate realistic tracking number
    tracking_number = f"MOCKTRACK{order_id[-4:]}{random.randint(1000, 9999)}"
    
    # Generate realistic ETA (2-7 days from now)
    eta_date = datetime.now() + timedelta(days=random.randint(2, 7))
    
    logging.info(f"[MOCK] Fulfilling order {order_id} to {shipping_address.get('address1', 'Unknown')} - Processing time: {processing_time:.2f}s")
    
    return {
        "order_id": order_id,
        "status": "fulfilled",
        "tracking_number": tracking_number,
        "carrier": random.choice(["MockCarrier", "MockExpress", "MockShipping"]),
        "eta": eta_date.strftime("%Y-%m-%d"),
        "processing_time": processing_time,
        "items_fulfilled": len(items),
        "shipping_address": shipping_address,
        "timestamp": datetime.now().isoformat()
    }
