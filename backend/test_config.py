#!/usr/bin/env python
"""Quick test script to debug config loading"""
import sys
print("Python started")
sys.stdout.flush()

print("Importing config...")
sys.stdout.flush()

from app.core.config import settings

print("✅ Config loaded successfully!")
print(f"CORS Origins: {settings.CORS_ORIGINS}")
print(f"Database URL: {settings.DATABASE_URL}")
