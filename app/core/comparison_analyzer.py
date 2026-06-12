"""
Cosmic Graph Intelligence - Comparison Analyzer

Judge LLM을 사용하여 두 응답을 자동으로 비교·분석한다.

평가 항목:
- relevance: 질문과의 관련성
- creativity: 창의성, 독창성
- diversity: 관점/아이디어의 다양성
- specificity: 구체적이고 실행 가능한 정도
- novelty: 일반적인 답변과 차별화된 정도
- coherence: 논리적 일관성
- explainability: 왜 그런 답이 나왔는지 설명 가능한 정도
"""

from __future__ import annotations

from typing import Any

from app.models.compare_schemas import ComparisonAnalysis, ScorePair
from app.models.config import get_settings
from app.utils.llm_client import generate_json
from app.utils.logger import get_logger

log = get_logger("analyzer")

JUDGE_PROMPT = """너는 AI 응답 품질을 평가하는 전문 심사위원이다.

동일한 질문에 대해 두 가지 시스템이 생성한 답변을 비교 평가해라.
- **System A**: 일반 LLM 직접 호출
- **System B**: CGI(Cosmic Graph Intelligence) 파이프라인을 통해 구조화된 개념 그래프를 기반으로 생성한 답변

## 질문
{question}

## System A (일반 LLM) 답변
{direct_content}

## System B (CGI) 답변
{cgi_content}

## 평가 기준
각 항목을 1~10점으로 평가해라 (10이 가장 높음).

1. **relevance**: 질문의 핵심을 얼마나 잘 다루고 있는가
2. **creativity**: 독창적인 아이디어나 접근법을 제시하는가
3. **diversity**: 다양한 관점이나 옵션을 제공하는가
4. **specificity**: 구체적이고 실행 가능한 제안을 하는가
5. **novelty**: 일반적이고 뻔한 답변을 넘어서는가
6. **coherence**: 논리적으로 일관되고 구조가 잘 잡혀있는가
7. **explainability**: 왜 그런 결론에 도달했는지 설명 가능한가

## 출력 형식 (JSON만 출력)
{{
  "scores": {{
    "relevance": {{"direct": N, "cgi": N}},
    "creativity": {{"direct": N, "cgi": N}},
    "diversity": {{"direct": N, "cgi": N}},
    "specificity": {{"direct": N, "cgi": N}},
    "novelty": {{"direct": N, "cgi": N}},
    "coherence": {{"direct": N, "cgi": N}},
    "explainability": {{"direct": N, "cgi": N}}
  }},
  "summary": "전체적인 비교 요약 (2~3문장)",
  "cgi_advantages": ["CGI가 더 나은 구체적인 점 1", "점 2", ...],
  "direct_advantages": ["일반 LLM이 더 나은 구체적인 점 1", ...],
  "key_differences": ["핵심 차이점 1", "차이점 2", ...],
  "winner": "cgi 또는 direct 또는 tie",
  "winner_reason": "왜 이쪽이 이겼는지 한 줄 설명"
}}"""


async def analyze_comparison(
    *,
    question: str,
    direct_content: str,
    cgi_content: str,
) -> ComparisonAnalysis:
    """
    Judge LLM을 사용하여 두 응답을 비교 분석한다.
    """
    settings = get_settings()

    prompt = JUDGE_PROMPT.format(
        question=question,
        direct_content=direct_content,
        cgi_content=cgi_content,
    )

    try:
        data: dict[str, Any] = await generate_json(
            prompt,
            system_prompt="너는 공정하고 전문적인 AI 응답 품질 심사위원이다. 편향 없이 두 답변을 비교 평가해라.",
            model=settings.judge_llm_model,
            temperature=0.3,
        )

        # 점수 파싱
        raw_scores = data.get("scores", {})
        scores: dict[str, ScorePair] = {}
        for key, pair in raw_scores.items():
            scores[key] = ScorePair(
                direct=int(pair.get("direct", 5)),
                cgi=int(pair.get("cgi", 5)),
            )

        analysis = ComparisonAnalysis(
            scores=scores,
            summary=data.get("summary", ""),
            cgi_advantages=data.get("cgi_advantages", []),
            direct_advantages=data.get("direct_advantages", []),
            key_differences=data.get("key_differences", []),
            winner=data.get("winner", "tie"),
            winner_reason=data.get("winner_reason", ""),
        )

        log.info("분석 완료: winner=%s", analysis.winner)
        return analysis

    except Exception as e:
        log.error("Judge LLM 분석 실패: %s", e)
        # 분석 실패 시 기본값 반환
        return ComparisonAnalysis(
            summary=f"자동 분석 실패: {str(e)}",
            winner="tie",
            winner_reason="분석을 수행할 수 없었습니다.",
        )
