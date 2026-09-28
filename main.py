import os
import sys
import logging

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

# Ensure project root is in sys.path
sys.path.insert(0, get_base_dir())

def setup_logging():
    log_dir = os.path.join(get_base_dir(), "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "piano_deck.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    setup_logging()
    logging.info("Starting Piano Deck — Senior Officers Executive Dashboard (PyQt6 Edition)...")
    
    try:
        from PyQt6 import QtWidgets
        from pyqt_deck import PyQtPianoDeck

        # High-DPI scaling configuration for PyQt6
        app = QtWidgets.QApplication(sys.argv)
        app.setStyle("Fusion")

        deck = PyQtPianoDeck()
        deck.show()
        deck.raise_()
        deck.activateWindow()
        sys.exit(app.exec())
    except ImportError as e:
        logging.warning(f"PyQt6 not available ({e}), falling back to Tkinter edition...")
        from piano_deck import PianoDeckBar
        app = PianoDeckBar()
        app.mainloop()
    except KeyboardInterrupt:
        logging.info("Piano Deck closed by user.")
    except Exception as e:
        logging.exception(f"Fatal error in Piano Deck: {e}")

if __name__ == "__main__":
    main()
