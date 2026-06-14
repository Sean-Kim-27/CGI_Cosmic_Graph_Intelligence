"""
Cosmic Graph Intelligence - FastAPI Application

우주적 상호작용을 모방한 그래프 기반 자기조직형 창의 지능체 시스템.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.compare import chat_router, router as compare_router

app = FastAPI(
    title="Cosmic Graph Intelligence",
    description=(
        "우주적 상호작용을 모방한 그래프 기반 자기조직형 창의 지능체 시스템.\n\n"
        "CGI vs 일반 LLM 비교 테스트를 통해 그래프 기반 접근법의 "
        "창의성·다양성·구조적 설명력을 검증합니다."
    ),
    version="0.1.0",
)

# CORS 설정 (프론트엔드 연동용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(chat_router)
app.include_router(compare_router)


@app.get("/")
async def root():
    """API 상태 확인."""
    return {
        "name": "Cosmic Graph Intelligence",
        "version": "0.1.0",
        "status": "running",
        "endpoints": {
            "chat": "POST /api/chat",
            "compare": "POST /api/compare",
            "report": "POST /api/compare/report",
            "batch": "POST /api/compare/batch",
            "docs": "GET /docs",
        },
    }


@app.get("/health")
async def health():
    """헬스 체크."""
    return {"status": "ok"}
