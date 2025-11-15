"""
Table dialog for adding/editing tables
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                            QLabel, QSpinBox, QComboBox, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from backend.table_service import table_service
from config import THEME_COLORS


class TableDialog(QDialog):
    """Dialog for adding or editing tables"""
    
    def __init__(self, parent=None, table=None):
        super().__init__(parent)
        self.table = table
        self.setWindowTitle("Add Table" if not table else "Edit Table")
        self.setModal(True)
        self.setFixedSize(300, 200)
        
        self.init_ui()
        self.setup_connections()
        
        if table:
            self.load_table_data()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Create form
        form_layout = QFormLayout()
        
        # Table number field
        self.table_number_input = QSpinBox()
        self.table_number_input.setRange(1, 999)
        self.table_number_input.setValue(1)
        form_layout.addRow("Table Number:", self.table_number_input)
        
        # Capacity field
        self.capacity_input = QSpinBox()
        self.capacity_input.setRange(1, 20)
        self.capacity_input.setValue(2)
        form_layout.addRow("Capacity:", self.capacity_input)
        
        # Status field (for editing only)
        if self.table:
            self.status_combo = QComboBox()
            self.status_combo.addItems(['free', 'occupied', 'served', 'billed'])
            form_layout.addRow("Status:", self.status_combo)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Save")
        self.save_button.setFont(QFont("Arial", 10, QFont.Bold))
        self.save_button.setMinimumHeight(35)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFont(QFont("Arial", 10))
        self.cancel_button.setMinimumHeight(35)
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        
        # Set stylesheet
        self.setStyleSheet(self.get_dialog_style())
    
    def setup_connections(self):
        """Setup signal connections"""
        self.save_button.clicked.connect(self.save_table)
        self.cancel_button.clicked.connect(self.reject)
    
    def load_table_data(self):
        """Load existing table data"""
        if self.table:
            self.table_number_input.setValue(self.table['table_number'])
            self.capacity_input.setValue(self.table['capacity'])
            
            if hasattr(self, 'status_combo'):
                self.status_combo.setCurrentText(self.table['status'])
    
    def save_table(self):
        """Save table"""
        table_number = self.table_number_input.value()
        capacity = self.capacity_input.value()
        
        try:
            if self.table:
                # Update existing table
                success = table_service.update_table_capacity(self.table['id'], capacity)
                
                if hasattr(self, 'status_combo'):
                    status_success = table_service.update_table_status(
                        self.table['id'], 
                        self.status_combo.currentText()
                    )
                    success = success and status_success
                
                if success:
                    QMessageBox.information(self, "Success", "Table updated successfully!")
                    self.accept()
                else:
                    QMessageBox.critical(self, "Error", "Failed to update table.")
            else:
                # Create new table
                success = table_service.create_table(table_number, capacity)
                
                if success:
                    QMessageBox.information(self, "Success", "Table created successfully!")
                    self.accept()
                else:
                    QMessageBox.critical(self, "Error", "Failed to create table. Table number may already exist.")
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{str(e)}")
    
    def get_dialog_style(self):
        """Get dialog stylesheet"""
        return f"""
        QDialog {{
            background-color: {THEME_COLORS['light']};
        }}
        
        QSpinBox, QComboBox {{
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 8px;
            background-color: white;
        }}
        
        QSpinBox:focus, QComboBox:focus {{
            border-color: {THEME_COLORS['primary']};
        }}
        
        QPushButton {{
            background-color: {THEME_COLORS['primary']};
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }}
        
        QPushButton:hover {{
            background-color: {THEME_COLORS['secondary']};
        }}
        
        QPushButton:pressed {{
            background-color: {THEME_COLORS['dark']};
        }}
        
        QLabel {{
            color: {THEME_COLORS['dark']};
            font-weight: bold;
        }}
        """
