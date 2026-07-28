from pathlib import Path
from typing import List, Union


def validate_file_exists(path: Union[str, Path]) -> Path:
    p = Path(str(path)).expanduser().resolve()
    if not p.exists():
        raise FileNotFoundError(f"El archivo no existe: {p}")
    if not p.is_file():
        raise ValueError(f"No es un archivo: {p}")
    return p


def validate_extension(path: Union[str, Path], extensions: List[str]) -> bool:
    return Path(str(path)).suffix.lower() in extensions


def validate_output_dir(path: Union[str, Path]) -> Path:
    p = Path(str(path)).expanduser().resolve()
    p.mkdir(parents=True, exist_ok=True)
    return p
