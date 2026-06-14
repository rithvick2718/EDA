import io
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QLabel, 
                               QPushButton, QScrollArea, QFrame, QHBoxLayout, 
                               QFileDialog, QMessageBox, QSizePolicy)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage

class HomePage(QWidget):
    def __init__(self, saved_plots):
        super().__init__()
        # Reference to the central list of saved plots from main_window
        self.saved_plots = saved_plots 
        
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # --- Header ---
        title_label = QLabel("Dashboard Gallery")
        title_label.setStyleSheet("font-size: 26px; font-weight: bold; margin-bottom: 5px;")
        self.layout.addWidget(title_label)
        
        desc_label = QLabel("Review, export, or remove your saved graphs.")
        desc_label.setStyleSheet("font-size: 14px; margin-bottom: 15px; color: gray;")
        self.layout.addWidget(desc_label)

        # --- Scrollable Gallery Area ---
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        self.gallery_widget = QWidget()
        self.gallery_layout = QGridLayout(self.gallery_widget)
        self.gallery_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.gallery_layout.setSpacing(20)

        self.scroll_area.setWidget(self.gallery_widget)
        self.layout.addWidget(self.scroll_area)

        self.refresh_dashboard()

    def refresh_dashboard(self):
        """Clears the gallery and rebuilds it based on the saved_plots list."""
        
        # 1. Clear existing widgets in the grid
        while self.gallery_layout.count():
            child = self.gallery_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # 2. Show empty state if no plots exist
        if not self.saved_plots:
            empty_label = QLabel("Your dashboard is empty.\nSave graphs from the analysis pages to see them here.")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setStyleSheet("font-size: 16px; color: gray;")
            self.gallery_layout.addWidget(empty_label, 0, 0)
            return

        # 3. Populate the grid (2 columns wide)
        row = 0
        col = 0
        for plot_data in self.saved_plots:
            card = self.create_plot_card(plot_data)
            self.gallery_layout.addWidget(card, row, col)
            
            col += 1
            if col > 1:  # Switch to next row after 2 columns
                col = 0
                row += 1

    def create_plot_card(self, plot_data):
        """Creates a UI card containing the thumbnail and action buttons."""
        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setStyleSheet("QFrame { border: 1px solid #444; border-radius: 8px; padding: 10px; }")
        
        card_layout = QVBoxLayout(card)
        
        # Title
        title_lbl = QLabel(f"<b>{plot_data['title']}</b>")
        title_lbl.setStyleSheet("border: none; font-size: 14px;")
        card_layout.addWidget(title_lbl)

        # Thumbnail (Render Matplotlib Figure to QPixmap safely)
        fig = plot_data['figure']
        buf = io.BytesIO()
        # Save figure to buffer as PNG to use as an image thumbnail
        fig.savefig(buf, format='png', bbox_inches='tight', dpi=500)
        buf.seek(0)
        
        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())
        
        img_label = QLabel()
        img_label.setPixmap(pixmap.scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img_label.setStyleSheet("border: none;")
        card_layout.addWidget(img_label)

        # Buttons (Export & Remove)
        btn_layout = QHBoxLayout()
        
        export_btn = QPushButton("Export (PNG/SVG)")
        export_btn.setStyleSheet("padding: 5px;")
        export_btn.clicked.connect(lambda _, p=plot_data: self.export_plot(p))
        
        remove_btn = QPushButton("Remove")
        remove_btn.setStyleSheet("padding: 5px; color: #ff4c4c;")
        remove_btn.clicked.connect(lambda _, p=plot_data: self.remove_plot(p))
        
        btn_layout.addWidget(export_btn)
        btn_layout.addWidget(remove_btn)
        
        card_layout.addLayout(btn_layout)
        return card

    def export_plot(self, plot_data):
        """Saves the high-resolution Matplotlib figure to the user's drive."""
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self, "Export Graph", plot_data['title'], 
            "PNG Image (*.png);;SVG Image (*.svg)"
        )
        
        if file_path:
            try:
                fig = plot_data['figure']
                # Determine format based on user selection
                ext = 'svg' if 'SVG' in selected_filter else 'png'
                fig.savefig(file_path, format=ext, bbox_inches='tight', dpi=500)
                QMessageBox.information(self, "Success", f"Graph exported successfully to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Failed to export graph:\n{str(e)}")

    def remove_plot(self, plot_data):
        """Removes a plot from the central list and refreshes the UI."""
        if plot_data in self.saved_plots:
            self.saved_plots.remove(plot_data)
            self.refresh_dashboard()