"""
Orders dialog for viewing waiter orders
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTableWidget,
                            QTableWidgetItem, QPushButton, QLabel, QHeaderView,
                            QMessageBox, QGroupBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

from config import THEME_COLORS, ORDER_STATUS_COLORS


class OrdersDialog(QDialog):
    """Dialog for viewing waiter orders"""
    
    def __init__(self, orders, parent=None):
        super().__init__(parent)
        self.orders = orders
        self.setWindowTitle("My Orders")
        self.setModal(True)
        self.setFixedSize(600, 400)
        
        self.init_ui()
        self.setup_connections()
        self.load_orders()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("My Orders")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet(f"color: {THEME_COLORS['primary']};")
        layout.addWidget(title_label)
        
        # Orders table
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(4)
        self.orders_table.setHorizontalHeaderLabels(['Order #', 'Table', 'Status', 'Amount'])
        self.orders_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.orders_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        layout.addWidget(self.orders_table)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.load_orders)
        
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.accept)
        
        button_layout.addWidget(self.refresh_button)
        button_layout.addStretch()
        button_layout.addWidget(self.close_button)
        
        layout.addLayout(button_layout)
        
        # Set stylesheet
        self.setStyleSheet(self.get_dialog_style())
    
    def setup_connections(self):
        """Setup signal connections"""
        pass
    
    def load_orders(self):
        """Load orders into the table"""
        self.orders_table.setRowCount(len(self.orders))
        
        for row, order in enumerate(self.orders):
            # Order number
            self.orders_table.setItem(row, 0, QTableWidgetItem(str(order['id'])))
            
            # Table number
            self.orders_table.setItem(row, 1, QTableWidgetItem(str(order['table_number'])))
            
            # Status
            status_item = QTableWidgetItem(order['status'].title())
            status_color = ORDER_STATUS_COLORS.get(order['status'], THEME_COLORS['dark'])
            status_item.setBackground(QColor(status_color))
            status_item.setForeground(QColor('white'))
            self.orders_table.setItem(row, 2, status_item)
            
            # Amount
            self.orders_table.setItem(row, 3, QTableWidgetItem(f"${order['total_amount']:.2f}"))
    
    def get_dialog_style(self):
        """Get dialog stylesheet"""
        return f"""
        QDialog {{
            background-color: {THEME_COLORS['light']};
        }}
        
        QTableWidget {{
            gridline-color: #ddd;
            background-color: white;
            alternate-background-color: #f8f9fa;
        }}
        
        QTableWidget::item {{
            padding: 8px;
        }}
        
        QTableWidget::item:selected {{
            background-color: {THEME_COLORS['primary']};
            color: white;
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
        }}
        """
