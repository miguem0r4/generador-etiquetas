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

        self.columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text=label, anchor="w").pack(fill="x", pady=(0, 2))

        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x")
        row.columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(row)
        self.entry.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        self.entry.configure(state="readonly")

        self.btn = ctk.CTkButton(row, text="Examinar", width=100, height=32, command=self._browse)
        self.btn.grid(row=0, column=1)

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
