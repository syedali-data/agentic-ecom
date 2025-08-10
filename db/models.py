"""
SQLAlchemy ORM models for Agentic-Ecom database.
Defines all database tables with relationships and constraints.
"""

import uuid
from datetime import datetime
from typing import Optional, Dict, List, Any
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, 
    Text, JSON, ForeignKey, Index, Enum as SQLEnum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.declarative import declared_attr
import enum

# Import base from database module
from .database import Base

# Custom UUID type for SQLite compatibility
class GUID(String):
    """Custom UUID type that works with both PostgreSQL and SQLite."""
    def __init__(self):
        super().__init__(36)

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, str):
                return str(value)
            else:
                return value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, str):
                return str(value)
            return value

# Enum definitions
class ProductStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DISCONTINUED = "discontinued"
    OUT_OF_STOCK = "out_of_stock"

class OrderStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class TicketStatus(enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class TicketPriority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class CampaignStatus(enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class AgentType(enum.Enum):
    SALES_GENIE = "sales_genie"
    LOGIBOT = "logibot"
    BUYBOT = "buybot"

class EventType(enum.Enum):
    PRODUCT_CREATED = "product_created"
    PRODUCT_UPDATED = "product_updated"
    ORDER_PLACED = "order_placed"
    ORDER_UPDATED = "order_updated"
    CUSTOMER_CREATED = "customer_created"
    AD_CAMPAIGN_LAUNCHED = "ad_campaign_launched"
    SUPPORT_TICKET_CREATED = "support_ticket_created"
    INVENTORY_UPDATED = "inventory_updated"
    PRICE_CHANGED = "price_changed"

# Base model with common fields
class BaseModel(Base):
    __abstract__ = True
    
    id = Column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

# Product model
class Product(BaseModel):
    __tablename__ = "products"
    
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    sku = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    price = Column(Float, nullable=False)
    cost_price = Column(Float)
    status = Column(SQLEnum(ProductStatus), default=ProductStatus.ACTIVE, nullable=False)
    image_url = Column(String(500))
    supplier_id = Column(String(100))
    supplier_name = Column(String(255))
    tags = Column(JSON)  # List of tags
    product_metadata = Column(JSON)  # Additional product data
    review_count = Column(Integer, default=0)
    average_rating = Column(Float, default=0.0)
    
    # Relationships
    order_items = relationship("OrderItem", back_populates="product")
    ad_campaigns = relationship("AdCampaign", back_populates="product")
    inventory_item = relationship("InventoryItem", back_populates="product", uselist=False)
    pricing_history = relationship("PricingHistory", back_populates="product")
    
    # Indexes
    __table_args__ = (
        Index('idx_products_category_status', 'category', 'status'),
        Index('idx_products_price', 'price'),
        Index('idx_products_rating', 'average_rating'),
    )

# Customer model
class Customer(BaseModel):
    __tablename__ = "customers"
    
    email = Column(String(255), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    address = Column(JSON)  # Shipping/billing address
    preferences = Column(JSON)  # Customer preferences
    total_orders = Column(Integer, default=0)
    total_spent = Column(Float, default=0.0)
    last_order_date = Column(DateTime)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    orders = relationship("Order", back_populates="customer")
    support_tickets = relationship("SupportTicket", back_populates="customer")
    
    # Indexes
    __table_args__ = (
        Index('idx_customers_email', 'email'),
        Index('idx_customers_active', 'is_active'),
    )

# Order model
class Order(BaseModel):
    __tablename__ = "orders"
    
    order_number = Column(String(100), unique=True, nullable=False, index=True)
    customer_id = Column(GUID(), ForeignKey("customers.id"), nullable=False)
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    subtotal = Column(Float, nullable=False)
    tax = Column(Float, default=0.0)
    shipping = Column(Float, default=0.0)
    total = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    shipping_address = Column(JSON)
    billing_address = Column(JSON)
    payment_method = Column(String(50))
    payment_status = Column(String(50))
    tracking_number = Column(String(100))
    notes = Column(Text)
    
    # Relationships
    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")
    
    # Indexes
    __table_args__ = (
        Index('idx_orders_customer_status', 'customer_id', 'status'),
        Index('idx_orders_number', 'order_number'),
        Index('idx_orders_date', 'created_at'),
    )

# Order Item model
class OrderItem(BaseModel):
    __tablename__ = "order_items"
    
    order_id = Column(GUID(), ForeignKey("orders.id"), nullable=False)
    product_id = Column(GUID(), ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    
    # Relationships
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")
    
    # Indexes
    __table_args__ = (
        Index('idx_order_items_order', 'order_id'),
        Index('idx_order_items_product', 'product_id'),
    )

# Support Ticket model
class SupportTicket(BaseModel):
    __tablename__ = "support_tickets"
    
    ticket_number = Column(String(100), unique=True, nullable=False, index=True)
    customer_id = Column(GUID(), ForeignKey("customers.id"), nullable=False)
    subject = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(SQLEnum(TicketStatus), default=TicketStatus.OPEN, nullable=False)
    priority = Column(SQLEnum(TicketPriority), default=TicketPriority.MEDIUM, nullable=False)
    assigned_agent = Column(String(100))
    category = Column(String(100))
    tags = Column(JSON)  # List of tags
    resolution = Column(Text)
    resolved_at = Column(DateTime)
    
    # Relationships
    customer = relationship("Customer", back_populates="support_tickets")
    
    # Indexes
    __table_args__ = (
        Index('idx_tickets_customer_status', 'customer_id', 'status'),
        Index('idx_tickets_priority', 'priority'),
        Index('idx_tickets_number', 'ticket_number'),
    )

# Ad Campaign model
class AdCampaign(BaseModel):
    __tablename__ = "ad_campaigns"
    
    name = Column(String(255), nullable=False)
    platform = Column(String(50), nullable=False)  # facebook, google, etc.
    status = Column(SQLEnum(CampaignStatus), default=CampaignStatus.DRAFT, nullable=False)
    budget = Column(Float, nullable=False)
    daily_budget = Column(Float)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    target_audience = Column(JSON)  # Targeting parameters
    ad_creative = Column(JSON)  # Ad content
    metrics = Column(JSON)  # Performance metrics
    product_id = Column(GUID(), ForeignKey("products.id"))
    
    # Relationships
    product = relationship("Product", back_populates="ad_campaigns")
    
    # Indexes
    __table_args__ = (
        Index('idx_campaigns_platform_status', 'platform', 'status'),
        Index('idx_campaigns_product', 'product_id'),
        Index('idx_campaigns_dates', 'start_date', 'end_date'),
    )

# Inventory Item model
class InventoryItem(BaseModel):
    __tablename__ = "inventory_items"
    
    product_id = Column(GUID(), ForeignKey("products.id"), unique=True, nullable=False)
    quantity = Column(Integer, default=0, nullable=False)
    reserved_quantity = Column(Integer, default=0, nullable=False)
    available_quantity = Column(Integer, default=0, nullable=False)
    low_stock_threshold = Column(Integer, default=10)
    supplier_stock = Column(Integer, default=0)
    
    # Relationships
    product = relationship("Product", back_populates="inventory_item")
    
    # Indexes
    __table_args__ = (
        Index('idx_inventory_product', 'product_id'),
        Index('idx_inventory_available', 'available_quantity'),
    )

# Pricing History model
class PricingHistory(BaseModel):
    __tablename__ = "pricing_history"
    
    product_id = Column(GUID(), ForeignKey("products.id"), nullable=False)
    old_price = Column(Float, nullable=False)
    new_price = Column(Float, nullable=False)
    change_reason = Column(String(255))
    change_type = Column(String(50))  # manual, automatic, etc.
    
    # Relationships
    product = relationship("Product", back_populates="pricing_history")
    
    # Indexes
    __table_args__ = (
        Index('idx_pricing_product', 'product_id'),
        Index('idx_pricing_date', 'created_at'),
    )

# Agent Session model
class AgentSession(BaseModel):
    __tablename__ = "agent_sessions"
    
    session_id = Column(String(100), unique=True, nullable=False, index=True)
    agent_type = Column(SQLEnum(AgentType), nullable=False)
    status = Column(String(50), default="active")  # active, completed, failed
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    duration_seconds = Column(Integer, default=0)
    tasks_completed = Column(Integer, default=0)
    errors_count = Column(Integer, default=0)
    session_metadata = Column(JSON)  # Session-specific data
    
    # Indexes
    __table_args__ = (
        Index('idx_sessions_agent_type', 'agent_type'),
        Index('idx_sessions_status', 'status'),
        Index('idx_sessions_start_time', 'start_time'),
    )

# Audit Log model
class AuditLog(BaseModel):
    __tablename__ = "audit_logs"
    
    user_id = Column(String(100), nullable=False)
    action = Column(String(100), nullable=False)  # create, update, delete
    resource_type = Column(String(50), nullable=False)  # product, order, etc.
    resource_id = Column(String(100), nullable=False)
    old_values = Column(JSON)
    new_values = Column(JSON)
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    
    # Indexes
    __table_args__ = (
        Index('idx_audit_user', 'user_id'),
        Index('idx_audit_action', 'action'),
        Index('idx_audit_resource', 'resource_type', 'resource_id'),
        Index('idx_audit_date', 'created_at'),
    )

# Event Log model
class EventLog(BaseModel):
    __tablename__ = "event_logs"
    
    event_type = Column(SQLEnum(EventType), nullable=False)
    source = Column(String(100), nullable=False)  # api, agent, system
    data = Column(JSON)  # Event-specific data
    processed = Column(Boolean, default=False, nullable=False)
    processed_at = Column(DateTime)
    
    # Indexes
    __table_args__ = (
        Index('idx_events_type', 'event_type'),
        Index('idx_events_source', 'source'),
        Index('idx_events_processed', 'processed'),
        Index('idx_events_date', 'created_at'),
    ) 