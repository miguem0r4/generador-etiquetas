from pathlib import Path

import customtkinter as ctk

from ...core.models import AppConfig
from ...core.overlay_pdf import overlay_pdf
from ..widgets.overlay_preview import OverlayPreview
from ..widgets.path_selector import PathSelector
from ..widgets.tooltip import ToolTip
from .base_tab import BaseTab


class OverlayTab(BaseTab):
    def __init__(self, parent, config: AppConfig, **kwargs):
        super().__init__(parent, config, **kwargs)

    def _build_common_ui(self) -> None:
        self._paths_frame = ctk.CTkFrame(self)
        self._paths_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))

        self.pdf_selector = PathSelector(self._paths_frame, "PDF de entrada", filetypes=[("Archivos PDF", "*.pdf")])
        self.pdf_selector.grid(row=0, column=0, sticky="ew", pady=(0, 3))

        self.excel_selector = PathSelector(
            self._paths_frame, "Excel de nombres", filetypes=[("Archivos Excel", "*.xlsx;*.xls")]
        )
        self.excel_selector.grid(row=1, column=0, sticky="ew", pady=(0, 3))

        self.images_selector = PathSelector(self._paths_frame, "Carpeta de imágenes", is_folder=True)
        self.images_selector.grid(row=2, column=0, sticky="ew", pady=(0, 3))

        self.output_selector = PathSelector(self._paths_frame, "Carpeta de salida", is_folder=True)
        self.output_selector.grid(row=3, column=0, sticky="ew", pady=(0, 3))

        self._middle_frame = ctk.CTkFrame(self)
        self._middle_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 5))
        self._middle_frame.columnconfigure(0, weight=0)
        self._middle_frame.columnconfigure(1, weight=0)

        self._params_frame = ctk.CTkFrame(self._middle_frame)
        self._params_frame.grid(row=0, column=0, sticky="ns", padx=(0, 10))

        self._build_params()

        self._preview_frame = ctk.CTkFrame(self._middle_frame)
        self._preview_frame.grid(row=0, column=1, sticky="ns")
        self.overlay_preview = OverlayPreview(
            self._preview_frame,
            self.offset_x_var, self.offset_y_var,
            self.img_width_var, self.img_height_var, self.img_scale_var,
        )
        self.overlay_preview.pack()

        self.run_btn = ctk.CTkButton(self, text="Ejecutar", command=self._on_run_clicked)
        self.run_btn.grid(row=2, column=0, sticky="w", pady=(5, 5))
        ToolTip(self.run_btn, "Inicia el proceso con los parámetros actuales")

        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.grid(row=3, column=0, sticky="ew", pady=(0, 5))
        self.progress_bar.set(0)

        from ..widgets.log_panel import LogPanel
        self.log_panel = LogPanel(self)
        self.log_panel.grid(row=4, column=0, sticky="nsew")

    def _build_params(self) -> None:
        pf = self._params_frame

        r = 0
        ctk.CTkLabel(pf, text="Image scale:").grid(row=r, column=0, sticky="w", padx=(0, 5))
        self.img_scale_var = ctk.StringVar(value=str(self.config.overlay.image_scale))
        e = ctk.CTkEntry(pf, textvariable=self.img_scale_var, width=55)
        e.grid(row=r, column=1, sticky="w", padx=(0, 20))
        ToolTip(e, "Factor de escala para la imagen superpuesta")

        ctk.CTkLabel(pf, text="Width:").grid(row=r, column=2, sticky="w", padx=(0, 5))
        self.img_width_var = ctk.StringVar(value=str(self.config.overlay.image_width))
        e = ctk.CTkEntry(pf, textvariable=self.img_width_var, width=55)
        e.grid(row=r, column=3, sticky="w")
        ToolTip(e, "Ancho base de la imagen en puntos")

        r = 1
        ctk.CTkLabel(pf, text="Height:").grid(row=r, column=0, sticky="w", padx=(0, 5))
        self.img_height_var = ctk.StringVar(value=str(self.config.overlay.image_height))
        e = ctk.CTkEntry(pf, textvariable=self.img_height_var, width=55)
        e.grid(row=r, column=1, sticky="w", padx=(0, 20))
        ToolTip(e, "Alto base de la imagen en puntos")

        ctk.CTkLabel(pf, text="Offset X:").grid(row=r, column=2, sticky="w", padx=(0, 5))
        self.offset_x_var = ctk.StringVar(value=str(self.config.overlay.offset_x))
        e = ctk.CTkEntry(pf, textvariable=self.offset_x_var, width=55)
        e.grid(row=r, column=3, sticky="w")
        ToolTip(e, "Margen horizontal desde el borde derecho")

        r = 2
        ctk.CTkLabel(pf, text="Offset Y:").grid(row=r, column=0, sticky="w", padx=(0, 5))
        self.offset_y_var = ctk.StringVar(value=str(self.config.overlay.offset_y))
        e = ctk.CTkEntry(pf, textvariable=self.offset_y_var, width=55)
        e.grid(row=r, column=1, sticky="w", padx=(0, 20))
        ToolTip(e, "Margen vertical desde el borde superior")

        ctk.CTkLabel(pf, text="Páginas por grupo:").grid(row=r, column=2, sticky="w", padx=(0, 5))
        self.ppg_var = ctk.StringVar(value=str(self.config.overlay.pages_per_group))
        e = ctk.CTkEntry(pf, textvariable=self.ppg_var, width=55)
        e.grid(row=r, column=3, sticky="w")
        ToolTip(e, "Cantidad de páginas que forman cada documento (ej: 2 = anverso+reverso)")

        r = 3
        ctk.CTkLabel(
            pf, text="Arrastrá la imagen en la vista\nprevia para ajustar posición.",
            font=("", 10), text_color="gray",
        ).grid(row=r, column=0, columnspan=4, sticky="w", pady=(10, 0))

    def _validate_paths(self) -> bool:
        if not super()._validate_paths():
            return False
        if not self.images_selector.get():
            self.log_panel.log("error", "Selecciona una carpeta de imágenes.")
            return False
        return True

    def _get_params(self) -> dict:
        return {
            "image_scale": int(self.img_scale_var.get()),
            "image_width": int(self.img_width_var.get()),
            "image_height": int(self.img_height_var.get()),
            "offset_x": int(self.offset_x_var.get()),
            "offset_y": int(self.offset_y_var.get()),
            "pages_per_group": int(self.ppg_var.get()),
        }

    def _run_task(self, pdf: str, excel: str, output: str, params: dict) -> None:
        from ...core.excel_reader import read_names

        try:
            names = read_names(Path(excel))
            images_folder = Path(self.images_selector.get())
            cfg = self.config.overlay
            cfg.image_scale = params["image_scale"]
            cfg.image_width = params["image_width"]
            cfg.image_height = params["image_height"]
            cfg.offset_x = params["offset_x"]
            cfg.offset_y = params["offset_y"]
            cfg.pages_per_group = params["pages_per_group"]

            output_dir = Path(output)
            output_dir.mkdir(parents=True, exist_ok=True)

            overlay_pdf(
                Path(pdf), names, images_folder, output_dir, cfg,
                on_progress=self._on_progress, on_log=self._on_log,
            )
        except Exception as e:
            self._on_log("error", f"Error: {e}")

    def update_config(self, config: AppConfig) -> None:
        super().update_config(config)
        self.img_scale_var.set(str(config.overlay.image_scale))
        self.img_width_var.set(str(config.overlay.image_width))
        self.img_height_var.set(str(config.overlay.image_height))
        self.offset_x_var.set(str(config.overlay.offset_x))
        self.offset_y_var.set(str(config.overlay.offset_y))
        self.ppg_var.set(str(config.overlay.pages_per_group))
