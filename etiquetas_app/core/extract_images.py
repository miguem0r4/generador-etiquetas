from pathlib import Path
from typing import Callable, List, Optional, Tuple

import fitz
from PIL import Image

from .models import ExtractConfig


def extract_images(
    pdf_path: Path,
    names: List[str],
    output_dir: Path,
    config: ExtractConfig,
    on_progress: Optional[Callable[[int, int], None]] = None,
    on_log: Optional[Callable[[str, str], None]] = None,
) -> dict:
    doc = fitz.open(str(pdf_path))
    total = len(doc)
    results: dict = {"success": 0, "errors": 0, "total": total, "details": []}

    if len(names) < total:
        _log(on_log, "warning", f"Hay menos nombres ({len(names)}) que páginas en el PDF ({total})")
    elif len(names) > total:
        _log(on_log, "warning", f"Hay más nombres ({len(names)}) que páginas en el PDF ({total})")

    for i in range(total):
        try:
            page = doc[i]
            mat = fitz.Matrix(config.render_scale, config.render_scale)
            pix = page.get_pixmap(matrix=mat)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            width, height = img.size
            crop_area = (
                int(width * config.crop_left_ratio),
                int(height * config.crop_top_ratio),
                int(width * config.crop_right_ratio),
                int(height * config.crop_bottom_ratio),
            )

            cropped = img.crop(crop_area)

            try:
                nombre = str(names[i])
            except IndexError:
                nombre = f"pagina_{i + 1}"

            nombre = nombre.replace("/", "_").replace("\\", "_")
            output_path = output_dir / f"{nombre}.png"
            cropped.save(output_path)

            results["success"] += 1
            _log(on_log, "info", f"✅ [{i + 1}/{total}] Guardado: {output_path.name}")

        except Exception as e:
            results["errors"] += 1
            results["details"].append(f"Página {i + 1}: {e}")
            _log(on_log, "error", f"❌ [{i + 1}/{total}] Error: {e}")

        if on_progress:
            on_progress(i + 1, total)

    doc.close()
    return results


def _log(callback: Optional[Callable], level: str, msg: str) -> None:
    if callback:
        callback(level, msg)
