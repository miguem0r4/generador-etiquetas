from pathlib import Path
from tkinter import filedialog
from typing import List, Optional, Tuple

import customtkinter as ctk


class PathSelector(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        label: str,
        is_folder: bool = False,
        filetypes: Optional[List[Tuple[str, str]]] = None,
        **kwargs,
    ):
        super().__init__(parent, **kwargs)
        self.is_folder = is_folder
        self.filetypes = filetypes or [("Todos los archivos", "*.*")]
        self._path: str = ""
        self._label_text = label

        self.columnconfigure(1, weight=1)

        ctk.CTkLabel(self, text=label, anchor="w").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 2)
        )

        self.entry = ctk.CTkEntry(self)
        self.entry.grid(row=1, column=0, sticky="ew", padx=(0, 5))
        self.entry.configure(state="readonly")

        ctk.CTkButton(self, text="Examinar", width=90, command=self._browse).grid(
            row=1, column=1, padx=(0, 0)
        )

    def _browse(self) -> None:
        if self.is_folder:
            path = filedialog.askdirectory(title=self._label_text)
        else:
            path = filedialog.askopenfilename(
                title=self._label_text,
                filetypes=self.filetypes,
            )
        if path:
            self._path = path
            self.entry.configure(state="normal")
            self.entry.delete(0, "end")
            self.entry.insert(0, path)
            self.entry.configure(state="readonly")

    def get(self) -> str:
        return self._path

    def set(self, path: str) -> None:
        self._path = str(path)
        self.entry.configure(state="normal")
        self.entry.delete(0, "end")
        self.entry.insert(0, str(path))
        self.entry.configure(state="readonly")

    def clear(self) -> None:
        self._path = ""
        self.entry.configure(state="normal")
        self.entry.delete(0, "end")
        self.entry.configure(state="readonly")
