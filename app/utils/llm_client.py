"""
Cosmic Graph Intelligence - LLM 클라이언트

Google Gemini API를 캡슐화한 비동기 클라이언트.
텍스트 생성, 임베딩, 응답 메타데이터 수집을 담당한다.
"""

from __future__ import annotations

import json
import time
from typing import Any

from google import genai
from google.genai import types

from app.models.config import get_settings
from app.utils.logger import get_logger

log = get_logger("llm_client")

_client: genai.Client | None = None


def _get_client() -> genai.Client:
    """Gemini 클라이언트 싱글턴."""
    global _client
    if _client is None:
        settings = get_settings()
        _client = genai.Client(api_key=settings.gemini_api_key)
    return _client


# ──────────────────────────────────────────────
# 텍스트 생성
# ──────────────────────────────────────────────
async def generate_completion(
    prompt: str,
    *,
    system_prompt: str = "",
    model: str | None = None,
    temperature: float = 0.7,
    max_tokens: int = 8192,
) -> dict[str, Any]:
    """
    LLM에 프롬프트를 보내고 응답을 반환한다.

    Returns:
        {
            "content": str,
            "model": str,
            "latency_ms": float,
            "tokens_used": int,
        }
    """
    settings = get_settings()
    model = model or settings.llm_model
    client = _get_client()

    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_tokens,
    )
    if system_prompt:
        config.system_instruction = system_prompt

    t0 = time.perf_counter()
    response = await client.aio.models.generate_content(
        model=model,
        contents=prompt,
        config=config,
    )
    latency_ms = (time.perf_counter() - t0) * 1000

    content = response.text or ""
    tokens_used = 0
    if response.usage_metadata:
        tokens_used = response.usage_metadata.total_token_count or 0

    result = {
        "content": content,
        "model": model,
        "latency_ms": round(latency_ms, 1),
        "tokens_used": tokens_used,
    }
    log.info(
        "LLM 완료  model=%s  tokens=%s  latency=%.0fms",
        model,
        result["tokens_used"],
        latency_ms,
    )
    return result


# ──────────────────────────────────────────────
# 임베딩
# ──────────────────────────────────────────────
async def generate_embeddings(
    texts: list[str],
    *,
    model: str | None = None,
) -> list[list[float]]:
    """텍스트 목록의 임베딩 벡터를 반환한다."""
    settings = get_settings()
    model = model or settings.embedding_model
    client = _get_client()

    embeddings: list[list[float]] = []
    # Gemini embed_content는 개별 호출
    for text in texts:
        response = await client.aio.models.embed_content(
            model=model,
            contents=text,
        )
        embeddings.append(list(response.embeddings[0].values))

    log.info("임베딩 완료  texts=%d  model=%s", len(texts), model)
    return embeddings


# ──────────────────────────────────────────────
# JSON 생성 (구조화 출력)
# ──────────────────────────────────────────────
async def generate_json(
    prompt: str,
    *,
    system_prompt: str = "",
    model: str | None = None,
    temperature: float = 0.4,
    max_tokens: int = 8192,
) -> dict[str, Any]:
    """
    LLM에게 JSON 형식으로 응답하도록 요청한다.
    응답의 content를 파싱하여 dict로 반환한다.
    """
    settings = get_settings()
    model = model or settings.llm_model
    client = _get_client()

    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_tokens,
        response_mime_type="application/json",
    )
    if system_prompt:
        config.system_instruction = system_prompt

    response = await client.aio.models.generate_content(
        model=model,
        contents=prompt,
        config=config,
    )

    content: str = response.text or "{}"

    # 마크다운 코드블록으로 감싸진 경우 제거
    if content.startswith("```"):
        lines = content.split("\n")
        content = "\n".join(
            lines[1:-1] if lines[-1].strip() == "```" else lines[1:]
        )

    parsed = json.loads(content)
    log.info("JSON 파싱 완료  model=%s", model)
    return parsed
