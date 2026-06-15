# 🌌 Cosmic Graph Intelligence (CGI)

**Cosmic Graph Intelligence (CGI)**는 대형 언어 모델(LLM)의 잠재된 창의성과 추론 능력을 극대화하기 위해 설계된 혁신적인 **메타 프롬프팅 아키텍처(Meta-Prompting Architecture)**입니다. 

일반적인 LLM은 입력된 프롬프트에 대해 가장 확률이 높은 '뻔한' 텍스트를 직렬로 생성하는 경향(선형적 사고)이 있습니다. CGI 파이프라인은 이 한계를 극복하기 위해 **그래프 이론(Graph Theory)**과 **천체 역학(Celestial Mechanics)**의 메타포를 결합하여, LLM이 **수평적 사고(Lateral Thinking)**를 할 수 있도록 강제합니다.

---

## 🚀 파이프라인 아키텍처 (How it works)

CGI 파이프라인은 질문이 들어오면 다음 5단계의 우주적 프로세스를 거쳐 답변을 생성합니다.

### 1️⃣ 은하 형성 (Node Generation)
사용자의 입력을 분석하여 도메인과 의도를 파악하고, LLM을 통해 다차원적인 **개념 노드(Concept Nodes)** 20개를 흩뿌립니다.
*   **활성 노드 (Active Nodes)**: 질문과 직접적으로 연관된 핵심 기술/개념 (예: `RAG`, `Vector DB`)
*   **주변 노드 (Orbiting Nodes)**: 간접적으로 연관된 창의적/보조적 개념 (예: `세렌디피티`, `인지 부하`)

### 2️⃣ 중력 엔진 (Gravity Engine)
생성된 노드들 사이의 관계를 수학적으로 계산하여 방향성 있는 지식 그래프(Knowledge Graph)를 구축합니다.
*   **인력 (Attraction)**: 두 개념이 얼마나 시너지를 내는지 (0.0 ~ 1.0)
*   **척력 (Repulsion)**: 두 개념이 얼마나 상충되거나 모순되는지 (0.0 ~ 1.0)

### 3️⃣ 천체 구조 탐지 (Celestial Structures)
그래프의 연결 가중치를 분석하여 답변의 뼈대가 될 구조물을 찾습니다.
*   **쌍성계 (Binary Systems)**: 서로 인력이 매우 강한 두 노드의 결합. (예: `[Vector DB] + [초개인화]`). 답변이 엇나가지 않도록 **일관성(Coherence)**을 부여합니다.
*   **웜홀 (Wormholes)**: 겉보기엔 관련이 없지만(낮은 인력) 척력도 없는 활성 노드와 주변 노드를 강제로 연결하여 **창의적 도약(Creative Leap)**을 유도합니다.

### 4️⃣ 블랙홀 압축 (Blackhole Compression & Pruning)
LLM의 컨텍스트 윈도우가 오염되는 것을 막기 위해 가지치기(Pruning)를 수행합니다.
*   연결이 약한 노드는 **이탈 노드(Escaped Node)**로 분류되어 우주 밖으로 버려집니다.
*   살아남은 핵심 구조(쌍성계, 웜홀)만을 고밀도의 마크다운 형태(압축된 컨텍스트)로 변환합니다.

### 5️⃣ 최종 응답 생성 (Generation)
블랙홀 압축기를 통해 생성된 "CGI 컨텍스트"를 원본 질문과 함께 LLM에 다시 주입합니다. 이를 통해 LLM은 뻔한 답변 대신, 쌍성계의 논리와 웜홀의 창의성을 모두 갖춘 압도적인 결과물을 출력하게 됩니다.

---

## ⚔️ 비교 테스트 엔진 (Compare Engine)

CGI 시스템의 효용성을 증명하기 위해, **동일한 질문에 대해 "일반 LLM 직접 호출"과 "CGI 파이프라인 적용 호출"을 나란히 비교하고 자동 평가하는 시스템**이 내장되어 있습니다.

### 평가 방식 (Judge LLM)
평가자(Judge) LLM이 두 응답을 읽고 다음 7가지 기준으로 자동 채점합니다.
1. `Relevance` (관련성)
2. `Creativity` (창의성)
3. `Diversity` (다양성)
4. `Specificity` (구체성)
5. `Explainability` (설명 가능성)
6. `Novelty` (참신성)
7. `Coherence` (일관성)

---

## 📊 이전 CGI 테스트 결과 (test_result*.json)

프로젝트 루트에 남아 있는 `test_result*.json` 비교 테스트 결과입니다. 각 파일은 같은 질문에 대해 일반 LLM 직접 응답(`direct_response`)과 CGI 컨텍스트 주입 응답(`cgi_response`)을 비교하고, Judge 분석(`analysis`)으로 승자를 기록합니다.

| Source file | Question | Mode | Winner | Direct latency | CGI latency | CGI graph metadata |
| --- | --- | --- | --- | --- | --- | --- |
| `test_result.json` | 백엔드 포트폴리오 프로젝트 추천 | `creative` | `direct` | `23131.4ms` | `49663.7ms` | nodes `20`, active `5`, orbiting `15`, binary `0`, wormhole `0` |
| `test_result_new.json` | 1인 개발 모바일 앱 수익화 아이디어 추천 | `creative` | `cgi` | `26576.6ms` | `59237.4ms` | nodes `20`, active `6`, orbiting `14`, binary `2`, wormhole `0` |
| `test_result_deep.json` | AI 맞춤 뉴스/콘텐츠 큐레이션 앱 아키텍처 설계 | `accurate` | `cgi` | `68894.6ms` | `157514.3ms` | nodes `20`, active `10`, orbiting `10`, binary `4`, wormhole `0` |

### Judge 요약

- `test_result.json`: Direct 응답이 승리했습니다. Judge는 백엔드 포트폴리오 추천 목적에는 더 넓은 범위의 다양한 옵션을 직관적으로 제시한 direct 응답이 더 실용적이라고 평가했습니다.
- `test_result_new.json`: CGI 응답이 승리했습니다. Judge는 CGI가 노드/쌍성계 프레임워크와 현대적 트렌드를 결합해 단순 아이디어 나열보다 전략적 깊이와 설명력이 높다고 평가했습니다.
- `test_result_deep.json`: CGI 응답이 승리했습니다. Judge는 CGI가 기술적 타당성을 유지하면서도 인지 부하 감소, 세렌디피티 등 제품 관점의 창의적 AI 전략을 포함해 서비스 설계 수준의 답변을 제공했다고 평가했습니다.

참고: 위 수치는 CGI 디렉터리의 JSON 파일을 직접 파싱해 반영했습니다. 파일 내부 문자열에 raw newline이 포함되어 있어 Python `json.loads(..., strict=False)`로 읽어 검증했습니다.

---

## 🛠️ 설치 및 실행 방법

### 1. 환경 설정
프로젝트 루트 폴더에 `.env` 파일을 생성하고 다음 변수를 입력합니다.
Gemini API key 없이 서버 user의 Codex auth를 재사용하려면 `LLM_PROVIDER=codex`를 사용합니다.

```env
# Codex auth 기반 실행
LLM_PROVIDER=codex
LLM_MODEL=gpt-5.5
CODEX_WORKDIR=/home/ubuntu/CGI/CGI_Cosmic_Graph_Intelligence

# Gemini 기반 실행을 선택할 때만 필요
# LLM_PROVIDER=gemini
# GEMINI_API_KEY=your_gemini_api_key_here
# LLM_MODEL=gemma-4-31b-it
# JUDGE_LLM_MODEL=gemma-4-31b-it

# CGI 모드 (accurate / balanced / creative / research)
CGI_MODE=balanced

# SQLite 기반 CGI 메모리. 저장은 전체 노드/엣지를 하되, 다음 프롬프트 주입은 recent+similar top-k로 제한해 지연과 토큰 증가를 막습니다.
CGI_MEMORY_ENABLED=true
CGI_MEMORY_DB_PATH=/home/ubuntu/CGI/CGI_Cosmic_Graph_Intelligence/data/cgi_memory.sqlite3
CGI_MEMORY_CONTEXT_LIMIT=18
CGI_MEMORY_RECENT_LIMIT=6
CGI_MEMORY_SIMILAR_LIMIT=12
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. API 서버 실행
FastAPI를 사용하여 서버를 띄웁니다.
```bash
LLM_PROVIDER=codex LLM_MODEL=gpt-5.5 CODEX_WORKDIR=/home/ubuntu/CGI/CGI_Cosmic_Graph_Intelligence \
  uvicorn app.main:app --host 0.0.0.0 --port 8000
```
브라우저에서 `http://localhost:8000/docs`에 접속하면 Swagger UI를 통해 테스트할 수 있습니다.

---

## 🌐 API 엔드포인트

### `POST /api/chat`
비교/Judge 없이 CGI 파이프라인 기반 최종 답변 텍스트만 반환합니다.
*   **Request Body**: `{"question": "질문 내용", "mode": "balanced"}`
*   **Response**: 최종 답변 문자열(`text/plain`)

### `POST /api/compare`
단건의 질문에 대해 비교 테스트를 수행합니다.
*   **Request Body**: `{"question": "질문 내용", "mode": "balanced"}`
*   **Response**: CGI 응답, 일반 응답, 생성된 노드 데이터 메타데이터, 평가 점수 및 승자 판별 결과(JSON)

### `POST /api/compare/report`
단건의 질문에 대해 비교 테스트를 수행한 후, 깔끔하게 정리된 **마크다운 리포트 문자열**을 반환합니다.

### `POST /api/compare/batch`
배열 형태로 여러 질문을 한 번에 전달하여 일괄 벤치마크 테스트를 수행합니다.
*   **Request Body**: `{"questions": ["질문1", "질문2"], "mode": "balanced"}`

---

## 📜 기술 명세 및 알고리즘 (Technical Specification)

이 프로젝트는 단순한 API 호출 래퍼(Wrapper)가 아닌, 수학적·구조적 알고리즘을 통해 프롬프트를 설계하는 메타 엔진입니다.

### 사용된 주요 라이브러리
*   **FastAPI**: 빠르고 비동기적인 API 서버 구축 및 비동기 처리(`async/await`)를 통한 병렬 LLM 호출 최적화.
*   **Pydantic**: JSON 파싱, 환경 변수(`.env`) 로드 및 노드/엣지 스키마에 대한 강력한 타입 안정성(Type Safety) 보장.
*   **google-genai**: Google의 최신 Gemini API를 호출하기 위한 공식 SDK. 구조화된 JSON 출력을 파싱하기 위해 사용.
*   **Pytest**: 단위 테스트 및 Mocking을 활용한 API 엔드포인트 무결성 검증.

### 핵심 알고리즘 및 동작 원리

**1. 구조화된 노드 추출 (Structured Node Extraction)**
단순 텍스트 출력을 넘어, 프롬프트 엔지니어링을 통해 LLM이 반드시 엄격한 JSON 스키마를 반환하도록 강제합니다. 질문의 의도(Intent)와 도메인(Domain)을 먼저 분류한 뒤, 본질에 가까운 **활성 노드(Active)** 10개와 창의적 확장을 위한 **주변 노드(Orbiting)** 10개를 생성합니다.

**2. 다중 쿼리 기반 인력/척력 스코어링 (Attraction & Repulsion Evaluation)**
LLM을 수학적 평가 함수처럼 활용합니다. `(Node A, Node B)` 쌍을 주입하면, 두 개념의 결합 시너지 지수(Attraction, 0.0~1.0)와 모순/충돌 지수(Repulsion, 0.0~1.0)를 계산하여 그래프의 엣지(Edge) 가중치로 저장합니다.

**3. 쌍성계 탐지 (Binary System Detection / Max-Weight Greedy)**
그래프 탐색 알고리즘을 사용하여 결합 스코어(Attraction)가 임계치(`T_BINARY`, 예: 0.8) 이상인 노드 쌍을 추출합니다. 하나의 노드가 여러 노드와 연결될 수 있지만, 가장 인력이 강한 조합을 우선(Greedy)하여 답변의 중심이 될 **안정적인 뼈대**를 구축합니다.

**4. 웜홀 라우팅 (Wormhole Routing / Conditional Graph Traversal)**
활성 노드와 주변 노드 간의 관계에서, 인력은 다소 낮지만(`T_WORMHOLE`, 예: 0.4~0.6) 척력 또한 낮은(`0.3` 이하) 간선을 찾습니다. 이는 **'겉보기엔 관련 없어 보이지만 상충되지도 않는'** 독특한 개념의 결합을 의미하며, 이를 통해 억지스럽지 않은 **창의적 도약**을 만들어냅니다.

**5. 고립 노드 프루닝 (Degree-based Pruning)**
그래프의 차수(Degree)를 분석하여 연결선이 없는 고립 노드나, 특정 임계값을 넘지 못한 약한 노드들을 식별하여 메모리에서 삭제(Escape)합니다. 이는 컨텍스트 윈도우의 낭비를 막고, LLM이 환각(Hallucination)에 빠질 확률을 획기적으로 낮춰줍니다.

**6. 블랙홀 컨텍스트 압축 (Blackhole Serialization)**
메모리에 객체 형태로 존재하는 그래프 자료구조(노드, 쌍성계, 웜홀 리스트)를 LLM이 이해하기 쉬운 고밀도의 자연어/마크다운 텍스트로 직렬화(Serialization)하여 최종 프롬프트로 주입합니다.

---

## 📂 디렉토리 구조

```text
CGI/
├── app/
│   ├── api/            # FastAPI 라우터 및 엔드포인트
│   ├── core/           # CGI 파이프라인 엔진 (Nodes, Graph, Compression, Judge 등)
│   ├── models/         # Pydantic 스키마 및 환경설정(Config)
│   └── utils/          # LLM API 클라이언트, 로거, 리포트 생성기 등
├── tests/              # Pytest 단위 테스트 코드
├── .env.example        # 환경변수 템플릿
├── run_test.py         # 콘솔에서 비교 테스트를 돌려볼 수 있는 파이썬 스크립트
└── list_models.py      # 사용 가능한 API 모델을 조회하는 유틸리티
```

---

*“Logic will get you from A to B. Imagination will take you everywhere.”*
**Cosmic Graph Intelligence**는 LLM에게 상상력의 지도를 쥐어줍니다.
