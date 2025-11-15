"""
Main window for SmartDine Desktop Edition
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QStackedWidget, QStatusBar,
                            QMenuBar, QAction, QMessageBox, QFrame)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor

from .login_window import LoginWindow
from .waiter_window import WaiterWindow
from .chef_window import ChefWindow
from .cashier_window import CashierWindow
from .admin_window import AdminWindow
from backend.auth_service import auth_service
from config import THEME_COLORS, APP_NAME
from utils.logger import logger


class MainWindow(QMainWindow):
    """Main application window"""
    
    # Signals
    user_logged_in = pyqtSignal(dict)
    user_logged_out = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.current_window = None
        self.login_window = None
        
        self.init_ui()
        self.setup_timers()
        self.show_login()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        
        # Set application style
        self.setStyleSheet(self.get_application_style())
        
        # Create central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Create main layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create stacked widget for different views
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)
        
        # Create status bar
        self.create_status_bar()
        
        # Create menu bar
        self.create_menu_bar()
        
        # Initialize role-specific windows
        self.waiter_window = WaiterWindow()
        self.chef_window = ChefWindow()
        self.cashier_window = CashierWindow()
        self.admin_window = AdminWindow()
        
        # Add windows to stacked widget
        self.stacked_widget.addWidget(self.waiter_window)
        self.stacked_widget.addWidget(self.chef_window)
        self.stacked_widget.addWidget(self.cashier_window)
        self.stacked_widget.addWidget(self.admin_window)
        
        # Connect signals
        self.user_logged_in.connect(self.on_user_logged_in)
        self.user_logged_out.connect(self.on_user_logged_out)
    
    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Add status labels
        self.user_label = QLabel("Not logged in")
        self.time_label = QLabel("")
        self.status_label = QLabel("Ready")
        
        self.status_bar.addWidget(self.user_label)
        self.status_bar.addPermanentWidget(self.time_label)
        self.status_bar.addPermanentWidget(self.status_label)
    
    def create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        logout_action = QAction('Logout', self)
        logout_action.triggered.connect(self.logout)
        file_menu.addAction(logout_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu('View')
        
        refresh_action = QAction('Refresh', self)
        refresh_action.triggered.connect(self.refresh_current_view)
        view_menu.addAction(refresh_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_timers(self):
        """Setup timers for periodic updates"""
        # Timer for updating time display
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)  # Update every second
        
        # Timer for refreshing data
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_current_view)
        self.refresh_timer.start(30000)  # Refresh every 30 seconds
    
    def show_login(self):
        """Show login window"""
        if not self.login_window:
            self.login_window = LoginWindow()
            self.login_window.login_successful.connect(self.on_login_successful)
        
        self.login_window.show()
        self.hide()
    
    def on_login_successful(self, user_data):
        """Handle successful login"""
        self.current_user = user_data
        self.user_logged_in.emit(user_data)
        self.login_window.hide()
        self.show()
    
    def on_user_logged_in(self, user_data):
        """Handle user logged in signal"""
        self.user_label.setText(f"Logged in as: {user_data['full_name']} ({user_data['role'].title()})")
        self.status_label.setText("Connected")
        
        # Show appropriate window based on role
        role = user_data['role']
        if role == 'waiter':
            self.stacked_widget.setCurrentWidget(self.waiter_window)
            self.current_window = self.waiter_window
        elif role == 'chef':
            self.stacked_widget.setCurrentWidget(self.chef_window)
            self.current_window = self.chef_window
        elif role == 'cashier':
            self.stacked_widget.setCurrentWidget(self.cashier_window)
            self.current_window = self.cashier_window
        elif role == 'admin':
            self.stacked_widget.setCurrentWidget(self.admin_window)
            self.current_window = self.admin_window
        
        # Initialize the current window
        if self.current_window:
            self.current_window.initialize()
    
    def on_user_logged_out(self):
        """Handle user logged out signal"""
        self.user_label.setText("Not logged in")
        self.status_label.setText("Disconnected")
        self.current_user = None
        self.current_window = None
        
        # Clear all windows
        self.waiter_window.clear_data()
        self.chef_window.clear_data()
        self.cashier_window.clear_data()
        self.admin_window.clear_data()
    
    def logout(self):
        """Logout current user"""
        if self.current_user:
            auth_service.logout()
            self.user_logged_out.emit()
            self.show_login()
    
    def refresh_current_view(self):
        """Refresh the current view"""
        if self.current_window and hasattr(self.current_window, 'refresh_data'):
            self.current_window.refresh_data()
    
    def update_time(self):
        """Update time display"""
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.setText(current_time)
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About SmartDine",
            f"""
            <h3>{APP_NAME}</h3>
            <p>Version 1.0.0</p>
            <p>A comprehensive restaurant management system for desktop use.</p>
            <p>Features include:</p>
            <ul>
                <li>Multi-role user management</li>
                <li>Menu and table management</li>
                <li>Order processing workflow</li>
                <li>Billing and payment processing</li>
                <li>Analytics and reporting</li>
            </ul>
            <p>Built with Python and PyQt5</p>
            """
        )
    
    def get_application_style(self):
        """Get application stylesheet"""
        return f"""
        QMainWindow {{
            background-color: {THEME_COLORS['light']};
        }}
        
        QMenuBar {{
            background-color: {THEME_COLORS['primary']};
            color: white;
            border: none;
            padding: 4px;
        }}
        
        QMenuBar::item {{
            background-color: transparent;
            padding: 8px 12px;
            border-radius: 4px;
        }}
        
        QMenuBar::item:selected {{
            background-color: {THEME_COLORS['secondary']};
        }}
        
        QMenu {{
            background-color: white;
            border: 1px solid #ccc;
            border-radius: 4px;
        }}
        
        QMenu::item {{
            padding: 8px 20px;
        }}
        
        QMenu::item:selected {{
            background-color: {THEME_COLORS['primary']};
            color: white;
        }}
        
        QStatusBar {{
            background-color: {THEME_COLORS['dark']};
            color: white;
            border-top: 1px solid #ccc;
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
        
        QPushButton:disabled {{
            background-color: #ccc;
            color: #666;
        }}
        
        QLabel {{
            color: {THEME_COLORS['dark']};
        }}
        
        QFrame {{
            border: 1px solid #ddd;
            border-radius: 4px;
        }}
        """
    
    def closeEvent(self, event):
        """Handle application close event"""
        reply = QMessageBox.question(
            self,
            'Exit Application',
            'Are you sure you want to exit SmartDine?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            logger.info("Application closing...")
            event.accept()
        else:
            event.ignore()
