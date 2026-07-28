#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Generador de Etiquetas - Procesamiento de PDFs con datos desde Excel",
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Ejecutar en modo línea de comandos (sin GUI)",
    )
    parser.add_argument(
        "--pdf",
        type=Path,
        help="Ruta al archivo PDF de entrada",
    )
    parser.add_argument(
        "--excel",
        type=Path,
        help="Ruta al archivo Excel con los nombres",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Carpeta donde se guardarán los resultados",
    )
    parser.add_argument(
        "--images",
        type=Path,
        help="Carpeta con imágenes overlay (solo modo overlay)",
    )
    parser.add_argument(
        "--mode",
        choices=["extract", "split", "overlay"],
        default="extract",
        help="Operación a realizar (default: extract)",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Ruta al archivo de configuración YAML",
    )

    args = parser.parse_args()

    if args.cli:
        _run_cli(args)
    else:
        _run_gui(args)


def _run_cli(args: argparse.Namespace) -> None:
    from etiquetas_app.utils.config import load_config
    from etiquetas_app.utils.validators import validate_file_exists, validate_output_dir

    config = load_config(args.config)

    if not args.pdf or not args.excel or not args.output:
        print("Error: En modo CLI necesitas --pdf, --excel y --output")
        sys.exit(1)

    pdf = validate_file_exists(args.pdf)
    excel = validate_file_exists(args.excel)
    output = validate_output_dir(args.output)

    from etiquetas_app.core.excel_reader import read_names

    names = read_names(excel)

    def log(level: str, msg: str) -> None:
        prefix = {"info": "", "warning": "⚠ ", "error": "❌ "}.get(level, "")
        print(f"{prefix}{msg}")

    def progress(current: int, total: int) -> None:
        pct = current / total * 100 if total > 0 else 0
        print(f"\r  Progreso: [{current}/{total}] {pct:.0f}%", end="", file=sys.stderr)
        if current == total:
            print(file=sys.stderr)

    if args.mode == "extract":
        from etiquetas_app.core.extract_images import extract_images

        result = extract_images(pdf, names, output, config.extract, on_progress=progress, on_log=log)
        print(f"\nHecho: {result['success']} imágenes extraídas, {result['errors']} errores")

    elif args.mode == "split":
        from etiquetas_app.core.split_pdf import split_pdf

        result = split_pdf(pdf, names, output, config.split, on_progress=progress, on_log=log)
        print(f"\nHecho: {result['success']} PDFs creados, {result['errors']} errores")

    elif args.mode == "overlay":
        from etiquetas_app.core.overlay_pdf import overlay_pdf

        if not args.images:
            print("Error: En modo overlay necesitas --images")
            sys.exit(1)
        images = validate_output_dir(args.images)

        result = overlay_pdf(
            pdf, names, images, output, config.overlay,
            on_progress=progress, on_log=log,
        )
        print(f"\nHecho: {result['success']} PDFs creados, {result['skipped']} saltados, {result['errors']} errores")


def _run_gui(args: argparse.Namespace) -> None:
    from etiquetas_app.gui.app import run_gui

    run_gui(config_path=args.config)


if __name__ == "__main__":
    main()
