import tkinter as tk
import threading

class ToastManager:
    """Displays non-intrusive, luxury floating notification toasts."""
    _current_toast = None

    @classmethod
    def show(cls, parent, title: str, message: str, icon: str = "✨", duration_ms: int = 3500, on_click=None):
        def _create():
            if cls._current_toast and cls._current_toast.winfo_exists():
                cls._current_toast.destroy()

            top = tk.Toplevel(parent)
            cls._current_toast = top
            top.overrideredirect(True)
            top.attributes("-topmost", True)
            top.attributes("-alpha", 0.96)
            top.config(bg="#1E1E24")

            # Border frame
            outer_frame = tk.Frame(top, bg="#D4AF37", bd=1)
            outer_frame.pack(fill="both", expand=True)

            inner_frame = tk.Frame(outer_frame, bg="#18191E", padx=16, pady=10)
            inner_frame.pack(fill="both", expand=True, padx=1, pady=1)

            # Icon
            lbl_icon = tk.Label(inner_frame, text=icon, font=("Segoe UI Emoji", 20), bg="#18191E", fg="#F5D77F")
            lbl_icon.pack(side="left", padx=(0, 12))

            # Content container
            text_frame = tk.Frame(inner_frame, bg="#18191E")
            text_frame.pack(side="left", fill="both")

            lbl_title = tk.Label(text_frame, text=title, font=("Segoe UI", 10, "bold"), bg="#18191E", fg="#FFFFFF", anchor="w")
            lbl_title.pack(anchor="w")

            hint_text = message
            if on_click:
                hint_text += "\n(Click here to open file in Explorer)"

            lbl_msg = tk.Label(text_frame, text=hint_text, font=("Segoe UI", 9), bg="#18191E", fg="#C5C7D0", anchor="w", wraplength=480, justify="left")
            lbl_msg.pack(anchor="w")

            # Position near top center of screen
            top.update_idletasks()
            w = top.winfo_reqwidth()
            h = top.winfo_reqheight()
            screen_w = top.winfo_screenwidth()
            x = (screen_w - w) // 2
            y = 45

            top.geometry(f"{w}x{h}+{x}+{y}")

            def _handle_click(e):
                top.destroy()
                if on_click:
                    try:
                        on_click()
                    except Exception:
                        pass

            # Fade out and close
            top.after(duration_ms, lambda: cls._fade_out(top))
            for widget in (top, outer_frame, inner_frame, lbl_title, lbl_msg, lbl_icon):
                widget.config(cursor="hand2" if on_click else "arrow")
                widget.bind("<Button-1>", _handle_click)

        if parent:
            parent.after(0, _create)

    @classmethod
    def _fade_out(cls, win, step=0):
        if not win or not win.winfo_exists():
            return
        try:
            cur_alpha = win.attributes("-alpha")
            if cur_alpha > 0.15:
                win.attributes("-alpha", cur_alpha - 0.15)
                win.after(30, lambda: cls._fade_out(win, step + 1))
            else:
                win.destroy()
        except Exception:
            pass
