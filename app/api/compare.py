"""
Cosmic Graph Intelligence - Compare API

CGI vs 일반 LLM 비교 테스트 엔드포인트.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

from app.core.compare_engine import run_chat, run_comparison
from app.models.compare_schemas import (
    BatchCompareRequest,
    CompareRequest,
    CompareResponse,
)
from app.core.exceptions import CGIException
from app.utils.logger import get_logger

log = get_logger("api.compare")

router = APIRouter(prefix="/api/compare", tags=["compare"])
chat_router = APIRouter(prefix="/api", tags=["chat"])


@chat_router.post("/chat", response_class=PlainTextResponse)
async def chat(request: CompareRequest) -> str:
    """
    비교 검증 없이 CGI 파이프라인 최종 답변만 반환한다.
    """
    log.info("chat 요청 수신: question=%s, mode=%s", request.question, request.mode)

    try:
        result = await run_chat(question=request.question, mode=request.mode)
        return result.content
    except CGIException as e:
        log.error("chat 커스텀 에러: %s (status: %d)", e.message, e.status_code)
        raise HTTPException(status_code=e.status_code, detail=f"chat 생성 중 오류 발생: {e.message}")
    except Exception as e:
        log.error("chat 생성 실패: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"서버 내부 오류: {str(e)}")


@router.post("", response_model=CompareResponse)
async def compare(request: CompareRequest) -> CompareResponse:
    """
    CGI vs 일반 LLM 비교 테스트를 실행한다.

    동일한 질문을 CGI 파이프라인과 일반 LLM에 각각 전송하고,
    Judge LLM이 7가지 기준으로 자동 비교 분석한 결과를 반환한다.
    """
    log.info("비교 요청 수신: question=%s, mode=%s", request.question, request.mode)

    try:
        result = await run_comparison(
            question=request.question,
            mode=request.mode,
        )
        return result

    except CGIException as e:
        log.error("비교 테스트 커스텀 에러: %s (status: %d)", e.message, e.status_code)
        raise HTTPException(status_code=e.status_code, detail=f"비교 테스트 중 오류 발생: {e.message}")
    except Exception as e:
        log.error("비교 테스트 실패: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"서버 내부 오류: {str(e)}")


@router.post("/report", response_class=PlainTextResponse)
async def compare_report(request: CompareRequest) -> str:
    """
    비교 테스트를 실행하고 마크다운 리포트만 반환한다.
    """
    log.info("리포트 요청 수신: question=%s", request.question)

    try:
        result = await run_comparison(
            question=request.question,
            mode=request.mode,
        )
        return result.report_markdown

    except CGIException as e:
        log.error("리포트 생성 커스텀 에러: %s (status: %d)", e.message, e.status_code)
        raise HTTPException(status_code=e.status_code, detail=f"리포트 생성 중 오류 발생: {e.message}")
    except Exception as e:
        log.error("리포트 생성 실패: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"서버 내부 오류: {str(e)}")


@router.post("/batch", response_model=list[CompareResponse])
async def compare_batch(request: BatchCompareRequest) -> list[CompareResponse]:
    """
    여러 질문에 대해 일괄 비교 테스트를 실행한다.
    """
    log.info("일괄 비교 요청 수신: %d개 질문", len(request.questions))

    results: list[CompareResponse] = []
    for i, question in enumerate(request.questions):
        log.info("[%d/%d] %s", i + 1, len(request.questions), question)
        try:
            result = await run_comparison(question=question, mode=request.mode)
            results.append(result)
        except Exception as e:
            log.error("질문 '%s' 실패: %s", question, e)
            # 실패한 질문은 스킵하고 계속 진행

    return results
