# ObsidianPilot — 기능 명세

## Phase 1: CLI Tool

### 1.1 데일리 노트 관리 (`daily`)

데일리 노트(`1_Daily/YYYY-MM/YYYY-MM-DD.md`)의 생성과 갱신.

**기능:**

- **생성**: 오늘 날짜의 데일리 노트가 없으면 `Templates/daily.md` 기반으로 생성
  - Templater 변수 치환: `<% tp.date.now('YYYY-MM-DD') %>` → 실제 날짜
  - 월별 폴더 자동 생성: `1_Daily/YYYY-MM/`
- **섹션별 추가**: 기존 데일리 노트의 특정 섹션에 내용 추가
  - `## Todo` — 할 일 항목
  - `## 일정` — 일정 테이블
  - `## 개발 로그` — 프로젝트별 작업 요약
  - `## 공부 기록` — 학습 내용
  - `## 메모` — 자유 메모

**CLI 예시:**

```bash
pilot daily                          # 오늘 데일리 노트 생성 (없으면)
pilot daily --add-log "BotTycoon: 인벤토리 구현"
pilot daily --add-todo "architecture.md 검토"
pilot daily --add-study "0-1 BFS 정리"
```

### 1.2 프로젝트 관리 (`project`)

프로젝트 `_index.md`(`2_Projects/[name]/_index.md`)의 갱신.

**기능:**

- **상태 갱신**: frontmatter의 `status` 필드 변경
- **결정 로그 추가**: `## 핵심 결정 로그` 테이블에 행 추가
- **배운 것 추가**: `## 배운 것` 섹션에 항목 추가
- **프로젝트 목록**: 등록된 프로젝트 목록과 현재 상태 출력

**CLI 예시:**

```bash
pilot project list                    # 전체 프로젝트 목록
pilot project BotTycoon --status active
pilot project BotTycoon --decision "Redis 대신 SQLite" --reason "단일 서버, 외부 의존성 최소화"
pilot project BotTycoon --learned "SQLAlchemy asyncio 세션 관리 패턴"
```

### 1.3 Inbox 정리 (`inbox`)

`0_Inbox/` 아이템을 LLM이 분석하여 적절한 위치로 이동 제안.

**기능:**

- **분류 (triage)**: Inbox 파일들을 읽어 카테고리 분류
  - `2_Projects/` — 특정 프로젝트에 속하는 내용
  - `3_Areas/` — 학습/영역 관련
  - `1_Daily/` — 데일리 노트에 추가할 내용
  - `Archive/` — 더 이상 필요 없는 내용
- **실행**: 사용자 확인 후 파일 이동/병합 실행
- **일상메모 처리**: `0_Inbox/일상메모.md`의 항목별 분류

**CLI 예시:**

```bash
pilot inbox list                      # Inbox 파일 목록
pilot inbox triage                    # LLM 분류 실행 (dry-run)
pilot inbox triage --execute          # 분류 결과 적용
```

### 1.4 의미 검색 (`search`)

볼트 전체를 임베딩하여 자연어 질문으로 관련 노트를 찾는다.

**기능:**

- **인덱싱**: 볼트의 모든 `.md` 파일을 청크로 분할 → 임베딩 → ChromaDB 저장
- **검색**: 자연어 질문 → 유사도 기반 관련 청크 반환
- **증분 업데이트**: 변경된 파일만 재인덱싱

**CLI 예시:**

```bash
pilot search index                    # 전체 인덱싱 (최초 1회)
pilot search index --incremental      # 변경분만 업데이트
pilot search "클린 아키텍처 관련 배운 것"
pilot search "BotTycoon에서 내린 기술 결정들"
```

### 1.5 요약 생성 (`summarize`)

LLM을 사용하여 기간별 활동 요약을 생성한다.

**기능:**

- **주간 요약**: 최근 7일 데일리 노트 기반 요약
- **월간 요약**: 해당 월 전체 활동 요약 (월간 노트 초안으로 활용 가능)
- **프로젝트 요약**: 특정 프로젝트의 최근 활동 요약

**CLI 예시:**

```bash
pilot summarize --weekly              # 이번 주 요약
pilot summarize --monthly             # 이번 달 요약
pilot summarize --project BotTycoon   # 프로젝트별 요약
```

### 1.6 자연어 통합 (`ask`)

위 기능을 자연어 명령으로 통합 호출한다.

**기능:**

- 자연어 입력을 LLM이 파싱하여 적절한 서비스 함수 호출
- 복합 명령 지원: "오늘 데일리 노트에 BotTycoon 작업 추가하고, _index.md도 갱신해줘"

**CLI 예시:**

```bash
pilot ask "오늘 데일리 노트에 BotTycoon 인벤토리 구현 추가해줘"
pilot ask "지난주에 뭐 했는지 정리해줘"
pilot ask "Inbox에 쌓인 거 정리해줘"
```

## Phase 2: MCP Server (계획)

Phase 1의 Core Services를 MCP 프로토콜로 노출한다.

### MCP 도구 (Tools)

| 도구 | 설명 | 매핑 |
|------|------|------|
| `create_daily_note` | 데일리 노트 생성 | `DailyService.create()` |
| `update_daily_note` | 데일리 노트 섹션 추가 | `DailyService.add_section()` |
| `update_project` | 프로젝트 _index.md 갱신 | `ProjectService.update()` |
| `triage_inbox` | Inbox 분류 | `InboxService.triage()` |
| `search_vault` | 의미 검색 | `SearchService.query()` |
| `summarize` | 요약 생성 | `SummarizeService.generate()` |

### MCP 리소스 (Resources)

| 리소스 | 설명 |
|--------|------|
| `vault://structure` | 볼트 디렉토리 구조 |
| `vault://daily/today` | 오늘의 데일리 노트 |
| `vault://projects` | 프로젝트 목록 + 현재 상태 |
| `vault://inbox` | Inbox 파일 목록 |

## 우선순위

1. **Phase 1-1**: VaultManager + TemplateEngine + DailyService (가장 자주 쓰이고 단순)
2. **Phase 1-2**: ProjectService + NoteParser
3. **Phase 1-3**: LLMService + InboxService
4. **Phase 1-4**: SearchService (ChromaDB 세팅 필요)
5. **Phase 1-5**: SummarizeService + ask 통합
6. **Phase 2**: MCP 서버 래핑
