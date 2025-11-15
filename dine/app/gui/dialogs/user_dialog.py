"""
User dialog for adding/editing users
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                            QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from backend.auth_service import auth_service
from config import THEME_COLORS, USER_ROLES
from utils.validators import validators


class UserDialog(QDialog):
    """Dialog for adding or editing users"""
    
    def __init__(self, parent=None, user=None):
        super().__init__(parent)
        self.user = user
        self.setWindowTitle("Add User" if not user else "Edit User")
        self.setModal(True)
        self.setFixedSize(400, 300)
        
        self.init_ui()
        self.setup_connections()
        
        if user:
            self.load_user_data()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Create form
        form_layout = QFormLayout()
        
        # Username field
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setMaxLength(50)
        form_layout.addRow("Username:", self.username_input)
        
        # Password field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMaxLength(100)
        form_layout.addRow("Password:", self.password_input)
        
        # Full name field
        self.full_name_input = QLineEdit()
        self.full_name_input.setPlaceholderText("Enter full name")
        self.full_name_input.setMaxLength(100)
        form_layout.addRow("Full Name:", self.full_name_input)
        
        # Email field
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email address")
        self.email_input.setMaxLength(100)
        form_layout.addRow("Email:", self.email_input)
        
        # Role field
        self.role_combo = QComboBox()
        self.role_combo.addItems([role.title() for role in USER_ROLES.keys()])
        form_layout.addRow("Role:", self.role_combo)
        
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
        self.save_button.clicked.connect(self.save_user)
        self.cancel_button.clicked.connect(self.reject)
    
    def load_user_data(self):
        """Load existing user data"""
        if self.user:
            self.username_input.setText(self.user['username'])
            self.username_input.setReadOnly(True)  # Don't allow username changes
            self.password_input.setPlaceholderText("Leave blank to keep current password")
            self.full_name_input.setText(self.user['full_name'])
            self.email_input.setText(self.user['email'] or '')
            
            # Set role
            role_index = list(USER_ROLES.keys()).index(self.user['role'])
            self.role_combo.setCurrentIndex(role_index)
    
    def save_user(self):
        """Save user"""
        # Validate input
        username = self.username_input.text().strip()
        password = self.password_input.text()
        full_name = self.full_name_input.text().strip()
        email = self.email_input.text().strip()
        role = list(USER_ROLES.keys())[self.role_combo.currentIndex()]
        
        if not username:
            QMessageBox.warning(self, "Validation Error", "Please enter a username.")
            self.username_input.setFocus()
            return
        
        if not full_name:
            QMessageBox.warning(self, "Validation Error", "Please enter a full name.")
            self.full_name_input.setFocus()
            return
        
        if not self.user and not password:
            QMessageBox.warning(self, "Validation Error", "Please enter a password for new users.")
            self.password_input.setFocus()
            return
        
        # Validate username format
        if not validators.is_valid_username(username):
            QMessageBox.warning(self, "Validation Error", 
                              "Username must be 3-20 characters, alphanumeric and underscore only.")
            self.username_input.setFocus()
            return
        
        # Validate password (only for new users or if password is provided)
        if password and not validators.is_valid_password(password):
            QMessageBox.warning(self, "Validation Error", 
                              "Password must be at least 6 characters with letters and numbers.")
            self.password_input.setFocus()
            return
        
        # Validate email if provided
        if email and not validators.is_valid_email(email):
            QMessageBox.warning(self, "Validation Error", "Please enter a valid email address.")
            self.email_input.setFocus()
            return
        
        try:
            if self.user:
                # Update existing user
                update_data = {
                    'full_name': full_name,
                    'email': email,
                    'role': role
                }
                
                if password:
                    update_data['password'] = password
                
                success = auth_service.update_user(self.user['id'], **update_data)
                
                if success:
                    QMessageBox.information(self, "Success", "User updated successfully!")
                    self.accept()
                else:
                    QMessageBox.critical(self, "Error", "Failed to update user.")
            else:
                # Create new user
                success = auth_service.create_user(
                    username=username,
                    password=password,
                    role=role,
                    full_name=full_name,
                    email=email
                )
                
                if success:
                    QMessageBox.information(self, "Success", "User created successfully!")
                    self.accept()
                else:
                    QMessageBox.critical(self, "Error", "Failed to create user. Username may already exist.")
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{str(e)}")
    
    def get_dialog_style(self):
        """Get dialog stylesheet"""
        return f"""
        QDialog {{
            background-color: {THEME_COLORS['light']};
        }}
        
        QLineEdit, QComboBox {{
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 8px;
            background-color: white;
        }}
        
        QLineEdit:focus, QComboBox:focus {{
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
