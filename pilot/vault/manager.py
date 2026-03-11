"""VaultManager — 볼트 파일 R/W 및 경로 해석."""

from pathlib import Path


class VaultManager:
    def __init__(self, vault_path: str) -> None:
        self.root = Path(vault_path)
        if not self.root.exists():
            raise FileNotFoundError(f"볼트 경로를 찾을 수 없습니다: {vault_path}")

    def read_note(self, relative_path: str) -> str:
        path = self.root / relative_path
        if not path.exists():
            raise FileNotFoundError(f"노트를 찾을 수 없습니다: {relative_path}")
        return path.read_text(encoding="utf-8")

    def write_note(self, relative_path: str, content: str) -> Path:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def exists(self, relative_path: str) -> bool:
        return (self.root / relative_path).exists()

    def list_files(self, directory: str, pattern: str = "*.md") -> list[Path]:
        dir_path = self.root / directory
        if not dir_path.exists():
            return []
        return sorted(dir_path.rglob(pattern))
