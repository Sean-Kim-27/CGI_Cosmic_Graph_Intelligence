"""
Cosmic Graph Intelligence - Compare API Tests
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from app.main import app
from app.models.compare_schemas import CompareResponse, ComparisonAnalysis, LLMResponse, CGIMetadata

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


@patch("app.api.compare.run_comparison")
def test_compare_endpoint(mock_run_comparison):
    # Mock return value
    mock_result = CompareResponse(
        question="테스트 질문",
        mode="balanced",
        direct_response=LLMResponse(content="직접 응답", model="test-model", latency_ms=100.0, tokens_used=10),
        cgi_response=LLMResponse(content="CGI 응답", model="test-model", latency_ms=200.0, tokens_used=20, cgi_context_used="컨텍스트"),
        cgi_metadata=CGIMetadata(
            nodes_generated=5,
            active_nodes=["A"],
            binary_systems=[["A", "B"]],
            wormhole_connections=[],
            pruning_summary={"active": 1}
        ),
        analysis=ComparisonAnalysis(
            scores={},
            summary="요약",
            cgi_advantages=[],
            direct_advantages=[],
            key_differences=[],
            winner="cgi",
            winner_reason="이유"
        ),
        timestamp="2026-06-13T00:00:00Z"
    )
    mock_run_comparison.return_value = mock_result

    # Send request
    response = client.post(
        "/api/compare",
        json={"question": "테스트 질문", "mode": "balanced"}
    )

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["question"] == "테스트 질문"
    assert data["mode"] == "balanced"
    assert data["direct_response"]["content"] == "직접 응답"
    assert data["cgi_response"]["content"] == "CGI 응답"
