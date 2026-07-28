from pathlib import Path

import customtkinter as ctk

from ...core.extract_images import extract_images
from ...core.models import AppConfig
from ..widgets.crop_preview import CropPreview
from .base_tab import BaseTab


class ExtractTab(BaseTab):
    def __init__(self, parent, config: AppConfig, **kwargs):
        super().__init__(parent, config, **kwargs)

    def _build_params(self) -> None:
        pf = self._params_frame
        pf.columnconfigure(0, weight=1)
        pf.columnconfigure(1, weight=0)
        pf.rowconfigure(0, weight=1)

        # --- Left side: sliders ---
        sf = ctk.CTkFrame(pf)
        sf.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        sf.columnconfigure(1, weight=1)

        self.crop_left_var = ctk.DoubleVar(value=self.config.extract.crop_left_ratio)
        self.crop_top_var = ctk.DoubleVar(value=self.config.extract.crop_top_ratio)
        self.crop_right_var = ctk.DoubleVar(value=self.config.extract.crop_right_ratio)
        self.crop_bottom_var = ctk.DoubleVar(value=self.config.extract.crop_bottom_ratio)

        r = 0
        ctk.CTkLabel(sf, text="Render scale:", font=("", 12)).grid(row=r, column=0, sticky="w", padx=(0, 5))
        self.render_scale_var = ctk.StringVar(value=str(self.config.extract.render_scale))
        ctk.CTkEntry(sf, textvariable=self.render_scale_var, width=55).grid(row=r, column=1, sticky="w")

        def pct(val):
            return f"{val * 100:.0f}%"

        r = 1
        ctk.CTkLabel(sf, text="Izquierda (L):", font=("", 12)).grid(row=r, column=0, sticky="w", padx=(0, 5), pady=(8, 0))
        ctk.CTkSlider(sf, from_=0.0, to=1.0, variable=self.crop_left_var, width=140).grid(
            row=r, column=1, sticky="ew", padx=(0, 8), pady=(8, 0)
        )
        self.crop_left_lbl = ctk.CTkLabel(sf, text=pct(self.config.extract.crop_left_ratio), width=40)
        self.crop_left_lbl.grid(row=r, column=2, sticky="w", pady=(8, 0))

        r = 2
        ctk.CTkLabel(sf, text="Superior (T):", font=("", 12)).grid(row=r, column=0, sticky="w", padx=(0, 5))
        ctk.CTkSlider(sf, from_=0.0, to=1.0, variable=self.crop_top_var, width=140).grid(
            row=r, column=1, sticky="ew", padx=(0, 8)
        )
        self.crop_top_lbl = ctk.CTkLabel(sf, text=pct(self.config.extract.crop_top_ratio), width=40)
        self.crop_top_lbl.grid(row=r, column=2, sticky="w")

        r = 3
        ctk.CTkLabel(sf, text="Derecha (R):", font=("", 12)).grid(row=r, column=0, sticky="w", padx=(0, 5))
        ctk.CTkSlider(sf, from_=0.0, to=1.0, variable=self.crop_right_var, width=140).grid(
            row=r, column=1, sticky="ew", padx=(0, 8)
        )
        self.crop_right_lbl = ctk.CTkLabel(sf, text=pct(self.config.extract.crop_right_ratio), width=40)
        self.crop_right_lbl.grid(row=r, column=2, sticky="w")

        r = 4
        ctk.CTkLabel(sf, text="Inferior (B):", font=("", 12)).grid(row=r, column=0, sticky="w", padx=(0, 5))
        ctk.CTkSlider(sf, from_=0.0, to=1.0, variable=self.crop_bottom_var, width=140).grid(
            row=r, column=1, sticky="ew", padx=(0, 8)
        )
        self.crop_bottom_lbl = ctk.CTkLabel(sf, text=pct(self.config.extract.crop_bottom_ratio), width=40)
        self.crop_bottom_lbl.grid(row=r, column=2, sticky="w")

        def _update(*_):
            self.crop_left_lbl.configure(text=pct(self.crop_left_var.get()))
            self.crop_top_lbl.configure(text=pct(self.crop_top_var.get()))
            self.crop_right_lbl.configure(text=pct(self.crop_right_var.get()))
            self.crop_bottom_lbl.configure(text=pct(self.crop_bottom_var.get()))

        self.crop_left_var.trace_add("write", _update)
        self.crop_top_var.trace_add("write", _update)
        self.crop_right_var.trace_add("write", _update)
        self.crop_bottom_var.trace_add("write", _update)

        # Hint text
        ctk.CTkLabel(
            sf, text="Arrastrá los bordes del rectángulo en la\nvista previa o mové los sliders.",
            font=("", 10), text_color="gray",
        ).grid(row=5, column=0, columnspan=3, sticky="w", pady=(10, 0))

        # --- Right side: crop preview ---
        self.crop_preview = CropPreview(
            pf, self.crop_left_var, self.crop_top_var,
            self.crop_right_var, self.crop_bottom_var,
        )
        self.crop_preview.grid(row=0, column=1, sticky="ns", padx=(0, 0))

    def _get_params(self) -> dict:
        return {
            "render_scale": int(self.render_scale_var.get()),
            "crop_left_ratio": self.crop_left_var.get(),
            "crop_top_ratio": self.crop_top_var.get(),
            "crop_right_ratio": self.crop_right_var.get(),
            "crop_bottom_ratio": self.crop_bottom_var.get(),
        }

    def _run_task(self, pdf: str, excel: str, output: str, params: dict) -> None:
        from ...core.excel_reader import read_names

        try:
            names = read_names(Path(excel))
            cfg = self.config.extract
            cfg.render_scale = params["render_scale"]
            cfg.crop_left_ratio = params["crop_left_ratio"]
            cfg.crop_top_ratio = params["crop_top_ratio"]
            cfg.crop_right_ratio = params["crop_right_ratio"]
            cfg.crop_bottom_ratio = params["crop_bottom_ratio"]

            output_dir = Path(output)
            output_dir.mkdir(parents=True, exist_ok=True)

            extract_images(
                Path(pdf), names, output_dir, cfg,
                on_progress=self._on_progress, on_log=self._on_log,
            )
        except Exception as e:
            self._on_log("error", f"Error: {e}")

    def update_config(self, config: AppConfig) -> None:
        super().update_config(config)
        self.render_scale_var.set(str(config.extract.render_scale))
        self.crop_left_var.set(config.extract.crop_left_ratio)
        self.crop_top_var.set(config.extract.crop_top_ratio)
        self.crop_right_var.set(config.extract.crop_right_ratio)
        self.crop_bottom_var.set(config.extract.crop_bottom_ratio)
