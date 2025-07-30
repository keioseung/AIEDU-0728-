from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import timedelta

from ..database import get_db
from ..models import User, ActivityLog
from ..schemas import UserCreate, UserLogin, UserResponse, Token
from ..auth import verify_password, get_password_hash, create_access_token, get_current_active_user
from ..log_utils import log_activity

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user_data: UserCreate, request: Request, db: Session = Depends(get_db)):
    """사용자 회원가입"""
    # 중복 사용자명 확인
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # 중복 이메일 확인 (이메일이 제공된 경우)
    if user_data.email:
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # 새 사용자 생성
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        role=user_data.role or "user"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # 회원가입 로그 기록
    log_activity(
        db=db,
        action="회원가입",
        details=f"새 사용자가 등록되었습니다. 역할: {user_data.role}",
        log_type="user",
        log_level="info",
        user_id=db_user.id,
        username=db_user.username,
        ip_address=request.client.host if request.client else None
    )
    
    return db_user

@router.post("/login", response_model=Token)
def login_user(user_credentials: UserLogin, request: Request, db: Session = Depends(get_db)):
    """사용자 로그인"""
    try:
        print(f"🔐 로그인 시도 - 사용자명: {user_credentials.username}")
        
        # 사용자 확인
        user = db.query(User).filter(User.username == user_credentials.username).first()
        if not user:
            print(f"❌ 사용자 없음: {user_credentials.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not verify_password(user_credentials.password, user.hashed_password):
            print(f"❌ 비밀번호 불일치: {user_credentials.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        print(f"✅ 사용자 인증 성공: {user.username} (역할: {user.role})")
        
        # is_active 필드는 Supabase 테이블에 없으므로 제거
        
        # 액세스 토큰 생성 (30일)
        access_token_expires = timedelta(minutes=30 * 24 * 60)
        print(f"🔐 토큰 생성 시작 - 만료시간: {access_token_expires}")
        
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        print(f"✅ 토큰 생성 완료 - 길이: {len(access_token)}")
        
        # 로그인 로그 기록
        log_activity(
            db=db,
            action="로그인",
            details=f"사용자가 성공적으로 로그인했습니다. 역할: {user.role}",
            log_type="user",
            log_level="success",
            user_id=user.id,
            username=user.username,
            ip_address=request.client.host if request.client else None
        )
        
        print(f"✅ 로그인 완료: {user.username}")
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ 로그인 중 예외 발생: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """현재 로그인한 사용자 정보 조회"""
    return current_user

@router.get("/users", response_model=list[UserResponse])
def get_all_users(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """모든 사용자 조회 (관리자만)"""
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    users = db.query(User).all()
    return users

@router.put("/users/{user_id}/role")
def update_user_role(
    user_id: int, 
    role_data: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """사용자 역할 변경 (관리자만)"""
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    new_role = role_data.get('role')
    if new_role not in ['user', 'admin']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role"
        )
    
    user.role = new_role
    db.commit()
    
    return {"message": "User role updated successfully"}

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """사용자 삭제 (관리자만)"""
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # 자기 자신은 삭제할 수 없음
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully"} 