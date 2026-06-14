"""
Cosmic Graph Intelligence - LLM 클라이언트

Google Gemini API를 캡슐화한 비동기 클라이언트.
텍스트 생성, 임베딩, 응답 메타데이터 수집을 담당한다.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from typing import Any

from google import genai
from google.genai import types
from google.genai.errors import APIError
from openai_codex import AsyncCodex, Sandbox

from app.core.exceptions import LLMTimeoutError, LLMTokenLimitError, JSONParsingError, CGIException
from app.models.config import get_settings
from app.utils.logger import get_logger

log = get_logger("llm_client")

_client: genai.Client | None = None
_codex_client: AsyncCodex | None = None
_codex_thread = None


def _get_client() -> genai.Client:
    """Gemini 클라이언트 싱글턴."""
    global _client
    if _client is None:
        settings = get_settings()
        _client = genai.Client(api_key=settings.gemini_api_key)
    return _client


async def _get_codex_client() -> AsyncCodex:
    """서버 user의 Codex auth를 재사용하는 Codex SDK 클라이언트."""
    global _codex_client
    if _codex_client is None:
        client = AsyncCodex()
        _codex_client = await client.__aenter__()
    return _codex_client


async def _run_codex(prompt: str, *, system_prompt: str = "", model: str | None = None) -> dict[str, Any]:
    settings = get_settings()
    model = model or settings.llm_model
    client = await _get_codex_client()
    thread = await client.thread_start(
        model=model,
        sandbox=Sandbox.workspace_write,
        cwd=os.path.abspath(settings.codex_workdir),
    )
    full_prompt = prompt
    if system_prompt:
        full_prompt = f"System instructions:\n{system_prompt}\n\nUser request:\n{prompt}"

    t0 = time.perf_counter()
    result = await thread.run(full_prompt)
    latency_ms = (time.perf_counter() - t0) * 1000
    return {
        "content": getattr(result, "final_response", str(result)).strip(),
        "model": model,
        "latency_ms": round(latency_ms, 1),
        "tokens_used": 0,
    }


def _strip_code_fence(content: str) -> str:
    content = content.strip()
    if content.startswith("```"):
        lines = content.split("\n")
        if lines[-1].strip() == "```":
            return "\n".join(lines[1:-1]).strip()
        return "\n".join(lines[1:]).strip()
    return content


def _local_embedding(text: str, dimensions: int = 64) -> list[float]:
    digest = hashlib.sha512(text.encode("utf-8")).digest()
    values = []
    for i in range(dimensions):
        byte = digest[i % len(digest)]
        values.append(round((byte / 127.5) - 1.0, 6))
    return values


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
    if settings.llm_provider == "codex":
        result = await _run_codex(prompt, system_prompt=system_prompt, model=model)
        log.info(
            "Codex LLM 완료  model=%s  tokens=%s  latency=%.0fms",
            model,
            result["tokens_used"],
            result["latency_ms"],
        )
        return result

    client = _get_client()

    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_tokens,
    )
    if system_prompt:
        config.system_instruction = system_prompt

    t0 = time.perf_counter()
    try:
        response = await client.aio.models.generate_content(
            model=model,
            contents=prompt,
            config=config,
        )
    except APIError as e:
        log.error("LLM API 에러: %s", e)
        # HTTP status code에 따른 처리 (Gemini APIError는 code 속성을 가짐)
        status = getattr(e, 'code', 500)
        if status in (429, 403): # Rate limit, Quota exceeded
            raise LLMTokenLimitError(f"API 할당량을 초과했습니다: {e.message}")
        elif status in (504, 503):
            raise LLMTimeoutError(f"API 서버 타임아웃/오류: {e.message}")
        else:
            raise CGIException(f"LLM 호출 실패: {e.message}", status_code=status)
    except Exception as e:
        log.error("예상치 못한 LLM 호출 에러: %s", e)
        raise CGIException(f"LLM 시스템 에러: {str(e)}")

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
    if settings.llm_provider == "codex":
        embeddings = [_local_embedding(text) for text in texts]
        log.info("로컬 임베딩 완료  texts=%d  provider=codex", len(texts))
        return embeddings

    client = _get_client()

    embeddings: list[list[float]] = []
    try:
        # Gemini embed_content는 개별 호출
        for text in texts:
            response = await client.aio.models.embed_content(
                model=model,
                contents=text,
            )
            embeddings.append(list(response.embeddings[0].values))
    except APIError as e:
        log.error("임베딩 생성 에러: %s", e)
        status = getattr(e, 'code', 500)
        if status == 429:
            raise LLMTokenLimitError(f"임베딩 API 할당량을 초과했습니다: {e.message}")
        raise CGIException(f"임베딩 실패: {e.message}", status_code=status)
    except Exception as e:
        raise CGIException(f"임베딩 시스템 에러: {str(e)}")

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
    if settings.llm_provider == "codex":
        result = await _run_codex(
            prompt,
            system_prompt=(
                f"{system_prompt}\n\n" if system_prompt else ""
            ) + "반드시 JSON 객체만 출력해라. 마크다운 설명은 넣지 마라.",
            model=model,
        )
        content = _strip_code_fence(result["content"])
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError as e:
            log.error("Codex JSON 파싱 에러: %s", e)
            raise JSONParsingError(f"JSON 디코딩에 실패했습니다. (내용: {content[:100]}...)")
        log.info("Codex JSON 파싱 완료  model=%s", model)
        return parsed

    client = _get_client()

    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_tokens,
        response_mime_type="application/json",
    )
    if system_prompt:
        config.system_instruction = system_prompt

    try:
        response = await client.aio.models.generate_content(
            model=model,
            contents=prompt,
            config=config,
        )
    except APIError as e:
        log.error("LLM JSON 생성 API 에러: %s", e)
        status = getattr(e, 'code', 500)
        if status == 429:
            raise LLMTokenLimitError(f"JSON 생성 API 할당량을 초과했습니다: {e.message}")
        raise CGIException(f"JSON 생성 실패: {e.message}", status_code=status)
    except Exception as e:
        raise CGIException(f"JSON 생성 시스템 에러: {str(e)}")

    content: str = response.text or "{}"

    # 마크다운 코드블록으로 감싸진 경우 제거
    if content.startswith("```"):
        lines = content.split("\n")
        content = "\n".join(
            lines[1:-1] if lines[-1].strip() == "```" else lines[1:]
        )

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError as e:
        log.error("JSON 파싱 에러: %s", e)
        raise JSONParsingError(f"JSON 디코딩에 실패했습니다. (내용: {content[:100]}...)")
    
    log.info("JSON 파싱 완료  model=%s", model)
    return parsed
