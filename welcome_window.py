from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from loader import load_csv_data
from resource_path import resource_path
from main_window import MainWindow

class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Window configuration
        self.setWindowTitle("EDA App")
        self.resize(500, 300)
        # Set the window icon (shows in the title bar on Windows/Linux)
        self.setWindowIcon(QIcon(resource_path("Icons/favicon-2048x2048.png")))
        # Create a central widget and set a vertical layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        # Add some spacing to center the content vertically
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        # 1. Welcome Label
        welcome_label = QLabel("Welcome to the EDA app!")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(welcome_label)
        # 2. Instruction Label
        instruction_label = QLabel("Upload the CSV file to start analysis")
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instruction_label.setStyleSheet("font-size: 16px; color: #555555;")
        layout.addWidget(instruction_label)
        # 3. Upload Button
        self.upload_button = QPushButton("Upload CSV")
        self.upload_button.setFixedSize(150, 40)
        self.upload_button.setStyleSheet("font-size: 14px; font-weight: bold;")
        # Add button to layout and center it
        layout.addWidget(self.upload_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.upload_button.clicked.connect(self.handle_file_upload)
    def handle_file_upload(self):
        # Open a file dialog, filtering strictly for .csv files
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Data File", 
            "", 
            "CSV Files (*.csv)"
        )

        # If the user cancels the dialog, file_path will be empty
        if not file_path:
            return

        # Pass the path to loader.py
        df, error_message = load_csv_data(file_path)

        if error_message:
            # Pop up an error message box if something went wrong
            QMessageBox.critical(self, "Upload Error", error_message)
        else:
            # Success! Show a temporary success message (we will replace 
            # this later with the code to open the MainWindow)
            QMessageBox.information(
                self, 
                "Success", 
                f"Data loaded successfully!\nRows: {df.shape[0]}, Columns: {df.shape[1]}"
            )
            self.main_app_window = MainWindow(df)
            
            # 2. Show the new window
            self.main_app_window.show()
            
            # 3. Close the welcome window
            self.close()
