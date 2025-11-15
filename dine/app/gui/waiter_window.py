"""
Waiter window for SmartDine Desktop Edition
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                            QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                            QComboBox, QSpinBox, QTextEdit, QGroupBox,
                            QHeaderView, QMessageBox, QFrame, QSplitter, QLineEdit)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette

from backend.menu_service import menu_service
from backend.table_service import table_service
from backend.order_service import order_service
from backend.auth_service import auth_service
from config import THEME_COLORS, TABLE_STATUS_COLORS, ORDER_STATUS_COLORS
from utils.logger import logger


class WaiterWindow(QWidget):
    """Waiter interface for taking orders"""
    
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.selected_table = None
        self.order_items = []
        
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
        self.setStyleSheet(self.get_waiter_style())
    
    def create_header(self, layout):
        """Create header section"""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.StyledPanel)
        header_layout = QHBoxLayout(header_frame)
        
        # Title
        title_label = QLabel("Waiter Dashboard")
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
        
        # Left side - Tables and Menu
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # Tables section
        self.create_tables_section(left_layout)
        
        # Menu section
        self.create_menu_section(left_layout)
        
        # Right side - Order details
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # Current order section
        self.create_order_section(right_layout)
        
        # Order items section
        self.create_order_items_section(right_layout)
        
        # Buttons section
        self.create_buttons_section(right_layout)
        
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([400, 600])
        
        layout.addWidget(splitter)
    
    def create_tables_section(self, layout):
        """Create tables management section"""
        tables_group = QGroupBox("Tables")
        tables_layout = QVBoxLayout(tables_group)
        
        # Tables table
        self.tables_table = QTableWidget()
        self.tables_table.setColumnCount(4)
        self.tables_table.setHorizontalHeaderLabels(['Table', 'Capacity', 'Status', 'Action'])
        self.tables_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tables_table.setMaximumHeight(200)
        
        tables_layout.addWidget(self.tables_table)
        
        # Table selection info
        self.table_info_label = QLabel("Select a table to start taking orders")
        self.table_info_label.setStyleSheet(f"color: {THEME_COLORS['dark']}; font-style: italic;")
        
        tables_layout.addWidget(self.table_info_label)
        
        layout.addWidget(tables_group)
    
    def create_menu_section(self, layout):
        """Create enhanced menu selection section"""
        menu_group = QGroupBox("🍽️ Menu & Products")
        menu_layout = QVBoxLayout(menu_group)
        
        # Menu header with search
        menu_header_layout = QHBoxLayout()
        
        # Search box
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("🔍 Search:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search menu items...")
        self.search_input.textChanged.connect(self.search_menu_items)
        search_layout.addWidget(self.search_input)
        
        # Category filter
        category_layout = QHBoxLayout()
        category_layout.addWidget(QLabel("📂 Category:"))
        
        self.category_combo = QComboBox()
        self.category_combo.addItems(['All', 'starters', 'main_course', 'desserts', 'beverages'])
        self.category_combo.currentTextChanged.connect(self.filter_menu_items)
        
        category_layout.addWidget(self.category_combo)
        
        menu_header_layout.addLayout(search_layout)
        menu_header_layout.addLayout(category_layout)
        
        menu_layout.addLayout(menu_header_layout)
        
        # Menu items with enhanced display
        self.menu_table = QTableWidget()
        self.menu_table.setColumnCount(6)
        self.menu_table.setHorizontalHeaderLabels(['Item', 'Price', 'Category', 'Available', 'Description', 'Add'])
        self.menu_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.menu_table.setMaximumHeight(350)
        self.menu_table.setAlternatingRowColors(True)
        
        menu_layout.addWidget(self.menu_table)
        
        # Menu statistics
        self.menu_stats_label = QLabel("Menu Statistics")
        self.menu_stats_label.setFont(QFont("Arial", 9))
        self.menu_stats_label.setStyleSheet(f"color: {THEME_COLORS['dark']}; font-style: italic;")
        
        menu_layout.addWidget(self.menu_stats_label)
        
        layout.addWidget(menu_group)
    
    def create_order_section(self, layout):
        """Create enhanced current order section"""
        order_group = QGroupBox("📝 Current Order")
        order_layout = QVBoxLayout(order_group)
        
        # Order info with enhanced display
        self.order_info_label = QLabel("🪑 No table selected")
        self.order_info_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.order_info_label.setStyleSheet(f"""
            QLabel {{
                color: {THEME_COLORS['primary']};
                background-color: {THEME_COLORS['light']};
                border: 2px solid {THEME_COLORS['primary']};
                border-radius: 8px;
                padding: 10px;
            }}
        """)
        self.order_info_label.setAlignment(Qt.AlignCenter)
        
        order_layout.addWidget(self.order_info_label)
        
        # Order status indicator
        self.order_status_label = QLabel("Status: Ready to take order")
        self.order_status_label.setFont(QFont("Arial", 10))
        self.order_status_label.setStyleSheet(f"color: {THEME_COLORS['success']}; font-weight: bold;")
        self.order_status_label.setAlignment(Qt.AlignCenter)
        
        order_layout.addWidget(self.order_status_label)
        
        # Order notes with enhanced styling
        notes_layout = QVBoxLayout()
        notes_layout.addWidget(QLabel("📝 Special Instructions:"))
        
        self.order_notes = QTextEdit()
        self.order_notes.setMaximumHeight(80)
        self.order_notes.setPlaceholderText("Enter special instructions for the kitchen (e.g., 'No onions', 'Extra spicy', 'Well done')...")
        self.order_notes.setStyleSheet(f"""
            QTextEdit {{
                border: 2px solid {THEME_COLORS['primary']};
                border-radius: 6px;
                padding: 8px;
                background-color: white;
                font-size: 11px;
            }}
            QTextEdit:focus {{
                border-color: {THEME_COLORS['secondary']};
            }}
        """)
        
        notes_layout.addWidget(self.order_notes)
        order_layout.addLayout(notes_layout)
        
        layout.addWidget(order_group)
    
    def create_order_items_section(self, layout):
        """Create enhanced order items section"""
        items_group = QGroupBox("🛒 Order Items")
        items_layout = QVBoxLayout(items_group)
        
        # Order items table with enhanced styling
        self.order_items_table = QTableWidget()
        self.order_items_table.setColumnCount(6)
        self.order_items_table.setHorizontalHeaderLabels(['Item', 'Qty', 'Unit Price', 'Total', 'Notes', 'Remove'])
        self.order_items_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.order_items_table.setAlternatingRowColors(True)
        self.order_items_table.setStyleSheet(f"""
            QTableWidget {{
                gridline-color: {THEME_COLORS['primary']};
                background-color: white;
                alternate-background-color: {THEME_COLORS['light']};
            }}
            QTableWidget::item {{
                padding: 8px;
                border-bottom: 1px solid #ddd;
            }}
            QTableWidget::item:selected {{
                background-color: {THEME_COLORS['primary']};
                color: white;
            }}
        """)
        
        items_layout.addWidget(self.order_items_table)
        
        # Order summary with enhanced display
        summary_layout = QHBoxLayout()
        
        # Item count
        self.item_count_label = QLabel("Items: 0")
        self.item_count_label.setFont(QFont("Arial", 10))
        self.item_count_label.setStyleSheet(f"color: {THEME_COLORS['dark']};")
        
        # Total amount with enhanced styling
        self.total_label = QLabel("💰 Total: $0.00")
        self.total_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.total_label.setStyleSheet(f"""
            QLabel {{
                color: {THEME_COLORS['success']};
                background-color: {THEME_COLORS['light']};
                border: 2px solid {THEME_COLORS['success']};
                border-radius: 8px;
                padding: 10px;
            }}
        """)
        self.total_label.setAlignment(Qt.AlignCenter)
        
        summary_layout.addWidget(self.item_count_label)
        summary_layout.addStretch()
        summary_layout.addWidget(self.total_label)
        
        items_layout.addLayout(summary_layout)
        
        layout.addWidget(items_group)
    
    def create_buttons_section(self, layout):
        """Create enhanced action buttons section"""
        buttons_group = QGroupBox("🚀 Order Actions")
        buttons_layout = QVBoxLayout(buttons_group)
        
        # Main action buttons
        main_buttons_layout = QHBoxLayout()
        
        # Place order button with enhanced styling
        self.place_order_button = QPushButton("📤 Send to Kitchen")
        self.place_order_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.place_order_button.setMinimumHeight(50)
        self.place_order_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEME_COLORS['success']};
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {THEME_COLORS['primary']};
                transform: scale(1.05);
            }}
            QPushButton:pressed {{
                background-color: {THEME_COLORS['dark']};
            }}
        """)
        self.place_order_button.clicked.connect(self.place_order)
        
        # Clear order button
        self.clear_order_button = QPushButton("🗑️ Clear Order")
        self.clear_order_button.setFont(QFont("Arial", 12))
        self.clear_order_button.setMinimumHeight(40)
        self.clear_order_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEME_COLORS['warning']};
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {THEME_COLORS['secondary']};
            }}
        """)
        self.clear_order_button.clicked.connect(self.clear_order)
        
        main_buttons_layout.addWidget(self.place_order_button)
        main_buttons_layout.addWidget(self.clear_order_button)
        
        buttons_layout.addLayout(main_buttons_layout)
        
        # Secondary action buttons
        secondary_buttons_layout = QHBoxLayout()
        
        # View orders button
        self.view_orders_button = QPushButton("📋 My Orders")
        self.view_orders_button.setFont(QFont("Arial", 11))
        self.view_orders_button.setMinimumHeight(35)
        self.view_orders_button.clicked.connect(self.view_my_orders)
        
        # Quick order button
        self.quick_order_button = QPushButton("⚡ Quick Order")
        self.quick_order_button.setFont(QFont("Arial", 11))
        self.quick_order_button.setMinimumHeight(35)
        self.quick_order_button.clicked.connect(self.quick_order)
        
        # Notifications button
        self.notifications_button = QPushButton("🔔 Notifications")
        self.notifications_button.setFont(QFont("Arial", 11))
        self.notifications_button.setMinimumHeight(35)
        self.notifications_button.clicked.connect(self.show_notifications)
        
        secondary_buttons_layout.addWidget(self.view_orders_button)
        secondary_buttons_layout.addWidget(self.quick_order_button)
        secondary_buttons_layout.addWidget(self.notifications_button)
        
        buttons_layout.addLayout(secondary_buttons_layout)
        
        # Real-time status indicator
        self.realtime_status_label = QLabel("🟢 Connected - Real-time updates active")
        self.realtime_status_label.setFont(QFont("Arial", 9))
        self.realtime_status_label.setStyleSheet(f"color: {THEME_COLORS['success']}; font-weight: bold;")
        self.realtime_status_label.setAlignment(Qt.AlignCenter)
        
        buttons_layout.addWidget(self.realtime_status_label)
        
        layout.addWidget(buttons_group)
    
    def setup_timers(self):
        """Setup timers for periodic updates"""
        # Timer for refreshing data
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_data)
        self.refresh_timer.start(5000)  # Refresh every 5 seconds
    
    def initialize(self):
        """Initialize the window with current user data"""
        self.current_user = auth_service.get_current_user()
        if self.current_user:
            self.load_tables()
            self.load_menu_items()
            self.update_status("Ready to take orders")
    
    def load_tables(self):
        """Load tables data"""
        try:
            tables = table_service.get_all_tables()
            
            self.tables_table.setRowCount(len(tables))
            
            for row, table in enumerate(tables):
                # Table number
                self.tables_table.setItem(row, 0, QTableWidgetItem(str(table['table_number'])))
                
                # Capacity
                self.tables_table.setItem(row, 1, QTableWidgetItem(str(table['capacity'])))
                
                # Status
                status_item = QTableWidgetItem(table['status'].title())
                status_color = TABLE_STATUS_COLORS.get(table['status'], THEME_COLORS['dark'])
                status_item.setBackground(QColor(status_color))
                status_item.setForeground(QColor('white'))
                self.tables_table.setItem(row, 2, status_item)
                
                # Action button
                if table['status'] == 'free':
                    action_button = QPushButton("Select")
                    action_button.clicked.connect(lambda checked, t=table: self.select_table(t))
                    self.tables_table.setCellWidget(row, 3, action_button)
                else:
                    action_item = QTableWidgetItem("Occupied")
                    self.tables_table.setItem(row, 3, action_item)
            
        except Exception as e:
            logger.error(f"Error loading tables: {e}")
            self.update_status(f"Error loading tables: {e}")
    
    def load_menu_items(self):
        """Load menu items with enhanced display"""
        try:
            category = self.category_combo.currentText()
            category_filter = None if category == 'All' else category
            
            menu_items = menu_service.get_all_menu_items(category=category_filter)
            
            self.menu_table.setRowCount(len(menu_items))
            
            available_count = 0
            total_count = len(menu_items)
            
            for row, item in enumerate(menu_items):
                # Item name with emoji based on category
                category_emoji = {
                    'starters': '🥗',
                    'main_course': '🍖',
                    'desserts': '🍰',
                    'beverages': '🥤'
                }.get(item['category'], '🍽️')
                
                item_name = f"{category_emoji} {item['name']}"
                self.menu_table.setItem(row, 0, QTableWidgetItem(item_name))
                
                # Price with styling
                price_item = QTableWidgetItem(f"${item['price']:.2f}")
                price_item.setFont(QFont("Arial", 10, QFont.Bold))
                self.menu_table.setItem(row, 1, price_item)
                
                # Category
                category_name = item['category'].replace('_', ' ').title()
                self.menu_table.setItem(row, 2, QTableWidgetItem(category_name))
                
                # Availability status
                if item['is_available']:
                    available_item = QTableWidgetItem("✅ Available")
                    available_item.setBackground(QColor(THEME_COLORS['success']))
                    available_item.setForeground(QColor('white'))
                    available_count += 1
                else:
                    available_item = QTableWidgetItem("❌ Unavailable")
                    available_item.setBackground(QColor(THEME_COLORS['warning']))
                    available_item.setForeground(QColor('white'))
                
                self.menu_table.setItem(row, 3, available_item)
                
                # Description (truncated)
                description = item['description'][:50] + "..." if len(item['description']) > 50 else item['description']
                self.menu_table.setItem(row, 4, QTableWidgetItem(description))
                
                # Add button with enhanced styling
                add_button = QPushButton("➕ Add to Order")
                add_button.setEnabled(item['is_available'])
                if item['is_available']:
                    add_button.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {THEME_COLORS['success']};
                            color: white;
                            border: none;
                            border-radius: 4px;
                            padding: 5px;
                            font-weight: bold;
                        }}
                        QPushButton:hover {{
                            background-color: {THEME_COLORS['primary']};
                        }}
                        QPushButton:disabled {{
                            background-color: #ccc;
                            color: #666;
                        }}
                    """)
                else:
                    add_button.setStyleSheet("""
                        QPushButton {
                            background-color: #ccc;
                            color: #666;
                            border: none;
                            border-radius: 4px;
                            padding: 5px;
                        }
                    """)
                
                add_button.clicked.connect(lambda checked, i=item: self.add_menu_item(i))
                self.menu_table.setCellWidget(row, 5, add_button)
            
            # Update menu statistics
            self.menu_stats_label.setText(f"📊 Menu: {available_count}/{total_count} items available")
            
        except Exception as e:
            logger.error(f"Error loading menu items: {e}")
            self.update_status(f"Error loading menu items: {e}")
    
    def search_menu_items(self):
        """Search menu items based on search input"""
        search_term = self.search_input.text().strip().lower()
        if not search_term:
            self.load_menu_items()
            return
        
        try:
            # Get all menu items and filter by search term
            all_items = menu_service.get_all_menu_items()
            filtered_items = []
            
            for item in all_items:
                if (search_term in item['name'].lower() or 
                    search_term in item['description'].lower() or
                    search_term in item['category'].lower()):
                    filtered_items.append(item)
            
            # Update table with filtered results
            self.menu_table.setRowCount(len(filtered_items))
            
            available_count = 0
            total_count = len(filtered_items)
            
            for row, item in enumerate(filtered_items):
                # Item name with emoji
                category_emoji = {
                    'starters': '🥗',
                    'main_course': '🍖',
                    'desserts': '🍰',
                    'beverages': '🥤'
                }.get(item['category'], '🍽️')
                
                item_name = f"{category_emoji} {item['name']}"
                self.menu_table.setItem(row, 0, QTableWidgetItem(item_name))
                
                # Price
                price_item = QTableWidgetItem(f"${item['price']:.2f}")
                price_item.setFont(QFont("Arial", 10, QFont.Bold))
                self.menu_table.setItem(row, 1, price_item)
                
                # Category
                category_name = item['category'].replace('_', ' ').title()
                self.menu_table.setItem(row, 2, QTableWidgetItem(category_name))
                
                # Availability
                if item['is_available']:
                    available_item = QTableWidgetItem("✅ Available")
                    available_item.setBackground(QColor(THEME_COLORS['success']))
                    available_item.setForeground(QColor('white'))
                    available_count += 1
                else:
                    available_item = QTableWidgetItem("❌ Unavailable")
                    available_item.setBackground(QColor(THEME_COLORS['warning']))
                    available_item.setForeground(QColor('white'))
                
                self.menu_table.setItem(row, 3, available_item)
                
                # Description
                description = item['description'][:50] + "..." if len(item['description']) > 50 else item['description']
                self.menu_table.setItem(row, 4, QTableWidgetItem(description))
                
                # Add button
                add_button = QPushButton("➕ Add to Order")
                add_button.setEnabled(item['is_available'])
                if item['is_available']:
                    add_button.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {THEME_COLORS['success']};
                            color: white;
                            border: none;
                            border-radius: 4px;
                            padding: 5px;
                            font-weight: bold;
                        }}
                        QPushButton:hover {{
                            background-color: {THEME_COLORS['primary']};
                        }}
                    """)
                else:
                    add_button.setStyleSheet("""
                        QPushButton {
                            background-color: #ccc;
                            color: #666;
                            border: none;
                            border-radius: 4px;
                            padding: 5px;
                        }
                    """)
                
                add_button.clicked.connect(lambda checked, i=item: self.add_menu_item(i))
                self.menu_table.setCellWidget(row, 5, add_button)
            
            # Update statistics
            self.menu_stats_label.setText(f"🔍 Search Results: {available_count}/{total_count} items found")
            
        except Exception as e:
            logger.error(f"Error searching menu items: {e}")
            self.update_status(f"Error searching menu: {e}")
    
    def filter_menu_items(self):
        """Filter menu items by category"""
        self.load_menu_items()
    
    def select_table(self, table):
        """Select a table for taking orders"""
        if table['status'] != 'free':
            QMessageBox.warning(self, "Table Occupied", "This table is already occupied.")
            return
        
        self.selected_table = table
        self.order_info_label.setText(f"Table {table['table_number']} - Capacity: {table['capacity']}")
        self.update_status(f"Selected table {table['table_number']}")
    
    def add_menu_item(self, menu_item):
        """Add menu item to current order"""
        if not self.selected_table:
            QMessageBox.warning(self, "No Table Selected", "Please select a table first.")
            return
        
        # Check if item already exists in order
        for item in self.order_items:
            if item['menu_item_id'] == menu_item['id']:
                item['quantity'] += 1
                self.update_order_items_display()
                return
        
        # Add new item
        self.order_items.append({
            'menu_item_id': menu_item['id'],
            'name': menu_item['name'],
            'price': menu_item['price'],
            'quantity': 1
        })
        
        self.update_order_items_display()
        self.update_status(f"Added {menu_item['name']} to order")
    
    def update_order_items_display(self):
        """Update the order items table display with enhanced styling"""
        self.order_items_table.setRowCount(len(self.order_items))
        
        total_amount = 0
        
        for row, item in enumerate(self.order_items):
            # Item name with emoji
            category_emoji = {
                'starters': '🥗',
                'main_course': '🍖',
                'desserts': '🍰',
                'beverages': '🥤'
            }.get(item.get('category', ''), '🍽️')
            
            item_name = f"{category_emoji} {item['name']}"
            self.order_items_table.setItem(row, 0, QTableWidgetItem(item_name))
            
            # Quantity with styling
            qty_item = QTableWidgetItem(f"x{item['quantity']}")
            qty_item.setFont(QFont("Arial", 10, QFont.Bold))
            self.order_items_table.setItem(row, 1, qty_item)
            
            # Unit price
            price_item = QTableWidgetItem(f"${item['price']:.2f}")
            price_item.setFont(QFont("Arial", 10))
            self.order_items_table.setItem(row, 2, price_item)
            
            # Total with enhanced styling
            item_total = item['price'] * item['quantity']
            total_amount += item_total
            total_item = QTableWidgetItem(f"${item_total:.2f}")
            total_item.setFont(QFont("Arial", 10, QFont.Bold))
            total_item.setBackground(QColor(THEME_COLORS['light']))
            self.order_items_table.setItem(row, 3, total_item)
            
            # Notes column (for special instructions)
            notes_item = QTableWidgetItem(item.get('special_instructions', ''))
            self.order_items_table.setItem(row, 4, notes_item)
            
            # Remove button with enhanced styling
            remove_button = QPushButton("🗑️ Remove")
            remove_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {THEME_COLORS['warning']};
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 5px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {THEME_COLORS['secondary']};
                }}
            """)
            remove_button.clicked.connect(lambda checked, r=row: self.remove_order_item(r))
            self.order_items_table.setCellWidget(row, 5, remove_button)
        
        # Update total with enhanced display
        self.total_label.setText(f"💰 Total: ${total_amount:.2f}")
        self.item_count_label.setText(f"Items: {len(self.order_items)}")
        
        # Update order status
        if len(self.order_items) > 0:
            self.order_status_label.setText("Status: Order ready to send to kitchen")
            self.order_status_label.setStyleSheet(f"color: {THEME_COLORS['success']}; font-weight: bold;")
        else:
            self.order_status_label.setText("Status: Add items to create order")
            self.order_status_label.setStyleSheet(f"color: {THEME_COLORS['warning']}; font-weight: bold;")
    
    def remove_order_item(self, row):
        """Remove item from order"""
        if 0 <= row < len(self.order_items):
            item = self.order_items.pop(row)
            self.update_order_items_display()
            self.update_status(f"Removed {item['name']} from order")
    
    def place_order(self):
        """Place the current order"""
        if not self.selected_table:
            QMessageBox.warning(self, "No Table Selected", "Please select a table first.")
            return
        
        if not self.order_items:
            QMessageBox.warning(self, "Empty Order", "Please add items to the order.")
            return
        
        try:
            # Prepare order items data
            order_items_data = []
            for item in self.order_items:
                order_items_data.append({
                    'menu_item_id': item['menu_item_id'],
                    'quantity': item['quantity'],
                    'special_instructions': ''
                })
            
            # Create order
            order_id = order_service.create_order(
                table_id=self.selected_table['id'],
                waiter_id=self.current_user['id'],
                order_items=order_items_data,
                notes=self.order_notes.toPlainText()
            )
            
            if order_id:
                QMessageBox.information(self, "Order Placed", f"Order #{order_id} has been placed successfully!")
                self.clear_order()
                self.load_tables()  # Refresh tables
                self.update_status("Order placed successfully")
            else:
                QMessageBox.critical(self, "Order Failed", "Failed to place order. Please try again.")
                
        except Exception as e:
            logger.error(f"Error placing order: {e}")
            QMessageBox.critical(self, "Order Error", f"Error placing order:\n{str(e)}")
    
    def clear_order(self):
        """Clear current order"""
        self.selected_table = None
        self.order_items = []
        self.order_notes.clear()
        self.order_info_label.setText("No order selected")
        self.total_label.setText("Total: $0.00")
        self.order_items_table.setRowCount(0)
        self.update_status("Order cleared")
    
    def view_my_orders(self):
        """View waiter's orders"""
        try:
            orders = order_service.get_orders_by_waiter(self.current_user['id'])
            
            if not orders:
                QMessageBox.information(self, "No Orders", "You have no orders yet.")
                return
            
            # Create orders dialog
            from .dialogs.orders_dialog import OrdersDialog
            orders_dialog = OrdersDialog(orders, self)
            orders_dialog.exec_()
            
        except Exception as e:
            logger.error(f"Error loading orders: {e}")
            QMessageBox.critical(self, "Error", f"Error loading orders:\n{str(e)}")
    
    def refresh_data(self):
        """Refresh all data"""
        self.load_tables()
        self.load_menu_items()
    
    def update_status(self, message):
        """Update status message"""
        self.status_label.setText(message)
        logger.info(f"Waiter status: {message}")
    
    def quick_order(self):
        """Quick order functionality for common items"""
        from PyQt5.QtWidgets import QInputDialog
        
        # Get popular items for quick order
        popular_items = [
            "Coffee", "Tea", "Soft Drinks", "Caesar Salad", 
            "Chicken Parmesan", "Pasta Carbonara", "Chocolate Cake"
        ]
        
        item, ok = QInputDialog.getItem(
            self, 
            'Quick Order', 
            'Select item for quick order:', 
            popular_items, 
            0, 
            False
        )
        
        if ok and item:
            # Find the menu item
            menu_items = menu_service.get_all_menu_items()
            selected_item = next((i for i in menu_items if i['name'] == item), None)
            
            if selected_item:
                self.add_menu_item(selected_item)
                self.update_status(f"Quick order: Added {item}")
            else:
                QMessageBox.warning(self, "Item Not Found", f"Could not find {item} in menu.")
    
    def show_notifications(self):
        """Show notifications dialog"""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
        
        dialog = QDialog(self)
        dialog.setWindowTitle("🔔 Notifications")
        dialog.setFixedSize(400, 300)
        
        layout = QVBoxLayout(dialog)
        
        # Notifications content
        notifications_label = QLabel("""
        🔔 SmartDine Notifications
        
        ✅ Real-time order updates active
        ✅ Kitchen notifications enabled
        ✅ Table status monitoring active
        ✅ Menu availability updates active
        
        📱 You will be notified when:
        • New orders are placed
        • Kitchen updates order status
        • Tables become available
        • Menu items become unavailable
        """)
        notifications_label.setFont(QFont("Arial", 10))
        notifications_label.setStyleSheet(f"color: {THEME_COLORS['dark']};")
        
        layout.addWidget(notifications_label)
        
        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)
        
        dialog.exec_()
    
    def clear_data(self):
        """Clear all data when logging out"""
        self.current_user = None
        self.selected_table = None
        self.order_items = []
        self.order_notes.clear()
        self.order_info_label.setText("🪑 No table selected")
        self.total_label.setText("💰 Total: $0.00")
        self.item_count_label.setText("Items: 0")
        self.order_status_label.setText("Status: Ready to take order")
        self.order_items_table.setRowCount(0)
        self.tables_table.setRowCount(0)
        self.menu_table.setRowCount(0)
        self.menu_stats_label.setText("Menu Statistics")
    
    def get_waiter_style(self):
        """Get waiter window stylesheet"""
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
        
        QTextEdit {{
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 5px;
            background-color: white;
        }}
        
        QComboBox {{
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 5px;
            background-color: white;
        }}
        """
