"""
Database Models

Defines all PostgreSQL tables for NeuroBudget.
"""

from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Boolean,
    Date,
    DateTime,
    Text,
)

from sqlalchemy.sql import func

from database.db import BaseModel


# ==========================================================
# Transactions Table
# ==========================================================

class Transaction(BaseModel):

    __tablename__ = "transactions"

    transaction_id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    transaction_date = Column(
        Date,
        nullable=False
    )

    merchant = Column(
        String(255),
        nullable=False
    )

    description = Column(Text)

    amount = Column(
        Float,
        nullable=False
    )

    transaction_type = Column(
        String(20),
        nullable=False
    )

    category = Column(
        String(100),
        nullable=False
    )

    payment_method = Column(
        String(100),
        nullable=False
    )

    account_type = Column(
        String(100),
        nullable=False
    )

    city = Column(
        String(100),
        nullable=False
    )

    balance_after_transaction = Column(
        Float,
        nullable=False
    )

    transaction_month = Column(String(30))

    month_number = Column(Integer)

    day = Column(Integer)

    weekday = Column(String(20))

    quarter = Column(Integer)

    year = Column(Integer)

    is_weekend = Column(Boolean)

    flow = Column(String(30))

    transaction_size = Column(String(30))

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    def __repr__(self):
        return f"<Transaction(id={self.transaction_id}, merchant='{self.merchant}', amount={self.amount})>"


# ==========================================================
# Goals Table
# ==========================================================

class Goal(BaseModel):

    __tablename__ = "goals"

    goal_id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    goal_name = Column(
        String(150),
        nullable=False
    )

    target_amount = Column(
        Float,
        nullable=False
    )

    current_amount = Column(
        Float,
        default=0,
        nullable=False
    )

    deadline_months = Column(
        Integer,
        nullable=False
    )

    monthly_required = Column(Float)

    status = Column(
        String(30),
        default="Active",
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    def __repr__(self):
        return f"<Goal(id={self.goal_id}, goal='{self.goal_name}')>"


# ==========================================================
# Forecast Table
# ==========================================================

class Forecast(BaseModel):

    __tablename__ = "forecasts"

    forecast_id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    prediction_date = Column(
        Date,
        nullable=False
    )

    predicted_expense = Column(
        Float,
        nullable=False
    )

    model_name = Column(
        String(100),
        nullable=False
    )

    confidence_score = Column(
        Float,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    def __repr__(self):
        return f"<Forecast(id={self.forecast_id}, prediction={self.predicted_expense})>"


# ==========================================================
# Reports Table
# ==========================================================

class Report(BaseModel):

    __tablename__ = "reports"

    report_id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    report_type = Column(
        String(100),
        nullable=False
    )

    report_json = Column(
        Text,
        nullable=False
    )

    pdf_path = Column(
        String(500),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    def __repr__(self):
        return f"<Report(id={self.report_id}, type='{self.report_type}')>"


# ==========================================================
# Chat History Table
# ==========================================================

class ChatHistory(BaseModel):

    __tablename__ = "chat_history"

    chat_id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    session_id = Column(
        String(100),
        index=True,
        nullable=False
    )

    user_message = Column(
        Text,
        nullable=False
    )

    ai_response = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    def __repr__(self):
        return f"<Chat(session='{self.session_id}')>"