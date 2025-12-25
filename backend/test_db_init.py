#!/usr/bin/env python
"""Test database initialization"""
import sys

print("Step 1: Importing database module...")
sys.stdout.flush()

from app.core import database

print("Step 2: Database module imported successfully")
sys.stdout.flush()

print("Step 3: Calling init_db()...")
sys.stdout.flush()

database.init_db()

print("✅ Database initialized successfully!")
