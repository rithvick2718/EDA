import sys
from PySide6.QtWidgets import (QApplication)
from UI.welcome_window import WelcomeWindow
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WelcomeWindow()
    window.show()
    sys.exit(app.exec())