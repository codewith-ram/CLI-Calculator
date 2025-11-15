"""
Login window for SmartDine Desktop Edition
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QFormLayout, QFrame,
                            QMessageBox, QComboBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QPalette, QColor

from backend.auth_service import auth_service
from config import THEME_COLORS, APP_NAME
from utils.logger import logger


class LoginWindow(QDialog):
    """Login dialog window"""
    
    # Signals
    login_successful = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Login - {APP_NAME}")
        self.setFixedSize(400, 300)
        self.setModal(True)
        
        self.init_ui()
        self.setup_connections()
    
    def init_ui(self):
        """Initialize the user interface"""
        # Set window properties
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        
        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Create header
        self.create_header(main_layout)
        
        # Create login form
        self.create_login_form(main_layout)
        
        # Create buttons
        self.create_buttons(main_layout)
        
        # Set stylesheet
        self.setStyleSheet(self.get_login_style())
    
    def create_header(self, layout):
        """Create header section"""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.StyledPanel)
        header_layout = QVBoxLayout(header_frame)
        
        # App title
        title_label = QLabel(APP_NAME)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet(f"color: {THEME_COLORS['primary']}; margin: 10px;")
        
        # Subtitle
        subtitle_label = QLabel("Restaurant Management System")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setFont(QFont("Arial", 10))
        subtitle_label.setStyleSheet(f"color: {THEME_COLORS['dark']}; margin-bottom: 10px;")
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        
        layout.addWidget(header_frame)
    
    def create_login_form(self, layout):
        """Create login form"""
        form_frame = QFrame()
        form_frame.setFrameStyle(QFrame.StyledPanel)
        form_layout = QFormLayout(form_frame)
        form_layout.setSpacing(15)
        
        # Username field
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setFont(QFont("Arial", 10))
        form_layout.addRow("Username:", self.username_input)
        
        # Password field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("Arial", 10))
        form_layout.addRow("Password:", self.password_input)
        
        # Role selection (for demo purposes)
        self.role_combo = QComboBox()
        self.role_combo.addItems(['admin', 'waiter', 'chef', 'cashier'])
        self.role_combo.setCurrentText('admin')
        form_layout.addRow("Role:", self.role_combo)
        
        layout.addWidget(form_frame)
    
    def create_buttons(self, layout):
        """Create button section"""
        button_layout = QHBoxLayout()
        
        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setFont(QFont("Arial", 10, QFont.Bold))
        self.login_button.setMinimumHeight(40)
        
        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFont(QFont("Arial", 10))
        self.cancel_button.setMinimumHeight(40)
        
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
    
    def setup_connections(self):
        """Setup signal connections"""
        self.login_button.clicked.connect(self.handle_login)
        self.cancel_button.clicked.connect(self.reject)
        
        # Enter key handling
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)
    
    def handle_login(self):
        """Handle login attempt"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Login Error", "Please enter both username and password.")
            return
        
        try:
            # Attempt authentication
            user_data = auth_service.authenticate_user(username, password)
            
            if user_data:
                logger.info(f"User {username} logged in successfully")
                self.login_successful.emit(user_data)
                self.accept()
            else:
                QMessageBox.warning(
                    self, 
                    "Login Failed", 
                    "Invalid username or password. Please try again."
                )
                self.password_input.clear()
                self.password_input.setFocus()
                
        except Exception as e:
            logger.error(f"Login error: {e}")
            QMessageBox.critical(
                self,
                "Login Error",
                f"An error occurred during login:\n{str(e)}"
            )
    
    def get_login_style(self):
        """Get login window stylesheet"""
        return f"""
        QDialog {{
            background-color: {THEME_COLORS['light']};
        }}
        
        QFrame {{
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 10px;
        }}
        
        QLineEdit {{
            padding: 8px 12px;
            border: 2px solid #ddd;
            border-radius: 4px;
            font-size: 12px;
            background-color: white;
        }}
        
        QLineEdit:focus {{
            border-color: {THEME_COLORS['primary']};
        }}
        
        QComboBox {{
            padding: 8px 12px;
            border: 2px solid #ddd;
            border-radius: 4px;
            font-size: 12px;
            background-color: white;
        }}
        
        QComboBox:focus {{
            border-color: {THEME_COLORS['primary']};
        }}
        
        QPushButton {{
            background-color: {THEME_COLORS['primary']};
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 12px;
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
    
    def showEvent(self, event):
        """Handle show event"""
        super().showEvent(event)
        self.username_input.setFocus()
        
        # Set default credentials for demo
        self.username_input.setText("admin")
        self.password_input.setText("admin123")
    
    def keyPressEvent(self, event):
        """Handle key press events"""
        if event.key() == Qt.Key_Escape:
            self.reject()
        else:
            super().keyPressEvent(event)
