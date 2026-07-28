import webbrowser
from typing import Optional

import customtkinter as ctk

APP_NAME = "Generador de Etiquetas"
VERSION = "v1.5.0"
AUTHOR = "@miguem0r4"
GITHUB_URL = "https://github.com/miguem0r4"
EMAIL = "ingmigmora@gmail.com"
MAILTO_URL = f"mailto:{EMAIL}"
TAGLINE = "PDFs + Excel  →  Imágenes  ·  Divisiones  ·  Overlays"

_ASCII_LOGO = """
█▀▀ ▀▄▀ █▀▀ █▄ █ ▀█▀ █ █ █▀▀ █   █
█▄▄  █  ██▄ █ ▀█  █  █▄█ ██▄ █▄▄ █▄▄
"""

_ASCII_PDF = "  📄 ✂ 🖼   v1.5.0"


def _make_link(label: ctk.CTkLabel, url: str) -> None:
    normal_color = label.cget("text_color")
    hover_color = ("#0066cc", "#66b3ff")

    def on_enter(e):
        label.configure(text_color=hover_color)

    def on_leave(e):
        label.configure(text_color=normal_color)

    def on_click(e):
        try:
            webbrowser.open(url)
        except Exception:
            pass

    label.bind("<Enter>", on_enter, add="+")
    label.bind("<Leave>", on_leave, add="+")
    label.bind("<Button-1>", on_click, add="+")
    label.configure(cursor="hand2")


class SplashWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self._close_after = 4000
        self._animating = True
        self._current_ascii = 0

        self.overrideredirect(True)
        self.transient(parent)
        self.grab_set()

        w, h = 440, 350
        pw, ph = parent.winfo_width(), parent.winfo_height()
        px, py = parent.winfo_x(), parent.winfo_y()
        x = px + (pw - w) // 2
        y = py + (ph - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

        self.configure(fg_color=("#ffffff", "#0d0d1a"))

        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(expand=True, fill="both", padx=25, pady=20)

        ascii_lines = [
            "█▀▀ █ █ █▀▄▀█ █▀▀ █   █",
            "█ █ █ █ █ ▀ █ ██▄ █▄▄ █",
            "▀▀▀ ▀▀▀ ▀   ▀ ▀▀▀ █▄▄█",
        ]
        for line in ascii_lines:
            ctk.CTkLabel(
                main, text=line, font=("Courier", 14, "bold"),
                text_color=("#1a6d1a", "#4CAF50"),
            ).pack(anchor="center")

        ctk.CTkLabel(
            main, text=TAGLINE, font=("", 10),
            text_color=("#666666", "#888888"),
        ).pack(anchor="center", pady=(6, 10))

        sep = ctk.CTkFrame(main, height=2, fg_color=("#cccccc", "#333355"))
        sep.pack(fill="x", padx=10, pady=(0, 12))

        ctk.CTkLabel(
            main, text="Desarrollado por", font=("", 11, "italic"),
            text_color=("#888888", "#999999"),
        ).pack(anchor="center")

        link_author = ctk.CTkLabel(
            main, text=f"github.com/{AUTHOR}", font=("", 13, "bold"),
            text_color=("#1a6d1a", "#4CAF50"),
        )
        link_author.pack(anchor="center", pady=(4, 0))
        _make_link(link_author, GITHUB_URL)

        link_email = ctk.CTkLabel(
            main, text=EMAIL, font=("", 11, "underline"),
            text_color=("#555555", "#aaaaaa"),
        )
        link_email.pack(anchor="center", pady=(0, 0))
        _make_link(link_email, MAILTO_URL)

        sep2 = ctk.CTkFrame(main, height=1, fg_color=("#dddddd", "#444466"))
        sep2.pack(fill="x", padx=30, pady=(10, 4))

        self._status_label = ctk.CTkLabel(
            main, text="", font=("", 13),
            text_color=("#4CAF50", "#4CAF50"),
        )
        self._status_label.pack(anchor="center")

        self._version_label = ctk.CTkLabel(
            main, text=VERSION, font=("", 9),
            text_color=("#aaaaaa", "#666666"),
        )
        self._version_label.pack(anchor="center")

        self._phase = 0

        self.after(200, self._animate_entry)

        self.bind("<Button-1>", lambda e: self._close())
        for child in main.winfo_children():
            child.bind("<Button-1>", lambda e: self._close(), add="+")

    def _animate_entry(self):
        if not self._animating:
            return
        phases = [
            "Cargando módulos",
            "Analizando dependencias",
            "Inicializando interfaz",
            "Listo",
        ]
        if self._phase < len(phases):
            self._status_label.configure(text=phases[self._phase] + " ...")
            self._phase += 1
            if self._phase < len(phases):
                self.after(600, self._animate_entry)
            else:
                self.after(800, self._fade_out)
        else:
            self._fade_out()

    def _fade_out(self, step=0):
        self._animating = False
        alphas = [1.0, 0.7, 0.4, 0.1, 0.0]
        if step < len(alphas):
            try:
                self.attributes("-alpha", alphas[step])
            except Exception:
                pass
            self.after(60, lambda: self._fade_out(step + 1))
        else:
            self._close()

    def _close(self):
        self._animating = False
        try:
            self.grab_release()
            self.destroy()
        except Exception:
            pass


class AboutDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Acerca de")
        self.geometry("380x340")
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)

        self.configure(fg_color=("#ffffff", "#0d0d1a"))

        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(expand=True, fill="both", padx=25, pady=20)

        ascii_lines = [
            "█▀▀ ▄▀▄ █▀▀ █   █▀▀",
            "█▄▄ █ █ ██▄ █▄▄ ██▄",
        ]
        for line in ascii_lines:
            ctk.CTkLabel(
                main, text=line, font=("Courier", 13, "bold"),
                text_color=("#1a6d1a", "#4CAF50"),
            ).pack(anchor="center")

        ctk.CTkLabel(
            main, text="Generador de Etiquetas", font=("", 18, "bold"),
        ).pack(anchor="center")

        ctk.CTkLabel(
            main, text=TAGLINE, font=("", 10),
            text_color=("#666666", "#999999"),
        ).pack(anchor="center", pady=(0, 8))

        sep = ctk.CTkFrame(main, height=1, fg_color=("#cccccc", "#444466"))
        sep.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(
            main, text="Desarrollado por", font=("", 11),
            text_color=("#888888", "#999999"),
        ).pack(anchor="center")

        link_author = ctk.CTkLabel(
            main, text=f"github.com/{AUTHOR}", font=("", 14, "bold"),
            text_color=("#1a6d1a", "#4CAF50"),
        )
        link_author.pack(anchor="center", pady=(3, 0))
        _make_link(link_author, GITHUB_URL)

        link_email = ctk.CTkLabel(
            main, text=EMAIL, font=("", 11, "underline"),
            text_color=("#555555", "#aaaaaa"),
        )
        link_email.pack(anchor="center", pady=(0, 0))
        _make_link(link_email, MAILTO_URL)

        ctk.CTkLabel(
            main, text=f"Versión: {VERSION}", font=("", 10),
            text_color=("#888888", "#888888"),
        ).pack(anchor="center", pady=(8, 0))

        ctk.CTkButton(
            main, text="Cerrar", width=100, command=self.destroy,
        ).pack(anchor="center", pady=(12, 0))
