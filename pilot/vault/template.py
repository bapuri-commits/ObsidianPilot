"""TemplateEngine — 템플릿 렌더링 (Templater 변수 치환)."""

import re
from datetime import datetime


def render_template(template_text: str, date: datetime | None = None) -> str:
    """Templater/Obsidian 변수를 치환한다.

    지원하는 패턴:
    - {{date:FORMAT}} → strftime 변환
    - <% tp.date.now('FORMAT') %> → strftime 변환
    - <% tp.file.cursor() %> → 제거
    """
    if date is None:
        date = datetime.now()

    result = re.sub(
        r"\{\{date:(.*?)\}\}",
        lambda m: _moment_to_strftime(m.group(1), date),
        template_text,
    )

    result = re.sub(
        r"<%\s*tp\.date\.now\(['\"](.+?)['\"]\)\s*%>",
        lambda m: _moment_to_strftime(m.group(1), date),
        result,
    )

    result = re.sub(r"<%\s*tp\.file\.cursor\(\)\s*%>", "", result)

    return result


def _moment_to_strftime(moment_format: str, date: datetime) -> str:
    """Moment.js 포맷을 Python strftime으로 변환."""
    mapping = {
        "YYYY": "%Y",
        "MM": "%m",
        "DD": "%d",
        "HH": "%H",
        "mm": "%M",
        "ss": "%S",
        "ddd": "%a",
        "dddd": "%A",
    }
    fmt = moment_format
    for moment, py in sorted(mapping.items(), key=lambda x: -len(x[0])):
        fmt = fmt.replace(moment, py)
    return date.strftime(fmt)
