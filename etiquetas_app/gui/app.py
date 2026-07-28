from pathlib import Path
from typing import Optional

import customtkinter as ctk

from ..core.models import AppConfig
from ..utils.config import load_config, save_config
from .settings_dialog import SettingsDialog
from .splash import AboutDialog, SplashWindow
from .widgets.tooltip import ToolTip
from .tabs.extract_tab import ExtractTab
from .tabs.overlay_tab import OverlayTab
from .tabs.split_tab import SplitTab


class App(ctk.CTk):
    def __init__(self, config_path: Optional[Path] = None):
        super().__init__()
        self.config_path = config_path
        self.config = load_config(self.config_path)

        self.title("Generador de Etiquetas")
        self.geometry("950x700")
        self.minsize(800, 600)

        ctk.set_appearance_mode(self.config.theme)
        ctk.set_default_color_theme("green")

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self.after(150, self._show_splash)

    def _build_ui(self) -> None:
        top_frame = ctk.CTkFrame(self, height=44, corner_radius=0)
        top_frame.pack(fill="x", padx=0, pady=(0, 0))
        top_frame.pack_propagate(False)

        ctk.CTkLabel(
            top_frame, text="Generador de Etiquetas", font=("", 18, "bold")
        ).pack(side="left", padx=15)

        btn_about = ctk.CTkButton(
            top_frame, text="Acerca de", width=100, command=self._open_about,
        )
        btn_about.pack(side="right", padx=(0, 8))
        ToolTip(btn_about, "Créditos y versión de la aplicación")

        btn_config = ctk.CTkButton(
            top_frame, text="Configuración", width=120, command=self._open_settings,
        )
        btn_config.pack(side="right", padx=(0, 8))
        ToolTip(btn_config, "Ajustar rutas predeterminadas, parámetros y tema visual")

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        self.tabs: dict = {}
        tab_defs = [
            ("Extraer Imágenes", ExtractTab),
            ("Dividir PDF", SplitTab),
            ("Insertar Etiquetas", OverlayTab),
        ]
        for name, tab_class in tab_defs:
            frame = self.tabview.add(name)
            tab = tab_class(frame, self.config)
            tab.pack(fill="both", expand=True)
            self.tabs[name] = tab

    def _show_splash(self) -> None:
        SplashWindow(self)

    def _open_about(self) -> None:
        AboutDialog(self)

    def _open_settings(self) -> None:
        def on_saved(cfg: AppConfig) -> None:
            self.config = cfg
            ctk.set_appearance_mode(self.config.theme)
            for tab in self.tabs.values():
                tab.update_config(cfg)
            save_config(cfg, self.config_path)

        SettingsDialog(self, self.config, on_save_callback=on_saved)

    def _on_close(self) -> None:
        save_config(self.config, self.config_path)
        self.destroy()


def run_gui(config_path: Optional[Path] = None) -> None:
    app = App(config_path)
    app.mainloop()
