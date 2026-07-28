from datetime import datetime

import customtkinter as ctk


class LogPanel(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.header = ctk.CTkLabel(self, text="Log", anchor="w", font=("", 13, "bold"))
        self.header.grid(row=0, column=0, sticky="w", pady=(0, 2))

        self.textbox = ctk.CTkTextbox(self, wrap="word", state="normal")
        self.textbox.grid(row=1, column=0, sticky="nsew")

        self.textbox.configure(state="disabled")

    def log(self, level: str, msg: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        tag = level.lower()

        self.textbox.configure(state="normal")
        self.textbox.insert("end", f"[{timestamp}] {msg}\n", tag)
        self.textbox.configure(state="disabled")
        self.textbox.see("end")

    def clear(self) -> None:
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.configure(state="disabled")
