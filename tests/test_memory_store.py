from __future__ import annotations

import sqlite3

from app.core.memory_store import CGIMemoryStore
from app.models.schemas import CosmicEdge, CosmicNode, InputAnalysis, PruningDecision


def test_memory_store_persists_run_nodes_edges_and_relationships(tmp_path):
    store = CGIMemoryStore(tmp_path / "cgi-memory.sqlite3")
    analysis = InputAnalysis(
        intent="system_design",
        keywords=["RAG", "뉴스"],
        domain=["AI"],
        output_type="design_document",
        suggested_node_count=2,
        original_input="AI 뉴스 앱 설계",
    )
    nodes = [
        CosmicNode(id="node_a", name="RAG", type="technology", mass=0.8, energy=0.7, description="검색 증강 생성"),
        CosmicNode(id="node_b", name="Vector DB", type="technology", mass=0.7, energy=0.6, description="임베딩 검색 저장소"),
    ]
    edges = [CosmicEdge(source="node_a", target="node_b", weight=0.9, attraction=0.9, repulsion=0.0)]
    decisions = [
        PruningDecision(node_id="node_a", node_name="RAG", next_state="active", immediate_utility=0.8),
        PruningDecision(node_id="node_b", node_name="Vector DB", next_state="orbiting", immediate_utility=0.6),
    ]

    run_id = store.save_run(
        question="AI 뉴스 앱 설계",
        mode="balanced",
        analysis=analysis,
        nodes=nodes,
        edges=edges,
        decisions=decisions,
        binary_systems=[["RAG", "Vector DB"]],
        wormhole_connections=[],
        compressed_context="context",
        response_content="answer",
        latency_ms=123.4,
    )

    assert run_id > 0
    with sqlite3.connect(tmp_path / "cgi-memory.sqlite3") as conn:
        assert conn.execute("select count(*) from cgi_runs").fetchone()[0] == 1
        assert conn.execute("select count(*) from cgi_nodes").fetchone()[0] == 2
        assert conn.execute("select count(*) from cgi_edges").fetchone()[0] == 1
        assert conn.execute("select count(*) from cgi_relationships where relationship_type='binary'").fetchone()[0] == 1


def test_memory_store_returns_bounded_recent_nodes_for_context(tmp_path):
    store = CGIMemoryStore(tmp_path / "cgi-memory.sqlite3")
    for idx in range(5):
        store.save_run(
            question=f"질문 {idx}",
            mode="balanced",
            analysis=InputAnalysis(original_input=f"질문 {idx}", keywords=["공통", f"키워드{idx}"], domain=["테스트"]),
            nodes=[CosmicNode(id=f"node_{idx}", name=f"노드{idx}", type="concept", description=f"설명 {idx}")],
            edges=[],
            decisions=[PruningDecision(node_id=f"node_{idx}", node_name=f"노드{idx}", next_state="active")],
            binary_systems=[],
            wormhole_connections=[],
            compressed_context="context",
            response_content="answer",
            latency_ms=1.0,
        )

    recent = store.get_recent_node_context(limit=3)

    assert [item["name"] for item in recent] == ["노드4", "노드3", "노드2"]
    assert all("description" in item for item in recent)


def test_memory_store_searches_all_saved_nodes_by_embedding_similarity(tmp_path):
    store = CGIMemoryStore(tmp_path / "cgi-memory.sqlite3")
    analysis = InputAnalysis(original_input="검색", keywords=["검색"], domain=["테스트"])
    for idx, embedding in enumerate(([1.0, 0.0], [0.0, 1.0], [0.8, 0.2], [])):
        store.save_run(
            question=f"질문 {idx}",
            mode="balanced",
            analysis=analysis,
            nodes=[
                CosmicNode(
                    id=f"node_{idx}",
                    name=f"노드{idx}",
                    type="concept",
                    description=f"설명 {idx}",
                    embedding=list(embedding),
                )
            ],
            edges=[],
            decisions=[PruningDecision(node_id=f"node_{idx}", node_name=f"노드{idx}", next_state="active")],
            binary_systems=[],
            wormhole_connections=[],
            compressed_context="context",
            response_content="answer",
            latency_ms=1.0,
        )

    similar = store.search_similar_node_context(query_embedding=[1.0, 0.0], limit=2)

    assert [item["name"] for item in similar] == ["노드0", "노드2"]
    assert similar[0]["similarity"] == 1.0
    assert "노드1" not in [item["name"] for item in similar]


def test_memory_store_formats_recent_and_similar_context_with_total_limit_and_dedup(tmp_path):
    store = CGIMemoryStore(tmp_path / "cgi-memory.sqlite3")
    analysis = InputAnalysis(original_input="검색", keywords=["검색"], domain=["테스트"])
    rows = [
        ("old_similar", "오래된 유사 노드", [1.0, 0.0]),
        ("middle", "중간 노드", [0.0, 1.0]),
        ("recent_similar", "최근 유사 노드", [0.9, 0.1]),
        ("latest", "최신 노드", [0.2, 0.8]),
    ]
    for node_id, name, embedding in rows:
        store.save_run(
            question=name,
            mode="balanced",
            analysis=analysis,
            nodes=[CosmicNode(id=node_id, name=name, type="concept", description=f"{name} 설명", embedding=embedding)],
            edges=[],
            decisions=[PruningDecision(node_id=node_id, node_name=name, next_state="active")],
            binary_systems=[],
            wormhole_connections=[],
            compressed_context="context",
            response_content="answer",
            latency_ms=1.0,
        )

    formatted = store.format_mixed_node_context(
        query_embedding=[1.0, 0.0],
        recent_limit=2,
        similar_limit=3,
        total_limit=3,
    )

    assert "최근 CGI 노드" in formatted
    assert "질문과 유사한 CGI 노드" in formatted
    assert formatted.count("- 최근 유사 노드 ") == 1
    assert "최신 노드" in formatted
    assert "오래된 유사 노드" in formatted
    assert "중간 노드" not in formatted
