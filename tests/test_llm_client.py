from __future__ import annotations

import pytest

from app.models import config as config_module
from app.utils import llm_client


@pytest.fixture(autouse=True)
def reset_settings_and_clients(monkeypatch):
    config_module._settings = None
    llm_client._client = None
    llm_client._codex_client = None
    llm_client._codex_thread = None
    monkeypatch.setenv("LLM_PROVIDER", "codex")
    monkeypatch.setenv("LLM_MODEL", "gpt-5.5")
    yield
    config_module._settings = None
    llm_client._client = None
    llm_client._codex_client = None
    llm_client._codex_thread = None


@pytest.mark.asyncio
async def test_generate_completion_uses_codex_auth_provider(monkeypatch):
    calls = []

    class FakeResult:
        final_response = "Codex 답변"

    class FakeThread:
        async def run(self, prompt):
            calls.append(prompt)
            return FakeResult()

    class FakeAsyncCodex:
        async def __aenter__(self):
            calls.append("entered")
            return self

        async def thread_start(self, **kwargs):
            calls.append(kwargs)
            return FakeThread()

    monkeypatch.setattr(llm_client, "AsyncCodex", FakeAsyncCodex)

    result = await llm_client.generate_completion("질문", system_prompt="시스템")

    assert result["content"] == "Codex 답변"
    assert result["model"] == "gpt-5.5"
    assert result["tokens_used"] == 0
    assert calls[0] == "entered"
    assert calls[1]["model"] == "gpt-5.5"
    assert "시스템" in calls[2]
    assert "질문" in calls[2]


@pytest.mark.asyncio
async def test_generate_json_uses_codex_and_parses_code_fenced_json(monkeypatch):
    class FakeResult:
        final_response = '```json\n{"intent":"test"}\n```'

    class FakeThread:
        async def run(self, prompt):
            return FakeResult()

    class FakeAsyncCodex:
        async def __aenter__(self):
            return self

        async def thread_start(self, **kwargs):
            return FakeThread()

    monkeypatch.setattr(llm_client, "AsyncCodex", FakeAsyncCodex)

    assert await llm_client.generate_json("JSON으로 답해") == {"intent": "test"}


@pytest.mark.asyncio
async def test_generate_embeddings_uses_local_deterministic_vectors_for_codex(monkeypatch):
    first = await llm_client.generate_embeddings(["alpha", "beta"])
    second = await llm_client.generate_embeddings(["alpha", "beta"])

    assert first == second
    assert len(first) == 2
    assert len(first[0]) == 64
    assert first[0] != first[1]
