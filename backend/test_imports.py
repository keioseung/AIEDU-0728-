#!/usr/bin/env python3
"""
Import test script to check if all modules can be imported correctly.
"""

import sys
import os

def test_imports():
    """Test all the imports used in main.py"""
    try:
        print("Testing imports...")
        
        # Test basic FastAPI imports
        from fastapi import FastAPI, Request, HTTPException
        from fastapi.middleware.cors import CORSMiddleware
        from fastapi.responses import JSONResponse
        from datetime import datetime
        print("✅ Basic FastAPI imports successful")
        
        # Test app package imports
        from app.api import ai_info, quiz, prompt, base_content, term, auth, logs, system, user_progress
        print("✅ App API imports successful")
        
        # Test database connection
        from app.database import engine
        print("✅ Database engine import successful")
        
        # Test models
        from app.models import Base
        print("✅ Models import successful")
        
        print("🎉 All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1) 