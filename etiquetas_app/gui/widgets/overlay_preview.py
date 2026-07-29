import tkinter as tk

import customtkinter as ctk

A4_W = 595
A4_H = 842


class OverlayPreview(ctk.CTkFrame):
    CANVAS_W = 180
    CANVAS_H = 230
    PAD = 15

    def __init__(
        self, parent,
        offset_x_var, offset_y_var,
        img_width_var, img_height_var, img_scale_var,
        **kwargs,
    ):
        super().__init__(parent, **kwargs)

        self.oxv = offset_x_var
        self.oyv = offset_y_var
        self.wv = img_width_var
        self.hv = img_height_var
        self.sv = img_scale_var

        self._dragging = False
        self._drag_start = None

        ctk.CTkLabel(self, text="Vista previa de posición:", anchor="w", font=("", 12, "bold")).pack(anchor="w")

        self.canvas = tk.Canvas(
            self, width=self.CANVAS_W, height=self.CANVAS_H,
            bg="#f0f0f0", highlightthickness=0,
        )
        self.canvas.pack(pady=(4, 0))

        self.canvas.bind("<Button-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)

        self.oxv.trace_add("write", lambda *_: self._render())
        self.oyv.trace_add("write", lambda *_: self._render())
        self.wv.trace_add("write", lambda *_: self._render())
        self.hv.trace_add("write", lambda *_: self._render())
        self.sv.trace_add("write", lambda *_: self._render())

        self._render()

    def _page_rect(self):
        pw = self.CANVAS_W - 2 * self.PAD
        ph = self.CANVAS_H - 2 * self.PAD
        ratio = A4_H / A4_W
        if ph / pw > ratio:
            w = pw
            h = pw * ratio
        else:
            h = ph
            w = ph / ratio
        px = self.PAD + (pw - w) / 2
        py = self.PAD + (ph - h) / 2
        return px, py, w, h

    def _img_rect(self):
        px, py, pw, ph = self._page_rect()
        try:
            sw = int(self.wv.get()) * int(self.sv.get())
            sh = int(self.hv.get()) * int(self.sv.get())
            ox = int(self.oxv.get())
            oy = int(self.oyv.get())
        except ValueError:
            return 0, 0, 0, 0

        ix = px + (A4_W - sw - ox) / A4_W * pw
        iy = py + oy / A4_H * ph
        iw = sw / A4_W * pw
        ih = sh / A4_H * ph
        return ix, iy, iw, ih

    def _render(self):
        c = self.canvas
        c.delete("all")

        px, py, pw, ph = self._page_rect()
        c.create_rectangle(px, py, px + pw, py + ph, outline="#bbb", width=1, fill="white")

        ix, iy, iw, ih = self._img_rect()
        if iw > 0 and ih > 0:
            c.create_rectangle(
                ix, iy, ix + iw, iy + ih,
                fill="#2196F3", stipple="gray25",
                outline="#1565C0", width=2,
            )
            cx, cy = ix + iw / 2, iy + ih / 2
            c.create_text(cx, cy, text="IMAGEN", font=("", 8, "bold"), fill="#0D47A1")

            try:
                ox = int(self.oxv.get())
                oy = int(self.oyv.get())
            except ValueError:
                ox = oy = 0
            c.create_text(px + pw - 4, iy + ih / 2, text=f"ox={ox}", font=("", 8), fill="#333", anchor="e")
            c.create_text(ix + iw / 2, py + 4, text=f"oy={oy}", font=("", 8), fill="#333", anchor="s")

            s = 4
            for hx, hy in [(ix, iy), (ix + iw, iy), (ix, iy + ih), (ix + iw, iy + ih)]:
                c.create_rectangle(hx - s, hy - s, hx + s, hy + s, fill="#1565C0", outline="white", width=1)

        c.create_text(px + pw / 2, py + ph + 10, text="Página (A4)", font=("", 8), fill="#888")

    def _on_press(self, event):
        ix, iy, iw, ih = self._img_rect()
        tol = 12
        if (ix - tol) <= event.x <= (ix + iw + tol) and (iy - tol) <= event.y <= (iy + ih + tol):
            self._dragging = True
            try:
                self._drag_start = (event.x, event.y, int(self.oxv.get()), int(self.oyv.get()))
            except ValueError:
                self._dragging = False

    def _on_drag(self, event):
        if not self._dragging or self._drag_start is None:
            return
        px, py, pw, ph = self._page_rect()
        sx, sy, sox, soy = self._drag_start
        dx = (event.x - sx) / pw * A4_W
        dy = (event.y - sy) / ph * A4_H

        try:
            sw = int(self.wv.get()) * int(self.sv.get())
            sh = int(self.hv.get()) * int(self.sv.get())
        except ValueError:
            return

        new_ox = max(0, min(int(A4_W - sw), sox - int(dx)))
        new_oy = max(0, min(int(A4_H - sh), soy + int(dy)))
        self.oxv.set(new_ox)
        self.oyv.set(new_oy)

    def _on_release(self, event):
        self._dragging = False
        self._drag_start = None
