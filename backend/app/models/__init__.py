"""
Models Package Initialization
==============================

This file makes the models directory a Python package and provides
convenient imports for all database models.

Import all models here to ensure they are registered with SQLAlchemy Base
before creating tables or running migrations.
"""

from app.models.user import User

# Import other models as they are created
# from app.models.chat import ChatSession
# from app.models.message import Message

# Export all models for easy importing
__all__ = [
    "User",
    # "ChatSession",
    # "Message",
]
