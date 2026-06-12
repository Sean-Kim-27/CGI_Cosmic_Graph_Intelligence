"""
Cosmic Graph Intelligence - Compare Engine

동일한 질문에 대해 CGI 파이프라인과 일반 LLM의 응답을 비교한다.

흐름:
1. 일반 LLM에 질문 직접 전송 → direct_response
2. CGI 파이프라인 실행 (노드 → 그래프 → 쌍성계 → 프루닝 → 웜홀 → 압축)
3. 압축된 context를 주입한 LLM 호출 → cgi_response
4. Judge LLM으로 두 응답 자동 비교 → analysis
"""

from __future__ import annotations

import time
from datetime import datetime, timezone, timedelta

from app.core.binary_detector import detect_binary_systems
from app.core.blackhole_compressor import compress_context
from app.core.comparison_analyzer import analyze_comparison
from app.core.escape_node_pruner import classify_nodes
from app.core.graph_engine import build_graph
from app.core.nodes import analyze_input, generate_concept_nodes
from app.core.wormhole import generate_wormhole_shortcuts
from app.models.compare_schemas import (
    CGIMetadata,
    CompareResponse,
    ComparisonAnalysis,
    LLMResponse,
)
from app.models.config import get_settings
from app.utils.llm_client import generate_completion, generate_embeddings
from app.utils.logger import get_logger
from app.utils.report_generator import generate_report

log = get_logger("compare_engine")

KST = timezone(timedelta(hours=9))


async def run_comparison(question: str, mode: str = "balanced") -> CompareResponse:
    """
    CGI vs 일반 LLM 비교 테스트를 실행한다.

    Args:
        question: 비교할 질문
        mode: CGI 모드 (accurate/balanced/creative/research)

    Returns:
        CompareResponse: 두 응답 + 자동 분석 결과
    """
    total_start = time.perf_counter()
    settings = get_settings()

    log.info("=" * 60)
    log.info("비교 테스트 시작")
    log.info("질문: %s", question)
    log.info("모드: %s", mode)
    log.info("=" * 60)

    # ──────────────────────────────────────────
    # Phase 1: 일반 LLM 직접 호출
    # ──────────────────────────────────────────
    log.info("▶ Phase 1: 일반 LLM 직접 호출")

    direct_result = await generate_completion(
        question,
        system_prompt="너는 도움이 되는 AI 어시스턴트다. 사용자의 질문에 상세하고 유용한 답변을 해라.",
        model=settings.llm_model,
    )

    direct_response = LLMResponse(
        content=direct_result["content"],
        model=direct_result["model"],
        latency_ms=direct_result["latency_ms"],
        tokens_used=direct_result["tokens_used"],
    )
    log.info("일반 LLM 응답 완료 (%.0fms)", direct_result["latency_ms"])

    # ──────────────────────────────────────────
    # Phase 2: CGI 파이프라인 실행
    # ──────────────────────────────────────────
    log.info("▶ Phase 2: CGI 파이프라인 실행")
    cgi_start = time.perf_counter()

    # 2.1 입력 분석
    log.info("  2.1 입력 분석")
    analysis = await analyze_input(question)

    # 2.2 개념 노드 생성
    log.info("  2.2 개념 노드 생성")
    nodes = await generate_concept_nodes(analysis)

    # 2.3 쿼리 임베딩 (프루닝에 사용)
    log.info("  2.3 쿼리 임베딩")
    query_embeddings = await generate_embeddings([question])
    query_embedding = query_embeddings[0]

    # 2.4 그래프 생성
    log.info("  2.4 그래프 생성")
    G, edges = await build_graph(nodes)

    # 2.5 쌍성계 탐지
    log.info("  2.5 쌍성계 탐지")
    binaries = detect_binary_systems(G, nodes)

    # 2.6 노드 프루닝
    log.info("  2.6 노드 프루닝")
    decisions = classify_nodes(nodes, analysis, query_embedding, mode=mode)

    # 2.7 웜홀 생성
    log.info("  2.7 웜홀 생성")
    wormhole_edges = generate_wormhole_shortcuts(G, nodes)

    # 2.8 블랙홀 압축
    log.info("  2.8 블랙홀 압축")
    compressed = compress_context(
        analysis=analysis,
        nodes=nodes,
        decisions=decisions,
        binaries=binaries,
        wormhole_edges=wormhole_edges,
    )

    cgi_pipeline_ms = (time.perf_counter() - cgi_start) * 1000

    # ──────────────────────────────────────────
    # Phase 3: CGI context 주입 LLM 호출
    # ──────────────────────────────────────────
    log.info("▶ Phase 3: CGI context 주입 LLM 호출")

    cgi_system_prompt = f"""너는 Cosmic Graph Intelligence 시스템의 Reasoning Agent다.
아래의 구조화된 개념 그래프 분석 결과를 기반으로 사용자의 질문에 답변해라.

단순히 일반적인 답변을 하지 말고, 아래 그래프에서 발견된 핵심 조합, 쌍성계, 웜홀 연결을 깊이 있게 활용하여
서로 다른 관점과 도메인을 포괄하는 다양한 창의적 아이디어(최소 3~5개)를 명확하고 일관성 있게 제시해라.

───────────────────────────
{compressed}
───────────────────────────"""

    cgi_result = await generate_completion(
        question,
        system_prompt=cgi_system_prompt,
        model=settings.llm_model,
    )

    cgi_response = LLMResponse(
        content=cgi_result["content"],
        model=cgi_result["model"],
        latency_ms=round(cgi_pipeline_ms + cgi_result["latency_ms"], 1),
        tokens_used=cgi_result["tokens_used"],
        cgi_context_used=compressed,
    )
    log.info(
        "CGI 응답 완료 (파이프라인=%.0fms + LLM=%.0fms)",
        cgi_pipeline_ms,
        cgi_result["latency_ms"],
    )

    # ──────────────────────────────────────────
    # CGI 메타데이터 구성
    # ──────────────────────────────────────────
    node_map = {n.id: n for n in nodes}
    pruning_summary: dict[str, int] = {}
    for d in decisions:
        pruning_summary[d.next_state] = pruning_summary.get(d.next_state, 0) + 1

    cgi_metadata = CGIMetadata(
        nodes_generated=len(nodes),
        active_nodes=[d.node_name for d in decisions if d.next_state == "active"],
        orbiting_nodes=[d.node_name for d in decisions if d.next_state == "orbiting"],
        dormant_nodes=[
            d.node_name
            for d in decisions
            if d.next_state == "dormant_wormhole_candidate"
        ],
        binary_systems=[b.nodes for b in binaries],
        wormhole_connections=[
            [
                node_map[e.source].name if e.source in node_map else e.source,
                node_map[e.target].name if e.target in node_map else e.target,
            ]
            for e in wormhole_edges
        ],
        pruning_summary=pruning_summary,
        compressed_context=compressed,
    )

    # ──────────────────────────────────────────
    # Phase 4: 자동 비교 분석
    # ──────────────────────────────────────────
    log.info("▶ Phase 4: Judge LLM 자동 비교 분석")
    comparison_analysis = await analyze_comparison(
        question=question,
        direct_content=direct_response.content,
        cgi_content=cgi_response.content,
    )

    total_ms = (time.perf_counter() - total_start) * 1000

    # ──────────────────────────────────────────
    # 결과 조합
    # ──────────────────────────────────────────
    response = CompareResponse(
        question=question,
        mode=mode,
        direct_response=direct_response,
        cgi_response=cgi_response,
        cgi_metadata=cgi_metadata,
        analysis=comparison_analysis,
        total_latency_ms=round(total_ms, 1),
        timestamp=datetime.now(KST).isoformat(),
    )

    # 마크다운 리포트 생성
    response.report_markdown = generate_report(response)

    log.info("=" * 60)
    log.info("비교 테스트 완료 (총 %.1fms)", total_ms)
    log.info("승자: %s", comparison_analysis.winner)
    log.info("=" * 60)

    return response
