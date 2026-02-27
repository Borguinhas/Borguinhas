
import sys
import os
import customtkinter
from utils.logger import setup_logging

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ui.main_window import MainWindow

def main():
    customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "dark-blue", "green"

    setup_logging()
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
