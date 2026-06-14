from __future__ import annotations

import sqlite3

import networkx as nx
import pytest

from app.core import compare_engine
from app.core.memory_store import CGIMemoryStore
from app.models.config import Settings
from app.models.schemas import CosmicEdge, CosmicNode, InputAnalysis


@pytest.mark.asyncio
async def test_run_chat_persists_cgi_graph_artifacts(monkeypatch, tmp_path):
    db_path = tmp_path / "cgi-memory.sqlite3"
    monkeypatch.setattr(
        compare_engine,
        "get_settings",
        lambda: Settings(
            llm_provider="codex",
            llm_model="test-model",
            cgi_memory_db_path=str(db_path),
            cgi_memory_enabled=True,
            cgi_memory_context_limit=4,
        ),
    )
    analysis = InputAnalysis(
        intent="general",
        keywords=["인사"],
        domain=["conversation"],
        original_input="안녕?",
        suggested_node_count=2,
    )
    nodes = [
        CosmicNode(id="node_a", name="인사", type="concept", mass=0.8, energy=0.8, description="대화 시작"),
        CosmicNode(id="node_b", name="친근함", type="emotion", mass=0.7, energy=0.7, description="친근한 톤"),
    ]
    graph = nx.Graph()
    graph.add_node("node_a")
    graph.add_node("node_b")
    graph.add_edge("node_a", "node_b", weight=0.8)
    edges = [CosmicEdge(source="node_a", target="node_b", weight=0.8, attraction=0.8)]

    async def fake_analyze_input(question: str) -> InputAnalysis:
        return analysis

    async def fake_generate_nodes(input_analysis: InputAnalysis) -> list[CosmicNode]:
        return nodes

    async def fake_embeddings(texts: list[str]) -> list[list[float]]:
        return [[0.1, 0.2] for _ in texts]

    async def fake_build_graph(generated_nodes: list[CosmicNode]):
        return graph, edges

    async def fake_completion(question: str, *, system_prompt: str, model: str):
        assert "과거 대화에서 저장된 최근 CGI 노드" not in system_prompt
        return {"content": "안녕하세요", "model": model, "latency_ms": 1.0, "tokens_used": 1}

    monkeypatch.setattr(compare_engine, "analyze_input", fake_analyze_input)
    monkeypatch.setattr(compare_engine, "generate_concept_nodes", fake_generate_nodes)
    monkeypatch.setattr(compare_engine, "generate_embeddings", fake_embeddings)
    monkeypatch.setattr(compare_engine, "build_graph", fake_build_graph)
    monkeypatch.setattr(compare_engine, "generate_completion", fake_completion)

    result = await compare_engine.run_chat("안녕?", mode="balanced")

    assert result.content == "안녕하세요"
    with sqlite3.connect(db_path) as conn:
        assert conn.execute("select count(*) from cgi_runs").fetchone()[0] == 1
        assert conn.execute("select count(*) from cgi_nodes").fetchone()[0] == 2
        assert conn.execute("select count(*) from cgi_edges").fetchone()[0] == 1


@pytest.mark.asyncio
async def test_run_chat_injects_recent_and_similar_bounded_memory(monkeypatch, tmp_path):
    db_path = tmp_path / "cgi-memory.sqlite3"
    store = CGIMemoryStore(db_path)
    existing_analysis = InputAnalysis(original_input="과거 질문", keywords=["메모리"], domain=["테스트"])
    for node_id, name, embedding in [
        ("old_similar", "오래된 유사 노드", [1.0, 0.0]),
        ("latest", "최신 노드", [0.2, 0.8]),
    ]:
        store.save_run(
            question=name,
            mode="balanced",
            analysis=existing_analysis,
            nodes=[CosmicNode(id=node_id, name=name, type="concept", description=f"{name} 설명", embedding=embedding)],
            edges=[],
            decisions=[],
            binary_systems=[],
            wormhole_connections=[],
            compressed_context="context",
            response_content="answer",
            latency_ms=1.0,
        )

    monkeypatch.setattr(
        compare_engine,
        "get_settings",
        lambda: Settings(
            llm_provider="codex",
            llm_model="test-model",
            cgi_memory_db_path=str(db_path),
            cgi_memory_enabled=True,
            cgi_memory_context_limit=3,
            cgi_memory_recent_limit=1,
            cgi_memory_similar_limit=2,
        ),
    )
    analysis = InputAnalysis(intent="general", keywords=["검증"], domain=["test"], original_input="현재 질문")
    nodes = [CosmicNode(id="current", name="현재 노드", type="concept", description="현재 설명", embedding=[1.0, 0.0])]
    graph = nx.Graph()
    graph.add_node("current")

    async def fake_analyze_input(question: str) -> InputAnalysis:
        return analysis

    async def fake_generate_nodes(input_analysis: InputAnalysis) -> list[CosmicNode]:
        return nodes

    async def fake_embeddings(texts: list[str]) -> list[list[float]]:
        return [[1.0, 0.0] for _ in texts]

    async def fake_build_graph(generated_nodes: list[CosmicNode]):
        return graph, []

    async def fake_completion(question: str, *, system_prompt: str, model: str):
        assert "최근 CGI 노드" in system_prompt
        assert "질문과 유사한 CGI 노드" in system_prompt
        assert "최신 노드" in system_prompt
        assert "오래된 유사 노드" in system_prompt
        return {"content": "메모리 반영 답변", "model": model, "latency_ms": 1.0, "tokens_used": 1}

    monkeypatch.setattr(compare_engine, "analyze_input", fake_analyze_input)
    monkeypatch.setattr(compare_engine, "generate_concept_nodes", fake_generate_nodes)
    monkeypatch.setattr(compare_engine, "generate_embeddings", fake_embeddings)
    monkeypatch.setattr(compare_engine, "build_graph", fake_build_graph)
    monkeypatch.setattr(compare_engine, "generate_completion", fake_completion)

    result = await compare_engine.run_chat("현재 질문", mode="balanced")

    assert result.content == "메모리 반영 답변"
