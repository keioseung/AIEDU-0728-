from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os

from .api import ai_info, quiz, prompt, base_content, term, auth, logs, system, user_progress

app = FastAPI()

# 환경 변수에서 CORS origins 가져오기
def get_cors_origins():
    # 환경 변수에서 origins 가져오기
    cors_origins_env = os.getenv("CORS_ORIGINS", "")
    if cors_origins_env:
        return [origin.strip() for origin in cors_origins_env.split(",")]
    
    # 기본 origins (개발 환경용)
    default_origins = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://simple-production-b0b3.up.railway.app",
        "https://simple-production-142c.up.railway.app",
    ]
    
    # Railway 환경에서 자동으로 프론트엔드 도메인 추가
    railway_frontend_url = os.getenv("RAILWAY_FRONTEND_URL")
    if railway_frontend_url:
        default_origins.append(railway_frontend_url)
    
    # 개발 환경에서는 모든 origin 허용
    if os.getenv("ENVIRONMENT", "development") == "development":
        default_origins.append("*")
    
    return default_origins

# CORS 설정
origins = get_cors_origins()

# CORS 설정 로그 출력
print(f"🔧 CORS Origins 설정: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# 추가 CORS 헤더를 위한 미들웨어
@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response = await call_next(request)
    
    # CORS 헤더 추가
    origin = request.headers.get("origin")
    if origin:
        response.headers["Access-Control-Allow-Origin"] = origin
    else:
        response.headers["Access-Control-Allow-Origin"] = "*"
    
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
    response.headers["Access-Control-Allow-Headers"] = "*"
    
    return response

# 헬스체크 엔드포인트
@app.get("/")
async def root():
    return {"message": "AI Mastery Hub Backend is running", "status": "healthy", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    try:
        from .database import engine
        import os
        
        # 환경 변수 확인
        database_url = os.getenv("DATABASE_URL", "Not set")
        
        # 데이터베이스 연결 테스트
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            
        # 프롬프트 테이블 확인
        with engine.connect() as conn:
            result = conn.execute("SELECT COUNT(*) FROM prompt")
            prompt_count = result.scalar()
            
        return {
            "status": "healthy", 
            "database": "connected",
            "database_url": database_url[:50] + "..." if len(database_url) > 50 else database_url,
            "prompt_table_count": prompt_count,
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        return {
            "status": "unhealthy", 
            "database": "disconnected", 
            "error": str(e), 
            "database_url": os.getenv("DATABASE_URL", "Not set"),
            "timestamp": "2024-01-01T00:00:00Z"
        }

@app.options("/{path:path}")
async def options_handler(path: str, request: Request):
    """OPTIONS 요청을 명시적으로 처리"""
    origin = request.headers.get("origin", "*")
    
    return JSONResponse(
        content={"message": "OK"},
        headers={
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Max-Age": "86400",
        }
    )

# 전역 예외 처리기
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc), "path": str(request.url)}
    )

# 404 처리기
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={"error": "Not found", "path": str(request.url)}
    )

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(logs.router, prefix="/api/logs", tags=["Activity Logs"])
app.include_router(system.router, prefix="/api/system", tags=["System Management"])
app.include_router(user_progress.router, prefix="/api/user-progress", tags=["User Progress"])
app.include_router(ai_info.router, prefix="/api/ai-info")
app.include_router(quiz.router, prefix="/api/quiz")
app.include_router(prompt.router, prefix="/api/prompt")
app.include_router(base_content.router, prefix="/api/base-content")
app.include_router(term.router, prefix="/api/term") 