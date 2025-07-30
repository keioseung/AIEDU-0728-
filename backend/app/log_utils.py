from sqlalchemy.orm import Session
from typing import Optional
from .models import ActivityLog

def log_activity(
    db: Session,
    action: str,
    details: str = "",
    log_type: str = "user",
    log_level: str = "info",
    user_id: Optional[int] = None,
    username: Optional[str] = None,
    session_id: Optional[str] = None,
    ip_address: Optional[str] = None
):
    """활동 로그를 기록하는 유틸리티 함수"""
    try:
        activity_log = ActivityLog(
            user_id=user_id,
            username=username,
            action=action,
            details=details,
            log_type=log_type,
            log_level=log_level,
            ip_address=ip_address,
            session_id=session_id
        )
        db.add(activity_log)
        db.commit()
        return activity_log
    except Exception as e:
        db.rollback()
        print(f"⚠️ 로그 기록 실패: {str(e)}")
        return None 