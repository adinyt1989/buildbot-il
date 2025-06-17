from sqlalchemy import Column, String, Integer, Float, DateTime, Enum, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.ext.declarative import declarative_base
import enum
import uuid
from datetime import datetime

Base = declarative_base()

class UserType(enum.Enum):
    CUSTOMER = "customer"
    SOLO = "solo"
    TEAM = "team"

class SubscriptionType(enum.Enum):
    FREE = "free"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class OrderStatus(enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class User(Base):
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone = Column(String(20), unique=True, nullable=False)
    type = Column(Enum(UserType), nullable=False)
    language = Column(String(2), default='he')
    balance_bc = Column(Float, default=0.0)
    subscription_type = Column(Enum(SubscriptionType), default=SubscriptionType.FREE)
    subscription_expiry = Column(DateTime)
    team_members = Column(ARRAY(UUID))
    created_at = Column(DateTime, default=datetime.utcnow)
    deposit_paid = Column(Boolean, default=False)
    deposit_amount = Column(Float, default=0.0)
    verification_status = Column(Boolean, default=False)
    rating = Column(Float, default=0.0)

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID, nullable=False)
    work_type = Column(String(50))
    budget = Column(Float)
    workers_needed = Column(Integer)
    location = Column(String(100))
    photos = Column(ARRAY(String))
    status = Column(Enum(OrderStatus), default=OrderStatus.DRAFT)
    created_at = Column(DateTime, default=datetime.utcnow)
    requires_deposit = Column(Boolean, default=False)
    deposit_id = Column(UUID)
    chat_id = Column(UUID)
    executor_id = Column(UUID)

class Achievement(Base):
    __tablename__ = 'achievements'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, nullable=False)
    type = Column(String(50), nullable=False)
    award_bc = Column(Float)
    award_date = Column(DateTime, default=datetime.utcnow)
    icon = Column(String(10))
