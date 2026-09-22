import tkinter as tk
import time
import logging

class SnippingOverlay:
    """
    Interactive fullscreen snipping overlay.
    Allows user to click and drag to select any rectangular region on the screen.
    """
    def __init__(self, parent, on_complete, on_cancel=None):
        self.parent = parent
        self.on_complete = on_complete
        self.on_cancel = on_cancel

        self.start_x = None
        self.start_y = None
        self.rect_id = None

        self.win = tk.Toplevel(parent)
        self.win.attributes("-fullscreen", True)
        self.win.attributes("-alpha", 0.28)  # Semi-transparent dark overlay
        self.win.attributes("-topmost", True)
        self.win.config(bg="#000000", cursor="cross")

        self.canvas = tk.Canvas(self.win, bg="#000000", highlightthickness=0, cursor="cross")
        self.canvas.pack(fill="both", expand=True)

        # Instructions banner at top center
        sw = self.win.winfo_screenwidth()
        self.canvas.create_rectangle(sw//2 - 180, 15, sw//2 + 180, 50, fill="#1E1F24", outline="#D4AF37", width=2)
        self.canvas.create_text(sw//2, 32, text="✂️ Click and drag to select area  •  ESC to cancel", font=("Segoe UI", 10, "bold"), fill="#FFFFFF")

        self.canvas.bind("<Button-1>", self._on_button_down)
        self.canvas.bind("<B1-Motion>", self._on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_button_up)
        self.win.bind("<Escape>", self._on_escape)

    def _on_button_down(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        # Create dashed gold rectangle
        self.rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="#FFD700", width=2)

    def _on_mouse_drag(self, event):
        if self.start_x is not None and self.rect_id:
            self.canvas.coords(self.rect_id, self.start_x, self.start_y, event.x, event.y)

    def _on_button_up(self, event):
        if self.start_x is None or self.start_y is None:
            self._on_escape()
            return

        end_x = event.x
        end_y = event.y

        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)

        # Destroy overlay first so it is not in the screenshot
        self.win.destroy()

        # Check if selection is larger than minimum threshold
        if (x2 - x1) > 10 and (y2 - y1) > 10:
            time.sleep(0.08)  # Let overlay repaint away
            if self.on_complete:
                self.on_complete((x1, y1, x2, y2))
        else:
            if self.on_cancel:
                self.on_cancel()

    def _on_escape(self, event=None):
        try:
            self.win.destroy()
        except Exception:
            pass
        if self.on_cancel:
            self.on_cancel()
