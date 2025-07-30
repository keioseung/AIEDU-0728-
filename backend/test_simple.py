#!/usr/bin/env python3
"""
간단한 import 테스트
"""

print("🚀 테스트 시작...")

try:
    print("📦 FastAPI import 시도...")
    from fastapi import FastAPI
    print("✅ FastAPI import 성공")
except Exception as e:
    print(f"❌ FastAPI import 실패: {e}")

try:
    print("📦 app.database import 시도...")
    from app.database import engine
    print("✅ app.database import 성공")
except Exception as e:
    print(f"❌ app.database import 실패: {e}")

try:
    print("📦 app.models import 시도...")
    from app.models import User
    print("✅ app.models import 성공")
except Exception as e:
    print(f"❌ app.models import 실패: {e}")

try:
    print("📦 app.auth import 시도...")
    from app.auth import verify_password
    print("✅ app.auth import 성공")
except Exception as e:
    print(f"❌ app.auth import 실패: {e}")

try:
    print("📦 app.api.auth import 시도...")
    from app.api.auth import router
    print("✅ app.api.auth import 성공")
except Exception as e:
    print(f"❌ app.api.auth import 실패: {e}")

print("🏁 테스트 완료") 