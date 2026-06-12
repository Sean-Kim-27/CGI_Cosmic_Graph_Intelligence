"""
Cosmic Graph Intelligence - Security Utilities

프롬프트 인젝션 및 탈옥(Jailbreak) 방지를 위한 입력값 정제 유틸리티.
"""

import re
from app.core.exceptions import SecurityError
from app.utils.logger import get_logger

log = get_logger("security")

# 프롬프트 인젝션을 유도하는 위험한 키워드 패턴 (대소문자 무관)
DANGEROUS_PATTERNS = [
    r"ignore\s+(all\s+)?(previous\s+)?instructions",
    r"disregard\s+(all\s+)?(previous\s+)?instructions",
    r"forget\s+(all\s+)?(previous\s+)?instructions",
    r"system\s+prompt",
    r"you\s+are\s+now",
    r"bypass",
    r"jailbreak",
    r" DAN ",  # Do Anything Now
    r"<system>",
    r"</system>",
    r"roleplay",
]

DANGEROUS_REGEX = re.compile("|".join(DANGEROUS_PATTERNS), re.IGNORECASE)

def sanitize_input(user_input: str) -> str:
    """
    사용자 입력에서 악의적인 프롬프트 인젝션 패턴을 필터링한다.
    의심스러운 패턴이 발견되면 SecurityError를 발생시킨다.
    """
    if not user_input or not isinstance(user_input, str):
        return ""
    
    # 1. 의심스러운 패턴 검사
    if DANGEROUS_REGEX.search(user_input):
        log.warning("프롬프트 인젝션 의심 패턴 감지: %s", user_input)
        raise SecurityError("입력에 허용되지 않는 키워드나 프롬프트 조작 패턴이 포함되어 있습니다.")
    
    # 2. XSS 및 이스케이프 문자 등 특수문자 제한 (필요 시 추가)
    # user_input = user_input.replace("```", "")
    
    return user_input.strip()
