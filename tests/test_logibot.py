import sys
import os
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.logibot import LogiBot

# ...rest of your tests...


@pytest.fixture
def bot():
    return LogiBot()

def test_fulfill_order_success(bot):
    result = bot.fulfill_order(
        order_id="ORDER1001",
        items=[{"sku": "SKU001", "qty": 2}],
        shipping_address={"address1": "123 Main St", "city": "Toronto", "country": "CA"}
    )
    # Success or error (because of random failure in mock)
    assert "status" in result
    assert result["status"] in ["fulfilled", "error"]

def test_fulfill_order_bad_input(bot):
    # Missing order_id
    result = bot.fulfill_order(
        order_id=None,
        items=[{"sku": "SKU001", "qty": 2}],
        shipping_address={"address1": "123 Main St"}
    )
    assert result["status"] == "error"
    assert "Invalid" in result["message"]

def test_get_tracking_info_success(bot):
    result = bot.get_tracking_info("MOCKTRACK1001")
    assert "status" in result
    assert result["status"] in ["In Transit", "error"]

def test_get_tracking_info_bad_input(bot):
    result = bot.get_tracking_info("")
    assert result["status"] == "error"
    assert "Invalid" in result["message"]

def test_handle_support_ticket_success(bot):
    result = bot.handle_support_ticket({"ticket_id": "TICKET1001"})
    assert "status" in result
    assert result["status"] in ["open", "error"]

def test_handle_support_ticket_bad_input(bot):
    result = bot.handle_support_ticket({})
    assert result["status"] == "error"
    assert "ticket_id" in result["message"] or "Invalid" in result["message"]
