
import sys
import os
import customtkinter

# Add the project root to the Python path to resolve local imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now we can safely import from other modules
from utils.logger import setup_logging
from ui.main_window import MainWindow

def main():
    customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "dark-blue", "green"

    # Initialize logging
    setup_logging()
    
    # Start the application
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
