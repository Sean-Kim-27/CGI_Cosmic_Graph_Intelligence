"""
Cosmic Graph Intelligence - 환경 설정 모듈

.env 파일에서 API 키와 시스템 설정을 로드한다.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """CGI 시스템 전역 설정."""

    openai_api_key: str | None = None
    gemini_api_key: str | None = None
    llm_provider: str = "gemini"  # gemini | codex
    llm_model: str = "gpt-4o"
    codex_workdir: str = "."
    embedding_model: str = "gemini-embedding-2"

    # 비교 테스트
    judge_llm_model: str = "gpt-4o"

    # CGI 파이프라인
    cgi_mode: str = "balanced"  # accurate | balanced | creative | research



    # Pruner Settings
    t_active: float = 0.65
    t_creative: float = 0.40
    t_noise: float = 0.45
    t_survival: float = 0.35
    t_garbage_u: float = 0.25
    t_garbage_c: float = 0.20
    t_garbage_n: float = 0.60
    
    # Wormhole Settings
    t_wormhole_min: float = 0.40
    t_wormhole_max: float = 0.60
    t_wormhole_repulsion: float = 0.30

    # 파이프라인 파라미터
    max_initial_nodes: int = 20
    min_edge_threshold: float = 0.10
    binary_threshold: float = 0.45

    # SQLite-backed CGI memory. Kept bounded at prompt time to avoid latency/token blow-up.
    cgi_memory_enabled: bool = True
    cgi_memory_db_path: str = "./data/cgi_memory.sqlite3"
    cgi_memory_context_limit: int = 18
    cgi_memory_recent_limit: int = 6
    cgi_memory_similar_limit: int = 12

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# 전역 싱글턴
_settings: Settings | None = None


def get_settings() -> Settings:
    """설정 싱글턴을 반환한다."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
