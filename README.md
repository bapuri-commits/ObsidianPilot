# ObsidianPilot

LLM 기반 Obsidian 볼트 관리 도구.

## 개요

Obsidian 볼트(The Record)를 CLI로 관리한다. 데일리 노트 생성, 프로젝트 기록 갱신, Inbox 정리, 의미 검색 등을 LLM과 함께 수행.

CLI로 시작하여 MCP 서버로 확장 예정. The_Agent가 MCP 클라이언트로 연결하면 통합 개인 비서 생태계의 일부가 된다.

## 설치

```bash
pip install -r requirements.txt
cp .env.example .env
# .env에 API 키 입력
```

## 설정

`config.yaml`에서 볼트 경로와 옵션을 설정한다.

## 사용법

```bash
# 데일리 노트
pilot daily                          # 오늘 데일리 노트 생성
pilot daily --add-log "작업 내용"

# 프로젝트 관리
pilot project list
pilot project BotTycoon --decision "결정 내용" --reason "이유"

# Inbox 정리
pilot inbox triage

# 검색
pilot search "클린 아키텍처 관련 노트"

# 자연어 명령
pilot ask "오늘 데일리 노트에 BotTycoon 작업 추가해줘"
```

## 아키텍처

Phase 1: CLI → Phase 2: MCP Server

자세한 내용은 `docs/architecture.md` 참고.

## 관련 프로젝트

- [The Record](../The%20Record) — 대상 Obsidian 볼트
- [The_Agent](../The_Agent) — MCP 클라이언트 (Phase 2)
- [school_sync](../school_sync) — MCP화 경로 참고
