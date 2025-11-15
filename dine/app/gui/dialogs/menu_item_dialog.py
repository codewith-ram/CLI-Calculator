"""
Menu item dialog for adding/editing menu items
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                            QLabel, QLineEdit, QTextEdit, QDoubleSpinBox,
                            QComboBox, QCheckBox, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from backend.menu_service import menu_service
from config import THEME_COLORS, MENU_CATEGORIES
from utils.validators import validators


class MenuItemDialog(QDialog):
    """Dialog for adding or editing menu items"""
    
    def __init__(self, parent=None, menu_item=None):
        super().__init__(parent)
        self.menu_item = menu_item
        self.setWindowTitle("Add Menu Item" if not menu_item else "Edit Menu Item")
        self.setModal(True)
        self.setFixedSize(400, 300)
        
        self.init_ui()
        self.setup_connections()
        
        if menu_item:
            self.load_menu_item_data()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Create form
        form_layout = QFormLayout()
        
        # Name field
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter item name")
        self.name_input.setMaxLength(100)
        form_layout.addRow("Name:", self.name_input)
        
        # Description field
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Enter item description")
        self.description_input.setMaximumHeight(60)
        form_layout.addRow("Description:", self.description_input)
        
        # Price field
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0.01, 999.99)
        self.price_input.setDecimals(2)
        self.price_input.setPrefix("$")
        self.price_input.setValue(0.01)
        form_layout.addRow("Price:", self.price_input)
        
        # Category field
        self.category_combo = QComboBox()
        self.category_combo.addItems([cat.replace('_', ' ').title() for cat in MENU_CATEGORIES])
        form_layout.addRow("Category:", self.category_combo)
        
        # Available checkbox
        self.available_checkbox = QCheckBox("Available")
        self.available_checkbox.setChecked(True)
        form_layout.addRow("", self.available_checkbox)
        
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
        self.save_button.clicked.connect(self.save_menu_item)
        self.cancel_button.clicked.connect(self.reject)
    
    def load_menu_item_data(self):
        """Load existing menu item data"""
        if self.menu_item:
            self.name_input.setText(self.menu_item['name'])
            self.description_input.setText(self.menu_item['description'] or '')
            self.price_input.setValue(self.menu_item['price'])
            
            # Set category
            category_index = MENU_CATEGORIES.index(self.menu_item['category'])
            self.category_combo.setCurrentIndex(category_index)
            
            self.available_checkbox.setChecked(self.menu_item['is_available'])
    
    def save_menu_item(self):
        """Save menu item"""
        # Validate input
        name = self.name_input.text().strip()
        description = self.description_input.toPlainText().strip()
        price = self.price_input.value()
        category = MENU_CATEGORIES[self.category_combo.currentIndex()]
        is_available = self.available_checkbox.isChecked()
        
        if not name:
            QMessageBox.warning(self, "Validation Error", "Please enter a name for the menu item.")
            self.name_input.setFocus()
            return
        
        if price <= 0:
            QMessageBox.warning(self, "Validation Error", "Please enter a valid price.")
            self.price_input.setFocus()
            return
        
        try:
            if self.menu_item:
                # Update existing item
                success = menu_service.update_menu_item(
                    self.menu_item['id'],
                    name=name,
                    description=description,
                    price=price,
                    category=category,
                    is_available=is_available
                )
                
                if success:
                    QMessageBox.information(self, "Success", "Menu item updated successfully!")
                    self.accept()
                else:
                    QMessageBox.critical(self, "Error", "Failed to update menu item.")
            else:
                # Create new item
                success = menu_service.create_menu_item(
                    name=name,
                    description=description,
                    price=price,
                    category=category,
                    is_available=is_available
                )
                
                if success:
                    QMessageBox.information(self, "Success", "Menu item created successfully!")
                    self.accept()
                else:
                    QMessageBox.critical(self, "Error", "Failed to create menu item.")
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{str(e)}")
    
    def get_dialog_style(self):
        """Get dialog stylesheet"""
        return f"""
        QDialog {{
            background-color: {THEME_COLORS['light']};
        }}
        
        QLineEdit, QTextEdit, QDoubleSpinBox, QComboBox {{
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 8px;
            background-color: white;
        }}
        
        QLineEdit:focus, QTextEdit:focus, QDoubleSpinBox:focus, QComboBox:focus {{
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
        
        QCheckBox {{
            color: {THEME_COLORS['dark']};
        }}
        
        QLabel {{
            color: {THEME_COLORS['dark']};
            font-weight: bold;
        }}
        """
