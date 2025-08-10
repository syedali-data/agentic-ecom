"""
Database service layer for Agentic-Ecom.
Provides high-level database operations and business logic.
"""

import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc
from datetime import datetime, timedelta

from db.models import (
    Product, Customer, Order, OrderItem, SupportTicket, 
    AdCampaign, InventoryItem, PricingHistory, AgentSession,
    AuditLog, EventLog, ProductStatus, OrderStatus, TicketStatus,
    TicketPriority, CampaignStatus, AgentType, EventType
)

logger = logging.getLogger(__name__)

class DatabaseService:
    """High-level database service for business operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    # Product operations
    def create_product(self, product_data: Dict[str, Any]) -> Product:
        """Create a new product."""
        try:
            product = Product(**product_data)
            self.db.add(product)
            self.db.commit()
            self.db.refresh(product)
            
            # Log the creation
            self._log_audit("system", "product_created", "product", product.id, 
                           old_values=None, new_values=product_data)
            
            logger.info(f"✅ Product created: {product.name} (ID: {product.id})")
            return product
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error creating product: {e}")
            raise
    
    def get_products(self, 
                    category: Optional[str] = None,
                    status: Optional[ProductStatus] = None,
                    min_price: Optional[float] = None,
                    max_price: Optional[float] = None,
                    limit: int = 100) -> List[Product]:
        """Get products with optional filtering."""
        query = self.db.query(Product)
        
        if category:
            query = query.filter(Product.category == category)
        if status:
            query = query.filter(Product.status == status)
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        
        return query.order_by(desc(Product.created_at)).limit(limit).all()
    
    def get_product_by_id(self, product_id: str) -> Optional[Product]:
        """Get product by ID."""
        return self.db.query(Product).filter(Product.id == product_id).first()
    
    def update_product(self, product_id: str, update_data: Dict[str, Any]) -> Optional[Product]:
        """Update a product."""
        try:
            product = self.get_product_by_id(product_id)
            if not product:
                return None
            
            # Store old values for audit
            old_values = {
                "name": product.name,
                "price": product.price,
                "status": product.status.value if product.status else None
            }
            
            # Update fields
            for key, value in update_data.items():
                if hasattr(product, key):
                    setattr(product, key, value)
            
            self.db.commit()
            self.db.refresh(product)
            
            # Log the update
            self._log_audit("system", "product_updated", "product", product_id,
                           old_values=old_values, new_values=update_data)
            
            logger.info(f"✅ Product updated: {product.name} (ID: {product_id})")
            return product
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error updating product: {e}")
            raise
    
    # Customer operations
    def create_customer(self, customer_data: Dict[str, Any]) -> Customer:
        """Create a new customer."""
        try:
            customer = Customer(**customer_data)
            self.db.add(customer)
            self.db.commit()
            self.db.refresh(customer)
            
            self._log_audit("system", "customer_created", "customer", customer.id,
                           old_values=None, new_values=customer_data)
            
            logger.info(f"✅ Customer created: {customer.email} (ID: {customer.id})")
            return customer
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error creating customer: {e}")
            raise
    
    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        """Get customer by email."""
        return self.db.query(Customer).filter(Customer.email == email).first()
    
    def get_customer_by_id(self, customer_id: str) -> Optional[Customer]:
        """Get customer by ID."""
        return self.db.query(Customer).filter(Customer.id == customer_id).first()
    
    # Order operations
    def create_order(self, order_data: Dict[str, Any], order_items: List[Dict[str, Any]]) -> Order:
        """Create a new order with order items."""
        try:
            # Create order
            order = Order(**order_data)
            self.db.add(order)
            self.db.flush()  # Get the order ID
            
            # Create order items
            for item_data in order_items:
                item_data['order_id'] = order.id
                order_item = OrderItem(**item_data)
                self.db.add(order_item)
            
            self.db.commit()
            self.db.refresh(order)
            
            # Log the order creation
            self._log_event(EventType.ORDER_PLACED, "api", {
                "order_id": order.id,
                "customer_id": order.customer_id,
                "total_amount": order.total
            })
            
            logger.info(f"✅ Order created: {order.order_number} (ID: {order.id})")
            return order
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error creating order: {e}")
            raise
    
    def get_orders_by_customer(self, customer_id: str) -> List[Order]:
        """Get all orders for a customer."""
        return self.db.query(Order).filter(Order.customer_id == customer_id).order_by(desc(Order.created_at)).all()
    
    def update_order_status(self, order_id: str, status: OrderStatus) -> Optional[Order]:
        """Update order status."""
        try:
            order = self.db.query(Order).filter(Order.id == order_id).first()
            if not order:
                return None
            
            old_status = order.status
            order.status = status
            self.db.commit()
            self.db.refresh(order)
            
            # Log the status change
            self._log_event(EventType.ORDER_UPDATED, "system", {
                "order_id": order_id,
                "old_status": old_status.value,
                "new_status": status.value
            })
            
            logger.info(f"✅ Order status updated: {order.order_number} -> {status.value}")
            return order
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error updating order status: {e}")
            raise
    
    # Support ticket operations
    def create_support_ticket(self, ticket_data: Dict[str, Any]) -> SupportTicket:
        """Create a new support ticket."""
        try:
            ticket = SupportTicket(**ticket_data)
            self.db.add(ticket)
            self.db.commit()
            self.db.refresh(ticket)
            
            # Log the ticket creation
            self._log_event(EventType.SUPPORT_TICKET_CREATED, "api", {
                "ticket_id": ticket.id,
                "customer_id": ticket.customer_id,
                "priority": ticket.priority.value
            })
            
            logger.info(f"✅ Support ticket created: {ticket.ticket_number} (ID: {ticket.id})")
            return ticket
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error creating support ticket: {e}")
            raise
    
    def get_tickets_by_status(self, status: TicketStatus) -> List[SupportTicket]:
        """Get tickets by status."""
        return self.db.query(SupportTicket).filter(SupportTicket.status == status).order_by(desc(SupportTicket.created_at)).all()
    
    def get_tickets_by_priority(self, priority: TicketPriority) -> List[SupportTicket]:
        """Get tickets by priority."""
        return self.db.query(SupportTicket).filter(SupportTicket.priority == priority).order_by(desc(SupportTicket.created_at)).all()
    
    # Inventory operations
    def update_inventory(self, product_id: str, quantity_change: int, reason: str = "manual") -> Optional[InventoryItem]:
        """Update inventory quantity."""
        try:
            inventory = self.db.query(InventoryItem).filter(InventoryItem.product_id == product_id).first()
            if not inventory:
                return None
            
            old_quantity = inventory.quantity
            inventory.quantity += quantity_change
            inventory.available_quantity = inventory.quantity - inventory.reserved_quantity
            
            self.db.commit()
            self.db.refresh(inventory)
            
            # Log the inventory update
            self._log_event(EventType.INVENTORY_UPDATED, "system", {
                "product_id": product_id,
                "old_quantity": old_quantity,
                "new_quantity": inventory.quantity,
                "change": quantity_change,
                "reason": reason
            })
            
            logger.info(f"✅ Inventory updated: Product {product_id} -> {inventory.quantity} units")
            return inventory
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error updating inventory: {e}")
            raise
    
    def get_low_stock_products(self) -> List[InventoryItem]:
        """Get products with low stock."""
        return self.db.query(InventoryItem).filter(
            InventoryItem.available_quantity <= InventoryItem.low_stock_threshold
        ).all()
    
    # Agent session operations
    def create_agent_session(self, session_data: Dict[str, Any]) -> AgentSession:
        """Create a new agent session."""
        try:
            session = AgentSession(**session_data)
            self.db.add(session)
            self.db.commit()
            self.db.refresh(session)
            
            logger.info(f"✅ Agent session created: {session.session_id}")
            return session
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error creating agent session: {e}")
            raise
    
    def update_agent_session(self, session_id: str, update_data: Dict[str, Any]) -> Optional[AgentSession]:
        """Update agent session."""
        try:
            session = self.db.query(AgentSession).filter(AgentSession.session_id == session_id).first()
            if not session:
                return None
            
            for key, value in update_data.items():
                if hasattr(session, key):
                    setattr(session, key, value)
            
            self.db.commit()
            self.db.refresh(session)
            
            logger.info(f"✅ Agent session updated: {session_id}")
            return session
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error updating agent session: {e}")
            raise
    
    # Analytics operations
    def get_sales_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get sales analytics for the last N days."""
        start_date = datetime.now() - timedelta(days=days)
        
        # Total orders and revenue
        orders = self.db.query(Order).filter(Order.created_at >= start_date).all()
        total_orders = len(orders)
        total_revenue = sum(order.total for order in orders)
        
        # Orders by status
        status_counts = {}
        for status in OrderStatus:
            count = self.db.query(Order).filter(
                and_(Order.status == status, Order.created_at >= start_date)
            ).count()
            status_counts[status.value] = count
        
        # Top products
        top_products = self.db.query(Product).order_by(desc(Product.review_count)).limit(5).all()
        
        return {
            "period_days": days,
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "average_order_value": total_revenue / total_orders if total_orders > 0 else 0,
            "orders_by_status": status_counts,
            "top_products": [
                {"id": p.id, "name": p.name, "reviews": p.review_count, "rating": p.average_rating}
                for p in top_products
            ]
        }
    
    def get_customer_analytics(self) -> Dict[str, Any]:
        """Get customer analytics."""
        total_customers = self.db.query(Customer).count()
        active_customers = self.db.query(Customer).filter(Customer.is_active == True).count()
        
        # Top customers by spending
        top_customers = self.db.query(Customer).order_by(desc(Customer.total_spent)).limit(10).all()
        
        return {
            "total_customers": total_customers,
            "active_customers": active_customers,
            "inactive_customers": total_customers - active_customers,
            "top_customers": [
                {"id": c.id, "email": c.email, "total_spent": c.total_spent, "orders": c.total_orders}
                for c in top_customers
            ]
        }
    
    # Audit and event logging
    def _log_audit(self, user_id: str, action: str, resource_type: str, resource_id: str,
                   old_values: Optional[Dict] = None, new_values: Optional[Dict] = None):
        """Log an audit event."""
        try:
            audit_log = AuditLog(
                user_id=user_id,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                old_values=old_values,
                new_values=new_values
            )
            self.db.add(audit_log)
            self.db.commit()
        except Exception as e:
            logger.error(f"❌ Error logging audit: {e}")
    
    def _log_event(self, event_type: EventType, source: str, data: Dict[str, Any]):
        """Log a business event."""
        try:
            event_log = EventLog(
                event_type=event_type,
                source=source,
                data=data
            )
            self.db.add(event_log)
            self.db.commit()
        except Exception as e:
            logger.error(f"❌ Error logging event: {e}")
    
    # Database health and maintenance
    def get_database_stats(self) -> Dict[str, int]:
        """Get database statistics."""
        stats = {}
        models = [Product, Customer, Order, SupportTicket, AdCampaign, 
                 InventoryItem, PricingHistory, AgentSession, AuditLog, EventLog]
        
        for model in models:
            try:
                count = self.db.query(model).count()
                stats[model.__tablename__] = count
            except Exception as e:
                logger.error(f"❌ Error getting count for {model.__tablename__}: {e}")
                stats[model.__tablename__] = 0
        
        return stats
    
    def cleanup_old_logs(self, days: int = 90):
        """Clean up old audit and event logs."""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Clean up old audit logs
            audit_deleted = self.db.query(AuditLog).filter(AuditLog.created_at < cutoff_date).delete()
            
            # Clean up old event logs (keep unprocessed ones)
            event_deleted = self.db.query(EventLog).filter(
                and_(EventLog.created_at < cutoff_date, EventLog.processed == True)
            ).delete()
            
            self.db.commit()
            
            logger.info(f"✅ Cleaned up {audit_deleted} audit logs and {event_deleted} event logs")
            return {"audit_logs_deleted": audit_deleted, "event_logs_deleted": event_deleted}
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error cleaning up logs: {e}")
            raise 