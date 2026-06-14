from __future__ import annotations

import json
import math
import sqlite3
from pathlib import Path
from typing import Iterable

from app.models.schemas import CosmicEdge, CosmicNode, InputAnalysis, PruningDecision


class CGIMemoryStore:
    """SQLite-backed bounded memory for CGI runs and generated graph artifacts."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path).expanduser()
        self.initialize()

    def initialize(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.execute("pragma journal_mode=WAL")
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS cgi_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL,
                    mode TEXT NOT NULL,
                    intent TEXT NOT NULL DEFAULT 'general',
                    keywords_json TEXT NOT NULL DEFAULT '[]',
                    domain_json TEXT NOT NULL DEFAULT '[]',
                    compressed_context TEXT NOT NULL DEFAULT '',
                    response_content TEXT NOT NULL DEFAULT '',
                    latency_ms REAL NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS cgi_nodes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id INTEGER NOT NULL REFERENCES cgi_runs(id) ON DELETE CASCADE,
                    node_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    state TEXT NOT NULL,
                    description TEXT NOT NULL DEFAULT '',
                    mass REAL NOT NULL DEFAULT 0,
                    energy REAL NOT NULL DEFAULT 0,
                    immediate_utility REAL NOT NULL DEFAULT 0,
                    creative_potential REAL NOT NULL DEFAULT 0,
                    noise_risk REAL NOT NULL DEFAULT 0,
                    memory_bonus REAL NOT NULL DEFAULT 0,
                    survival_score REAL NOT NULL DEFAULT 0,
                    embedding_json TEXT NOT NULL DEFAULT '[]',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS cgi_edges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id INTEGER NOT NULL REFERENCES cgi_runs(id) ON DELETE CASCADE,
                    source_node_id TEXT NOT NULL,
                    target_node_id TEXT NOT NULL,
                    weight REAL NOT NULL DEFAULT 0,
                    attraction REAL NOT NULL DEFAULT 0,
                    repulsion REAL NOT NULL DEFAULT 0,
                    edge_type TEXT NOT NULL DEFAULT 'semantic',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS cgi_relationships (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id INTEGER NOT NULL REFERENCES cgi_runs(id) ON DELETE CASCADE,
                    relationship_type TEXT NOT NULL,
                    node_a TEXT NOT NULL,
                    node_b TEXT NOT NULL,
                    score REAL NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_cgi_nodes_name ON cgi_nodes(name)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_cgi_nodes_run_id ON cgi_nodes(run_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_cgi_runs_created_at ON cgi_runs(created_at)")

    def save_run(
        self,
        *,
        question: str,
        mode: str,
        analysis: InputAnalysis,
        nodes: list[CosmicNode],
        edges: list[CosmicEdge],
        decisions: list[PruningDecision],
        binary_systems: list[list[str]],
        wormhole_connections: list[list[str]],
        compressed_context: str,
        response_content: str,
        latency_ms: float,
    ) -> int:
        decision_by_id = {decision.node_id: decision for decision in decisions}
        with self._connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO cgi_runs (
                    question, mode, intent, keywords_json, domain_json,
                    compressed_context, response_content, latency_ms
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    question,
                    mode,
                    analysis.intent,
                    json.dumps(analysis.keywords, ensure_ascii=False),
                    json.dumps(analysis.domain, ensure_ascii=False),
                    compressed_context,
                    response_content,
                    float(latency_ms),
                ),
            )
            run_id = int(cur.lastrowid)

            for node in nodes:
                decision = decision_by_id.get(node.id)
                conn.execute(
                    """
                    INSERT INTO cgi_nodes (
                        run_id, node_id, name, type, state, description, mass, energy,
                        immediate_utility, creative_potential, noise_risk, memory_bonus,
                        survival_score, embedding_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        run_id,
                        node.id,
                        node.name,
                        node.type,
                        decision.next_state if decision else node.state,
                        node.description,
                        float(node.mass),
                        float(node.energy),
                        float(decision.immediate_utility if decision else node.immediate_utility),
                        float(decision.creative_potential if decision else node.creative_potential),
                        float(decision.noise_risk if decision else node.noise_risk),
                        float(decision.memory_bonus if decision else node.memory_bonus),
                        float(decision.survival_score if decision else node.survival_score),
                        json.dumps(node.embedding),
                    ),
                )

            for edge in edges:
                conn.execute(
                    """
                    INSERT INTO cgi_edges (
                        run_id, source_node_id, target_node_id, weight,
                        attraction, repulsion, edge_type
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        run_id,
                        edge.source,
                        edge.target,
                        float(edge.weight),
                        float(edge.attraction),
                        float(edge.repulsion),
                        edge.edge_type,
                    ),
                )

            self._insert_relationships(conn, run_id, "binary", binary_systems)
            self._insert_relationships(conn, run_id, "wormhole", wormhole_connections)
            return run_id

    def get_recent_node_context(self, *, limit: int = 12) -> list[dict[str, object]]:
        if limit <= 0:
            return []
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT n.id AS storage_id, n.name, n.type, n.state, n.description, n.immediate_utility,
                       n.creative_potential, r.question, r.created_at
                FROM cgi_nodes n
                JOIN cgi_runs r ON r.id = n.run_id
                ORDER BY n.id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]

    def search_similar_node_context(
        self,
        *,
        query_embedding: list[float],
        limit: int = 12,
    ) -> list[dict[str, object]]:
        """Search all persisted node embeddings and return the top-k most similar nodes."""
        if limit <= 0 or not query_embedding:
            return []
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT n.id AS storage_id, n.name, n.type, n.state, n.description,
                       n.immediate_utility, n.creative_potential, n.embedding_json,
                       r.question, r.created_at
                FROM cgi_nodes n
                JOIN cgi_runs r ON r.id = n.run_id
                WHERE n.embedding_json IS NOT NULL AND n.embedding_json != '[]'
                """
            ).fetchall()

        scored: list[dict[str, object]] = []
        for row in rows:
            try:
                embedding = json.loads(row["embedding_json"] or "[]")
            except json.JSONDecodeError:
                continue
            similarity = self._cosine_similarity(query_embedding, embedding)
            if similarity <= 0:
                continue
            item = dict(row)
            item.pop("embedding_json", None)
            item["similarity"] = round(similarity, 6)
            scored.append(item)

        scored.sort(key=lambda item: (float(item["similarity"]), int(item["storage_id"])), reverse=True)
        return scored[:limit]

    def format_mixed_node_context(
        self,
        *,
        query_embedding: list[float],
        recent_limit: int = 6,
        similar_limit: int = 12,
        total_limit: int = 18,
    ) -> str:
        """Format bounded recent + similarity-search memory without duplicate nodes."""
        if total_limit <= 0:
            return ""

        recent_nodes = self.get_recent_node_context(limit=max(0, recent_limit))
        similar_nodes = self.search_similar_node_context(
            query_embedding=query_embedding,
            limit=max(0, similar_limit),
        )

        used_ids: set[int] = set()
        recent_selected: list[dict[str, object]] = []
        similar_selected: list[dict[str, object]] = []

        for node in recent_nodes:
            if len(recent_selected) + len(similar_selected) >= total_limit:
                break
            storage_id = int(node["storage_id"])
            if storage_id in used_ids:
                continue
            used_ids.add(storage_id)
            recent_selected.append(node)

        for node in similar_nodes:
            if len(recent_selected) + len(similar_selected) >= total_limit:
                break
            storage_id = int(node["storage_id"])
            if storage_id in used_ids:
                continue
            used_ids.add(storage_id)
            similar_selected.append(node)

        if not recent_selected and not similar_selected:
            return ""

        lines = ["## 과거 대화에서 저장된 CGI 메모리"]
        if recent_selected:
            lines.append("### 최근 CGI 노드")
            lines.extend(self._format_node_line(node) for node in recent_selected)
        if similar_selected:
            lines.append("### 질문과 유사한 CGI 노드")
            for node in similar_selected:
                similarity = node.get("similarity")
                suffix = f" 유사도={similarity}" if similarity is not None else ""
                lines.append(f"{self._format_node_line(node)}{suffix}")
        lines.append("위 과거 노드는 관련성이 있을 때만 참고하고, 현재 사용자 질문을 우선해라.")
        return "\n".join(lines)

    def format_recent_node_context(self, *, limit: int = 12) -> str:
        nodes = self.get_recent_node_context(limit=limit)
        if not nodes:
            return ""
        lines = ["## 과거 대화에서 저장된 최근 CGI 노드"]
        for node in nodes:
            desc = str(node.get("description") or "")
            if len(desc) > 120:
                desc = desc[:117] + "..."
            lines.append(
                f"- {node['name']} ({node['state']}, {node['type']}): {desc}"
            )
        lines.append("위 과거 노드는 관련성이 있을 때만 참고하고, 현재 사용자 질문을 우선해라.")
        return "\n".join(lines)

    @staticmethod
    def _format_node_line(node: dict[str, object]) -> str:
        desc = str(node.get("description") or "")
        if len(desc) > 120:
            desc = desc[:117] + "..."
        return f"- {node['name']} ({node['state']}, {node['type']}): {desc}"

    @staticmethod
    def _cosine_similarity(left: list[float], right: list[float]) -> float:
        size = min(len(left), len(right))
        if size <= 0:
            return 0.0
        dot = sum(float(left[i]) * float(right[i]) for i in range(size))
        left_norm = math.sqrt(sum(float(left[i]) ** 2 for i in range(size)))
        right_norm = math.sqrt(sum(float(right[i]) ** 2 for i in range(size)))
        if left_norm == 0 or right_norm == 0:
            return 0.0
        return dot / (left_norm * right_norm)

    def _insert_relationships(
        self,
        conn: sqlite3.Connection,
        run_id: int,
        relationship_type: str,
        pairs: Iterable[list[str]],
    ) -> None:
        for pair in pairs:
            if len(pair) < 2:
                continue
            conn.execute(
                """
                INSERT INTO cgi_relationships (run_id, relationship_type, node_a, node_b)
                VALUES (?, ?, ?, ?)
                """,
                (run_id, relationship_type, pair[0], pair[1]),
            )

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys=ON")
        return conn
