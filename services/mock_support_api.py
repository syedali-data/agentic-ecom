import logging
import random
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

def handle_support_ticket(ticket: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mock support API for ticket handling.
    
    Args:
        ticket: Support ticket dictionary containing ticket_id and other details
        
    Returns:
        Dict containing support response and status
    """
    # Input Validation with detailed error messages
    if not ticket or not isinstance(ticket, dict):
        return {"status": "error", "message": "Invalid or missing ticket", "code": "INVALID_TICKET"}
    
    if "ticket_id" not in ticket or not ticket["ticket_id"]:
        return {"status": "error", "message": "Ticket must have ticket_id", "code": "MISSING_TICKET_ID"}
    
    # Validate ticket structure
    required_fields = ['ticket_id', 'subject', 'description']
    missing_fields = [field for field in required_fields if not ticket.get(field)]
    if missing_fields:
        return {"status": "error", "message": f"Missing required ticket fields: {', '.join(missing_fields)}", "code": "INCOMPLETE_TICKET"}

    # Simulate API Failure (10% chance)
    if random.random() < 0.1:
        logging.error("[MOCK] Simulated API failure in support")
        return {"status": "error", "message": "Simulated API failure: support service is down", "code": "SERVICE_UNAVAILABLE"}

    # Simulate processing delay (0.2-1.0 seconds)
    processing_time = random.uniform(0.2, 1.0)
    
    # Generate realistic response based on ticket priority
    priority = ticket.get('priority', 'medium')
    responses = {
        'high': [
            "Thank you for contacting us! This is a high-priority issue and we're addressing it immediately.",
            "We understand this is urgent. Our team is working on this right now.",
            "This high-priority ticket has been escalated to our senior support team."
        ],
        'medium': [
            "Thank you for contacting us! We are reviewing your issue and will respond within 24 hours.",
            "We've received your ticket and our support team will get back to you soon.",
            "Your issue has been logged and is being reviewed by our support specialists."
        ],
        'low': [
            "Thank you for contacting us! We are reviewing your issue.",
            "We've received your inquiry and will respond within 48 hours.",
            "Your ticket has been submitted and is in our queue for review."
        ]
    }
    
    response_text = random.choice(responses.get(priority, responses['medium']))
    
    # Generate realistic status based on priority
    status_options = {
        'high': ['open', 'in_progress'],
        'medium': ['open', 'pending'],
        'low': ['open', 'pending']
    }
    status = random.choice(status_options.get(priority, ['open']))
    
    logging.info(f"[MOCK] Handling support ticket {ticket['ticket_id']} (Priority: {priority}) - Processing time: {processing_time:.2f}s")
    
    return {
        "ticket_id": ticket["ticket_id"],
        "response": response_text,
        "status": status,
        "priority": priority,
        "assigned_to": f"support_agent_{random.randint(1, 10)}",
        "processing_time": processing_time,
        "estimated_resolution": (datetime.now() + timedelta(hours=random.randint(1, 48))).isoformat(),
        "timestamp": datetime.now().isoformat()
    }
