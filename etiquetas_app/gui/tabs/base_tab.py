import queue
import threading
from typing import Optional

import customtkinter as ctk

from ...core.models import AppConfig
from ..widgets.log_panel import LogPanel
from ..widgets.path_selector import PathSelector
from ..widgets.tooltip import ToolTip


class BaseTab(ctk.CTkFrame):
    def __init__(self, parent, config: AppConfig, **kwargs):
        super().__init__(parent, **kwargs)
        self.config = config

        self.columnconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)

        self._progress_queue: queue.Queue = queue.Queue()
        self._thread: Optional[threading.Thread] = None

        self._build_common_ui()
        self._build_params()

    def _build_common_ui(self) -> None:
        self._paths_frame = ctk.CTkFrame(self)
        self._paths_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        self._paths_frame.columnconfigure(0, weight=1)

        self.pdf_selector = PathSelector(self._paths_frame, "PDF de entrada", filetypes=[("Archivos PDF", "*.pdf")])
        self.pdf_selector.grid(row=0, column=0, sticky="ew", pady=(0, 3))

        self.excel_selector = PathSelector(
            self._paths_frame, "Excel de nombres", filetypes=[("Archivos Excel", "*.xlsx;*.xls")]
        )
        self.excel_selector.grid(row=1, column=0, sticky="ew", pady=(0, 3))

        self.output_selector = PathSelector(self._paths_frame, "Carpeta de salida", is_folder=True)
        self.output_selector.grid(row=2, column=0, sticky="ew", pady=(0, 3))

        self._params_frame = ctk.CTkFrame(self)
        self._params_frame.grid(row=1, column=0, sticky="ew", pady=(0, 5))

        self.run_btn = ctk.CTkButton(self, text="Ejecutar", command=self._on_run_clicked)
        self.run_btn.grid(row=2, column=0, sticky="w", pady=(5, 5))
        ToolTip(self.run_btn, "Iniciar el procesamiento con los archivos y parámetros seleccionados")

        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.grid(row=3, column=0, sticky="ew", pady=(0, 5))
        self.progress_bar.set(0)

        self.log_panel = LogPanel(self)
        self.log_panel.grid(row=4, column=0, sticky="nsew")

    def _build_params(self) -> None:
        pass

    def _on_run_clicked(self) -> None:
        if self._thread and self._thread.is_alive():
            return

        if not self._validate_paths():
            return

        additional_params = self._get_params()
        pdf = self.pdf_selector.get()
        excel = self.excel_selector.get()
        output = self.output_selector.get()

        self.progress_bar.set(0)
        self.log_panel.clear()
        self.run_btn.configure(state="disabled", text="Procesando...")

        self._progress_queue = queue.Queue()

        self._thread = threading.Thread(
            target=self._run_task,
            args=(pdf, excel, output, additional_params),
            daemon=True,
        )
        self._thread.start()
        self._poll_thread()

    def _validate_paths(self) -> bool:
        if not self.pdf_selector.get():
            self.log_panel.log("error", "Selecciona un archivo PDF.")
            return False
        if not self.excel_selector.get():
            self.log_panel.log("error", "Selecciona un archivo Excel.")
            return False
        if not self.output_selector.get():
            self.log_panel.log("error", "Selecciona una carpeta de salida.")
            return False
        return True

    def _get_params(self) -> dict:
        return {}

    def _run_task(self, pdf: str, excel: str, output: str, params: dict) -> None:
        pass

    def _on_log(self, level: str, msg: str) -> None:
        self._progress_queue.put(("log", level, msg))

    def _on_progress(self, current: int, total: int) -> None:
        self._progress_queue.put(("progress", current, total))

    def _poll_thread(self) -> None:
        try:
            while True:
                msg = self._progress_queue.get_nowait()
                if msg[0] == "progress":
                    c, t = msg[1], msg[2]
                    self.progress_bar.set(c / t if t > 0 else 0)
                elif msg[0] == "log":
                    self.log_panel.log(msg[1], msg[2])
        except queue.Empty:
            pass

        if self._thread and self._thread.is_alive():
            self.after(100, self._poll_thread)
        else:
            self.run_btn.configure(state="normal", text="Ejecutar")

    def update_config(self, config: AppConfig) -> None:
        self.config = config
