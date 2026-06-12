"""
Cosmic Graph Intelligence - Report Generator

비교 테스트 결과를 마크다운 리포트로 변환한다.
"""

from __future__ import annotations

from app.models.compare_schemas import CompareResponse


def generate_report(result: CompareResponse) -> str:
    """CompareResponse를 읽기 쉬운 마크다운 리포트로 변환한다."""

    lines: list[str] = []

    lines.append("# 🔬 CGI vs Direct LLM 비교 리포트")
    lines.append("")
    lines.append(f"**시간**: {result.timestamp}")
    lines.append(f"**모드**: {result.mode}")
    lines.append(f"**총 소요 시간**: {result.total_latency_ms:.0f}ms")
    lines.append("")

    # ── 질문 ──
    lines.append("---")
    lines.append("## 📝 질문")
    lines.append(f"> {result.question}")
    lines.append("")

    # ── 점수 비교 ──
    lines.append("---")
    lines.append("## 📊 항목별 점수 비교")
    lines.append("")
    lines.append("| 항목 | 일반 LLM | CGI | 차이 | 승자 |")
    lines.append("|---|:---:|:---:|:---:|:---:|")

    total_direct = 0
    total_cgi = 0
    label_map = {
        "relevance": "관련성",
        "creativity": "창의성",
        "diversity": "다양성",
        "specificity": "구체성",
        "novelty": "참신성",
        "coherence": "일관성",
        "explainability": "설명가능성",
    }

    for key, pair in result.analysis.scores.items():
        label = label_map.get(key, key)
        diff = pair.cgi - pair.direct
        total_direct += pair.direct
        total_cgi += pair.cgi

        if diff > 0:
            marker = f"+{diff} ✅"
            winner_col = "CGI"
        elif diff < 0:
            marker = f"{diff} ❌"
            winner_col = "LLM"
        else:
            marker = "0 ➖"
            winner_col = "무승부"

        lines.append(f"| {label} | {pair.direct} | {pair.cgi} | {marker} | {winner_col} |")

    # 합계
    total_diff = total_cgi - total_direct
    if total_diff > 0:
        total_marker = f"+{total_diff} ✅"
    elif total_diff < 0:
        total_marker = f"{total_diff} ❌"
    else:
        total_marker = "0 ➖"
    lines.append(f"| **합계** | **{total_direct}** | **{total_cgi}** | **{total_marker}** | |")
    lines.append("")

    # ── 종합 결과 ──
    winner_emoji = {"cgi": "🏆 CGI 승리", "direct": "🏆 일반 LLM 승리", "tie": "🤝 무승부"}
    lines.append("---")
    lines.append(f"## {winner_emoji.get(result.analysis.winner, '🤝 무승부')}")
    lines.append("")
    lines.append(f"**이유**: {result.analysis.winner_reason}")
    lines.append("")
    lines.append(f"**요약**: {result.analysis.summary}")
    lines.append("")

    # ── CGI 장점 ──
    if result.analysis.cgi_advantages:
        lines.append("### ✅ CGI가 더 나은 점")
        for adv in result.analysis.cgi_advantages:
            lines.append(f"- {adv}")
        lines.append("")

    # ── 일반 LLM 장점 ──
    if result.analysis.direct_advantages:
        lines.append("### ⚠️ 일반 LLM이 더 나은 점")
        for adv in result.analysis.direct_advantages:
            lines.append(f"- {adv}")
        lines.append("")

    # ── 핵심 차이점 ──
    if result.analysis.key_differences:
        lines.append("### 🔍 핵심 차이점")
        for diff in result.analysis.key_differences:
            lines.append(f"- {diff}")
        lines.append("")

    # ── 응답 비교 ──
    lines.append("---")
    lines.append("## 💬 응답 비교")
    lines.append("")
    lines.append("### 일반 LLM 응답")
    lines.append(f"- 모델: `{result.direct_response.model}`")
    lines.append(f"- 응답 시간: {result.direct_response.latency_ms:.0f}ms")
    lines.append(f"- 사용 토큰: {result.direct_response.tokens_used}")
    lines.append("")
    lines.append(result.direct_response.content)
    lines.append("")

    lines.append("### CGI 응답")
    lines.append(f"- 모델: `{result.cgi_response.model}`")
    lines.append(f"- 응답 시간: {result.cgi_response.latency_ms:.0f}ms (파이프라인 포함)")
    lines.append(f"- 사용 토큰: {result.cgi_response.tokens_used}")
    lines.append("")
    lines.append(result.cgi_response.content)
    lines.append("")

    # ── CGI 메타데이터 ──
    meta = result.cgi_metadata
    lines.append("---")
    lines.append("## 🌌 CGI 파이프라인 메타데이터")
    lines.append("")
    lines.append(f"- 생성 노드 수: {meta.nodes_generated}")
    lines.append(f"- 활성 노드: {', '.join(meta.active_nodes)}")
    if meta.orbiting_nodes:
        lines.append(f"- 주변 후보 노드: {', '.join(meta.orbiting_nodes)}")
    if meta.dormant_nodes:
        lines.append(f"- 웜홀 후보 노드: {', '.join(meta.dormant_nodes)}")
    lines.append("")

    if meta.binary_systems:
        lines.append("### 쌍성계")
        for bs in meta.binary_systems:
            lines.append(f"- {bs[0]} + {bs[1]}")
        lines.append("")

    if meta.wormhole_connections:
        lines.append("### 웜홀 연결")
        for wh in meta.wormhole_connections:
            lines.append(f"- {wh[0]} ↔ {wh[1]}")
        lines.append("")

    if meta.pruning_summary:
        lines.append("### 프루닝 요약")
        for state, count in meta.pruning_summary.items():
            lines.append(f"- {state}: {count}개")
        lines.append("")

    return "\n".join(lines)
