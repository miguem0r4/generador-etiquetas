import customtkinter as ctk

APP_NAME = "Generador de Etiquetas"
VERSION = "v1.4.0"
AUTHOR = "@miguem0r4"
EMAIL = "ingmigmora@gmail.com"
TAGLINE = "PDFs + Excel → Imágenes · Divisiones · Overlays"


class SplashWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self._close_after = 3500
        self._animating = True

        self.overrideredirect(True)
        self.transient(parent)
        self.grab_set()

        w, h = 420, 320
        pw, ph = parent.winfo_width(), parent.winfo_height()
        px, py = parent.winfo_x(), parent.winfo_y()
        x, y = px + (pw - w) // 2, py + (ph - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

        self.configure(fg_color=("#ffffff", "#1a1a2e"))

        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(expand=True, fill="both", padx=30, pady=30)

        ctk.CTkLabel(
            main, text=APP_NAME, font=("", 22, "bold"),
            text_color=("#1a1a1a", "#e0e0e0"),
        ).pack(anchor="center")

        ctk.CTkLabel(
            main, text=TAGLINE, font=("", 10),
            text_color=("#666666", "#888888"),
        ).pack(anchor="center", pady=(2, 12))

        sep = ctk.CTkFrame(main, height=2, fg_color=("#cccccc", "#444444"))
        sep.pack(fill="x", padx=20, pady=(0, 16))

        ctk.CTkLabel(
            main, text="Desarrollado por", font=("", 11, "italic"),
            text_color=("#888888", "#999999"),
        ).pack(anchor="center")

        ctk.CTkLabel(
            main, text=AUTHOR, font=("", 16, "bold"),
            text_color=("#1a6d1a", "#4CAF50"),
        ).pack(anchor="center", pady=(4, 2))

        ctk.CTkLabel(
            main, text=EMAIL, font=("", 12),
            text_color=("#555555", "#aaaaaa"),
        ).pack(anchor="center")

        sep2 = ctk.CTkFrame(main, height=1, fg_color=("#dddddd", "#555555"))
        sep2.pack(fill="x", padx=40, pady=(16, 6))

        self._dots_label = ctk.CTkLabel(
            main, text="", font=("", 20),
            text_color=("#4CAF50", "#4CAF50"),
        )
        self._dots_label.pack(anchor="center", pady=(0, 4))

        self._version_label = ctk.CTkLabel(
            main, text=VERSION, font=("", 9),
            text_color=("#aaaaaa", "#666666"),
        )
        self._version_label.pack(anchor="center")

        self._dot_count = 0
        self._animate_dots()

        self.after(self._close_after, self._on_timeout)
        self.bind("<Button-1>", lambda e: self._close())
        main.bind("<Button-1>", lambda e: self._close())
        for child in main.winfo_children():
            child.bind("<Button-1>", lambda e: self._close())

    def _animate_dots(self):
        if not self._animating:
            return
        dots = [".", "..", "...", "   "]
        self._dots_label.configure(text=dots[self._dot_count % len(dots)])
        self._dot_count += 1
        self.after(400, self._animate_dots)

    def _on_timeout(self):
        self._fade_out()

    def _fade_out(self):
        self._animating = False
        try:
            for a in [1.0, 0.8, 0.6, 0.4, 0.2, 0.0]:
                self.after(int(50), lambda v=a: self.attributes("-alpha", v))
                self.update()
            self._close()
        except Exception:
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
        self.geometry("360x300")
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)

        self.configure(fg_color=("#ffffff", "#1a1a2e"))

        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(expand=True, fill="both", padx=30, pady=25)

        ctk.CTkLabel(
            main, text=APP_NAME, font=("", 20, "bold"),
        ).pack(anchor="center")

        ctk.CTkLabel(
            main, text=VERSION, font=("", 11),
            text_color=("#888888", "#888888"),
        ).pack(anchor="center", pady=(2, 12))

        ctk.CTkLabel(
            main, text=TAGLINE, font=("", 10),
            text_color=("#666666", "#999999"),
        ).pack(anchor="center")

        sep = ctk.CTkFrame(main, height=1, fg_color=("#cccccc", "#444444"))
        sep.pack(fill="x", padx=20, pady=(14, 14))

        ctk.CTkLabel(
            main, text="Desarrollado por", font=("", 11),
            text_color=("#888888", "#999999"),
        ).pack(anchor="center")

        ctk.CTkLabel(
            main, text=AUTHOR, font=("", 15, "bold"),
            text_color=("#1a6d1a", "#4CAF50"),
        ).pack(anchor="center", pady=(2, 0))

        ctk.CTkLabel(
            main, text=EMAIL, font=("", 11),
            text_color=("#555555", "#aaaaaa"),
        ).pack(anchor="center")

        ctk.CTkButton(
            main, text="Cerrar", width=100, command=self.destroy,
        ).pack(anchor="center", pady=(18, 0))
