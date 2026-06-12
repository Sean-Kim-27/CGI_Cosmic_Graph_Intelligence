# Cosmic Graph Intelligence 설계안

## 1. 프로젝트 개요

**Cosmic Graph Intelligence**는 우주의 다체 상호작용, 쌍성계 형성, 블랙홀, 양자얽힘, 웜홀 개념을 컴퓨터공학적으로 추상화한 **그래프 기반 자기조직형 지능체 시스템**이다.

이 프로젝트는 실제 우주의 중력, 웜홀, 양자얽힘을 직접 사용하는 것이 아니라, 해당 개념들을 다음과 같은 AI 시스템 구성요소로 변환한다.

* 중력 → 노드 간 관계 강도
* 삼체문제 → 다중 에이전트 간 동적 상호작용
* 쌍성계 → 안정적으로 결합한 에이전트 조합
* 블랙홀 → 정보를 강하게 압축하는 중심 허브 노드
* 양자얽힘 → 멀리 떨어진 노드 사이의 숨은 상관관계 메모리
* 웜홀 → 서로 멀리 있는 개념을 빠르게 연결하는 shortcut edge
* 탈출 천체 → 현재 문제 해결에 기여도가 낮아 비활성화되는 후보 노드

최종 목표는 단순 질의응답 AI가 아니라, 여러 개의 지능 노드가 서로 상호작용하며 새로운 아이디어, 가설, 설계안, 문제 해결 전략을 생성하는 **창의적 탐색형 AI 시스템**을 만드는 것이다.

---

## 2. 개발 목표

### 2.1 1차 목표

사용자가 하나의 주제나 문제를 입력하면, 시스템이 관련 개념 노드를 생성하고, 노드 간 관계를 계산한 뒤, 안정적인 클러스터를 만들어 새로운 아이디어나 답변을 생성한다.

예시:

```text
입력:
백엔드 포트폴리오 프로젝트 아이디어 추천

활성화 노드:
Spring, MySQL, AWS, 지도 API, 감정 분석, 로컬 관광, 추억여행

형성된 쌍성계:
Spring + MySQL
지도 API + 로컬 관광
감정 분석 + 추억여행

최종 출력:
개인 추억 기반 로컬 여행 스케줄러 백엔드 프로젝트
```

### 2.2 장기 목표

* 자기조직화되는 지능체 네트워크 구현
* 사용자의 관심사에 따라 노드 관계가 강화되는 장기 기억 구조 구현
* 멀리 떨어진 개념 간 shortcut 연결을 통한 창의적 발상 생성
* 다중 에이전트 기반 문제 해결 시스템 구현
* 추후 LLM, RAG, 그래프 신경망, 시뮬레이션 기반 탐색 알고리즘과 결합

---

## 3. 핵심 개념 매핑

| 우주 개념 | 컴퓨터공학적 해석        | 구현 방식                              |
| ----- | ---------------- | ---------------------------------- |
| 천체    | 지능 노드 또는 개념 노드   | AgentNode, ConceptNode             |
| 중력    | 노드 간 끌림          | similarity, importance, usefulness |
| 반발력   | 중복, 충돌, 모순       | redundancy, conflict               |
| 삼체문제  | 여러 노드 간 불안정 상호작용 | dynamic graph update               |
| 쌍성계   | 안정적인 2개 노드 조합    | strong edge pair                   |
| 성단    | 여러 노드의 클러스터      | community detection                |
| 블랙홀   | 정보 압축 허브         | summarizer, compressor             |
| 양자얽힘  | 숨은 상관관계          | co-activation memory               |
| 웜홀    | 먼 개념 간 shortcut  | long-range edge                    |
| 탈출 천체 | 비활성화 노드          | pruning, decay                     |

---

## 4. 전체 시스템 구조

```text
[User Input]
    ↓
[Input Analyzer]
    ↓
[Concept Node Generator]
    ↓
[Cosmic Graph Engine]
    ├─ Attraction Calculator
    ├─ Repulsion Calculator
    ├─ Stability Evaluator
    ├─ Cluster/Binary Detector
    └─ Escape Node Pruner
       ├─ Immediate Utility Scorer
       ├─ Creative Potential Scorer
       ├─ Noise/Risk Scorer
       └─ Survival Threshold Classifier
    ↓
[Entanglement Memory]
    ├─ Past Co-activation Search
    ├─ Hidden Relation Retrieval
    └─ Wormhole Shortcut Generator
    ↓
[Black Hole Compressor]
    ↓
[Reasoning Agent]
    ↓
[Final Response Generator]
```

---

## 5. 주요 모듈 설계

## 5.1 Input Analyzer

사용자의 입력을 분석하여 문제 유형, 핵심 키워드, 요구 출력 형식을 추출한다.

### 역할

* 사용자 질문 분류
* 핵심 개념 추출
* 출력 목적 파악
* 필요한 노드 유형 결정

### 예시 입력

```text
우주적 네트워크를 모방한 AI를 개발하고 싶어
```

### 예시 출력

```json
{
  "intent": "system_design",
  "keywords": ["우주적 네트워크", "AI", "모방", "지능체"],
  "domain": ["computer_science", "ai_architecture", "complex_system"],
  "output_type": "design_document"
}
```

---

## 5.2 Concept Node Generator

입력에서 나온 개념들을 기반으로 초기 노드들을 생성한다.

### 노드 예시

```json
{
  "id": "node_001",
  "name": "Spring",
  "type": "technology",
  "mass": 0.75,
  "energy": 0.60,
  "embedding": [0.12, 0.44, 0.91],
  "state": "active"
}
```

### 주요 속성

| 속성          | 의미                                    |
| ----------- | ------------------------------------- |
| id          | 노드 고유 ID                              |
| name        | 개념명                                   |
| type        | 기술, 개념, 데이터, 목표 등                     |
| mass        | 중요도                                   |
| energy      | 활성도                                   |
| embedding   | 의미 벡터                                 |
| state       | active, orbiting, dormant, escaped, garbage, compressed |
| memory_refs | 과거 메모리 연결                             |

---

## 5.3 Cosmic Graph Engine

시스템의 핵심 모듈이다. 노드 간 관계를 계산하고, 그래프를 갱신하며, 안정적인 조합을 찾는다.

### 5.3.1 Attraction 계산

두 노드가 서로 얼마나 강하게 연결될 수 있는지 계산한다.

```text
attraction(i, j)
= semantic_similarity(i, j)
× importance(i)
× importance(j)
× complementarity(i, j)
```

### 5.3.2 Repulsion 계산

두 노드가 서로 충돌하거나 중복되는 정도를 계산한다.

```text
repulsion(i, j)
= redundancy(i, j)
+ contradiction(i, j)
+ context_mismatch(i, j)
```

### 5.3.3 Edge Weight 계산

최종 관계 강도는 끌림에서 반발을 뺀 값으로 계산한다.

```text
edge_weight(i, j)
= attraction(i, j) - repulsion(i, j)
```

### 5.3.4 안정성 평가

두 노드 또는 세 노드 이상의 조합이 안정적인지 평가한다.

```text
stability(cluster)
= internal_cohesion
- internal_conflict
+ usefulness_to_task
- redundancy_penalty
```

---

## 5.4 Binary System Detector

강하게 연결된 두 노드를 찾아 쌍성계로 묶는다.

### 쌍성계 조건

* edge_weight가 특정 threshold 이상
* 두 노드의 역할이 상호보완적
* 현재 문제 해결에 함께 기여
* 중복도가 지나치게 높지 않음

### 예시

```text
Spring + MySQL
지도 API + 로컬 관광
감정 분석 + 추억여행
LLM + Vector DB
```

### 출력 구조

```json
{
  "binary_id": "binary_001",
  "nodes": ["Spring", "MySQL"],
  "stability": 0.87,
  "role": "backend_core"
}
```

---

## 5.5 Escape Node Pruner

현재 문제 해결에 적합하지 않은 노드를 무조건 삭제하지 않고, **즉시 유용성**, **창의적 잠재력**, **노이즈 위험**, **과거 성공 기록**을 함께 평가하여 노드의 생존 상태를 결정한다.

이 모듈의 핵심 목적은 단순한 정리 작업이 아니라, 당장은 멀어 보이지만 나중에 웜홀 연결을 만들 수 있는 노드를 보존하는 것이다.

### 5.5.1 노드 상태 분류

| 상태 | 의미 | 처리 방식 |
|---|---|---|
| active | 현재 문제 해결에 직접 기여하는 노드 | 최종 추론 context에 포함 |
| orbiting | 직접 핵심은 아니지만 주변 후보로 유효한 노드 | 낮은 우선순위로 유지 |
| dormant | 지금은 멀지만 웜홀 후보 가능성이 있는 노드 | Entanglement Memory에 보존 |
| escaped | 현재 세션에서는 제외되는 노드 | 장기 메모리에 약하게 저장 |
| garbage | 반복적으로 가치가 낮고 노이즈가 큰 노드 | 삭제 또는 재사용 금지 후보 |

상태 변화는 다음과 같이 설계한다.

```text
active → orbiting → dormant → escaped → garbage
```

단, `dormant` 상태의 노드는 완전히 버려진 것이 아니라, 추후 다른 입력에서 `Wormhole Shortcut Generator`에 의해 재활성화될 수 있다.

---

### 5.5.2 핵심 점수 정의

각 노드 `i`에 대해 다음 네 가지 점수를 계산한다.

```text
Uᵢ = Immediate Utility Score
Cᵢ = Creative Potential Score
Nᵢ = Noise / Risk Score
Mᵢ = Memory Bonus Score
```

| 점수 | 의미 |
|---|---|
| Uᵢ | 지금 문제 해결에 얼마나 직접적으로 도움 되는가 |
| Cᵢ | 멀리 떨어진 개념과 연결해 창의적 웜홀을 만들 가능성이 있는가 |
| Nᵢ | 노이즈, 중복, 모순, 환각 위험이 얼마나 큰가 |
| Mᵢ | 과거에 좋은 결과를 만든 조합에 포함된 적이 있는가 |

최종 생존 점수는 다음과 같이 계산한다.

```text
Sᵢ = λUᵢ + (1 - λ)Cᵢ - μNᵢ + ηMᵢ
```

| 기호 | 의미 |
|---|---|
| Sᵢ | 최종 생존 점수 |
| λ | 즉시 유용성과 창의성 사이의 균형 계수 |
| μ | 노이즈 패널티 강도 |
| η | 과거 성공 기록 보정치 |

모드별 기본값은 다음과 같다.

| 모드 | λ | μ | η | 특징 |
|---|---:|---:|---:|---|
| accurate | 0.80 | 0.80 | 0.20 | 정확성과 관련성을 우선 |
| balanced | 0.60 | 0.65 | 0.25 | 일반 사용 기본값 |
| creative | 0.45 | 0.55 | 0.30 | 창의적 웜홀 후보를 더 오래 보존 |
| research | 0.40 | 0.60 | 0.35 | 가설 생성과 장기 연결 탐색에 유리 |

---

### 5.5.3 Immediate Utility Score

`Uᵢ`는 현재 입력과 직접적으로 연결되는 정도를 계산한다.

```text
Uᵢ =
0.45 × relevance_to_query
+ 0.25 × task_usefulness
+ 0.20 × cluster_support
+ 0.10 × user_preference_match
```

| 항목 | 의미 |
|---|---|
| relevance_to_query | 사용자 입력과 의미적으로 가까운 정도 |
| task_usefulness | 현재 문제 해결에 필요한 기능적 기여도 |
| cluster_support | 안정적인 클러스터 형성에 기여하는 정도 |
| user_preference_match | 사용자 관심사나 이전 선택과 맞는 정도 |

예를 들어 사용자가 “백엔드 포트폴리오 프로젝트”를 입력했을 때 `Spring`, `MySQL`, `AWS`는 `Uᵢ`가 높다. 반면 `양자얽힘`, `추억여행`은 `Uᵢ`만 보면 낮거나 중간일 수 있다.

---

### 5.5.4 Creative Potential Score

`Cᵢ`는 노드가 당장은 멀어 보여도 창의적 shortcut, 즉 웜홀 연결을 만들 가능성이 있는지 평가한다.

```text
Cᵢ =
0.30 × novelty
+ 0.25 × bridge_potential
+ 0.20 × cross_domain_distance
+ 0.15 × entanglement_memory
+ 0.10 × reinterpretability
```

| 항목 | 의미 |
|---|---|
| novelty | 기존 답변에서 흔하지 않은 개념인가 |
| bridge_potential | 서로 다른 클러스터를 이어줄 수 있는가 |
| cross_domain_distance | 현재 주제와 멀지만 완전히 무관하지는 않은가 |
| entanglement_memory | 과거에 좋은 결과와 함께 쓰인 적이 있는가 |
| reinterpretability | 현재 문제에 비유, 구조, 기능으로 재해석 가능한가 |

중요한 기준은 **멀리 있는가**가 아니라 **설명 가능한 연결 경로가 있는가**이다.

예시:

```text
백엔드 포트폴리오 → 지도 API → 로컬 관광 → 추억여행
```

이 경우 `추억여행`은 즉시 유용성은 낮아도, `지도 API`, `사용자 기록`, `개인화 추천`과 연결되면 높은 창의적 잠재력을 가진다.

---

### 5.5.5 Noise / Risk Score

`Nᵢ`는 노드가 결과 품질을 떨어뜨릴 위험을 계산한다.

```text
Nᵢ =
0.35 × contradiction
+ 0.25 × redundancy
+ 0.20 × hallucination_risk
+ 0.10 × context_mismatch
+ 0.10 × low_explainability
```

| 항목 | 의미 |
|---|---|
| contradiction | 다른 노드 또는 사실과 충돌하는 정도 |
| redundancy | 이미 존재하는 노드와 중복되는 정도 |
| hallucination_risk | 근거 없는 연결을 만들 가능성 |
| context_mismatch | 현재 사용자의 목적과 어긋나는 정도 |
| low_explainability | 왜 필요한지 설명하기 어려운 정도 |

창의성이 높아도 `Nᵢ`가 높으면 최종 답변에는 사용하지 않는다. 이 경우 해당 노드는 `dormant`가 아니라 `escaped` 또는 `garbage`로 보낸다.

---

### 5.5.6 최소 생존 임계값

초기 MVP에서는 다음 threshold를 사용한다.

```text
T_active   = 0.65
T_creative = 0.60
T_noise    = 0.45
T_survival = 0.35
T_garbage_U = 0.25
T_garbage_C = 0.30
T_garbage_N = 0.60
```

판정 규칙은 다음과 같다.

```text
if Uᵢ >= T_active:
    active

elif Cᵢ >= T_creative and Nᵢ <= T_noise:
    dormant_wormhole_candidate

elif Sᵢ >= T_survival:
    orbiting

elif Uᵢ < T_garbage_U and Cᵢ < T_garbage_C and Nᵢ > T_garbage_N:
    garbage

else:
    escaped
```

핵심 원칙은 다음과 같다.

```text
낮은 관련도만으로 노드를 죽이지 않는다.
높은 노이즈는 빠르게 제거한다.
낮은 관련도 + 높은 창의성 + 낮은 위험도는 웜홀 후보로 살린다.
반복적으로 기여하지 못한 노드는 점점 먼 상태로 보낸다.
한 번이라도 좋은 웜홀을 만든 노드는 메모리 보너스를 준다.
```

---

### 5.5.7 예시 판정

입력:

```text
백엔드 개발자 포트폴리오로 쓸만한 독특한 프로젝트를 추천해줘
```

| 노드 | Uᵢ | Cᵢ | Nᵢ | 판정 |
|---|---:|---:|---:|---|
| Spring | 0.92 | 0.30 | 0.10 | active |
| MySQL | 0.88 | 0.25 | 0.10 | active |
| AWS | 0.80 | 0.35 | 0.15 | active |
| 지도 API | 0.70 | 0.65 | 0.15 | active |
| 감정 분석 | 0.55 | 0.72 | 0.20 | orbiting |
| 추억여행 | 0.42 | 0.83 | 0.18 | dormant_wormhole_candidate |
| 양자얽힘 | 0.20 | 0.75 | 0.35 | dormant_wormhole_candidate, 단 최종 사용 전 설명 가능성 재검증 |
| 고양이 | 0.15 | 0.40 | 0.30 | escaped |
| 비트코인 | 0.18 | 0.35 | 0.55 | escaped 또는 garbage 후보 |

이 예시에서 `추억여행`은 당장 백엔드와 직접 관련성이 낮지만, `지도 API`, `사용자 기록`, `개인화 추천`과 연결될 수 있으므로 웜홀 후보로 보존한다.

---

### 5.5.8 구현용 의사코드

```python
def classify_node(node, context):
    U = compute_immediate_utility(node, context)
    C = compute_creative_potential(node, context)
    N = compute_noise_risk(node, context)
    M = compute_memory_bonus(node, context)

    if context.mode == "creative":
        lambda_weight = 0.45
        mu = 0.55
        eta = 0.30
    elif context.mode == "accurate":
        lambda_weight = 0.80
        mu = 0.80
        eta = 0.20
    elif context.mode == "research":
        lambda_weight = 0.40
        mu = 0.60
        eta = 0.35
    else:
        lambda_weight = 0.60
        mu = 0.65
        eta = 0.25

    S = (
        lambda_weight * U
        + (1 - lambda_weight) * C
        - mu * N
        + eta * M
    )

    if U >= 0.65:
        state = "active"
    elif C >= 0.60 and N <= 0.45:
        state = "dormant_wormhole_candidate"
    elif S >= 0.35:
        state = "orbiting"
    elif U < 0.25 and C < 0.30 and N > 0.60:
        state = "garbage"
    else:
        state = "escaped"

    return {
        "node_id": node.id,
        "state": state,
        "survival_score": S,
        "immediate_utility": U,
        "creative_potential": C,
        "noise_risk": N,
        "memory_bonus": M,
    }
```

---

### 5.5.9 튜닝 전략

초기에는 고정 threshold로 시작하되, 사용자 피드백과 결과 품질에 따라 자동 조정한다.

| 상황 | 조정 방향 |
|---|---|
| 결과가 너무 평범함 | `T_creative`를 낮추고 `Cᵢ` 가중치를 높임 |
| 결과가 너무 뜬금없음 | `T_noise`를 낮추고 `Nᵢ` 패널티를 높임 |
| 유용한 노드가 너무 빨리 사라짐 | `T_survival`을 낮추고 `Mᵢ` 보너스를 높임 |
| 그래프가 너무 복잡함 | active/orbiting/dormant 노드 수에 상한 설정 |
| 사용자가 특정 조합을 채택함 | 해당 노드들의 `Mᵢ`와 entanglement score 증가 |

권장 노드 생존 예산은 다음과 같다.

```text
초기 노드 30개 기준
active: 8~12개
orbiting: 5~8개
dormant_wormhole_candidate: 3~6개
escaped/garbage: 나머지
```

최종적으로 Pruner의 판정 기준은 다음 문장으로 정의한다.

```text
Garbage는 멀리 있는 노드가 아니라, 설명 가능한 연결 경로가 없고 반복적으로 품질을 떨어뜨리는 노드다.
```


---

## 5.6 Entanglement Memory

멀리 떨어진 노드 사이의 숨은 상관관계를 저장하는 모듈이다.

### 핵심 아이디어

직접 연결되어 있지 않은 개념이라도, 과거에 함께 사용되어 좋은 결과를 만든 적이 있다면 둘 사이의 entanglement score를 높인다.

```text
entanglement_score(A, B)
= co_activation_frequency
+ shared_success_score
+ cross_domain_novelty
+ user_preference_boost
```

### 예시

```text
백엔드 프로젝트 ↔ 추억여행
지도 API ↔ 지역 관광
감정 분석 ↔ 개인화 추천
블랙홀 ↔ 정보 압축
웜홀 ↔ shortcut search
```

---

## 5.7 Wormhole Shortcut Generator

서로 멀리 떨어져 있지만 연결하면 창의적인 결과가 나올 수 있는 노드들을 연결한다.

### 역할

* 기존 그래프에서 거리가 먼 노드 탐색
* entanglement score가 높은 노드 후보 검색
* 창의적 연결 생성
* 새로운 아이디어 후보 생성

### 예시

```text
입력:
AI 포트폴리오 프로젝트

일반 연결:
Spring → MySQL → AWS

웜홀 연결:
AI 포트폴리오 → 추억여행 → 로컬 관광 → 지도 API

결과:
추억 기반 로컬 여행 스케줄러
```

---

## 5.8 Black Hole Compressor

여러 노드와 클러스터의 정보를 압축하여 최종 추론에 사용할 핵심 요약을 만든다.

### 역할

* 클러스터별 핵심 의미 요약
* 중복 제거
* 중요한 정보 우선순위화
* 최종 reasoning context 생성

### 예시 입력

```text
Spring, MySQL, AWS, 지도 API, 감정 분석, 추억여행, 로컬 관광
```

### 예시 출력

```text
사용자는 백엔드 중심의 포트폴리오 프로젝트를 원하며,
지도 API와 감정 분석을 결합한 개인화 로컬 여행 스케줄러가 적합하다.
```

---

## 6. 데이터 구조 설계

## 6.1 Node Schema

```python
class CosmicNode:
    id: str
    name: str
    type: str
    mass: float
    energy: float
    embedding: list[float]
    state: str
    immediate_utility: float
    creative_potential: float
    noise_risk: float
    memory_bonus: float
    survival_score: float
    metadata: dict
```

## 6.2 Edge Schema

```python
class CosmicEdge:
    source: str
    target: str
    weight: float
    attraction: float
    repulsion: float
    entanglement_score: float
    edge_type: str
```

## 6.3 Cluster Schema

```python
class CosmicCluster:
    id: str
    node_ids: list[str]
    stability: float
    role: str
    summary: str
```

## 6.4 Memory Schema

```python
class EntanglementMemory:
    node_a: str
    node_b: str
    co_activation_count: int
    success_score: float
    last_used_at: str
    context: str
```

## 6.5 Pruning Decision Schema

```python
class PruningDecision:
    node_id: str
    previous_state: str
    next_state: str
    immediate_utility: float
    creative_potential: float
    noise_risk: float
    memory_bonus: float
    survival_score: float
    reason: str
```

---

## 7. 핵심 알고리즘 흐름

## 7.1 기본 실행 흐름

```text
1. 사용자 입력 수신
2. 입력에서 핵심 개념 추출
3. 개념 노드 생성
4. 노드 임베딩 생성
5. 모든 노드 쌍에 대해 attraction/repulsion 계산
6. 그래프 edge weight 갱신
7. 안정적인 쌍성계 탐색
8. Escape Node Pruner로 노드를 active/orbiting/dormant/escaped/garbage 상태로 분류
9. dormant_wormhole_candidate를 포함해 Entanglement Memory에서 숨은 연결 검색
10. Wormhole Shortcut 생성
11. Black Hole Compressor가 핵심 정보 압축
12. Reasoning Agent가 최종 답변 생성
13. 결과에 기여한 노드 관계를 메모리에 업데이트
```

---

## 7.2 Pseudo Code

```python
def run_cosmic_intelligence(user_input: str):
    analysis = analyze_input(user_input)

    nodes = generate_concept_nodes(analysis)

    graph = initialize_graph(nodes)

    for node_i in nodes:
        for node_j in nodes:
            if node_i.id == node_j.id:
                continue

            attraction = calculate_attraction(node_i, node_j)
            repulsion = calculate_repulsion(node_i, node_j)

            weight = attraction - repulsion

            if weight > MIN_EDGE_THRESHOLD:
                graph.add_edge(
                    node_i.id,
                    node_j.id,
                    weight=weight,
                    attraction=attraction,
                    repulsion=repulsion
                )

    binaries = detect_binary_systems(graph)

    clusters = detect_stable_clusters(graph)

    pruning_decisions = [
        classify_node(node, context=analysis)
        for node in nodes
    ]

    active_nodes = filter_nodes_by_state(pruning_decisions, "active")
    orbiting_nodes = filter_nodes_by_state(pruning_decisions, "orbiting")
    dormant_nodes = filter_nodes_by_state(
        pruning_decisions,
        "dormant_wormhole_candidate"
    )

    entangled_nodes = retrieve_entangled_nodes(
        active_nodes + orbiting_nodes + dormant_nodes
    )

    wormhole_edges = create_wormhole_shortcuts(
        graph,
        entangled_nodes,
        candidate_nodes=dormant_nodes
    )

    compressed_context = black_hole_compress(
        nodes=active_nodes,
        binaries=binaries,
        clusters=clusters,
        wormhole_edges=wormhole_edges,
        pruning_decisions=pruning_decisions
    )

    result = reasoning_agent(compressed_context)

    update_entanglement_memory(result)

    return result
```

---

## 8. 기술 스택

## 8.1 MVP 기준

| 영역         | 기술                                         |
| ---------- | ------------------------------------------ |
| 언어         | Python                                     |
| 그래프 처리     | NetworkX                                   |
| 임베딩        | Sentence Transformers 또는 OpenAI Embeddings |
| 벡터 DB      | Chroma                                     |
| 에이전트 워크플로우 | LangGraph                                  |
| API 서버     | FastAPI                                    |
| 데이터 저장     | SQLite 또는 PostgreSQL                       |
| 프론트엔드      | React 또는 Next.js                           |
| 시각화        | D3.js 또는 Cytoscape.js                      |

## 8.2 확장 단계

| 영역        | 기술                   |
| --------- | -------------------- |
| 딥러닝 모델    | PyTorch              |
| 그래프 신경망   | PyTorch Geometric    |
| 대규모 벡터 검색 | FAISS, Milvus        |
| 비동기 작업    | Celery, Redis        |
| 배포        | Docker, AWS EC2, ECS |
| 관측성       | Prometheus, Grafana  |
| 로그 분석     | OpenTelemetry        |

---

## 9. MVP 기능 명세

## 9.1 필수 기능

### 1. 주제 입력

사용자가 탐색하고 싶은 주제를 입력한다.

```text
예:
백엔드 포트폴리오 프로젝트 추천
```

### 2. 개념 노드 생성

입력과 관련된 개념 노드를 자동 생성한다.

```text
Spring, MySQL, AWS, 지도 API, 감정 분석, 로컬 관광
```

### 3. 관계 계산

각 노드 간 의미 유사도, 보완성, 중복도, 충돌도를 계산한다.

### 4. 쌍성계 탐색

가장 안정적인 2개 노드 조합을 찾는다.

```text
Spring + MySQL
지도 API + 로컬 관광
```

### 5. 웜홀 연결 생성

직접적으로 가깝지는 않지만 창의적인 결과를 만들 수 있는 연결을 추가한다.

```text
백엔드 → 추억여행
감정 분석 → 로컬 관광
```

### 6. 결과 생성

최종적으로 하나 이상의 아이디어, 설계안, 답변을 생성한다.

---

## 10. API 설계

## 10.1 주제 분석 API

```http
POST /api/analyze
```

### Request

```json
{
  "input": "백엔드 포트폴리오 프로젝트 추천"
}
```

### Response

```json
{
  "intent": "idea_generation",
  "keywords": ["백엔드", "포트폴리오", "프로젝트"],
  "domain": ["software_engineering", "career"]
}
```

---

## 10.2 그래프 생성 API

```http
POST /api/graph/generate
```

### Request

```json
{
  "keywords": ["백엔드", "포트폴리오", "프로젝트"]
}
```

### Response

```json
{
  "nodes": [],
  "edges": [],
  "clusters": []
}
```

---

## 10.3 결과 생성 API

```http
POST /api/generate
```

### Request

```json
{
  "input": "AI 기반 백엔드 프로젝트 아이디어를 추천해줘",
  "mode": "creative"
}
```

### Response

```json
{
  "answer": "개인 추억 기반 로컬 여행 스케줄러를 추천합니다.",
  "binaries": [
    ["Spring", "MySQL"],
    ["지도 API", "로컬 관광"]
  ],
  "wormholes": [
    ["백엔드", "추억여행"],
    ["감정 분석", "개인화 추천"]
  ]
}
```

---

## 11. 폴더 구조

```text
cosmic-graph-intelligence/
├── README.md
├── requirements.txt
├── .env.example
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── analyze.py
│   │   ├── graph.py
│   │   └── generate.py
│   ├── core/
│   │   ├── nodes.py
│   │   ├── edges.py
│   │   ├── graph_engine.py
│   │   ├── attraction.py
│   │   ├── repulsion.py
│   │   ├── stability.py
│   │   ├── binary_detector.py
│   │   ├── escape_node_pruner.py
│   │   ├── utility_score.py
│   │   ├── creative_potential.py
│   │   ├── noise_risk.py
│   │   ├── wormhole.py
│   │   └── blackhole_compressor.py
│   ├── memory/
│   │   ├── entanglement_memory.py
│   │   ├── vector_store.py
│   │   └── memory_updater.py
│   ├── agents/
│   │   ├── reasoning_agent.py
│   │   ├── critique_agent.py
│   │   └── creative_agent.py
│   ├── models/
│   │   ├── schemas.py
│   │   └── config.py
│   └── utils/
│       ├── embeddings.py
│       └── logger.py
├── frontend/
│   ├── package.json
│   └── src/
│       ├── App.tsx
│       ├── components/
│       │   ├── GraphView.tsx
│       │   ├── NodeCard.tsx
│       │   └── ResultPanel.tsx
│       └── api/
│           └── client.ts
└── tests/
    ├── test_graph_engine.py
    ├── test_attraction.py
    ├── test_repulsion.py
    ├── test_escape_node_pruner.py
    ├── test_creative_potential.py
    └── test_wormhole.py
```

---

## 12. 개발 단계별 로드맵

## Phase 1. 개념 증명

목표: 입력 → 노드 생성 → 그래프 생성 → 쌍성계 탐색까지 구현

작업:

* FastAPI 서버 생성
* ConceptNode 클래스 구현
* NetworkX 기반 그래프 생성
* 노드 간 유사도 계산
* attraction/repulsion 기본 공식 구현
* binary detector 구현
* Escape Node Pruner의 기본 threshold 구현
* 노드 상태 분류 결과를 포함한 JSON 결과 반환

완료 기준:

```text
사용자 입력을 넣으면 관련 노드, edge, 안정적인 쌍성계 조합, 노드별 생존 상태가 반환된다.
```

---

## Phase 2. Entanglement Memory 구현

목표: 과거에 함께 쓰인 개념 조합을 기억하고 재사용

작업:

* Chroma 또는 SQLite 기반 메모리 저장
* co-activation 기록
* success_score 업데이트
* 유사 입력이 들어왔을 때 과거 연결 검색
* entanglement_score 계산
* dormant_wormhole_candidate의 재활성화 기록 저장

완료 기준:

```text
과거에 좋은 결과를 냈던 개념 조합이 다음 실행에서 다시 추천된다.
```

---

## Phase 3. Wormhole Shortcut 구현

목표: 멀리 떨어진 개념 간 창의적 연결 생성

작업:

* 그래프 거리 계산
* 직접 연결이 약하지만 entanglement_score가 높은 노드 탐색
* dormant_wormhole_candidate 중 재해석 가능한 노드 선별
* shortcut edge 생성
* 창의성 점수 계산
* 결과 생성에 반영

완료 기준:

```text
일반적인 연결 외에 창의적 연결 후보가 생성된다.
```

---

## Phase 4. Black Hole Compressor 구현

목표: 복잡한 그래프 결과를 압축해 최종 답변에 사용할 context 생성

작업:

* 클러스터별 요약
* 중복 노드 제거
* 중요 노드 우선순위화
* LLM 입력 context 생성
* 최종 답변 생성

완료 기준:

```text
그래프 결과를 기반으로 자연어 답변이 생성된다.
```

---

## Phase 5. 프론트엔드 시각화

목표: 노드, 엣지, 쌍성계, 웜홀 연결을 시각적으로 확인

작업:

* React 프로젝트 생성
* 그래프 시각화 컴포넌트 구현
* 노드 상태별 UI 구분
* edge weight 표시
* 쌍성계와 웜홀 연결 강조
* 최종 결과 패널 구현

완료 기준:

```text
사용자가 입력한 주제에 대해 생성된 지능체 그래프를 웹 화면에서 볼 수 있다.
```

---

## 13. 성능 평가 지표

## 13.1 정량 지표

| 지표                  | 설명                    |
| ------------------- | --------------------- |
| relevance_score     | 결과가 입력 주제와 얼마나 관련 있는가 |
| novelty_score       | 결과가 얼마나 새롭고 창의적인가     |
| stability_score     | 노드 조합이 얼마나 안정적인가      |
| diversity_score     | 다양한 관점이 포함되었는가        |
| redundancy_score    | 중복 개념이 얼마나 적은가        |
| survival_precision  | Pruner가 실제 유용한 노드를 과도하게 제거하지 않았는가 |
| wormhole_recall     | 잠재적 창의 노드를 dormant 후보로 충분히 보존했는가 |
| garbage_filter_rate | 노이즈 노드를 효과적으로 제거했는가 |
| user_feedback_score | 사용자의 만족도              |

## 13.2 정성 평가

* 결과가 기존 답변보다 창의적인가?
* 사용자의 관심사와 연결되는가?
* 설명 가능한 구조를 제공하는가?
* 노드 간 관계가 직관적으로 이해되는가?
* 반복 사용 시 더 나은 연결을 만들어내는가?

---

## 14. 위험 요소와 대응 전략

## 14.1 결과가 너무 랜덤해질 위험

문제:

* 웜홀 연결이 과도하면 말이 안 되는 결과가 나올 수 있다.

대응:

* novelty_score와 relevance_score를 함께 평가
* relevance가 낮은 shortcut은 제거
* 창의성 모드와 정확성 모드를 분리

---

## 14.2 그래프가 너무 복잡해질 위험

문제:

* 노드가 많아지면 계산량과 해석 난이도가 증가한다.

대응:

* 초기 MVP에서는 노드 수 10~30개로 제한
* edge threshold 적용
* escaped node pruning 적용
* top-k cluster만 최종 추론에 사용

---

## 14.3 Pruner가 창의성을 죽일 위험

문제:

* 관련도 기준만 강하게 적용하면 멀리 있는 창의적 노드가 너무 빨리 제거될 수 있다.

대응:

* `Uᵢ`와 `Cᵢ`를 분리해서 계산
* `dormant_wormhole_candidate` 상태를 별도로 유지
* 낮은 관련도라도 `Cᵢ`가 높고 `Nᵢ`가 낮으면 보존
* 결과 채택 여부에 따라 `Mᵢ`와 entanglement score를 업데이트

---

## 14.4 기존 LLM과 차별성이 약할 위험

문제:

* 단순히 LLM에 프롬프트를 잘 넣는 수준에 머물 수 있다.

대응:

* 그래프 구조를 명시적으로 저장
* 관계 변화 기록
* entanglement memory 업데이트
* 결과 생성 과정 시각화
* 사용자가 “왜 이런 아이디어가 나왔는지” 확인 가능하게 설계

---

## 15. 초기 MVP 예시 시나리오

### 입력

```text
백엔드 개발자 포트폴리오로 쓸만한 독특한 프로젝트를 추천해줘
```

### 생성 노드

```text
Spring
MySQL
AWS
지도 API
로컬 관광
추억여행
감정 분석
개인화 추천
일정 생성
사용자 기록
```

### 쌍성계

```text
Spring + MySQL
지도 API + 로컬 관광
감정 분석 + 개인화 추천
추억여행 + 사용자 기록
```

### 웜홀 연결

```text
백엔드 포트폴리오 ↔ 추억여행
지역 관광 ↔ 감정 분석
사용자 기록 ↔ 일정 생성
```

### 최종 결과

```text
개인 추억 기반 로컬 여행 스케줄러

사용자가 과거에 살았던 지역, 학교, 자주 갔던 장소를 입력하면
지도 API와 로컬 관광 데이터를 결합해 여행 코스를 생성한다.
감정 분석을 통해 사용자의 추억 키워드를 분류하고,
Spring Boot와 MySQL로 장소, 일정, 사용자 기록을 관리한다.
AWS에 배포하면 백엔드 포트폴리오로 활용하기 좋다.
```

---

## 16. 최종 검토 결과

이번 수정으로 기존 설계안의 약점이었던 `Escape Node Pruner`의 단순 pruning 문제를 보완했다. 특히 당장의 관련도만으로 노드를 제거하지 않고, 창의적 잠재력과 노이즈 위험을 분리해 평가하도록 구조를 강화했다.

### 보완된 점

* `active`, `orbiting`, `dormant`, `escaped`, `garbage` 상태를 명확히 구분했다.
* 즉시 유용성 `Uᵢ`, 창의적 잠재력 `Cᵢ`, 노이즈 위험 `Nᵢ`, 메모리 보너스 `Mᵢ`를 도입했다.
* 최종 생존 점수 `Sᵢ`와 모드별 threshold를 정의했다.
* 창의적 웜홀 후보를 `dormant_wormhole_candidate`로 보존하는 구조를 추가했다.
* 데이터 스키마, 알고리즘 흐름, 의사코드, 폴더 구조, 로드맵, 평가 지표를 Pruner 설계와 맞게 정리했다.

### 남은 개발 과제

* `Cᵢ`의 bridge_potential을 어떻게 계산할지 실험이 필요하다.
* 사용자 피드백을 `Mᵢ`에 반영하는 업데이트 정책을 실제 데이터로 검증해야 한다.
* creative 모드에서 결과가 너무 뜬금없어지지 않도록 `Nᵢ` 패널티를 지속적으로 튜닝해야 한다.
* MVP에서는 노드 수를 제한하고, 먼저 10~30개 노드 규모에서 threshold를 검증하는 것이 좋다.

### 최종 판단

현재 설계안은 단순한 아이디어 문서에서 한 단계 나아가, 실제 MVP 개발을 시작할 수 있는 수준의 구조를 갖췄다. 특히 Pruner가 창의성을 제거하지 않고 보존하는 방향으로 수정되었기 때문에, 프로젝트의 핵심 컨셉인 “우주적 상호작용을 모방한 창의 지능체”와 더 잘 맞는다.

---

## 17. 최종 정의

Cosmic Graph Intelligence는 우주를 직접 계산 자원으로 사용하는 시스템이 아니다.

이 시스템은 우주의 구조적 원리에서 영감을 받아 다음과 같은 AI 구조를 만든다.

```text
지능 = 고정된 하나의 모델이 아니라,
여러 개념 노드가 서로 끌어당기고 밀어내며,
안정적인 조합을 만들고,
멀리 떨어진 기억과 연결되며,
중심 허브에서 압축되어
새로운 결과를 생성하는 동적 네트워크
```

즉 이 프로젝트의 핵심은 다음 한 문장으로 요약된다.

```text
우주적 상호작용을 모방한 그래프 기반 자기조직형 창의 지능체
```
