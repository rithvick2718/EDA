from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, QSizePolicy,QPushButton,QHBoxLayout)
from PySide6.QtCore import Qt

# --- Local Imports ---
from Plots.heatmap import create_correlation_heatmap
from dark_mode import is_dark

class CorrelationPage(QWidget):
    def __init__(self, df, save_callback):
        super().__init__()
        self.df = df
        self.save_callback = save_callback  # Store it so save_current_plot can use it

        self.setup_ui()
        
        # Automatically generate the heatmap as soon as the page is created
        self.generate_heatmap()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        # self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(15)

        # 4. Save to Dashboard Button
        self.save_btn = QPushButton("Save to Dashboard")
        self.save_btn.setStyleSheet("padding: 5px 15px;")
        self.save_btn.clicked.connect(self.save_current_plot)
        self.save_btn.setEnabled(False) # Disabled until a graph is made
        
        # Add to your controls_layout:
        controls_layout.addWidget(self.save_btn)
        self.layout.addLayout(controls_layout)

        # --- Header ---
        title_label = QLabel("Correlation Analysis")
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 10px;")
        self.layout.addWidget(title_label)
        
        desc_label = QLabel("Heatmap displaying the Pearson correlation coefficients between all numerical variables.")
        desc_label.setStyleSheet("font-size: 14px; margin-bottom: 15px;")
        self.layout.addWidget(desc_label)
        

        # --- Plot Canvas Area ---
        self.plot_container = QFrame()
        self.plot_container.setFrameShape(QFrame.Shape.StyledPanel)
        self.plot_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        self.plot_layout = QVBoxLayout(self.plot_container)
        self.layout.addWidget(self.plot_container)

    def generate_heatmap(self):
        """Clears the layout and directly embeds the correlation heatmap."""
        
        # 1. Clear existing plot or placeholders
        self.clear_plot_area()

        # 2. Generate the FigureCanvas
        # Note: Your Matplotlib function should ideally handle filtering out non-numerical columns
        canvas = create_correlation_heatmap(self.df, is_dark_mode=is_dark())

        # 3. Add the canvas to the layout
        if canvas:
            self.plot_layout.addWidget(canvas)
            self.current_canvas = canvas  # Track it!
            self.save_btn.setEnabled(True) # Turn on the Save button
        else:
            # Fallback if the dataset lacks numerical columns or the canvas fails to generate
            error_label = QLabel("Not enough numerical variables to generate a correlation heatmap.")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            error_label.setStyleSheet("color: red; font-size: 16px;")
            self.plot_layout.addWidget(error_label)

    def clear_plot_area(self):
        """Safely removes and deletes all widgets currently in the plot layout."""
        while self.plot_layout.count():
            child = self.plot_layout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)

    def save_current_plot(self):
        """Extracts the Matplotlib figure and sends it to the central dashboard."""
        if hasattr(self, 'current_canvas') and self.current_canvas:
            
            # Generate a title based on what the user selected
            # For Univariate:
            title = f"Heatmap" 
            # (For Bivariate, change it to f"Bivariate: {self.var1_combo.currentText()} vs {self.var2_combo.currentText()}")
            
            # Extract the actual Matplotlib Figure object
            fig = self.current_canvas.figure
            
            # Trigger the callback to main_window
            self.save_callback(title, fig)
    
    def update_data(self, new_df):
        """Refreshes the page and automatically regenerates the heatmap with the new dataset."""
        self.df = new_df
        self.save_btn.setEnabled(False)
        self.generate_heatmap()