import io
from pathlib import Path
from typing import Callable, List, Optional

from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from .models import OverlayConfig


def _create_overlay(
    imagen_path: Path,
    page_width: float,
    page_height: float,
    config: OverlayConfig,
) -> PdfReader:
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(page_width, page_height))

    img_width = config.image_width * config.image_scale
    img_height = config.image_height * config.image_scale

    x = page_width - img_width - config.offset_x
    y = page_height - img_height - config.offset_y

    c.drawImage(ImageReader(str(imagen_path)), x, y, width=img_width, height=img_height)
    c.save()

    packet.seek(0)
    return PdfReader(packet)


def overlay_pdf(
    pdf_path: Path,
    names: List[str],
    images_folder: Path,
    output_dir: Path,
    config: OverlayConfig,
    on_progress: Optional[Callable[[int, int], None]] = None,
    on_log: Optional[Callable[[str, str], None]] = None,
) -> dict:
    reader = PdfReader(str(pdf_path))
    total_paginas = len(reader.pages)
    ppg = config.pages_per_group
    total_groups = (total_paginas + ppg - 1) // ppg
    results: dict = {"success": 0, "errors": 0, "skipped": 0, "total": total_groups, "details": []}

    indice_nombre = 0

    for i in range(0, total_paginas, ppg):
        if indice_nombre >= len(names):
            _log(on_log, "warning", "No hay más nombres en el Excel")
            break

        try:
            writer = PdfWriter()
            nombre_archivo = str(names[indice_nombre]).strip()
            imagen_path = images_folder / f"{nombre_archivo}.png"

            if not imagen_path.exists():
                _log(on_log, "warning", f"⚠️ No se encontró imagen para: {nombre_archivo}")
                results["skipped"] += 1
                indice_nombre += 1
                continue

            for j in range(ppg):
                if i + j < total_paginas:
                    page = reader.pages[i + j]
                    if j == 0:
                        overlay = _create_overlay(
                            imagen_path,
                            float(page.mediabox.width),
                            float(page.mediabox.height),
                            config,
                        )
                        page.merge_page(overlay.pages[0])
                    writer.add_page(page)

            output_path = output_dir / f"{nombre_archivo}.pdf"
            with open(output_path, "wb") as f:
                writer.write(f)

            results["success"] += 1
            _log(on_log, "info", f"✅ [{indice_nombre + 1}/{total_groups}] Creado: {output_path.name}")

        except Exception as e:
            results["errors"] += 1
            results["details"].append(f"Nombre {indice_nombre + 1}: {e}")
            _log(on_log, "error", f"❌ [{indice_nombre + 1}/{total_groups}] Error: {e}")

        indice_nombre += 1
        if on_progress:
            on_progress(indice_nombre, total_groups)

    return results


def _log(callback: Optional[Callable], level: str, msg: str) -> None:
    if callback:
        callback(level, msg)
