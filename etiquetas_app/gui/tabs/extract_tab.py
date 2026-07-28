from pathlib import Path

import customtkinter as ctk

from ...core.extract_images import extract_images
from ...core.models import AppConfig
from .base_tab import BaseTab


class ExtractTab(BaseTab):
    def __init__(self, parent, config: AppConfig, **kwargs):
        super().__init__(parent, config, **kwargs)

    def _build_params(self) -> None:
        pf = self._params_frame
        pf.columnconfigure(1, weight=1)

        r = 0
        ctk.CTkLabel(pf, text="Render scale:").grid(row=r, column=0, sticky="w", padx=(0, 5))
        self.render_scale_var = ctk.StringVar(value=str(self.config.extract.render_scale))
        ctk.CTkEntry(pf, textvariable=self.render_scale_var, width=55).grid(row=r, column=1, sticky="w", padx=(0, 20))

        ctk.CTkLabel(pf, text="Crop left:").grid(row=r, column=2, sticky="w", padx=(0, 5))
        self.crop_left_var = ctk.DoubleVar(value=self.config.extract.crop_left_ratio)
        ctk.CTkSlider(pf, from_=0.0, to=1.0, variable=self.crop_left_var, width=100).grid(
            row=r, column=3, sticky="w"
        )
        self.crop_left_lbl = ctk.CTkLabel(pf, text=f"{self.config.extract.crop_left_ratio:.2f}", width=35)
        self.crop_left_lbl.grid(row=r, column=4, sticky="w")

        r = 1
        ctk.CTkLabel(pf, text="Crop top:").grid(row=r, column=0, sticky="w", padx=(0, 5))
        self.crop_top_var = ctk.DoubleVar(value=self.config.extract.crop_top_ratio)
        ctk.CTkSlider(pf, from_=0.0, to=1.0, variable=self.crop_top_var, width=100).grid(
            row=r, column=1, sticky="w"
        )
        self.crop_top_lbl = ctk.CTkLabel(pf, text=f"{self.config.extract.crop_top_ratio:.2f}", width=35)
        self.crop_top_lbl.grid(row=r, column=2, sticky="w")

        ctk.CTkLabel(pf, text="Crop right:").grid(row=r, column=2, sticky="w", padx=(20, 5))
        self.crop_right_var = ctk.DoubleVar(value=self.config.extract.crop_right_ratio)
        ctk.CTkSlider(pf, from_=0.0, to=1.0, variable=self.crop_right_var, width=100).grid(
            row=r, column=3, sticky="w"
        )
        self.crop_right_lbl = ctk.CTkLabel(pf, text=f"{self.config.extract.crop_right_ratio:.2f}", width=35)
        self.crop_right_lbl.grid(row=r, column=4, sticky="w")

        r = 2
        ctk.CTkLabel(pf, text="Crop bottom:").grid(row=r, column=0, sticky="w", padx=(0, 5))
        self.crop_bottom_var = ctk.DoubleVar(value=self.config.extract.crop_bottom_ratio)
        ctk.CTkSlider(pf, from_=0.0, to=1.0, variable=self.crop_bottom_var, width=100).grid(
            row=r, column=1, sticky="w"
        )
        self.crop_bottom_lbl = ctk.CTkLabel(pf, text=f"{self.config.extract.crop_bottom_ratio:.2f}", width=35)
        self.crop_bottom_lbl.grid(row=r, column=2, sticky="w")

        def _update(*_):
            self.crop_left_lbl.configure(text=f"{self.crop_left_var.get():.2f}")
            self.crop_top_lbl.configure(text=f"{self.crop_top_var.get():.2f}")
            self.crop_right_lbl.configure(text=f"{self.crop_right_var.get():.2f}")
            self.crop_bottom_lbl.configure(text=f"{self.crop_bottom_var.get():.2f}")

        self.crop_left_var.trace_add("write", _update)
        self.crop_top_var.trace_add("write", _update)
        self.crop_right_var.trace_add("write", _update)
        self.crop_bottom_var.trace_add("write", _update)

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
