"""
Database models for SmartDine Desktop Edition
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    """User model for authentication and role management"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)  # admin, waiter, chef, cashier
    full_name = Column(String(100), nullable=False)
    email = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    orders = relationship("Order", back_populates="waiter")
    bills = relationship("Bill", back_populates="cashier")


class MenuItem(Base):
    """Menu items with categories and pricing"""
    __tablename__ = 'menu_items'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)  # starters, main_course, desserts, beverages
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order_items = relationship("OrderItem", back_populates="menu_item")


class Table(Base):
    """Restaurant tables management"""
    __tablename__ = 'tables'
    
    id = Column(Integer, primary_key=True)
    table_number = Column(Integer, unique=True, nullable=False)
    capacity = Column(Integer, nullable=False)
    status = Column(String(20), default='free')  # free, occupied, served, billed
    current_order_id = Column(Integer, ForeignKey('orders.id'), nullable=True)
    
    # Relationships
    orders = relationship("Order", back_populates="table", foreign_keys="Order.table_id")


class Order(Base):
    """Customer orders"""
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    table_id = Column(Integer, ForeignKey('tables.id'), nullable=False)
    waiter_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(String(20), default='pending')  # pending, cooking, ready, served, cancelled
    total_amount = Column(Float, default=0.0)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    table = relationship("Table", back_populates="orders", foreign_keys=[table_id])
    waiter = relationship("User", back_populates="orders", foreign_keys=[waiter_id])
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan", foreign_keys="OrderItem.order_id")
    bills = relationship("Bill", back_populates="order", foreign_keys="Bill.order_id")


class OrderItem(Base):
    """Individual items within an order"""
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    menu_item_id = Column(Integer, ForeignKey('menu_items.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    special_instructions = Column(Text)
    
    # Relationships
    order = relationship("Order", back_populates="order_items", foreign_keys=[order_id])
    menu_item = relationship("MenuItem", back_populates="order_items", foreign_keys=[menu_item_id])


class Bill(Base):
    """Billing and payment information"""
    __tablename__ = 'bills'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    cashier_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    subtotal = Column(Float, nullable=False)
    tax_rate = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    discount_amount = Column(Float, default=0.0)
    service_charge = Column(Float, default=0.0)
    total_amount = Column(Float, nullable=False)
    payment_method = Column(String(20), nullable=False)  # cash, card, upi
    payment_status = Column(String(20), default='pending')  # pending, paid, refunded
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    order = relationship("Order", back_populates="bills", foreign_keys=[order_id])
    cashier = relationship("User", back_populates="bills", foreign_keys=[cashier_id])
