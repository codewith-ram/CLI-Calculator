"""
Chef window for SmartDine Desktop Edition
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                            QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                            QGroupBox, QHeaderView, QMessageBox, QFrame,
                            QSplitter, QTextEdit, QTabWidget)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor

from backend.order_service import order_service
from backend.auth_service import auth_service
from config import THEME_COLORS, ORDER_STATUS_COLORS
from utils.logger import logger


class ChefWindow(QWidget):
    """Chef interface for managing kitchen orders"""
    
    def __init__(self):
        super().__init__()
        self.current_user = None
        
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
        self.setStyleSheet(self.get_chef_style())
    
    def create_header(self, layout):
        """Create header section"""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.StyledPanel)
        header_layout = QHBoxLayout(header_frame)
        
        # Title
        title_label = QLabel("Kitchen Dashboard")
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
        # Create main dashboard layout
        dashboard_layout = QVBoxLayout()
        
        # Kitchen status overview
        self.create_kitchen_status_section(dashboard_layout)
        
        # Create splitter for main content
        splitter = QSplitter(Qt.Horizontal)
        
        # Left side - Kitchen Queue
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # Kitchen queue section
        self.create_kitchen_queue_section(left_layout)
        
        # Right side - Order Details and Actions
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # Order details section
        self.create_order_details_section(right_layout)
        
        # Action buttons
        self.create_action_buttons_section(right_layout)
        
        # Kitchen timer
        self.create_kitchen_timer_section(right_layout)
        
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([600, 600])
        
        dashboard_layout.addWidget(splitter)
        layout.addLayout(dashboard_layout)
    
    def create_kitchen_status_section(self, layout):
        """Create kitchen status overview section"""
        status_group = QGroupBox("Kitchen Status")
        status_layout = QHBoxLayout(status_group)
        
        # Status cards
        self.pending_card = self.create_status_card("Pending Orders", "0", THEME_COLORS['warning'])
        self.cooking_card = self.create_status_card("Cooking", "0", THEME_COLORS['info'])
        self.ready_card = self.create_status_card("Ready to Serve", "0", THEME_COLORS['success'])
        self.total_card = self.create_status_card("Total Today", "0", THEME_COLORS['primary'])
        
        status_layout.addWidget(self.pending_card)
        status_layout.addWidget(self.cooking_card)
        status_layout.addWidget(self.ready_card)
        status_layout.addWidget(self.total_card)
        
        layout.addWidget(status_group)
    
    def create_status_card(self, title, value, color):
        """Create a status card widget"""
        card = QFrame()
        card.setFrameStyle(QFrame.StyledPanel)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 8px;
                padding: 10px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignCenter)
        
        # Value
        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 24, QFont.Bold))
        value_label.setStyleSheet("color: white;")
        value_label.setAlignment(Qt.AlignCenter)
        
        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 10))
        title_label.setStyleSheet("color: white;")
        title_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(value_label)
        layout.addWidget(title_label)
        
        return card
    
    def create_kitchen_queue_section(self, layout):
        """Create kitchen queue section"""
        queue_group = QGroupBox("Kitchen Queue")
        queue_layout = QVBoxLayout(queue_group)
        
        # Queue tabs
        self.queue_tabs = QTabWidget()
        
        # Pending orders tab
        self.pending_tab = QWidget()
        pending_layout = QVBoxLayout(self.pending_tab)
        
        self.pending_orders_table = QTableWidget()
        self.pending_orders_table.setColumnCount(6)
        self.pending_orders_table.setHorizontalHeaderLabels(['Order #', 'Table', 'Time', 'Items', 'Priority', 'Action'])
        self.pending_orders_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.pending_orders_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.pending_orders_table.itemSelectionChanged.connect(self.on_order_selected)
        
        pending_layout.addWidget(self.pending_orders_table)
        self.queue_tabs.addTab(self.pending_tab, "Pending")
        
        # Cooking orders tab
        self.cooking_tab = QWidget()
        cooking_layout = QVBoxLayout(self.cooking_tab)
        
        self.cooking_orders_table = QTableWidget()
        self.cooking_orders_table.setColumnCount(6)
        self.cooking_orders_table.setHorizontalHeaderLabels(['Order #', 'Table', 'Started', 'Items', 'Timer', 'Action'])
        self.cooking_orders_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.cooking_orders_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.cooking_orders_table.itemSelectionChanged.connect(self.on_order_selected)
        
        cooking_layout.addWidget(self.cooking_orders_table)
        self.queue_tabs.addTab(self.cooking_tab, "Cooking")
        
        # Ready orders tab
        self.ready_tab = QWidget()
        ready_layout = QVBoxLayout(self.ready_tab)
        
        self.ready_orders_table = QTableWidget()
        self.ready_orders_table.setColumnCount(5)
        self.ready_orders_table.setHorizontalHeaderLabels(['Order #', 'Table', 'Ready Time', 'Items', 'Action'])
        self.ready_orders_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ready_orders_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.ready_orders_table.itemSelectionChanged.connect(self.on_order_selected)
        
        ready_layout.addWidget(self.ready_orders_table)
        self.queue_tabs.addTab(self.ready_tab, "Ready")
        
        queue_layout.addWidget(self.queue_tabs)
        layout.addWidget(queue_group)
    
    def create_order_details_section(self, layout):
        """Create order details section"""
        details_group = QGroupBox("Order Details")
        details_layout = QVBoxLayout(details_group)
        
        # Order info
        self.order_info_label = QLabel("Select an order to view details")
        self.order_info_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.order_info_label.setStyleSheet(f"color: {THEME_COLORS['primary']};")
        
        details_layout.addWidget(self.order_info_label)
        
        # Order items
        self.order_items_text = QTextEdit()
        self.order_items_text.setReadOnly(True)
        self.order_items_text.setMaximumHeight(200)
        self.order_items_text.setPlaceholderText("Order items will appear here...")
        
        details_layout.addWidget(QLabel("Order Items:"))
        details_layout.addWidget(self.order_items_text)
        
        # Order notes
        self.order_notes_text = QTextEdit()
        self.order_notes_text.setReadOnly(True)
        self.order_notes_text.setMaximumHeight(100)
        self.order_notes_text.setPlaceholderText("Special instructions will appear here...")
        
        details_layout.addWidget(QLabel("Special Instructions:"))
        details_layout.addWidget(self.order_notes_text)
        
        layout.addWidget(details_group)
    
    def create_action_buttons_section(self, layout):
        """Create action buttons section"""
        buttons_group = QGroupBox("Order Actions")
        buttons_layout = QVBoxLayout(buttons_group)
        
        # Status update buttons
        status_layout = QHBoxLayout()
        
        self.start_cooking_button = QPushButton("🔥 Start Cooking")
        self.start_cooking_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.start_cooking_button.setMinimumHeight(40)
        self.start_cooking_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEME_COLORS['warning']};
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {THEME_COLORS['info']};
            }}
        """)
        self.start_cooking_button.clicked.connect(self.start_cooking)
        
        self.mark_ready_button = QPushButton("✅ Mark Ready")
        self.mark_ready_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.mark_ready_button.setMinimumHeight(40)
        self.mark_ready_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEME_COLORS['success']};
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {THEME_COLORS['primary']};
            }}
        """)
        self.mark_ready_button.clicked.connect(self.mark_ready)
        
        self.mark_served_button = QPushButton("🍽️ Mark Served")
        self.mark_served_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.mark_served_button.setMinimumHeight(40)
        self.mark_served_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEME_COLORS['primary']};
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {THEME_COLORS['secondary']};
            }}
        """)
        self.mark_served_button.clicked.connect(self.mark_served)
        
        status_layout.addWidget(self.start_cooking_button)
        status_layout.addWidget(self.mark_ready_button)
        status_layout.addWidget(self.mark_served_button)
        
        buttons_layout.addLayout(status_layout)
        
        # Quick actions
        quick_actions_layout = QHBoxLayout()
        
        self.priority_button = QPushButton("⚡ High Priority")
        self.priority_button.setFont(QFont("Arial", 10))
        self.priority_button.setMinimumHeight(30)
        self.priority_button.clicked.connect(self.set_priority)
        
        self.notes_button = QPushButton("📝 Add Notes")
        self.notes_button.setFont(QFont("Arial", 10))
        self.notes_button.setMinimumHeight(30)
        self.notes_button.clicked.connect(self.add_kitchen_notes)
        
        quick_actions_layout.addWidget(self.priority_button)
        quick_actions_layout.addWidget(self.notes_button)
        
        buttons_layout.addLayout(quick_actions_layout)
        
        layout.addWidget(buttons_group)
    
    def create_kitchen_timer_section(self, layout):
        """Create kitchen timer section"""
        timer_group = QGroupBox("Kitchen Timer")
        timer_layout = QVBoxLayout(timer_group)
        
        # Current order timer
        self.timer_label = QLabel("00:00")
        self.timer_label.setFont(QFont("Arial", 36, QFont.Bold))
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet(f"""
            QLabel {{
                color: {THEME_COLORS['primary']};
                background-color: {THEME_COLORS['light']};
                border: 2px solid {THEME_COLORS['primary']};
                border-radius: 10px;
                padding: 10px;
            }}
        """)
        
        timer_layout.addWidget(self.timer_label)
        
        # Timer controls
        timer_controls_layout = QHBoxLayout()
        
        self.start_timer_button = QPushButton("⏱️ Start Timer")
        self.start_timer_button.clicked.connect(self.start_timer)
        
        self.reset_timer_button = QPushButton("🔄 Reset")
        self.reset_timer_button.clicked.connect(self.reset_timer)
        
        timer_controls_layout.addWidget(self.start_timer_button)
        timer_controls_layout.addWidget(self.reset_timer_button)
        
        timer_layout.addLayout(timer_controls_layout)
        
        # Kitchen statistics
        self.stats_label = QLabel("Kitchen Statistics")
        self.stats_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.stats_label.setStyleSheet(f"color: {THEME_COLORS['dark']};")
        
        timer_layout.addWidget(self.stats_label)
        
        layout.addWidget(timer_group)
    
    def setup_timers(self):
        """Setup timers for periodic updates"""
        # Timer for refreshing data
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_data)
        self.refresh_timer.start(5000)  # Refresh every 5 seconds for real-time updates
        
        # Kitchen timer
        self.kitchen_timer = QTimer()
        self.kitchen_timer.timeout.connect(self.update_kitchen_timer)
        self.timer_seconds = 0
        self.timer_running = False
    
    def initialize(self):
        """Initialize the window with current user data"""
        self.current_user = auth_service.get_current_user()
        if self.current_user:
            self.load_pending_orders()
            self.update_status("Kitchen ready")
    
    def load_pending_orders(self):
        """Load pending orders into the new dashboard"""
        try:
            # Get orders by status
            pending_orders = order_service.get_orders_by_status('pending')
            cooking_orders = order_service.get_orders_by_status('cooking')
            ready_orders = order_service.get_orders_by_status('ready')
            
            # Update status cards
            self.update_status_cards(len(pending_orders), len(cooking_orders), len(ready_orders))
            
            # Load pending orders
            self.load_orders_to_table(self.pending_orders_table, pending_orders, 'pending')
            
            # Load cooking orders
            self.load_orders_to_table(self.cooking_orders_table, cooking_orders, 'cooking')
            
            # Load ready orders
            self.load_orders_to_table(self.ready_orders_table, ready_orders, 'ready')
            
            # Update statistics
            self.update_statistics()
            
        except Exception as e:
            logger.error(f"Error loading pending orders: {e}")
            self.update_status(f"Error loading orders: {e}")
    
    def update_status_cards(self, pending_count, cooking_count, ready_count):
        """Update status cards with current counts"""
        # Update card values
        for i, (card, count) in enumerate([
            (self.pending_card, pending_count),
            (self.cooking_card, cooking_count),
            (self.ready_card, ready_count)
        ]):
            # Find the value label in the card
            value_label = card.findChild(QLabel)
            if value_label:
                value_label.setText(str(count))
        
        # Update total count
        total_count = pending_count + cooking_count + ready_count
        total_value_label = self.total_card.findChild(QLabel)
        if total_value_label:
            total_value_label.setText(str(total_count))
    
    def load_orders_to_table(self, table, orders, status):
        """Load orders into a specific table widget"""
        table.setRowCount(len(orders))
        
        for row, order in enumerate(orders):
            # Order number
            table.setItem(row, 0, QTableWidgetItem(str(order['id'])))
            
            # Table number
            table.setItem(row, 1, QTableWidgetItem(str(order['table_number'])))
            
            # Time column (different for each status)
            if status == 'pending':
                time_text = order['created_at'].strftime("%H:%M") if order['created_at'] else "N/A"
                table.setItem(row, 2, QTableWidgetItem(time_text))
                
                # Items count
                items_count = len(order.get('order_items', []))
                table.setItem(row, 3, QTableWidgetItem(str(items_count)))
                
                # Priority (simple implementation)
                priority = "Normal"
                table.setItem(row, 4, QTableWidgetItem(priority))
                
                # Action button
                action_button = QPushButton("🔥 Start")
                action_button.clicked.connect(lambda checked, o=order: self.start_cooking_order(o))
                table.setCellWidget(row, 5, action_button)
                
            elif status == 'cooking':
                time_text = order['created_at'].strftime("%H:%M") if order['created_at'] else "N/A"
                table.setItem(row, 2, QTableWidgetItem(time_text))
                
                # Items count
                items_count = len(order.get('order_items', []))
                table.setItem(row, 3, QTableWidgetItem(str(items_count)))
                
                # Timer (placeholder)
                table.setItem(row, 4, QTableWidgetItem("00:05"))
                
                # Action button
                action_button = QPushButton("✅ Ready")
                action_button.clicked.connect(lambda checked, o=order: self.mark_ready_order(o))
                table.setCellWidget(row, 5, action_button)
                
            elif status == 'ready':
                time_text = order['created_at'].strftime("%H:%M") if order['created_at'] else "N/A"
                table.setItem(row, 2, QTableWidgetItem(time_text))
                
                # Items count
                items_count = len(order.get('order_items', []))
                table.setItem(row, 3, QTableWidgetItem(str(items_count)))
                
                # Action button
                action_button = QPushButton("🍽️ Served")
                action_button.clicked.connect(lambda checked, o=order: self.mark_served_order(o))
                table.setCellWidget(row, 4, action_button)
    
    def on_order_selected(self):
        """Handle order selection"""
        current_row = self.orders_table.currentRow()
        if current_row >= 0:
            order_id = int(self.orders_table.item(current_row, 0).text())
            self.load_order_details(order_id)
    
    def select_order(self, order):
        """Select an order for detailed view"""
        self.load_order_details(order['id'])
    
    def load_order_details(self, order_id):
        """Load detailed order information"""
        try:
            order = order_service.get_order(order_id)
            if order:
                # Update order info
                self.order_info_label.setText(
                    f"Order #{order['id']} - Table {order['table_number']} - {order['waiter_name']}"
                )
                
                # Update order items
                items_text = ""
                for item in order['order_items']:
                    items_text += f"• {item['menu_item_name']} x{item['quantity']}\n"
                    if item['special_instructions']:
                        items_text += f"  Note: {item['special_instructions']}\n"
                
                self.order_items_text.setText(items_text)
                
                # Update order notes
                self.order_notes_text.setText(order['notes'] or "No special instructions")
                
                # Update button states based on order status
                self.update_button_states(order['status'])
                
        except Exception as e:
            logger.error(f"Error loading order details: {e}")
            self.update_status(f"Error loading order details: {e}")
    
    def update_button_states(self, order_status):
        """Update button states based on order status"""
        self.start_cooking_button.setEnabled(order_status == 'pending')
        self.mark_ready_button.setEnabled(order_status == 'cooking')
        self.mark_served_button.setEnabled(order_status == 'ready')
    
    def start_cooking(self):
        """Start cooking an order"""
        current_row = self.orders_table.currentRow()
        if current_row >= 0:
            order_id = int(self.orders_table.item(current_row, 0).text())
            self.update_order_status(order_id, 'cooking')
    
    def mark_ready(self):
        """Mark order as ready"""
        current_row = self.orders_table.currentRow()
        if current_row >= 0:
            order_id = int(self.orders_table.item(current_row, 0).text())
            self.update_order_status(order_id, 'ready')
    
    def mark_served(self):
        """Mark order as served"""
        current_row = self.orders_table.currentRow()
        if current_row >= 0:
            order_id = int(self.orders_table.item(current_row, 0).text())
            self.update_order_status(order_id, 'served')
    
    def update_order_status(self, order_id, new_status):
        """Update order status"""
        try:
            success = order_service.update_order_status(order_id, new_status)
            if success:
                self.update_status(f"Order #{order_id} status updated to {new_status}")
                self.load_pending_orders()
                self.load_order_details(order_id)
            else:
                QMessageBox.warning(self, "Update Failed", "Failed to update order status.")
                
        except Exception as e:
            logger.error(f"Error updating order status: {e}")
            QMessageBox.critical(self, "Update Error", f"Error updating order status:\n{str(e)}")
    
    def update_statistics(self):
        """Update kitchen statistics"""
        try:
            stats = order_service.get_order_statistics()
            stats_text = f"""
            📊 Kitchen Performance
            Total Orders: {stats['total_orders']}
            Pending: {stats['pending_orders']}
            Cooking: {stats['cooking_orders']}
            Ready: {stats['ready_orders']}
            Active: {stats['active_orders']}
            """
            self.stats_label.setText(stats_text)
            
        except Exception as e:
            logger.error(f"Error updating statistics: {e}")
    
    def start_cooking_order(self, order):
        """Start cooking a specific order"""
        try:
            success = order_service.update_order_status(order['id'], 'cooking')
            if success:
                self.update_status(f"Started cooking Order #{order['id']}")
                self.start_timer()
                self.load_pending_orders()
            else:
                QMessageBox.warning(self, "Update Failed", "Failed to start cooking order.")
        except Exception as e:
            logger.error(f"Error starting cooking: {e}")
            QMessageBox.critical(self, "Error", f"Error starting cooking:\n{str(e)}")
    
    def mark_ready_order(self, order):
        """Mark order as ready"""
        try:
            success = order_service.update_order_status(order['id'], 'ready')
            if success:
                self.update_status(f"Order #{order['id']} is ready to serve!")
                self.reset_timer()
                self.load_pending_orders()
            else:
                QMessageBox.warning(self, "Update Failed", "Failed to mark order as ready.")
        except Exception as e:
            logger.error(f"Error marking ready: {e}")
            QMessageBox.critical(self, "Error", f"Error marking ready:\n{str(e)}")
    
    def mark_served_order(self, order):
        """Mark order as served"""
        try:
            success = order_service.update_order_status(order['id'], 'served')
            if success:
                self.update_status(f"Order #{order['id']} served to table {order['table_number']}")
                self.load_pending_orders()
            else:
                QMessageBox.warning(self, "Update Failed", "Failed to mark order as served.")
        except Exception as e:
            logger.error(f"Error marking served: {e}")
            QMessageBox.critical(self, "Error", f"Error marking served:\n{str(e)}")
    
    def start_timer(self):
        """Start the kitchen timer"""
        if not self.timer_running:
            self.timer_running = True
            self.timer_seconds = 0
            self.kitchen_timer.start(1000)  # Update every second
            self.start_timer_button.setText("⏸️ Pause")
        else:
            self.pause_timer()
    
    def pause_timer(self):
        """Pause the kitchen timer"""
        self.timer_running = False
        self.kitchen_timer.stop()
        self.start_timer_button.setText("⏱️ Resume")
    
    def reset_timer(self):
        """Reset the kitchen timer"""
        self.timer_running = False
        self.kitchen_timer.stop()
        self.timer_seconds = 0
        self.timer_label.setText("00:00")
        self.start_timer_button.setText("⏱️ Start Timer")
    
    def update_kitchen_timer(self):
        """Update the kitchen timer display"""
        if self.timer_running:
            self.timer_seconds += 1
            minutes = self.timer_seconds // 60
            seconds = self.timer_seconds % 60
            self.timer_label.setText(f"{minutes:02d}:{seconds:02d}")
    
    def set_priority(self):
        """Set high priority for current order"""
        QMessageBox.information(self, "Priority Set", "Order marked as high priority!")
        self.update_status("Order priority updated")
    
    def add_kitchen_notes(self):
        """Add kitchen notes to current order"""
        from PyQt5.QtWidgets import QInputDialog
        text, ok = QInputDialog.getText(self, 'Kitchen Notes', 'Enter kitchen notes:')
        if ok and text:
            QMessageBox.information(self, "Notes Added", f"Kitchen notes added: {text}")
            self.update_status("Kitchen notes added")
    
    def refresh_data(self):
        """Refresh all data"""
        self.load_pending_orders()
    
    def update_status(self, message):
        """Update status message"""
        self.status_label.setText(message)
        logger.info(f"Chef status: {message}")
    
    def clear_data(self):
        """Clear all data when logging out"""
        self.current_user = None
        self.orders_table.setRowCount(0)
        self.order_info_label.setText("Select an order to view details")
        self.order_items_text.clear()
        self.order_notes_text.clear()
        self.stats_label.setText("Kitchen Statistics")
    
    def get_chef_style(self):
        """Get chef window stylesheet"""
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
        """
