import sys
from PySide6.QtWidgets import (QApplication)
from welcome_window import WelcomeWindow

if __name__ == "__main__":
    # 1. Create the application instance
    app = QApplication(sys.argv)
    # 2. Instantiate your WelcomeWindow
    window = WelcomeWindow()
    # 3. Show the window
    window.show()
    # 4. Start the application's event loop
    sys.exit(app.exec())