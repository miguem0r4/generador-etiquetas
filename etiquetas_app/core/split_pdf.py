from pathlib import Path
from typing import Callable, List, Optional

from PyPDF2 import PdfReader, PdfWriter

from .models import SplitConfig


def split_pdf(
    pdf_path: Path,
    names: List[str],
    output_dir: Path,
    config: SplitConfig,
    on_progress: Optional[Callable[[int, int], None]] = None,
    on_log: Optional[Callable[[str, str], None]] = None,
) -> dict:
    reader = PdfReader(str(pdf_path))
    total_paginas = len(reader.pages)
    ppg = config.pages_per_group
    total_groups = (total_paginas + ppg - 1) // ppg
    results: dict = {"success": 0, "errors": 0, "total": total_groups, "details": []}

    if total_paginas // ppg > len(names):
        _log(on_log, "warning", "No hay suficientes nombres en el Excel para todas las páginas.")

    indice_nombre = 0

    for i in range(0, total_paginas, ppg):
        try:
            writer = PdfWriter()
            for j in range(ppg):
                if i + j < total_paginas:
                    writer.add_page(reader.pages[i + j])

            if indice_nombre < len(names):
                nombre_archivo = str(names[indice_nombre])
            else:
                nombre_archivo = f"archivo_{indice_nombre + 1}"

            output_path = output_dir / f"{nombre_archivo}.pdf"
            with open(output_path, "wb") as f:
                writer.write(f)

            results["success"] += 1
            _log(on_log, "info", f"✅ [{indice_nombre + 1}/{total_groups}] Creado: {output_path.name}")

        except Exception as e:
            results["errors"] += 1
            results["details"].append(f"Grupo {indice_nombre + 1}: {e}")
            _log(on_log, "error", f"❌ [{indice_nombre + 1}/{total_groups}] Error: {e}")

        indice_nombre += 1
        if on_progress:
            on_progress(indice_nombre, total_groups)

    return results


def _log(callback: Optional[Callable], level: str, msg: str) -> None:
    if callback:
        callback(level, msg)
