"""ObsidianPilot CLI 진입점."""

import typer

app = typer.Typer(
    name="pilot",
    help="LLM 기반 Obsidian 볼트 관리 도구",
)


@app.command()
def daily() -> None:
    """데일리 노트 관리."""
    typer.echo("daily 명령 — 아직 구현되지 않았습니다.")


@app.command()
def project() -> None:
    """프로젝트 _index.md 관리."""
    typer.echo("project 명령 — 아직 구현되지 않았습니다.")


@app.command()
def inbox() -> None:
    """Inbox 정리."""
    typer.echo("inbox 명령 — 아직 구현되지 않았습니다.")


@app.command()
def search(query: str = typer.Argument(..., help="검색 질문")) -> None:
    """의미 기반 검색."""
    typer.echo(f"search '{query}' — 아직 구현되지 않았습니다.")


@app.command()
def ask(question: str = typer.Argument(..., help="자연어 명령")) -> None:
    """자연어 통합 명령."""
    typer.echo(f"ask '{question}' — 아직 구현되지 않았습니다.")


if __name__ == "__main__":
    app()
