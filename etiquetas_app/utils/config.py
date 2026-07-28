from pathlib import Path
from typing import Optional

import yaml

from ..core.models import AppConfig

CONFIG_DIR = Path.home() / ".config" / "etiquetas"
DEFAULT_CONFIG_FILE = CONFIG_DIR / "config.yaml"


def get_config_path() -> Path:
    return DEFAULT_CONFIG_FILE


def load_config(path: Optional[Path] = None) -> AppConfig:
    path = path or DEFAULT_CONFIG_FILE
    if not path.exists():
        return AppConfig()

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return AppConfig.from_dict(data)
    except Exception:
        return AppConfig()


def save_config(config: AppConfig, path: Optional[Path] = None) -> None:
    path = path or DEFAULT_CONFIG_FILE
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(config.to_dict(), f, default_flow_style=False, allow_unicode=True)
