"""
Cosmic Graph Intelligence - Concept Node Generator

사용자 입력을 분석하고 관련 개념 노드를 LLM으로 생성한다.
"""

from __future__ import annotations

import uuid
from typing import Any

from app.models.schemas import CosmicNode, InputAnalysis
from app.utils.llm_client import generate_json, generate_embeddings
from app.utils.logger import get_logger

log = get_logger("nodes")


# ──────────────────────────────────────────────
# 입력 분석
# ──────────────────────────────────────────────
async def analyze_input(user_input: str) -> InputAnalysis:
    """사용자 입력에서 의도, 키워드, 도메인을 추출한다."""

    prompt = f"""다음 사용자 입력을 분석하여 JSON으로 출력해라.

사용자 입력: "{user_input}"

출력 형식:
{{
  "intent": "idea_generation | system_design | problem_solving | analysis | general",
  "keywords": ["핵심 키워드 5~10개"],
  "domain": ["관련 도메인 2~4개"],
  "output_type": "idea_list | design_document | solution | analysis_report | text"
}}"""

    data: dict[str, Any] = await generate_json(
        prompt,
        system_prompt="너는 사용자 입력을 정확하게 분석하는 AI다.",
    )

    return InputAnalysis(
        intent=data.get("intent", "general"),
        keywords=data.get("keywords", []),
        domain=data.get("domain", []),
        output_type=data.get("output_type", "text"),
        original_input=user_input,
    )


# ──────────────────────────────────────────────
# 개념 노드 생성
# ──────────────────────────────────────────────
async def generate_concept_nodes(
    analysis: InputAnalysis,
    *,
    max_nodes: int = 20,
) -> list[CosmicNode]:
    """입력 분석 결과를 기반으로 관련 개념 노드를 생성한다."""

    prompt = f"""다음 주제에 대해 관련된 개념 노드를 {max_nodes}개 생성해라.

주제: "{analysis.original_input}"
키워드: {analysis.keywords}
도메인: {analysis.domain}
의도: {analysis.intent}

각 노드는 다양한 관점(기술, 개념, 데이터, 목표, 감정, 장소, 활동 등)에서 생성해라.
일부는 직접 관련된 것, 일부는 간접적이지만 창의적 연결이 가능한 것으로 구성해라.

출력 형식 (JSON 배열):
[
  {{
    "name": "노드 이름",
    "type": "technology | concept | data | goal | emotion | place | activity | domain",
    "mass": 0.0~1.0,
    "energy": 0.0~1.0,
    "description": "이 노드가 주제와 어떤 관련이 있는지 한 줄 설명"
  }}
]

mass는 주제와의 직접적 관련도, energy는 활용 잠재력이다.
반드시 {max_nodes}개를 생성해라."""

    data: Any = await generate_json(
        prompt,
        system_prompt="너는 창의적 개념 탐색 전문가다. 다양한 관점의 개념을 생성해라.",
    )

    # 데이터가 dict 안에 감싸져 있을 수 있음
    if isinstance(data, dict):
        for v in data.values():
            if isinstance(v, list):
                data = v
                break

    nodes: list[CosmicNode] = []
    for item in data:
        node = CosmicNode(
            id=f"node_{uuid.uuid4().hex[:8]}",
            name=item.get("name", "unknown"),
            type=item.get("type", "concept"),
            mass=float(item.get("mass", 0.5)),
            energy=float(item.get("energy", 0.5)),
            description=item.get("description", ""),
        )
        nodes.append(node)

    log.info("노드 생성 완료: %d개", len(nodes))

    # 임베딩 생성
    texts = [f"{n.name}: {n.description}" for n in nodes]
    embeddings = await generate_embeddings(texts)
    for node, emb in zip(nodes, embeddings):
        node.embedding = emb

    log.info("임베딩 부여 완료")
    return nodes
