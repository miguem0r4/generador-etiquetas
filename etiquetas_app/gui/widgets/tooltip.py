import customtkinter as ctk


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self._window = None
        widget.bind("<Enter>", self._show, add="+")
        widget.bind("<Leave>", self._hide, add="+")
        widget.bind("<ButtonPress>", self._hide, add="+")

    def _show(self, event=None):
        if self._window:
            return
        x = self.widget.winfo_rootx() + 10
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4
        self._window = ctk.CTkToplevel(self.widget)
        self._window.wm_overrideredirect(True)
        self._window.wm_geometry(f"+{x}+{y}")
        self._window.attributes("-topmost", True)
        self._window.configure(fg_color=("#333333", "#e0e0e0"))
        label = ctk.CTkLabel(
            self._window, text=self.text,
            text_color=("#ffffff", "#111111"),
            font=("", 11),
            padx=8, pady=4,
        )
        label.pack()

    def _hide(self, event=None):
        if self._window:
            self._window.destroy()
            self._window = None
