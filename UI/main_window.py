from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, 
                               QScrollArea, QFrame, QSplitter, QToolBar, QFileDialog, 
                               QMessageBox, QApplication, QMenuBar, QStackedWidget)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction

# --- Local Imports ---
from profiler import profile_dataset
from loader import load_csv_data
from resource_path import resource_path

# --- Page Imports ---
from UI.Pages.home import HomePage
from UI.Pages.univariate_page import UnivariatePage
from UI.Pages.bivariate_page import BivariatePage
from UI.Pages.correlation import CorrelationPage


class MainWindow(QMainWindow):
    def __init__(self, df):
        super().__init__()
        self.df = df
        
        # Master list to hold saved plots for the dashboard
        self.saved_plots = [] 
        
        self.setWindowTitle("EDA App - Analysis Dashboard")
        self.resize(1000, 650)
        self.setWindowIcon(QIcon(resource_path("Icons/favicon-2048x2048.png")))

        # --- Menu Bar Setup ---

        # Sidebar toggle action
        self.toggle_action = QAction("Sidebar", self)
        self.toggle_action.triggered.connect(self.toggle_sidebar)
        self.toggle_action.setShortcut("Ctrl+`") 

        # Upload CSV action
        self.upload_action = QAction("Upload CSV", self)
        self.upload_action.triggered.connect(self.upload_new_csv)
        self.upload_action.setShortcut("Ctrl+N") 

        menubar = self.menuBar()

        file_menu = menubar.addMenu("&File")
        view_menu = menubar.addMenu("&View")

        # Add actions to menus
        file_menu.addAction(self.upload_action)
        view_menu.addAction(self.toggle_action)

        # --- Main Layout (Splitter) ---
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(self.splitter)

        # --- Left Sidebar ---

        self.left_scroll = QScrollArea()
        self.left_scroll.setWidgetResizable(True)
        self.left_scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.left_widget = QWidget()
        self.left_layout = QVBoxLayout(self.left_widget)
        self.left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Sidebar spacing and margins
        self.left_layout.setSpacing(10) 
        self.left_layout.setContentsMargins(10, 10, 10, 10) 

        # Base style for headings
        heading_css = "font-size: 14px; font-weight: bold; padding-bottom: 2px;"

        # Navigation Buttons
        nav_label = QLabel("Analysis Tools")
        nav_label.setStyleSheet(heading_css)
        self.left_layout.addWidget(nav_label)

        self.btn_home = QPushButton("Dashboard (Home)")
        self.btn_univariate = QPushButton("Univariate Analysis")
        self.btn_bivariate = QPushButton("Bivariate Analysis")
        self.btn_correlation = QPushButton("Correlation Analysis")

        for btn in [self.btn_home, self.btn_univariate, self.btn_bivariate, self.btn_correlation]:
            self.left_layout.addWidget(btn)

        # Dataset Summary
        summary_label = QLabel("Dataset Summary")
        summary_label.setStyleSheet(heading_css)
        summary_label.setContentsMargins(0, 10, 0, 0) 
        self.left_layout.addWidget(summary_label)

        self.stats_display = QLabel("")
        self.stats_display.setStyleSheet("font-size: 12px;")
        self.left_layout.addWidget(self.stats_display)

        # Dataset Columns List
        cols_label = QLabel("Dataset Columns")
        cols_label.setStyleSheet(heading_css)
        cols_label.setContentsMargins(0, 10, 0, 0)
        self.left_layout.addWidget(cols_label)

        self.cols_display = QLabel("")
        self.cols_display.setStyleSheet("font-size: 12px;")
        self.cols_display.setWordWrap(True)
        self.left_layout.addWidget(self.cols_display)

        self.left_scroll.setWidget(self.left_widget)

        # --- Right Canvas (Stacked Widget) ---

        self.right_scroll = QScrollArea()
        self.right_scroll.setWidgetResizable(True)
        self.right_scroll.setFrameShape(QFrame.Shape.NoFrame)

        # Create the Stacked Widget container
        self.stacked_widget = QStackedWidget()
        
        # Instantiate your Pages (Passing the dataset and the save callback)
        self.home_page = HomePage(self.saved_plots)
        self.univariate_page = UnivariatePage(self.df, self.add_plot_to_dashboard)
        self.bivariate_page = BivariatePage(self.df, self.add_plot_to_dashboard)
        self.correlation_page = CorrelationPage(self.df, self.add_plot_to_dashboard)

        # Add pages to the Stacked Widget
        self.stacked_widget.addWidget(self.home_page)         # Index 0
        self.stacked_widget.addWidget(self.univariate_page)   # Index 1
        self.stacked_widget.addWidget(self.bivariate_page)    # Index 2
        self.stacked_widget.addWidget(self.correlation_page)  # Index 3

        # Connect Sidebar Buttons to Switch Pages
        self.btn_home.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.home_page))
        self.btn_univariate.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.univariate_page))
        self.btn_bivariate.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.bivariate_page))
        self.btn_correlation.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.correlation_page))

        self.right_scroll.setWidget(self.stacked_widget)

        # Assemble the splitter
        self.splitter.addWidget(self.left_scroll)
        self.splitter.addWidget(self.right_scroll)
        
        # Set initial width ratio (sidebar vs canvas)
        self.splitter.setSizes([200, 800])

        self.refresh_sidebar_data()

    # --- Logic Methods ---

    def toggle_sidebar(self):
        is_visible = self.left_scroll.isVisible()
        self.left_scroll.setVisible(not is_visible)

    def upload_new_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select New Data File", "", "CSV Files (*.csv)")
        if not file_path:
            return

        new_df, error_message = load_csv_data(file_path)

        if error_message:
            QMessageBox.critical(self, "Upload Error", error_message)
        else:
            self.df = new_df
            self.refresh_sidebar_data()
            self.univariate_page.update_data(new_df)
            self.bivariate_page.update_data(new_df)
            self.correlation_page.update_data(new_df)
            QMessageBox.information(self, "Success", "New dataset loaded successfully!\nNote: You may need to restart the app to apply this to all pages.")

    def refresh_sidebar_data(self):
        total_rows = len(self.df)
        total_cols = len(self.df.columns)
        total_missing = self.df.isna().sum().sum()
        memory_mb = self.df.memory_usage(deep=True).sum() / (1024 * 1024)

        stats_text = (
            f"<b>Rows:</b> {total_rows:,}<br><br>"
            f"<b>Columns:</b> {total_cols:,}<br><br>"
            f"<b>Missing:</b> {total_missing:,}<br><br>"
            f"<b>Memory:</b> {memory_mb:.2f} MB"
        )
        self.stats_display.setText(stats_text)

        profile_data = profile_dataset(self.df)
        cols_text = ""
        for idx, (col_name, info) in enumerate(profile_data.items(), start=1):
            cols_text += f"<b>{idx}. {col_name}</b> <i>({info['type']})</i><br><br>"

        self.cols_display.setText(cols_text)

    def add_plot_to_dashboard(self, title, figure):
        """Callback passed to analysis pages to save graphs to the Home dashboard."""
        self.saved_plots.append({
            'title': title,
            'figure': figure
        })
        # Tell the home page to redraw itself with the newly saved graph
        self.home_page.refresh_dashboard()
        QMessageBox.information(self, "Saved", f"'{title}' added to Dashboard!")