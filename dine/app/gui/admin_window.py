"""
Admin window for SmartDine Desktop Edition
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                            QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                            QGroupBox, QHeaderView, QMessageBox, QFrame,
                            QTabWidget, QTextEdit, QComboBox, QLineEdit,
                            QDoubleSpinBox, QSpinBox, QCheckBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor

from backend.menu_service import menu_service
from backend.table_service import table_service
from backend.auth_service import auth_service
from backend.report_service import report_service
from backend.billing_service import billing_service
from config import THEME_COLORS, MENU_CATEGORIES, USER_ROLES
from utils.logger import logger


class AdminWindow(QWidget):
    """Admin interface for system management"""
    
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
        self.setStyleSheet(self.get_admin_style())
    
    def create_header(self, layout):
        """Create header section"""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.StyledPanel)
        header_layout = QHBoxLayout(header_frame)
        
        # Title
        title_label = QLabel("Admin Dashboard")
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
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Create tabs
        self.create_menu_tab()
        self.create_tables_tab()
        self.create_users_tab()
        self.create_reports_tab()
        self.create_system_tab()
        
        layout.addWidget(self.tab_widget)
    
    def create_menu_tab(self):
        """Create menu management tab"""
        menu_widget = QWidget()
        menu_layout = QVBoxLayout(menu_widget)
        
        # Menu items section
        menu_group = QGroupBox("Menu Items")
        menu_group_layout = QVBoxLayout(menu_group)
        
        # Menu items table
        self.menu_table = QTableWidget()
        self.menu_table.setColumnCount(6)
        self.menu_table.setHorizontalHeaderLabels(['ID', 'Name', 'Price', 'Category', 'Available', 'Action'])
        self.menu_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.menu_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        menu_group_layout.addWidget(self.menu_table)
        
        # Menu actions
        menu_actions_layout = QHBoxLayout()
        
        self.add_menu_button = QPushButton("Add Item")
        self.add_menu_button.clicked.connect(self.add_menu_item)
        
        self.edit_menu_button = QPushButton("Edit Item")
        self.edit_menu_button.clicked.connect(self.edit_menu_item)
        
        self.delete_menu_button = QPushButton("Delete Item")
        self.delete_menu_button.clicked.connect(self.delete_menu_item)
        
        self.toggle_availability_button = QPushButton("Toggle Availability")
        self.toggle_availability_button.clicked.connect(self.toggle_menu_availability)
        
        menu_actions_layout.addWidget(self.add_menu_button)
        menu_actions_layout.addWidget(self.edit_menu_button)
        menu_actions_layout.addWidget(self.delete_menu_button)
        menu_actions_layout.addWidget(self.toggle_availability_button)
        menu_actions_layout.addStretch()
        
        menu_group_layout.addLayout(menu_actions_layout)
        menu_layout.addWidget(menu_group)
        
        self.tab_widget.addTab(menu_widget, "Menu Management")
    
    def create_tables_tab(self):
        """Create tables management tab"""
        tables_widget = QWidget()
        tables_layout = QVBoxLayout(tables_widget)
        
        # Tables section
        tables_group = QGroupBox("Tables")
        tables_group_layout = QVBoxLayout(tables_group)
        
        # Tables table
        self.tables_table = QTableWidget()
        self.tables_table.setColumnCount(4)
        self.tables_table.setHorizontalHeaderLabels(['Table #', 'Capacity', 'Status', 'Action'])
        self.tables_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tables_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        tables_group_layout.addWidget(self.tables_table)
        
        # Table actions
        table_actions_layout = QHBoxLayout()
        
        self.add_table_button = QPushButton("Add Table")
        self.add_table_button.clicked.connect(self.add_table)
        
        self.edit_table_button = QPushButton("Edit Table")
        self.edit_table_button.clicked.connect(self.edit_table)
        
        self.delete_table_button = QPushButton("Delete Table")
        self.delete_table_button.clicked.connect(self.delete_table)
        
        table_actions_layout.addWidget(self.add_table_button)
        table_actions_layout.addWidget(self.edit_table_button)
        table_actions_layout.addWidget(self.delete_table_button)
        table_actions_layout.addStretch()
        
        tables_group_layout.addLayout(table_actions_layout)
        tables_layout.addWidget(tables_group)
        
        # Table statistics
        stats_group = QGroupBox("Table Statistics")
        stats_layout = QVBoxLayout(stats_group)
        
        self.table_stats_label = QLabel("Loading statistics...")
        self.table_stats_label.setFont(QFont("Arial", 10))
        
        stats_layout.addWidget(self.table_stats_label)
        tables_layout.addWidget(stats_group)
        
        self.tab_widget.addTab(tables_widget, "Table Management")
    
    def create_users_tab(self):
        """Create users management tab"""
        users_widget = QWidget()
        users_layout = QVBoxLayout(users_widget)
        
        # Users section
        users_group = QGroupBox("Users")
        users_group_layout = QVBoxLayout(users_group)
        
        # Users table
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(6)
        self.users_table.setHorizontalHeaderLabels(['ID', 'Username', 'Role', 'Full Name', 'Email', 'Status'])
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.users_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        users_group_layout.addWidget(self.users_table)
        
        # User actions
        user_actions_layout = QHBoxLayout()
        
        self.add_user_button = QPushButton("Add User")
        self.add_user_button.clicked.connect(self.add_user)
        
        self.edit_user_button = QPushButton("Edit User")
        self.edit_user_button.clicked.connect(self.edit_user)
        
        self.deactivate_user_button = QPushButton("Deactivate User")
        self.deactivate_user_button.clicked.connect(self.deactivate_user)
        
        user_actions_layout.addWidget(self.add_user_button)
        user_actions_layout.addWidget(self.edit_user_button)
        user_actions_layout.addWidget(self.deactivate_user_button)
        user_actions_layout.addStretch()
        
        users_group_layout.addLayout(user_actions_layout)
        users_layout.addWidget(users_group)
        
        self.tab_widget.addTab(users_widget, "User Management")
    
    def create_reports_tab(self):
        """Create reports tab"""
        reports_widget = QWidget()
        reports_layout = QVBoxLayout(reports_widget)
        
        # Reports section
        reports_group = QGroupBox("Reports & Analytics")
        reports_group_layout = QVBoxLayout(reports_group)
        
        # Report buttons
        report_buttons_layout = QGridLayout()
        
        self.daily_sales_button = QPushButton("Daily Sales Report")
        self.daily_sales_button.clicked.connect(self.generate_daily_sales_report)
        
        self.sales_summary_button = QPushButton("Sales Summary")
        self.sales_summary_button.clicked.connect(self.generate_sales_summary)
        
        self.top_items_button = QPushButton("Top Menu Items")
        self.top_items_button.clicked.connect(self.generate_top_items_report)
        
        self.revenue_report_button = QPushButton("Revenue Report")
        self.revenue_report_button.clicked.connect(self.generate_revenue_report)
        
        report_buttons_layout.addWidget(self.daily_sales_button, 0, 0)
        report_buttons_layout.addWidget(self.sales_summary_button, 0, 1)
        report_buttons_layout.addWidget(self.top_items_button, 1, 0)
        report_buttons_layout.addWidget(self.revenue_report_button, 1, 1)
        
        reports_group_layout.addLayout(report_buttons_layout)
        
        # Report output
        self.report_output = QTextEdit()
        self.report_output.setReadOnly(True)
        self.report_output.setMaximumHeight(300)
        self.report_output.setPlaceholderText("Report output will appear here...")
        
        reports_group_layout.addWidget(QLabel("Report Output:"))
        reports_group_layout.addWidget(self.report_output)
        
        reports_layout.addWidget(reports_group)
        
        self.tab_widget.addTab(reports_widget, "Reports & Analytics")
    
    def create_system_tab(self):
        """Create system management tab"""
        system_widget = QWidget()
        system_layout = QVBoxLayout(system_widget)
        
        # System info section
        system_group = QGroupBox("System Information")
        system_group_layout = QVBoxLayout(system_group)
        
        self.system_info_label = QLabel("Loading system information...")
        self.system_info_label.setFont(QFont("Arial", 10))
        
        system_group_layout.addWidget(self.system_info_label)
        system_layout.addWidget(system_group)
        
        # Database section
        db_group = QGroupBox("Database Management")
        db_group_layout = QVBoxLayout(db_group)
        
        db_actions_layout = QHBoxLayout()
        
        self.backup_db_button = QPushButton("Backup Database")
        self.backup_db_button.clicked.connect(self.backup_database)
        
        self.refresh_data_button = QPushButton("Refresh All Data")
        self.refresh_data_button.clicked.connect(self.refresh_all_data)
        
        db_actions_layout.addWidget(self.backup_db_button)
        db_actions_layout.addWidget(self.refresh_data_button)
        db_actions_layout.addStretch()
        
        db_group_layout.addLayout(db_actions_layout)
        system_layout.addWidget(db_group)
        
        self.tab_widget.addTab(system_widget, "System Management")
    
    def setup_timers(self):
        """Setup timers for periodic updates"""
        # Timer for refreshing data
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_data)
        self.refresh_timer.start(30000)  # Refresh every 30 seconds
    
    def initialize(self):
        """Initialize the window with current user data"""
        self.current_user = auth_service.get_current_user()
        if self.current_user:
            self.load_menu_items()
            self.load_tables()
            self.load_users()
            self.load_system_info()
            self.update_status("Admin dashboard ready")
    
    def load_menu_items(self):
        """Load menu items"""
        try:
            menu_items = menu_service.get_all_menu_items(available_only=False)
            
            self.menu_table.setRowCount(len(menu_items))
            
            for row, item in enumerate(menu_items):
                # ID
                self.menu_table.setItem(row, 0, QTableWidgetItem(str(item['id'])))
                
                # Name
                self.menu_table.setItem(row, 1, QTableWidgetItem(item['name']))
                
                # Price
                self.menu_table.setItem(row, 2, QTableWidgetItem(f"${item['price']:.2f}"))
                
                # Category
                self.menu_table.setItem(row, 3, QTableWidgetItem(item['category'].replace('_', ' ').title()))
                
                # Available
                available_item = QTableWidgetItem("Yes" if item['is_available'] else "No")
                if item['is_available']:
                    available_item.setBackground(QColor(THEME_COLORS['success']))
                    available_item.setForeground(QColor('white'))
                else:
                    available_item.setBackground(QColor(THEME_COLORS['warning']))
                    available_item.setForeground(QColor('white'))
                
                self.menu_table.setItem(row, 4, available_item)
                
                # Action button
                action_button = QPushButton("Edit")
                action_button.clicked.connect(lambda checked, i=item: self.edit_menu_item_dialog(i))
                self.menu_table.setCellWidget(row, 5, action_button)
            
        except Exception as e:
            logger.error(f"Error loading menu items: {e}")
            self.update_status(f"Error loading menu items: {e}")
    
    def load_tables(self):
        """Load tables"""
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
                if table['status'] == 'free':
                    status_item.setBackground(QColor(THEME_COLORS['success']))
                elif table['status'] == 'occupied':
                    status_item.setBackground(QColor(THEME_COLORS['warning']))
                else:
                    status_item.setBackground(QColor(THEME_COLORS['dark']))
                
                status_item.setForeground(QColor('white'))
                self.tables_table.setItem(row, 2, status_item)
                
                # Action button
                action_button = QPushButton("Edit")
                action_button.clicked.connect(lambda checked, t=table: self.edit_table_dialog(t))
                self.tables_table.setCellWidget(row, 3, action_button)
            
            # Update table statistics
            self.update_table_statistics()
            
        except Exception as e:
            logger.error(f"Error loading tables: {e}")
            self.update_status(f"Error loading tables: {e}")
    
    def load_users(self):
        """Load users"""
        try:
            users = auth_service.get_all_users()
            
            self.users_table.setRowCount(len(users))
            
            for row, user in enumerate(users):
                # ID
                self.users_table.setItem(row, 0, QTableWidgetItem(str(user['id'])))
                
                # Username
                self.users_table.setItem(row, 1, QTableWidgetItem(user['username']))
                
                # Role
                self.users_table.setItem(row, 2, QTableWidgetItem(user['role'].title()))
                
                # Full name
                self.users_table.setItem(row, 3, QTableWidgetItem(user['full_name']))
                
                # Email
                self.users_table.setItem(row, 4, QTableWidgetItem(user['email'] or "N/A"))
                
                # Status
                status_item = QTableWidgetItem("Active" if user['is_active'] else "Inactive")
                if user['is_active']:
                    status_item.setBackground(QColor(THEME_COLORS['success']))
                else:
                    status_item.setBackground(QColor(THEME_COLORS['warning']))
                
                status_item.setForeground(QColor('white'))
                self.users_table.setItem(row, 5, status_item)
            
        except Exception as e:
            logger.error(f"Error loading users: {e}")
            self.update_status(f"Error loading users: {e}")
    
    def load_system_info(self):
        """Load system information"""
        try:
            from datetime import datetime
            import os
            
            # Get database size
            db_size = 0
            if os.path.exists("smartdine.db"):
                db_size = os.path.getsize("smartdine.db")
            
            # Get current time
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            system_info = f"""
            System Information:
            Current Time: {current_time}
            Database Size: {db_size / 1024:.2f} KB
            Application Version: 1.0.0
            Python Version: {os.sys.version}
            """
            
            self.system_info_label.setText(system_info)
            
        except Exception as e:
            logger.error(f"Error loading system info: {e}")
            self.system_info_label.setText(f"Error loading system information: {e}")
    
    def update_table_statistics(self):
        """Update table statistics"""
        try:
            stats = table_service.get_table_statistics()
            stats_text = f"""
            Table Statistics:
            Total Tables: {stats['total_tables']}
            Free Tables: {stats['free_tables']}
            Occupied Tables: {stats['occupied_tables']}
            Served Tables: {stats['served_tables']}
            Billed Tables: {stats['billed_tables']}
            Occupancy Rate: {stats['occupancy_rate']:.1f}%
            """
            self.table_stats_label.setText(stats_text)
            
        except Exception as e:
            logger.error(f"Error updating table statistics: {e}")
            self.table_stats_label.setText(f"Error loading statistics: {e}")
    
    def add_menu_item(self):
        """Add new menu item"""
        from .dialogs.menu_item_dialog import MenuItemDialog
        dialog = MenuItemDialog(self)
        if dialog.exec_() == dialog.Accepted:
            self.load_menu_items()
            self.update_status("Menu item added")
    
    def edit_menu_item(self):
        """Edit selected menu item"""
        current_row = self.menu_table.currentRow()
        if current_row >= 0:
            item_id = int(self.menu_table.item(current_row, 0).text())
            item = menu_service.get_menu_item(item_id)
            if item:
                from .dialogs.menu_item_dialog import MenuItemDialog
                dialog = MenuItemDialog(self, item)
                if dialog.exec_() == dialog.Accepted:
                    self.load_menu_items()
                    self.update_status("Menu item updated")
    
    def edit_menu_item_dialog(self, item):
        """Edit menu item dialog"""
        from .dialogs.menu_item_dialog import MenuItemDialog
        dialog = MenuItemDialog(self, item)
        if dialog.exec_() == dialog.Accepted:
            self.load_menu_items()
            self.update_status("Menu item updated")
    
    def delete_menu_item(self):
        """Delete selected menu item"""
        current_row = self.menu_table.currentRow()
        if current_row >= 0:
            item_id = int(self.menu_table.item(current_row, 0).text())
            item_name = self.menu_table.item(current_row, 1).text()
            
            reply = QMessageBox.question(
                self, "Delete Menu Item",
                f"Are you sure you want to delete '{item_name}'?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                success = menu_service.delete_menu_item(item_id)
                if success:
                    self.load_menu_items()
                    self.update_status(f"Menu item '{item_name}' deleted")
                else:
                    QMessageBox.warning(self, "Delete Failed", "Failed to delete menu item.")
    
    def toggle_menu_availability(self):
        """Toggle menu item availability"""
        current_row = self.menu_table.currentRow()
        if current_row >= 0:
            item_id = int(self.menu_table.item(current_row, 0).text())
            success = menu_service.toggle_availability(item_id)
            if success:
                self.load_menu_items()
                self.update_status("Menu item availability toggled")
            else:
                QMessageBox.warning(self, "Toggle Failed", "Failed to toggle availability.")
    
    def add_table(self):
        """Add new table"""
        from .dialogs.table_dialog import TableDialog
        dialog = TableDialog(self)
        if dialog.exec_() == dialog.Accepted:
            self.load_tables()
            self.update_status("Table added")
    
    def edit_table(self):
        """Edit selected table"""
        current_row = self.tables_table.currentRow()
        if current_row >= 0:
            table_number = int(self.tables_table.item(current_row, 0).text())
            tables = table_service.get_all_tables()
            table = next((t for t in tables if t['table_number'] == table_number), None)
            if table:
                from .dialogs.table_dialog import TableDialog
                dialog = TableDialog(self, table)
                if dialog.exec_() == dialog.Accepted:
                    self.load_tables()
                    self.update_status("Table updated")
    
    def edit_table_dialog(self, table):
        """Edit table dialog"""
        from .dialogs.table_dialog import TableDialog
        dialog = TableDialog(self, table)
        if dialog.exec_() == dialog.Accepted:
            self.load_tables()
            self.update_status("Table updated")
    
    def delete_table(self):
        """Delete selected table"""
        current_row = self.tables_table.currentRow()
        if current_row >= 0:
            table_number = int(self.tables_table.item(current_row, 0).text())
            
            reply = QMessageBox.question(
                self, "Delete Table",
                f"Are you sure you want to delete table {table_number}?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                tables = table_service.get_all_tables()
                table = next((t for t in tables if t['table_number'] == table_number), None)
                if table:
                    success = table_service.delete_table(table['id'])
                    if success:
                        self.load_tables()
                        self.update_status(f"Table {table_number} deleted")
                    else:
                        QMessageBox.warning(self, "Delete Failed", "Failed to delete table.")
    
    def add_user(self):
        """Add new user"""
        from .dialogs.user_dialog import UserDialog
        dialog = UserDialog(self)
        if dialog.exec_() == dialog.Accepted:
            self.load_users()
            self.update_status("User added")
    
    def edit_user(self):
        """Edit selected user"""
        current_row = self.users_table.currentRow()
        if current_row >= 0:
            user_id = int(self.users_table.item(current_row, 0).text())
            user = auth_service.get_user_by_id(user_id)
            if user:
                from .dialogs.user_dialog import UserDialog
                dialog = UserDialog(self, user)
                if dialog.exec_() == dialog.Accepted:
                    self.load_users()
                    self.update_status("User updated")
    
    def deactivate_user(self):
        """Deactivate selected user"""
        current_row = self.users_table.currentRow()
        if current_row >= 0:
            user_id = int(self.users_table.item(current_row, 0).text())
            username = self.users_table.item(current_row, 1).text()
            
            reply = QMessageBox.question(
                self, "Deactivate User",
                f"Are you sure you want to deactivate user '{username}'?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                success = auth_service.deactivate_user(user_id)
                if success:
                    self.load_users()
                    self.update_status(f"User '{username}' deactivated")
                else:
                    QMessageBox.warning(self, "Deactivate Failed", "Failed to deactivate user.")
    
    def generate_daily_sales_report(self):
        """Generate daily sales report"""
        try:
            from datetime import date
            summary = billing_service.get_daily_sales_summary()
            
            report_text = f"""
            Daily Sales Report - {summary['date']}
            ======================================
            
            Total Bills: {summary['total_bills']}
            Total Revenue: ${summary['total_revenue']:.2f}
            Total Tax: ${summary['total_tax']:.2f}
            Total Discount: ${summary['total_discount']:.2f}
            Average Bill: ${summary['average_bill_amount']:.2f}
            
            Payment Methods:
            """
            
            for method, count in summary['payment_methods'].items():
                report_text += f"  {method.upper()}: {count}\n"
            
            self.report_output.setText(report_text)
            self.update_status("Daily sales report generated")
            
        except Exception as e:
            logger.error(f"Error generating daily sales report: {e}")
            self.report_output.setText(f"Error generating report: {e}")
    
    def generate_sales_summary(self):
        """Generate sales summary report"""
        try:
            from datetime import date, timedelta
            
            end_date = date.today()
            start_date = end_date - timedelta(days=7)  # Last 7 days
            
            summary = report_service.get_sales_summary(start_date, end_date)
            
            report_text = f"""
            Sales Summary Report
            ====================
            Period: {start_date} to {end_date}
            
            Total Revenue: ${summary['total_revenue']:.2f}
            Total Bills: {summary['total_bills']}
            Total Tax: ${summary['total_tax']:.2f}
            Total Discount: ${summary['total_discount']:.2f}
            Average Bill: ${summary['average_bill']:.2f}
            """
            
            self.report_output.setText(report_text)
            self.update_status("Sales summary report generated")
            
        except Exception as e:
            logger.error(f"Error generating sales summary: {e}")
            self.report_output.setText(f"Error generating report: {e}")
    
    def generate_top_items_report(self):
        """Generate top items report"""
        try:
            from datetime import date, timedelta
            
            end_date = date.today()
            start_date = end_date - timedelta(days=7)  # Last 7 days
            
            top_items = report_service.get_top_menu_items(start_date, end_date, limit=10)
            
            report_text = f"""
            Top Menu Items Report
            =====================
            Period: {start_date} to {end_date}
            
            Rank | Item Name | Quantity | Revenue
            -----|-----------|----------|---------
            """
            
            for i, item in enumerate(top_items, 1):
                report_text += f"{i:4d} | {item['name'][:20]:20s} | {item['total_quantity']:8d} | ${item['total_revenue']:8.2f}\n"
            
            self.report_output.setText(report_text)
            self.update_status("Top items report generated")
            
        except Exception as e:
            logger.error(f"Error generating top items report: {e}")
            self.report_output.setText(f"Error generating report: {e}")
    
    def generate_revenue_report(self):
        """Generate revenue report"""
        try:
            from datetime import date, timedelta
            
            end_date = date.today()
            start_date = end_date - timedelta(days=7)  # Last 7 days
            
            revenue_data = report_service.get_revenue_by_date(start_date, end_date)
            
            report_text = f"""
            Revenue Report
            =============
            Period: {start_date} to {end_date}
            
            Date       | Bills | Revenue  | Tax      | Discount
            -----------|-------|----------|----------|----------
            """
            
            for day in revenue_data:
                report_text += f"{day['date']} | {day['bill_count']:5d} | ${day['revenue']:8.2f} | ${day['tax']:8.2f} | ${day['discount']:8.2f}\n"
            
            self.report_output.setText(report_text)
            self.update_status("Revenue report generated")
            
        except Exception as e:
            logger.error(f"Error generating revenue report: {e}")
            self.report_output.setText(f"Error generating report: {e}")
    
    def backup_database(self):
        """Backup database"""
        try:
            import shutil
            from datetime import datetime
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"smartdine_backup_{timestamp}.db"
            
            shutil.copy2("smartdine.db", backup_filename)
            
            QMessageBox.information(self, "Backup Complete", f"Database backed up as {backup_filename}")
            self.update_status("Database backup completed")
            
        except Exception as e:
            logger.error(f"Error backing up database: {e}")
            QMessageBox.critical(self, "Backup Failed", f"Error backing up database:\n{str(e)}")
    
    def refresh_all_data(self):
        """Refresh all data"""
        self.load_menu_items()
        self.load_tables()
        self.load_users()
        self.load_system_info()
        self.update_status("All data refreshed")
    
    def refresh_data(self):
        """Refresh data periodically"""
        self.load_system_info()
    
    def update_status(self, message):
        """Update status message"""
        self.status_label.setText(message)
        logger.info(f"Admin status: {message}")
    
    def clear_data(self):
        """Clear all data when logging out"""
        self.current_user = None
        self.menu_table.setRowCount(0)
        self.tables_table.setRowCount(0)
        self.users_table.setRowCount(0)
        self.report_output.clear()
        self.system_info_label.setText("Loading system information...")
        self.table_stats_label.setText("Loading statistics...")
    
    def get_admin_style(self):
        """Get admin window stylesheet"""
        return f"""
        QWidget {{
            background-color: {THEME_COLORS['light']};
        }}
        
        QTabWidget::pane {{
            border: 1px solid {THEME_COLORS['primary']};
            border-radius: 5px;
        }}
        
        QTabBar::tab {{
            background-color: {THEME_COLORS['primary']};
            color: white;
            padding: 8px 16px;
            margin-right: 2px;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
        }}
        
        QTabBar::tab:selected {{
            background-color: white;
            color: {THEME_COLORS['primary']};
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
            font-family: 'Courier New', monospace;
        }}
        """
