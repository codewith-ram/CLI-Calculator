"""
Cashier window for SmartDine Desktop Edition
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                            QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                            QGroupBox, QHeaderView, QMessageBox, QFrame,
                            QSplitter, QComboBox, QDoubleSpinBox, QTextEdit)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor

from backend.billing_service import billing_service
from backend.table_service import table_service
from backend.auth_service import auth_service
from config import THEME_COLORS, PAYMENT_METHODS
from utils.logger import logger


class CashierWindow(QWidget):
    """Cashier interface for billing and payments"""
    
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.selected_table = None
        self.current_bill = None
        
        self.init_ui()
        self.setup_timers()
    
    def init_ui(self):
        """Initialize the user interface"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create header
        self.create_header(main_layout)
        
        # Create main content area
        self.create_main_content(main_layout)
        
        # Set stylesheet
        self.setStyleSheet(self.get_cashier_style())
    
    def create_header(self, layout):
        """Create header section"""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.StyledPanel)
        header_layout = QHBoxLayout(header_frame)
        
        # Title
        title_label = QLabel("Cashier Dashboard")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet(f"color: {THEME_COLORS['primary']};")
        
        # Status
        self.status_label = QLabel("Ready")
        self.status_label.setFont(QFont("Arial", 12))
        self.status_label.setStyleSheet(f"color: {THEME_COLORS['success']};")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.status_label)
        
        layout.addWidget(header_frame)
    
    def create_main_content(self, layout):
        """Create main content area"""
        # Create splitter for main content
        splitter = QSplitter(Qt.Horizontal)
        
        # Left side - Tables and Bills
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # Tables section
        self.create_tables_section(left_layout)
        
        # Bills section
        self.create_bills_section(left_layout)
        
        # Right side - Bill Details and Payment
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # Bill details section
        self.create_bill_details_section(right_layout)
        
        # Payment section
        self.create_payment_section(right_layout)
        
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([400, 600])
        
        layout.addWidget(splitter)
    
    def create_tables_section(self, layout):
        """Create tables section"""
        tables_group = QGroupBox("Tables")
        tables_layout = QVBoxLayout(tables_group)
        
        # Tables table
        self.tables_table = QTableWidget()
        self.tables_table.setColumnCount(4)
        self.tables_table.setHorizontalHeaderLabels(['Table', 'Status', 'Order', 'Action'])
        self.tables_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tables_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.tables_table.itemSelectionChanged.connect(self.on_table_selected)
        
        tables_layout.addWidget(self.tables_table)
        
        layout.addWidget(tables_group)
    
    def create_bills_section(self, layout):
        """Create bills section"""
        bills_group = QGroupBox("Pending Bills")
        bills_layout = QVBoxLayout(bills_group)
        
        # Bills table
        self.bills_table = QTableWidget()
        self.bills_table.setColumnCount(4)
        self.bills_table.setHorizontalHeaderLabels(['Bill #', 'Table', 'Amount', 'Action'])
        self.bills_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.bills_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.bills_table.itemSelectionChanged.connect(self.on_bill_selected)
        
        bills_layout.addWidget(self.bills_table)
        
        layout.addWidget(bills_group)
    
    def create_bill_details_section(self, layout):
        """Create bill details section"""
        details_group = QGroupBox("Bill Details")
        details_layout = QVBoxLayout(details_group)
        
        # Bill info
        self.bill_info_label = QLabel("Select a table or bill to view details")
        self.bill_info_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.bill_info_label.setStyleSheet(f"color: {THEME_COLORS['primary']};")
        
        details_layout.addWidget(self.bill_info_label)
        
        # Bill items
        self.bill_items_text = QTextEdit()
        self.bill_items_text.setReadOnly(True)
        self.bill_items_text.setMaximumHeight(200)
        self.bill_items_text.setPlaceholderText("Bill items will appear here...")
        
        details_layout.addWidget(QLabel("Order Items:"))
        details_layout.addWidget(self.bill_items_text)
        
        # Bill summary
        self.bill_summary_label = QLabel("Bill Summary")
        self.bill_summary_label.setFont(QFont("Arial", 10, QFont.Bold))
        
        details_layout.addWidget(self.bill_summary_label)
        
        layout.addWidget(details_group)
    
    def create_payment_section(self, layout):
        """Create payment section"""
        payment_group = QGroupBox("Payment Processing")
        payment_layout = QVBoxLayout(payment_group)
        
        # Payment method
        payment_method_layout = QHBoxLayout()
        payment_method_layout.addWidget(QLabel("Payment Method:"))
        
        self.payment_method_combo = QComboBox()
        self.payment_method_combo.addItems(PAYMENT_METHODS)
        self.payment_method_combo.setCurrentText('cash')
        
        payment_method_layout.addWidget(self.payment_method_combo)
        payment_method_layout.addStretch()
        
        payment_layout.addLayout(payment_method_layout)
        
        # Bill adjustments
        adjustments_layout = QGridLayout()
        
        # Tax rate
        adjustments_layout.addWidget(QLabel("Tax Rate (%):"), 0, 0)
        self.tax_rate_spin = QDoubleSpinBox()
        self.tax_rate_spin.setRange(0.0, 100.0)
        self.tax_rate_spin.setValue(8.5)
        self.tax_rate_spin.setSuffix("%")
        adjustments_layout.addWidget(self.tax_rate_spin, 0, 1)
        
        # Discount amount
        adjustments_layout.addWidget(QLabel("Discount ($):"), 1, 0)
        self.discount_spin = QDoubleSpinBox()
        self.discount_spin.setRange(0.0, 999.99)
        self.discount_spin.setValue(0.0)
        self.discount_spin.setPrefix("$")
        adjustments_layout.addWidget(self.discount_spin, 1, 1)
        
        # Service charge
        adjustments_layout.addWidget(QLabel("Service Charge ($):"), 2, 0)
        self.service_charge_spin = QDoubleSpinBox()
        self.service_charge_spin.setRange(0.0, 999.99)
        self.service_charge_spin.setValue(0.0)
        self.service_charge_spin.setPrefix("$")
        adjustments_layout.addWidget(self.service_charge_spin, 2, 1)
        
        payment_layout.addLayout(adjustments_layout)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        
        self.create_bill_button = QPushButton("Create Bill")
        self.create_bill_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.create_bill_button.setMinimumHeight(40)
        self.create_bill_button.clicked.connect(self.create_bill)
        
        self.process_payment_button = QPushButton("Process Payment")
        self.process_payment_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.process_payment_button.setMinimumHeight(40)
        self.process_payment_button.clicked.connect(self.process_payment)
        
        self.print_bill_button = QPushButton("Print Bill")
        self.print_bill_button.setFont(QFont("Arial", 12))
        self.print_bill_button.setMinimumHeight(40)
        self.print_bill_button.clicked.connect(self.print_bill)
        
        buttons_layout.addWidget(self.create_bill_button)
        buttons_layout.addWidget(self.process_payment_button)
        buttons_layout.addWidget(self.print_bill_button)
        
        payment_layout.addLayout(buttons_layout)
        
        layout.addWidget(payment_group)
    
    def setup_timers(self):
        """Setup timers for periodic updates"""
        # Timer for refreshing data
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_data)
        self.refresh_timer.start(15000)  # Refresh every 15 seconds
    
    def initialize(self):
        """Initialize the window with current user data"""
        self.current_user = auth_service.get_current_user()
        if self.current_user:
            self.load_tables()
            self.load_pending_bills()
            self.update_status("Ready for billing")
    
    def load_tables(self):
        """Load tables data"""
        try:
            tables = table_service.get_all_tables()
            
            self.tables_table.setRowCount(len(tables))
            
            for row, table in enumerate(tables):
                # Table number
                self.tables_table.setItem(row, 0, QTableWidgetItem(str(table['table_number'])))
                
                # Status
                status_item = QTableWidgetItem(table['status'].title())
                if table['status'] == 'served':
                    status_item.setBackground(QColor(THEME_COLORS['success']))
                    status_item.setForeground(QColor('white'))
                elif table['status'] == 'occupied':
                    status_item.setBackground(QColor(THEME_COLORS['warning']))
                    status_item.setForeground(QColor('white'))
                else:
                    status_item.setBackground(QColor(THEME_COLORS['dark']))
                    status_item.setForeground(QColor('white'))
                
                self.tables_table.setItem(row, 1, status_item)
                
                # Order info
                if table['current_order']:
                    order_info = f"Order #{table['current_order']['id']}"
                else:
                    order_info = "No order"
                
                self.tables_table.setItem(row, 2, QTableWidgetItem(order_info))
                
                # Action button
                if table['status'] == 'served':
                    action_button = QPushButton("Create Bill")
                    action_button.clicked.connect(lambda checked, t=table: self.select_table_for_billing(t))
                    self.tables_table.setCellWidget(row, 3, action_button)
                else:
                    action_item = QTableWidgetItem("N/A")
                    self.tables_table.setItem(row, 3, action_item)
            
        except Exception as e:
            logger.error(f"Error loading tables: {e}")
            self.update_status(f"Error loading tables: {e}")
    
    def load_pending_bills(self):
        """Load pending bills"""
        try:
            bills = billing_service.get_pending_bills()
            
            self.bills_table.setRowCount(len(bills))
            
            for row, bill in enumerate(bills):
                # Bill number
                self.bills_table.setItem(row, 0, QTableWidgetItem(str(bill['id'])))
                
                # Table number
                self.bills_table.setItem(row, 1, QTableWidgetItem(str(bill['table_number'])))
                
                # Amount
                self.bills_table.setItem(row, 2, QTableWidgetItem(f"${bill['total_amount']:.2f}"))
                
                # Action button
                action_button = QPushButton("View")
                action_button.clicked.connect(lambda checked, b=bill: self.select_bill(b))
                self.bills_table.setCellWidget(row, 3, action_button)
            
        except Exception as e:
            logger.error(f"Error loading pending bills: {e}")
            self.update_status(f"Error loading bills: {e}")
    
    def on_table_selected(self):
        """Handle table selection"""
        current_row = self.tables_table.currentRow()
        if current_row >= 0:
            table_number = self.tables_table.item(current_row, 0).text()
            self.select_table_for_billing_by_number(int(table_number))
    
    def on_bill_selected(self):
        """Handle bill selection"""
        current_row = self.bills_table.currentRow()
        if current_row >= 0:
            bill_id = int(self.bills_table.item(current_row, 0).text())
            self.load_bill_details(bill_id)
    
    def select_table_for_billing(self, table):
        """Select table for billing"""
        if table['status'] != 'served':
            QMessageBox.warning(self, "Table Not Ready", "This table is not ready for billing.")
            return
        
        self.selected_table = table
        self.load_table_order_details(table)
    
    def select_table_for_billing_by_number(self, table_number):
        """Select table for billing by number"""
        try:
            tables = table_service.get_all_tables()
            table = next((t for t in tables if t['table_number'] == table_number), None)
            if table:
                self.select_table_for_billing(table)
        except Exception as e:
            logger.error(f"Error selecting table: {e}")
    
    def select_bill(self, bill):
        """Select a bill for processing"""
        self.load_bill_details(bill['id'])
    
    def load_table_order_details(self, table):
        """Load order details for table"""
        try:
            if table['current_order']:
                order = table['current_order']
                self.bill_info_label.setText(f"Table {table['table_number']} - Order #{order['id']}")
                
                # Load order items
                items_text = ""
                total_amount = 0
                
                for item in order.get('order_items', []):
                    items_text += f"• {item['menu_item_name']} x{item['quantity']} @ ${item['unit_price']:.2f} = ${item['total_price']:.2f}\n"
                    total_amount += item['total_price']
                
                self.bill_items_text.setText(items_text)
                
                # Update bill summary
                self.bill_summary_label.setText(f"Subtotal: ${total_amount:.2f}")
                
                # Enable create bill button
                self.create_bill_button.setEnabled(True)
                
        except Exception as e:
            logger.error(f"Error loading table order details: {e}")
            self.update_status(f"Error loading order details: {e}")
    
    def load_bill_details(self, bill_id):
        """Load bill details"""
        try:
            bill = billing_service.get_bill(bill_id)
            if bill:
                self.bill_info_label.setText(f"Bill #{bill['id']} - Table {bill['table_number']}")
                
                # Load bill items
                items_text = ""
                for item in bill['order_items']:
                    items_text += f"• {item['menu_item_name']} x{item['quantity']} @ ${item['unit_price']:.2f} = ${item['total_price']:.2f}\n"
                
                self.bill_items_text.setText(items_text)
                
                # Update bill summary
                summary_text = f"""
                Subtotal: ${bill['subtotal']:.2f}
                Tax ({bill['tax_rate']:.1f}%): ${bill['tax_amount']:.2f}
                Service Charge: ${bill['service_charge']:.2f}
                Discount: -${bill['discount_amount']:.2f}
                Total: ${bill['total_amount']:.2f}
                """
                self.bill_summary_label.setText(summary_text)
                
                # Update payment method
                self.payment_method_combo.setCurrentText(bill['payment_method'])
                
                # Enable payment processing
                self.process_payment_button.setEnabled(True)
                self.print_bill_button.setEnabled(True)
                
                self.current_bill = bill
                
        except Exception as e:
            logger.error(f"Error loading bill details: {e}")
            self.update_status(f"Error loading bill details: {e}")
    
    def create_bill(self):
        """Create a bill for the selected table"""
        if not self.selected_table or not self.selected_table['current_order']:
            QMessageBox.warning(self, "No Order", "No order found for this table.")
            return
        
        try:
            order_id = self.selected_table['current_order']['id']
            
            # Create bill
            bill_id = billing_service.create_bill(
                order_id=order_id,
                cashier_id=self.current_user['id'],
                tax_rate=self.tax_rate_spin.value(),
                discount_amount=self.discount_spin.value(),
                service_charge=self.service_charge_spin.value(),
                payment_method=self.payment_method_combo.currentText()
            )
            
            if bill_id:
                QMessageBox.information(self, "Bill Created", f"Bill #{bill_id} created successfully!")
                self.load_pending_bills()
                self.load_bill_details(bill_id)
                self.update_status(f"Bill #{bill_id} created")
            else:
                QMessageBox.critical(self, "Bill Creation Failed", "Failed to create bill.")
                
        except Exception as e:
            logger.error(f"Error creating bill: {e}")
            QMessageBox.critical(self, "Bill Error", f"Error creating bill:\n{str(e)}")
    
    def process_payment(self):
        """Process payment for the current bill"""
        if not self.current_bill:
            QMessageBox.warning(self, "No Bill", "Please select a bill to process payment.")
            return
        
        try:
            success = billing_service.process_payment(
                self.current_bill['id'],
                self.payment_method_combo.currentText()
            )
            
            if success:
                QMessageBox.information(self, "Payment Processed", "Payment processed successfully!")
                self.load_tables()
                self.load_pending_bills()
                self.clear_bill_details()
                self.update_status("Payment processed successfully")
            else:
                QMessageBox.warning(self, "Payment Failed", "Failed to process payment.")
                
        except Exception as e:
            logger.error(f"Error processing payment: {e}")
            QMessageBox.critical(self, "Payment Error", f"Error processing payment:\n{str(e)}")
    
    def print_bill(self):
        """Print the current bill"""
        if not self.current_bill:
            QMessageBox.warning(self, "No Bill", "Please select a bill to print.")
            return
        
        try:
            from ..utils.pdf_generator import pdf_generator
            import os
            
            # Generate PDF
            filename = f"bill_{self.current_bill['id']}.pdf"
            filepath = os.path.join("reports", filename)
            
            success = pdf_generator.generate_bill_pdf(self.current_bill, filepath)
            
            if success:
                QMessageBox.information(self, "Bill Printed", f"Bill saved as {filepath}")
                self.update_status("Bill printed successfully")
            else:
                QMessageBox.warning(self, "Print Failed", "Failed to generate bill PDF.")
                
        except Exception as e:
            logger.error(f"Error printing bill: {e}")
            QMessageBox.critical(self, "Print Error", f"Error printing bill:\n{str(e)}")
    
    def clear_bill_details(self):
        """Clear bill details"""
        self.bill_info_label.setText("Select a table or bill to view details")
        self.bill_items_text.clear()
        self.bill_summary_label.setText("Bill Summary")
        self.current_bill = None
        self.create_bill_button.setEnabled(False)
        self.process_payment_button.setEnabled(False)
        self.print_bill_button.setEnabled(False)
    
    def refresh_data(self):
        """Refresh all data"""
        self.load_tables()
        self.load_pending_bills()
    
    def update_status(self, message):
        """Update status message"""
        self.status_label.setText(message)
        logger.info(f"Cashier status: {message}")
    
    def clear_data(self):
        """Clear all data when logging out"""
        self.current_user = None
        self.selected_table = None
        self.current_bill = None
        self.tables_table.setRowCount(0)
        self.bills_table.setRowCount(0)
        self.clear_bill_details()
    
    def get_cashier_style(self):
        """Get cashier window stylesheet"""
        return f"""
        QWidget {{
            background-color: {THEME_COLORS['light']};
        }}
        
        QGroupBox {{
            font-weight: bold;
            border: 2px solid {THEME_COLORS['primary']};
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
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
        
        QPushButton:disabled {{
            background-color: #ccc;
            color: #666;
        }}
        
        QTextEdit {{
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 5px;
            background-color: white;
        }}
        
        QComboBox, QDoubleSpinBox {{
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 5px;
            background-color: white;
        }}
        """
