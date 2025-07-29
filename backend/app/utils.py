from datetime import datetime, timezone, timedelta

# pytz가 없을 경우를 대비한 fallback
try:
    import pytz
    PYTZ_AVAILABLE = True
except ImportError:
    PYTZ_AVAILABLE = False

def get_kst_now():
    """현재 KST 시간을 반환합니다."""
    if PYTZ_AVAILABLE:
        kst = pytz.timezone('Asia/Seoul')
        return datetime.now(kst)
    else:
        # pytz가 없을 경우 UTC+9로 계산
        utc_now = datetime.now(timezone.utc)
        kst_offset = timezone(timedelta(hours=9))
        return utc_now.astimezone(kst_offset)

def get_kst_date():
    """현재 KST 날짜를 YYYY-MM-DD 형식으로 반환합니다."""
    if PYTZ_AVAILABLE:
        kst = pytz.timezone('Asia/Seoul')
        now = datetime.now(kst)
    else:
        # pytz가 없을 경우 UTC+9로 계산
        utc_now = datetime.now(timezone.utc)
        kst_offset = timezone(timedelta(hours=9))
        now = utc_now.astimezone(kst_offset)
    return now.strftime('%Y-%m-%d')

def get_kst_datetime():
    """현재 KST datetime 객체를 반환합니다."""
    if PYTZ_AVAILABLE:
        kst = pytz.timezone('Asia/Seoul')
        return datetime.now(kst)
    else:
        # pytz가 없을 경우 UTC+9로 계산
        utc_now = datetime.now(timezone.utc)
        kst_offset = timezone(timedelta(hours=9))
        return utc_now.astimezone(kst_offset)

def to_kst_date(date_obj):
    """Date 객체를 KST 날짜 문자열로 변환합니다."""
    if PYTZ_AVAILABLE:
        kst = pytz.timezone('Asia/Seoul')
        if date_obj.tzinfo is None:
            # UTC로 가정하고 KST로 변환
            utc = pytz.utc.localize(date_obj)
            kst_time = utc.astimezone(kst)
        else:
            kst_time = date_obj.astimezone(kst)
    else:
        # pytz가 없을 경우 UTC+9로 계산
        if date_obj.tzinfo is None:
            # UTC로 가정
            utc_time = date_obj.replace(tzinfo=timezone.utc)
        else:
            utc_time = date_obj.astimezone(timezone.utc)
        kst_offset = timezone(timedelta(hours=9))
        kst_time = utc_time.astimezone(kst_offset)
    return kst_time.strftime('%Y-%m-%d')

def parse_kst_date(date_string):
    """날짜 문자열을 KST datetime 객체로 파싱합니다."""
    dt = datetime.strptime(date_string, '%Y-%m-%d')
    if PYTZ_AVAILABLE:
        kst = pytz.timezone('Asia/Seoul')
        return kst.localize(dt)
    else:
        # pytz가 없을 경우 UTC+9로 설정
        kst_offset = timezone(timedelta(hours=9))
        return dt.replace(tzinfo=kst_offset) 