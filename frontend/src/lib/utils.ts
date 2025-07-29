// KST 시간대 유틸리티 함수들

/**
 * 현재 KST 날짜를 YYYY-MM-DD 형식으로 반환
 */
export function getKSTDate(): string {
  const now = new Date()
  const kstOffset = 9 * 60 // KST는 UTC+9
  const utc = now.getTime() + (now.getTimezoneOffset() * 60000)
  const kst = new Date(utc + (kstOffset * 60000))
  return kst.toISOString().split('T')[0]
}

/**
 * 현재 KST 시간을 ISO 문자열로 반환
 */
export function getKSTISOString(): string {
  const now = new Date()
  const kstOffset = 9 * 60 // KST는 UTC+9
  const utc = now.getTime() + (now.getTimezoneOffset() * 60000)
  const kst = new Date(utc + (kstOffset * 60000))
  return kst.toISOString()
}

/**
 * Date 객체를 KST 날짜 문자열로 변환
 */
export function toKSTDateString(date: Date): string {
  const kstOffset = 9 * 60 // KST는 UTC+9
  const utc = date.getTime() + (date.getTimezoneOffset() * 60000)
  const kst = new Date(utc + (kstOffset * 60000))
  return kst.toISOString().split('T')[0]
}

/**
 * KST 기준으로 오늘 날짜인지 확인
 */
export function isToday(dateString: string): boolean {
  return dateString === getKSTDate()
}

/**
 * KST 기준으로 날짜 포맷팅
 */
export function formatKSTDate(dateString: string): string {
  const date = new Date(dateString + 'T00:00:00+09:00') // KST로 파싱
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    timeZone: 'Asia/Seoul'
  })
} 