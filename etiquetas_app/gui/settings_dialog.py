from pathlib import Path
from typing import Callable, Optional

import customtkinter as ctk

from ..core.models import AppConfig, ExtractConfig, OverlayConfig, SplitConfig


class SettingsDialog(ctk.CTkToplevel):
    def __init__(
        self,
        parent,
        config: AppConfig,
        on_save_callback: Optional[Callable[[AppConfig], None]] = None,
    ):
        super().__init__(parent)
        self.config = AppConfig.from_dict(config.to_dict())
        self.on_save_callback = on_save_callback

        self.title("Configuración")
        self.geometry("580x500")
        self.transient(parent)
        self.grab_set()

        self._build_ui()

    def _build_ui(self) -> None:
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        self._build_paths_tab(self.tabview.add("Rutas"))
        self._build_extract_tab(self.tabview.add("Extract"))
        self._build_overlay_tab(self.tabview.add("Overlay"))
        self._build_split_tab(self.tabview.add("Split"))
        self._build_appearance_tab(self.tabview.add("Apariencia"))

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkButton(btn_frame, text="Restaurar defaults", command=self._restore_defaults).pack(
            side="left", padx=5
        )
        ctk.CTkButton(btn_frame, text="Cancelar", command=self.destroy).pack(side="right", padx=5)
        ctk.CTkButton(btn_frame, text="Guardar", command=self._save).pack(side="right", padx=5)

    def _build_paths_tab(self, parent) -> None:
        parent.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(parent, text="Carpeta salida por defecto:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        self.default_output_var = ctk.StringVar(value=self.config.paths.get("default_output", ""))
        ctk.CTkEntry(parent, textvariable=self.default_output_var).grid(
            row=0, column=1, sticky="ew", padx=5, pady=5
        )

        ctk.CTkLabel(parent, text="Carpeta imágenes overlay:").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        self.images_folder_var = ctk.StringVar(value=self.config.paths.get("images_folder", ""))
        ctk.CTkEntry(parent, textvariable=self.images_folder_var).grid(
            row=1, column=1, sticky="ew", padx=5, pady=5
        )

    def _build_extract_tab(self, parent) -> None:
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_columnconfigure(3, weight=1)

        row = 0
        for label, key, attr in [
            ("Render scale:", "render_scale", int),
            ("Crop left ratio:", "crop_left_ratio", float),
            ("Crop top ratio:", "crop_top_ratio", float),
            ("Crop right ratio:", "crop_right_ratio", float),
            ("Crop bottom ratio:", "crop_bottom_ratio", float),
        ]:
            ctk.CTkLabel(parent, text=label).grid(row=row, column=0, sticky="w", padx=5, pady=3)
            var = ctk.StringVar(value=str(getattr(self.config.extract, key)))
            setattr(self, f"extract_{key}_var", var)
            width = 40 if attr == int else 60
            ctk.CTkEntry(parent, textvariable=var, width=width).grid(
                row=row, column=1, sticky="w", padx=5, pady=3
            )
            row += 1

    def _build_overlay_tab(self, parent) -> None:
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_columnconfigure(3, weight=1)

        for i, (label, key) in enumerate(
            [
                ("Image scale:", "image_scale"),
                ("Image width:", "image_width"),
                ("Image height:", "image_height"),
                ("Offset X:", "offset_x"),
                ("Offset Y:", "offset_y"),
                ("Páginas por grupo:", "pages_per_group"),
            ]
        ):
            ctk.CTkLabel(parent, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=3)
            var = ctk.StringVar(value=str(getattr(self.config.overlay, key)))
            setattr(self, f"overlay_{key}_var", var)
            ctk.CTkEntry(parent, textvariable=var, width=60).grid(
                row=i, column=1, sticky="w", padx=5, pady=3
            )

    def _build_split_tab(self, parent) -> None:
        parent.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(parent, text="Páginas por grupo:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        self.split_ppg_var = ctk.StringVar(value=str(self.config.split.pages_per_group))
        ctk.CTkEntry(parent, textvariable=self.split_ppg_var, width=50).grid(
            row=0, column=1, sticky="w", padx=5, pady=5
        )

    def _build_appearance_tab(self, parent) -> None:
        parent.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(parent, text="Tema:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.theme_var = ctk.StringVar(value=self.config.theme)
        ctk.CTkOptionMenu(parent, values=["dark", "light", "system"], variable=self.theme_var).grid(
            row=0, column=1, sticky="w", padx=5, pady=5
        )

    def _restore_defaults(self) -> None:
        defaults = AppConfig()
        self.default_output_var.set(defaults.paths.get("default_output", ""))
        self.images_folder_var.set(defaults.paths.get("images_folder", ""))
        self.theme_var.set(defaults.theme)

        for key in ["render_scale", "crop_left_ratio", "crop_top_ratio", "crop_right_ratio", "crop_bottom_ratio"]:
            var = getattr(self, f"extract_{key}_var", None)
            if var:
                var.set(str(getattr(defaults.extract, key)))

        for key in ["image_scale", "image_width", "image_height", "offset_x", "offset_y", "pages_per_group"]:
            var = getattr(self, f"overlay_{key}_var", None)
            if var:
                var.set(str(getattr(defaults.overlay, key)))

        self.split_ppg_var.set(str(defaults.split.pages_per_group))

    def _save(self) -> None:
        self.config.paths["default_output"] = self.default_output_var.get()
        self.config.paths["images_folder"] = self.images_folder_var.get()
        self.config.theme = self.theme_var.get()

        self.config.extract = ExtractConfig(
            render_scale=int(self._get_var("extract_render_scale_var")),
            crop_left_ratio=float(self._get_var("extract_crop_left_ratio_var")),
            crop_top_ratio=float(self._get_var("extract_crop_top_ratio_var")),
            crop_right_ratio=float(self._get_var("extract_crop_right_ratio_var")),
            crop_bottom_ratio=float(self._get_var("extract_crop_bottom_ratio_var")),
        )

        self.config.overlay = OverlayConfig(
            image_scale=int(self._get_var("overlay_image_scale_var")),
            image_width=int(self._get_var("overlay_image_width_var")),
            image_height=int(self._get_var("overlay_image_height_var")),
            offset_x=int(self._get_var("overlay_offset_x_var")),
            offset_y=int(self._get_var("overlay_offset_y_var")),
            pages_per_group=int(self._get_var("overlay_pages_per_group_var")),
        )

        self.config.split = SplitConfig(
            pages_per_group=int(self.split_ppg_var.get())
        )

        if self.on_save_callback:
            self.on_save_callback(self.config)

        self.destroy()

    def _get_var(self, name: str) -> str:
        var = getattr(self, name, None)
        return var.get() if var else ""
