from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QComboBox, QPushButton, QFrame, 
                               QSizePolicy, QMessageBox)
from PySide6.QtCore import Qt

# --- Local Imports ---
from profiler import profile_dataset
from Plots.scatter import create_scatter_plot
from Plots.catplot import create_cat_v_num, create_cat_v_cat
from dark_mode import is_dark

class BivariatePage(QWidget):
    def __init__(self, df, save_callback):
        super().__init__()
        self.df = df
        self.save_callback = save_callback  # Store it so save_current_plot can use it
        # Profile the dataset to get column types
        self.profile = profile_dataset(self.df)
        
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        # self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # --- Header ---
        title_label = QLabel("Bivariate Analysis")
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 10px;")
        self.layout.addWidget(title_label)

        # --- Controls Area ---
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(15)
        
        # 1. Variable 1 Dropdown
        self.var1_combo = QComboBox()
        self.var1_combo.addItems(list(self.df.columns))
        self.var1_combo.setMinimumWidth(150)
        
        # 2. Variable 2 Dropdown
        self.var2_combo = QComboBox()
        self.var2_combo.addItems(list(self.df.columns))
        self.var2_combo.setMinimumWidth(150)
        
        # Optional: Set the second combo to the second column by default if possible
        if len(self.df.columns) > 1:
            self.var2_combo.setCurrentIndex(1)

        # 3. Make Graph Button
        self.generate_btn = QPushButton("Make Graph")
        self.generate_btn.setStyleSheet("font-weight: bold; padding: 5px 15px;")
        self.generate_btn.clicked.connect(self.generate_graph)

        # 4. Save to Dashboard Button
        self.save_btn = QPushButton("Save to Dashboard")
        self.save_btn.setStyleSheet("padding: 5px 15px;")
        self.save_btn.clicked.connect(self.save_current_plot)
        self.save_btn.setEnabled(False) # Disabled until a graph is made
        
        # Add to your controls_layout:

        # Assemble Controls
        controls_layout.addWidget(QLabel("<b>Variable 1:</b>"))
        controls_layout.addWidget(self.var1_combo)
        controls_layout.addWidget(QLabel("<b>Variable 2:</b>"))
        controls_layout.addWidget(self.var2_combo)
        controls_layout.addWidget(self.generate_btn)
        controls_layout.addWidget(self.save_btn)
        controls_layout.addStretch()

        self.layout.addLayout(controls_layout)

        # --- Plot Canvas Area ---
        self.plot_container = QFrame()
        self.plot_container.setFrameShape(QFrame.Shape.StyledPanel)
        self.plot_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        self.plot_layout = QVBoxLayout(self.plot_container)
        
        # Initial Placeholder Text
        self.placeholder = QLabel("Select two variables and click 'Make Graph' to view their relationship.")
        self.placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.placeholder.setStyleSheet("color: gray; font-size: 16px;")
        self.plot_layout.addWidget(self.placeholder)

        self.layout.addWidget(self.plot_container)

    def generate_graph(self):
        """Clears the old plot, determines variable types, and generates the correct bivariate plot."""
        var1 = self.var1_combo.currentText()
        var2 = self.var2_combo.currentText()

        # Safety check: Prevent plotting a variable against itself
        if var1 == var2:
            QMessageBox.warning(self, "Invalid Selection", "Please select two different variables for bivariate analysis.")
            return

        # 1. Clear existing plot or placeholder
        self.clear_plot_area()

        # 2. Determine types of Var 1 and Var 2
        col1_info = self.profile.get(var1, {})
        col2_info = self.profile.get(var2, {})
        
        col1_type = col1_info.get('type', 'Numerical').lower()
        col2_type = col2_info.get('type', 'Numerical').lower()

        is_cat1 = col1_type in ['categorical', 'object']
        is_cat2 = col2_type in ['categorical', 'object']

        # 3. Route to the correct plotting function
        canvas = None
        
        if not is_cat1 and not is_cat2:
            # Both are Numerical
            canvas = create_scatter_plot(self.df, var1, var2, is_dark_mode=is_dark())
            
        elif is_cat1 and is_cat2:
            # Both are Categorical
            canvas = create_cat_v_cat(self.df, var1, var2, is_dark_mode=is_dark())
            
        else:
            # One is Categorical, One is Numerical
            # Note: Your create_cat_v_num function will receive var1 and var2 in the order selected.
            # You may want to handle which axis gets the Categorical data inside that Matplotlib function.
            canvas = create_cat_v_num(self.df, var1, var2, is_dark_mode=is_dark())

        # 4. Add the canvas to the layout
        if canvas:
            self.plot_layout.addWidget(canvas)
            self.current_canvas = canvas  # Track it!
            self.save_btn.setEnabled(True) # Turn on the Save button

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
            title = f"Bivariate: {self.var1_combo.currentText()} vs {self.var2_combo.currentText()}" 
            # (For Bivariate, change it to f"Bivariate: {self.var1_combo.currentText()} vs {self.var2_combo.currentText()}")
            
            # Extract the actual Matplotlib Figure object
            fig = self.current_canvas.figure
            
            # Trigger the callback to main_window
            self.save_callback(title, fig)
    
    def update_data(self, new_df):
        """Refreshes the page with a newly uploaded dataset."""
        self.df = new_df
        self.profile = profile_dataset(self.df)
        
        # Update Dropdown 1
        self.var1_combo.blockSignals(True)
        self.var1_combo.clear()
        self.var1_combo.addItems(list(self.df.columns))
        self.var1_combo.blockSignals(False)
        
        # Update Dropdown 2
        self.var2_combo.blockSignals(True)
        self.var2_combo.clear()
        self.var2_combo.addItems(list(self.df.columns))
        if len(self.df.columns) > 1:
            self.var2_combo.setCurrentIndex(1)
        self.var2_combo.blockSignals(False)
        
        # Reset the UI state
        self.clear_plot_area()
        self.save_btn.setEnabled(False)

        # Restore the placeholder text
        self.placeholder = QLabel("Select two variables and click 'Make Graph' to view their relationship.")
        self.placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.placeholder.setStyleSheet("color: gray; font-size: 16px;")
        self.plot_layout.addWidget(self.placeholder)