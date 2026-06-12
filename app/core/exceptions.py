"""
Cosmic Graph Intelligence - Exceptions

CGI 파이프라인 전반에서 사용하는 커스텀 예외 클래스 모음.
"""

class CGIException(Exception):
    """CGI 시스템의 기본 예외 클래스."""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class LLMTimeoutError(CGIException):
    """LLM API 응답 타임아웃."""
    def __init__(self, message: str = "LLM API 응답 시간이 초과되었습니다."):
        super().__init__(message, status_code=504)


class LLMTokenLimitError(CGIException):
    """LLM API 토큰 제한 초과 또는 Rate Limit 초과."""
    def __init__(self, message: str = "LLM API 토큰 제한 또는 Rate Limit를 초과했습니다."):
        super().__init__(message, status_code=429)


class JSONParsingError(CGIException):
    """LLM 응답에서 JSON 파싱 실패."""
    def __init__(self, message: str = "LLM 응답에서 JSON을 파싱할 수 없습니다."):
        super().__init__(message, status_code=400)


class SecurityError(CGIException):
    """보안/프롬프트 인젝션 감지."""
    def __init__(self, message: str = "악의적인 프롬프트 패턴이 감지되어 요청이 거부되었습니다."):
        super().__init__(message, status_code=403)
