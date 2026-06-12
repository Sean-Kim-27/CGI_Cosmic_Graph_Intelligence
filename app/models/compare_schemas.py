"""
Cosmic Graph Intelligence - 비교 테스트 스키마

CGI vs 일반 LLM 비교 테스트에 사용되는 요청/응답 모델을 정의한다.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


# ──────────────────────────────────────────────
# 요청
# ──────────────────────────────────────────────
class CompareRequest(BaseModel):
    """비교 테스트 요청."""

    question: str
    mode: str = "balanced"  # accurate | balanced | creative | research


class BatchCompareRequest(BaseModel):
    """일괄 비교 테스트 요청."""

    questions: list[str]
    mode: str = "balanced"


# ──────────────────────────────────────────────
# LLM 응답 래퍼
# ──────────────────────────────────────────────
class LLMResponse(BaseModel):
    """LLM 호출 결과."""

    content: str
    model: str
    latency_ms: float = 0.0
    tokens_used: int = 0
    cgi_context_used: str | None = None


# ──────────────────────────────────────────────
# CGI 메타데이터
# ──────────────────────────────────────────────
class CGIMetadata(BaseModel):
    """CGI 파이프라인 실행 결과 메타데이터."""

    nodes_generated: int = 0
    active_nodes: list[str] = Field(default_factory=list)
    orbiting_nodes: list[str] = Field(default_factory=list)
    dormant_nodes: list[str] = Field(default_factory=list)
    binary_systems: list[list[str]] = Field(default_factory=list)
    wormhole_connections: list[list[str]] = Field(default_factory=list)
    pruning_summary: dict[str, int] = Field(default_factory=dict)
    compressed_context: str = ""


# ──────────────────────────────────────────────
# 점수 쌍
# ──────────────────────────────────────────────
class ScorePair(BaseModel):
    """하나의 평가 항목에 대한 direct vs cgi 점수."""

    direct: int = 0  # 1‒10
    cgi: int = 0  # 1‒10


# ──────────────────────────────────────────────
# 비교 분석 결과
# ──────────────────────────────────────────────
class ComparisonAnalysis(BaseModel):
    """Judge LLM 자동 분석 결과."""

    scores: dict[str, ScorePair] = Field(default_factory=dict)
    summary: str = ""
    cgi_advantages: list[str] = Field(default_factory=list)
    direct_advantages: list[str] = Field(default_factory=list)
    key_differences: list[str] = Field(default_factory=list)
    winner: str = "tie"  # cgi | direct | tie
    winner_reason: str = ""


# ──────────────────────────────────────────────
# 최종 비교 응답
# ──────────────────────────────────────────────
class CompareResponse(BaseModel):
    """비교 테스트 전체 응답."""

    question: str
    mode: str

    direct_response: LLMResponse
    cgi_response: LLMResponse
    cgi_metadata: CGIMetadata

    analysis: ComparisonAnalysis

    total_latency_ms: float = 0.0
    timestamp: str = ""
    report_markdown: str = ""
