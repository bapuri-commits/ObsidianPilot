"""설정 로드."""

import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()

_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.yaml"


def load_config() -> dict:
    with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    vault_env = os.getenv("VAULT_PATH")
    if vault_env:
        cfg["vault"]["path"] = vault_env

    return cfg
