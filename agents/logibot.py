import sys
import os
import uuid
import logging
from dotenv import load_dotenv
from anthropic import Anthropic

# --- Add project root for imports ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.log_rotation import get_rotating_file_handler

# --- Session ID Formatter for Logging ---
class SessionIDLogFormatter(logging.Formatter):
    def __init__(self, session_id, fmt=None, datefmt=None, style='%'):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        self.session_id = session_id

    def format(self, record):
        record.session_id = self.session_id
        return super().format(record)

# --- Generate a Unique Session/Run ID ---
SESSION_ID = str(uuid.uuid4())

# --- Logging Setup with Rotation ---
log_format = "%(asctime)s [%(levelname)s] [Session:%(session_id)s] %(message)s"
formatter = SessionIDLogFormatter(SESSION_ID, fmt=log_format)

os.makedirs("logs/logibot", exist_ok=True)
file_handler = get_rotating_file_handler("logs/logibot/logibot.log", when="midnight", backup_count=14)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger = logging.getLogger("logibot")
logger.setLevel(logging.INFO)
logger.handlers = []  # Clear duplicate handlers
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# --- NDJSON Agent Event Logger ---
LOG_JSON_PATH = "logs/logibot/logibot_log.json"
def log_action(agent, action, detail=None, level="INFO", **kwargs):
    import datetime, json
    timestamp = datetime.datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "level": level,
        "agent": agent,
        "action": action,
        "detail": detail,
        "session_id": SESSION_ID,
        **kwargs
    }
    # Print to console (optional)
    print(f"[{timestamp}] [{level}] {agent} | {action} | {detail}")
    # NDJSON log (one JSON per line, pandas-friendly)
    with open(LOG_JSON_PATH, "a") as jsonf:
        jsonf.write(json.dumps(log_entry) + "\n")

# --- Load Environment Variables ---
load_dotenv()
API_MODE = os.getenv("LOGIBOT_API_MODE", "mock")

# --- Initialize Claude Client ---
claude_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
logger.info("Claude API client initialized successfully")

# --- Kill Switch Helper ---
def is_kill_switch_on():
    root = os.path.dirname(os.path.dirname(__file__))
    return os.path.exists(os.path.join(root, "status.lock"))

# --- Import Your Mock API Services ---
from services.mock_fulfillment_api import fulfill_order as mock_fulfill_order
from services.mock_tracking_api import get_tracking_info as mock_get_tracking_info
from services.mock_support_api import handle_support_ticket as mock_handle_support_ticket

# --- Main LogiBot Agent ---
class LogiBot:
    def __init__(self):
        self.api_mode = API_MODE

    def fulfill_order(self, order_id, items, shipping_address):
        if is_kill_switch_on():
            logger.warning("Kill switch is ON. Aborting fulfillment operation.")
            log_action("LogiBot", "KillSwitch", "Fulfillment paused by kill switch", level="WARNING")
            return {"status": "error", "message": "System paused by kill switch."}
        try:
            if self.api_mode == "mock":
                result = mock_fulfill_order(order_id, items, shipping_address)
            else:
                raise NotImplementedError("Live fulfillment not implemented.")

            if isinstance(result, dict) and result.get("status") == "error":
                logger.error(f"Fulfillment failed: {result.get('message')}")
                log_action("LogiBot", "FulfillmentFailed", result.get('message'), level="ERROR")
                return result
            logger.info(f"Order fulfilled: {order_id}")
            log_action("LogiBot", "OrderFulfilled", f"Order ID: {order_id}")
            return result
        except Exception as e:
            logger.error(f"Fulfillment exception: {e}")
            log_action("LogiBot", "FulfillmentException", str(e), level="ERROR")
            return {"status": "error", "message": str(e)}

    def get_tracking_info(self, tracking_number):
        if is_kill_switch_on():
            logger.warning("Kill switch is ON. Aborting tracking operation.")
            log_action("LogiBot", "KillSwitch", "Tracking paused by kill switch", level="WARNING")
            return {"status": "error", "message": "System paused by kill switch."}
        try:
            if self.api_mode == "mock":
                result = mock_get_tracking_info(tracking_number)
            else:
                raise NotImplementedError("Live tracking not implemented.")

            if isinstance(result, dict) and result.get("status") == "error":
                logger.error(f"Tracking failed: {result.get('message')}")
                log_action("LogiBot", "TrackingFailed", result.get('message'), level="ERROR")
                return result
            logger.info(f"Tracking fetched for: {tracking_number}")
            log_action("LogiBot", "TrackingFetched", f"Tracking Number: {tracking_number}")
            return result
        except Exception as e:
            logger.error(f"Tracking exception: {e}")
            log_action("LogiBot", "TrackingException", str(e), level="ERROR")
            return {"status": "error", "message": str(e)}

    def handle_support_ticket(self, ticket):
        if is_kill_switch_on():
            logger.warning("Kill switch is ON. Aborting support operation.")
            log_action("LogiBot", "KillSwitch", "Support paused by kill switch", level="WARNING")
            return {"status": "error", "message": "System paused by kill switch."}
        try:
            # Use Claude for intelligent support responses
            support_response = self._generate_support_response(ticket)
            
            if self.api_mode == "mock":
                result = mock_handle_support_ticket(ticket)
                # Enhance mock response with AI-generated content
                result["ai_response"] = support_response
            else:
                raise NotImplementedError("Live support not implemented.")

            if isinstance(result, dict) and result.get("status") == "error":
                logger.error(f"Support ticket failed: {result.get('message')}")
                log_action("LogiBot", "SupportTicketFailed", result.get('message'), level="ERROR")
                return result
            logger.info(f"Support ticket handled: {ticket.get('ticket_id')}")
            log_action("LogiBot", "SupportTicketHandled", f"Ticket ID: {ticket.get('ticket_id')}")
            return result
        except Exception as e:
            logger.error(f"Support exception: {e}")
            log_action("LogiBot", "SupportException", str(e), level="ERROR")
            return {"status": "error", "message": str(e)}

    def _generate_support_response(self, ticket):
        """Use Claude Sonnet 4 to generate intelligent support responses"""
        try:
            prompt = f"""
            You are a professional e-commerce customer support agent. A customer has submitted a support ticket with the following details:
            
            Ticket ID: {ticket.get('ticket_id')}
            Customer Email: {ticket.get('customer_email')}
            Message: {ticket.get('message')}
            
            Please provide a helpful, professional, and empathetic response that:
            1. Acknowledges their concern
            2. Provides clear, actionable information
            3. Maintains a positive tone
            4. Follows e-commerce best practices
            
            Response should be 2-3 sentences maximum.
            """
            
            response = claude_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=150,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
        except Exception as e:
            logger.error(f"Claude support response generation failed: {e}")
            return "Thank you for contacting us. We're looking into your request and will get back to you soon."

    def analyze_fraud_patterns(self, order_data):
        """Use Claude to analyze potential fraud patterns"""
        try:
            prompt = f"""
            Analyze this order for potential fraud indicators:
            
            Order Data: {order_data}
            
            Consider:
            1. Unusual shipping address patterns
            2. Suspicious payment methods
            3. Order value vs customer history
            4. Geographic risk factors
            5. Timing patterns
            
            Return: "SAFE", "SUSPICIOUS", or "HIGH_RISK" with brief reasoning.
            """
            
            response = claude_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=100,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
        except Exception as e:
            logger.error(f"Claude fraud analysis failed: {e}")
            return "SAFE - Analysis unavailable"

    def optimize_fulfillment_process(self, order_history):
        """Use Claude to optimize fulfillment workflows"""
        try:
            prompt = f"""
            Analyze this order fulfillment history and suggest optimizations:
            
            Order History: {order_history}
            
            Focus on:
            1. Common delays or issues
            2. Process bottlenecks
            3. Customer satisfaction patterns
            4. Cost optimization opportunities
            
            Provide 2-3 specific, actionable recommendations.
            """
            
            response = claude_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=200,
                temperature=0.5,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
        except Exception as e:
            logger.error(f"Claude process optimization failed: {e}")
            return "Process optimization analysis unavailable"

# --- Script Entrypoint ---
if __name__ == "__main__":
    logger.info("LogiBot session started.")
    bot = LogiBot()
    order_result = bot.fulfill_order(
        order_id="ORDER1234",
        items=[{"sku": "SKU001", "qty": 1}],
        shipping_address={"address1": "123 Main St", "city": "Toronto", "country": "CA"}
    )
    print("Fulfillment Result:", order_result)

    # Only fetch tracking if fulfillment was successful
    tracking_num = order_result.get("tracking_number", "MOCKTRACK1234")
    track_result = bot.get_tracking_info(tracking_num)
    print("Tracking Info:", track_result)

    support_result = bot.handle_support_ticket({
        "ticket_id": "TICKET5678",
        "customer_email": "customer@email.com",
        "message": "Where is my order?"
    })
    print("Support Ticket:", support_result)

    logger.info("LogiBot session finished.")
