# ObsidianPilot — 아키텍처

## 개요

LLM 기반 Obsidian 볼트 관리 도구.
CLI로 시작하여 MCP 서버로 확장하는 경로를 밟는다.

## 해결하는 문제

1. **수동 노트 관리의 번거로움** — 데일리 노트 작성, 프로젝트 `_index.md` 갱신, Inbox 정리를 매번 손으로 해야 함
2. **볼트 내 지식 검색의 한계** — Obsidian 검색은 키워드 기반, 의미 기반 검색 불가
3. **IDE 종속성** — 현재 The Record 관리는 Cursor 안에서만 가능 (`the-record-workflow.mdc`)
4. **The_Agent와의 역할 분리** — The_Agent는 개인 비서 플랫폼, Obsidian 연동은 전문 도구로 독립시키고 MCP로 연결

## Phase별 아키텍처

### Phase 1: CLI Tool

```
┌─────────────────────────────────────┐
│  CLI (Typer)                        │
│  ├── note create  (데일리/TIL/프로젝트) │
│  ├── note update  (섹션 추가/수정)     │
│  ├── inbox triage (Inbox 정리)       │
│  ├── search       (의미 검색)         │
│  └── summarize    (요약 생성)         │
├─────────────────────────────────────┤
│  Core Services                      │
│  ├── VaultManager   (파일 R/W, 경로) │
│  ├── TemplateEngine (템플릿 렌더링)   │
│  ├── NoteParser     (YAML+MD 파싱)   │
│  ├── LLMService     (Anthropic API)  │
│  └── SearchEngine   (임베딩 + 벡터)   │
├─────────────────────────────────────┤
│  Vault (The Record)                 │
│  ├── 0_Inbox/  1_Daily/  2_Projects/│
│  ├── 3_Areas/  Templates/           │
│  └── .obsidian/                     │
└─────────────────────────────────────┘
```

### Phase 2: MCP Server

```
┌──────────────┐    MCP     ┌──────────────┐
│  The_Agent   │ ◄────────► │ ObsidianPilot│
│  (MCP Client)│            │ (MCP Server) │
└──────────────┘            └──────────────┘
```

Phase 1의 Core Services를 그대로 재사용하여 MCP 도구/리소스로 노출한다.

## 레이어 구조

```
pilot/
├── cli.py              # CLI 진입점 (Typer)
├── config.py           # 볼트 경로, API 키 등 설정 로드
├── vault/
│   ├── manager.py      # VaultManager — 파일 R/W, 경로 해석, 위키링크 처리
│   ├── parser.py       # NoteParser — YAML frontmatter + Markdown 파싱
│   └── template.py     # TemplateEngine — 템플릿 렌더링 (Templater 호환)
├── services/
│   ├── daily.py        # DailyService — 데일리 노트 CRUD
│   ├── project.py      # ProjectService — 프로젝트 _index.md 관리
│   ├── inbox.py        # InboxService — Inbox 정리 (LLM 분류)
│   ├── search.py       # SearchService — 임베딩 기반 의미 검색
│   └── llm.py          # LLMService — Anthropic Claude API 래퍼
└── mcp_server.py       # Phase 2: MCP 서버 진입점
```

### 레이어 규칙

- **CLI** → Services만 호출. Vault 레이어 직접 접근 금지.
- **Services** → Vault 레이어를 통해 파일 접근. 직접 파일 I/O 금지.
- **Vault** → 파일시스템 접근. Obsidian 볼트의 구조와 규칙을 캡슐화.

## 대상 볼트: The Record

PARA 기반 Obsidian 볼트. 구조는 `the-record-workflow.mdc`에 정의되어 있으며, 이 도구가 이해하고 조작할 수 있어야 하는 주요 경로:

| 경로 | 역할 | ObsidianPilot 동작 |
|------|------|---------------------|
| `0_Inbox/` | 빠른 캡처, 일상 메모 | 읽기 + 분류(triage) |
| `1_Daily/YYYY-MM/YYYY-MM-DD.md` | 데일리 노트 | 생성 + 섹션별 추가/수정 |
| `2_Projects/[name]/_index.md` | 프로젝트 메타 | 상태/결정 로그/배운 것 갱신 |
| `3_Areas/` | 학습/영역별 자료 | 읽기 + 새 노트 생성 |
| `Templates/` | 노트 템플릿 | 읽기 전용 (렌더링 소스) |

## 기술 스택

| 구분 | 선택 | 이유 |
|------|------|------|
| 언어 | Python 3.12 | 기존 프로젝트와 통일 |
| CLI | Typer | 선언적 CLI, 자동 도움말 |
| LLM | Anthropic Claude API | 기존 사용 중 |
| 임베딩/벡터 | ChromaDB + OpenAI Embeddings | The_Agent RAG 계획과 일치 |
| MD 파싱 | python-frontmatter + markdown-it-py | YAML frontmatter + 위키링크 |
| 설정 | PyYAML + python-dotenv | 기존 패턴 |
| MCP (Phase 2) | mcp python SDK | school_sync와 동일 |

## school_sync와의 비교 (MCP화 경로)

| | school_sync | ObsidianPilot |
|---|---|---|
| 데이터 소스 | 웹 크롤링 (eclass, portal) | 로컬 파일시스템 (Obsidian vault) |
| 현재 인터페이스 | CLI (`main.py`) | CLI (`pilot`) |
| 출력 | `output/normalized/*.json` | 볼트 내 `.md` 파일 직접 수정 |
| MCP 도구 (계획) | `crawl`, `get_timetable`, `ask` | `create_note`, `update_note`, `search`, `triage_inbox` |
| MCP 리소스 | `briefing.md` | 볼트 구조, 최근 노트 |

## 의존 관계

```
ObsidianPilot
├── reads/writes → The Record (Obsidian vault)
├── future MCP client → The_Agent
└── pattern reference → school_sync (MCP화 경로)
```
