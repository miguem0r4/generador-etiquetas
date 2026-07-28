from pathlib import Path

import customtkinter as ctk

from ...core.models import AppConfig
from ...core.split_pdf import split_pdf
from .base_tab import BaseTab


class SplitTab(BaseTab):
    def __init__(self, parent, config: AppConfig, **kwargs):
        super().__init__(parent, config, **kwargs)

    def _build_params(self) -> None:
        ctk.CTkLabel(self._params_frame, text="Páginas por grupo:").grid(
            row=0, column=0, sticky="w", padx=(0, 5)
        )
        self.ppg_var = ctk.StringVar(value=str(self.config.split.pages_per_group))
        ctk.CTkEntry(self._params_frame, textvariable=self.ppg_var, width=55).grid(
            row=0, column=1, sticky="w"
        )

    def _get_params(self) -> dict:
        return {"pages_per_group": int(self.ppg_var.get())}

    def _run_task(self, pdf: str, excel: str, output: str, params: dict) -> None:
        from ...core.excel_reader import read_names

        try:
            names = read_names(Path(excel))
            self.config.split.pages_per_group = params["pages_per_group"]
            output_dir = Path(output)
            output_dir.mkdir(parents=True, exist_ok=True)

            split_pdf(
                Path(pdf), names, output_dir, self.config.split,
                on_progress=self._on_progress, on_log=self._on_log,
            )
        except Exception as e:
            self._on_log("error", f"Error: {e}")

    def update_config(self, config: AppConfig) -> None:
        super().update_config(config)
        self.ppg_var.set(str(config.split.pages_per_group))
