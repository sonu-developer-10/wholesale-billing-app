from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    item_code = Column(String, unique=True, index=True)
    item_name = Column(String)
    category = Column(String)
    set_details = Column(String)
    fix_price_per_set = Column(Float)
    available_sets = Column(Integer)

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String, unique=True)
    address = Column(String, nullable=True)
    balance_due = Column(Float, default=0.0)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    total_amount = Column(Float)
    cash_paid = Column(Float, default=0.0)
    online_paid = Column(Float, default=0.0)
    due_amount = Column(Float, default=0.0)
    delivery_status = Column(String, default="Packed for Delivery")
    created_at = Column(DateTime, default=datetime.utcnow)