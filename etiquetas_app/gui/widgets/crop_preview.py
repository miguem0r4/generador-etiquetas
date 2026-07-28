import tkinter as tk

import customtkinter as ctk


class CropPreview(ctk.CTkFrame):
    CANVAS_W = 200
    CANVAS_H = 260
    PAD = 15
    PAGE_W = CANVAS_W - 2 * PAD
    PAGE_H = CANVAS_H - 2 * PAD

    def __init__(self, parent, left_var, top_var, right_var, bottom_var, **kwargs):
        super().__init__(parent, **kwargs)

        self.lv = left_var
        self.tv = top_var
        self.rv = right_var
        self.bv = bottom_var

        self._drag_edge = None

        ctk.CTkLabel(self, text="Vista previa del recorte:", anchor="w", font=("", 12, "bold")).pack(anchor="w")

        self.canvas = tk.Canvas(
            self, width=self.CANVAS_W, height=self.CANVAS_H,
            bg="#f0f0f0", highlightthickness=0,
        )
        self.canvas.pack(pady=(4, 0))

        self.canvas.bind("<Button-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)

        self.lv.trace_add("write", lambda *_: self._render_preview())
        self.tv.trace_add("write", lambda *_: self._render_preview())
        self.rv.trace_add("write", lambda *_: self._render_preview())
        self.bv.trace_add("write", lambda *_: self._render_preview())

        self._render_preview()

    def _render_preview(self):
        c = self.canvas
        c.delete("all")

        pw, ph = self.PAGE_W, self.PAGE_H
        px, py = self.PAD, self.PAD

        c.create_rectangle(px, py, px + pw, py + ph, outline="#bbb", width=1, fill="white")

        l = px + pw * self.lv.get()
        t = py + ph * self.tv.get()
        r = px + pw * self.rv.get()
        b = py + ph * self.bv.get()

        c.create_rectangle(l, t, r, b, fill="#4CAF50", stipple="gray25", outline="#2E7D32", width=2)

        cx, cy = (l + r) / 2, (t + b) / 2
        c.create_text(cx, cy, text="RECORTE", font=("", 9, "bold"), fill="#1B5E20")

        self._draw_edge_label(c, "L", l, (t + b) / 2, self.lv.get())
        self._draw_edge_label(c, "T", (l + r) / 2, t, self.tv.get(), "top")
        self._draw_edge_label(c, "R", r, (t + b) / 2, self.rv.get())
        self._draw_edge_label(c, "B", (l + r) / 2, b, self.bv.get(), "top")

        self._draw_handle(c, l, t)
        self._draw_handle(c, r, t)
        self._draw_handle(c, l, b)
        self._draw_handle(c, r, b)

    def _draw_edge_label(self, c, text, x, y, value, anchor="w"):
        label = f"{text}: {value:.0%}"
        if anchor == "top":
            c.create_text(x, y - 10, text=label, font=("", 8), fill="#333", anchor="s")
        else:
            dx = -8 if text in ("L",) else 8
            c.create_text(x + dx, y, text=label, font=("", 8), fill="#333", anchor="e" if text == "L" else "w")

    def _draw_handle(self, c, x, y):
        s = 5
        c.create_rectangle(x - s, y - s, x + s, y + s, fill="#2E7D32", outline="white", width=1)

    def _on_press(self, event):
        pw, ph = self.PAGE_W, self.PAGE_H
        px, py = self.PAD, self.PAD
        tol = 8
        l = px + pw * self.lv.get()
        t = py + ph * self.tv.get()
        r = px + pw * self.rv.get()
        b = py + ph * self.bv.get()
        x, y = event.x, event.y

        edges = []
        if abs(x - l) < tol and t < y < b:
            edges.append("L")
        if abs(x - r) < tol and t < y < b:
            edges.append("R")
        if abs(y - t) < tol and l < x < r:
            edges.append("T")
        if abs(y - b) < tol and l < x < r:
            edges.append("B")

        self._drag_edge = edges[0] if edges else None
        self._drag_start = (x, y, self.lv.get(), self.tv.get(), self.rv.get(), self.bv.get())

    def _on_drag(self, event):
        if not self._drag_edge:
            return
        pw, ph = self.PAGE_W, self.PAGE_H
        _, _, start_l, start_t, start_r, start_b = self._drag_start
        dx = (event.x - self._drag_start[0]) / pw
        dy = (event.y - self._drag_start[1]) / ph

        if self._drag_edge == "L":
            val = max(0.0, min(start_r - 0.02, start_l + dx))
            self.lv.set(val)
        elif self._drag_edge == "R":
            val = max(start_l + 0.02, min(1.0, start_r + dx))
            self.rv.set(val)
        elif self._drag_edge == "T":
            val = max(0.0, min(start_b - 0.02, start_t + dy))
            self.tv.set(val)
        elif self._drag_edge == "B":
            val = max(start_t + 0.02, min(1.0, start_b + dy))
            self.bv.set(val)

    def _on_release(self, event):
        self._drag_edge = None
