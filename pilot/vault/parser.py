"""NoteParser — YAML frontmatter + Markdown 파싱."""

from dataclasses import dataclass, field

import frontmatter


@dataclass
class ParsedNote:
    metadata: dict = field(default_factory=dict)
    content: str = ""
    sections: dict[str, str] = field(default_factory=dict)


def parse_note(text: str) -> ParsedNote:
    post = frontmatter.loads(text)
    sections = _extract_sections(post.content)
    return ParsedNote(
        metadata=dict(post.metadata),
        content=post.content,
        sections=sections,
    )


def render_note(note: ParsedNote) -> str:
    post = frontmatter.Post(note.content, **note.metadata)
    return frontmatter.dumps(post)


def _extract_sections(content: str) -> dict[str, str]:
    """H2 헤더 기준으로 섹션을 분리한다."""
    sections: dict[str, str] = {}
    current_header = ""
    current_lines: list[str] = []

    for line in content.split("\n"):
        if line.startswith("## "):
            if current_header:
                sections[current_header] = "\n".join(current_lines).strip()
            current_header = line[3:].strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_header:
        sections[current_header] = "\n".join(current_lines).strip()

    return sections
