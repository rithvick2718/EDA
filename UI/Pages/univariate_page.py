from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QComboBox, QPushButton, QFrame, QSizePolicy)
from PySide6.QtCore import Qt

from profiler import profile_dataset
from Plots.histogram import create_histogram 
from Plots.barplot import create_bar_plot
from Plots.piechart import create_pie_chart
from dark_mode import is_dark

class UnivariatePage(QWidget):
    def __init__(self, df,save_callback ):
        super().__init__()
        self.df = df
        self.save_callback = save_callback  # Store it so save_current_plot can use it

        # Profile the dataset to get column types (Categorical vs Numerical)
        # Assuming profile_dataset returns a dict like: 
        # {'col1': {'type': 'Numerical'}, 'col2': {'type': 'Categorical'}}
        self.profile = profile_dataset(self.df)
        
        self.setup_ui()
        self.on_variable_changed()  # Trigger initial state of the dropdowns

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        # self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # --- Header ---
        title_label = QLabel("Univariate Analysis")
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 10px;")
        self.layout.addWidget(title_label)

        # --- Controls Area ---
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(15)
        
        # 1. Variable Selection Dropdown
        self.var_combo = QComboBox()
        self.var_combo.addItems(list(self.df.columns))
        self.var_combo.setMinimumWidth(200)
        self.var_combo.currentIndexChanged.connect(self.on_variable_changed)
        
        # 2. Plot Type Selection Dropdown (Hidden by default)
        self.plot_type_combo = QComboBox()
        self.plot_type_combo.addItems(["Bar Plot", "Pie Chart"])
        self.plot_type_combo.setMinimumWidth(150)
        self.plot_type_combo.hide()

        # 3. Make Graph Button
        self.generate_btn = QPushButton("Make Graph")
        self.generate_btn.setStyleSheet("font-weight: bold; padding: 5px 15px;")
        self.generate_btn.clicked.connect(self.generate_graph)

        # 4. Save to Dashboard Button
        self.save_btn = QPushButton("Save to Dashboard")
        self.save_btn.setStyleSheet("padding: 5px 15px;")
        self.save_btn.clicked.connect(self.save_current_plot)
        self.save_btn.setEnabled(False) # Disabled until a graph is made
        
        # Assemble Controls
        controls_layout.addWidget(QLabel("<b>Select Variable:</b>"))
        controls_layout.addWidget(self.var_combo)
        controls_layout.addWidget(self.plot_type_combo)
        controls_layout.addWidget(self.generate_btn)
        controls_layout.addWidget(self.save_btn)
        controls_layout.addStretch()  # Pushes everything to the left

        self.layout.addLayout(controls_layout)

        # --- Plot Canvas Area ---
        self.plot_container = QFrame()
        self.plot_container.setFrameShape(QFrame.Shape.StyledPanel)
        self.plot_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        self.plot_layout = QVBoxLayout(self.plot_container)
        
        # Initial Placeholder Text
        self.placeholder = QLabel("Select a variable and click 'Make Graph' to view the distribution.")
        self.placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.placeholder.setStyleSheet("color: gray; font-size: 16px;")
        self.plot_layout.addWidget(self.placeholder)

        self.layout.addWidget(self.plot_container)
        
    def on_variable_changed(self):
        """Dynamically adjust UI based on whether the selected column is Numerical or Categorical."""
        selected_col = self.var_combo.currentText()
        col_info = self.profile.get(selected_col, {})
        
        # Default to Numerical if undefined
        col_type = col_info.get('type', 'Numerical').lower()

        if col_type == 'categorical' or col_type == 'object':
            self.plot_type_combo.show()
        else:
            self.plot_type_combo.hide()

    def generate_graph(self):
        """Clears the old plot and embeds a new FigureCanvas based on selections."""
        selected_col = self.var_combo.currentText()
        col_info = self.profile.get(selected_col, {})
        col_type = col_info.get('type', 'Numerical').lower()

        # 1. Clear existing plot or placeholder
        self.clear_plot_area()

        # 2. Generate the new FigureCanvas
        canvas = None
        if col_type == 'numerical':
            canvas = create_histogram(self.df, selected_col, is_dark_mode=is_dark())
            
        elif col_type == 'categorical' or col_type == 'object':
            plot_type = self.plot_type_combo.currentText()
            if plot_type == "Bar Plot":
                canvas = create_bar_plot(self.df, selected_col,is_dark_mode=is_dark())
            elif plot_type == "Pie Chart":
                canvas = create_pie_chart(self.df, selected_col,is_dark_mode=is_dark())

        # 3. Add the canvas to the layout
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
            title = f"Univariate: {self.var_combo.currentText()}" 
            # (For Bivariate, change it to f"Bivariate: {self.var1_combo.currentText()} vs {self.var2_combo.currentText()}")
            
            # Extract the actual Matplotlib Figure object
            fig = self.current_canvas.figure
            
            # Trigger the callback to main_window
            self.save_callback(title, fig)
    def update_data(self, new_df):
        """Refreshes the page with a newly uploaded dataset."""
        self.df = new_df
        self.profile = profile_dataset(self.df)
        
        # Update dropdowns safely
        self.var_combo.blockSignals(True)
        self.var_combo.clear()
        self.var_combo.addItems(list(self.df.columns))
        self.var_combo.blockSignals(False)
        
        # Reset the UI state
        self.clear_plot_area()
        self.on_variable_changed()
        self.save_btn.setEnabled(False)

        # Restore the placeholder text
        self.placeholder = QLabel("Select a variable and click 'Make Graph' to view the distribution.")
        self.placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.placeholder.setStyleSheet("color: gray; font-size: 16px;")
        self.plot_layout.addWidget(self.placeholder)