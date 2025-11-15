"""
EzMart E-Commerce Analytics Dashboard
A full-stack Python GUI application with SQLite database
Author: Senior Full-Stack Developer
Version: 1.0.0
"""

import sys
import sqlite3
import json
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QFrame, QScrollArea, QGridLayout,
    QProgressBar, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt, QTimer, QSize, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor, QPainter, QPen
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QPieSeries, QBarSeries, QBarSet, QValueAxis, QBarCategoryAxis
import random


class DatabaseManager:
    """Handles all database operations for the EzMart dashboard"""
    
    def __init__(self, db_name="ezmart.db"):
        self.db_name = db_name
        self.init_database()
        self.populate_sample_data()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER NOT NULL,
                sold INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_date DATE NOT NULL,
                total_amount REAL NOT NULL,
                status TEXT NOT NULL,
                country TEXT NOT NULL
            )
        ''')
        
        # Analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                revenue REAL NOT NULL,
                orders INTEGER NOT NULL,
                visitors INTEGER NOT NULL
            )
        ''')
        
        # Traffic sources table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS traffic_sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                percentage REAL NOT NULL,
                visits INTEGER NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def populate_sample_data(self):
        """Populate database with sample e-commerce data"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM products")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        # Sample products
        products = [
            # Electronics
            ("iPhone 15 Pro", "Electronics", 1199.99, 45, 234),
            ("Samsung Galaxy S24", "Electronics", 999.99, 67, 189),
            ("MacBook Pro M3", "Electronics", 2499.99, 23, 78),
            ("Sony WH-1000XM5", "Electronics", 399.99, 120, 345),
            ("iPad Air", "Electronics", 699.99, 89, 267),
            
            # Fashion
            ("Nike Air Max", "Fashion", 159.99, 234, 567),
            ("Levi's Jeans", "Fashion", 79.99, 0, 432),  # Out of stock
            ("Adidas Hoodie", "Fashion", 89.99, 156, 234),
            ("Ray-Ban Sunglasses", "Fashion", 199.99, 78, 123),
            ("Leather Jacket", "Fashion", 299.99, 45, 89),
            
            # Home & Kitchen
            ("Dyson Vacuum", "Home & Kitchen", 599.99, 34, 145),
            ("KitchenAid Mixer", "Home & Kitchen", 379.99, 56, 234),
            ("Ninja Air Fryer", "Home & Kitchen", 129.99, 0, 456),  # Out of stock
            ("Instant Pot", "Home & Kitchen", 99.99, 123, 678),
            ("Bedding Set", "Home & Kitchen", 149.99, 89, 234),
            
            # Beauty & Personal Care
            ("Dyson Hair Dryer", "Beauty & Personal Care", 429.99, 67, 123),
            ("Skincare Set", "Beauty & Personal Care", 89.99, 234, 567),
            ("Perfume Collection", "Beauty & Personal Care", 159.99, 0, 234),  # Out of stock
            ("Electric Toothbrush", "Beauty & Personal Care", 149.99, 145, 345),
            ("Makeup Kit", "Beauty & Personal Care", 79.99, 189, 456),
        ]
        
        cursor.executemany(
            "INSERT INTO products (name, category, price, stock, sold) VALUES (?, ?, ?, ?, ?)",
            products
        )
        
        # Sample orders for last 8 days
        countries = ["United States", "United Kingdom", "Indonesia", "Russia", "Canada", "Australia"]
        base_date = datetime.now() - timedelta(days=7)
        
        for i in range(8):
            date = base_date + timedelta(days=i)
            num_orders = random.randint(120, 180)
            
            for _ in range(num_orders):
                amount = random.uniform(50, 1500)
                status = random.choice(["Completed", "Processing", "Shipped", "Delivered"])
                country = random.choice(countries)
                cursor.execute(
                    "INSERT INTO orders (order_date, total_amount, status, country) VALUES (?, ?, ?, ?)",
                    (date.strftime("%Y-%m-%d"), amount, status, country)
                )
        
        # Analytics data for last 8 days
        analytics_data = [
            (base_date + timedelta(days=0), 12500, 145, 28934),
            (base_date + timedelta(days=1), 13200, 158, 30123),
            (base_date + timedelta(days=2), 11800, 142, 27456),
            (base_date + timedelta(days=3), 14100, 169, 31234),
            (base_date + timedelta(days=4), 13800, 165, 29876),
            (base_date + timedelta(days=5), 15200, 178, 33456),
            (base_date + timedelta(days=6), 14600, 171, 31987),
            (base_date + timedelta(days=7), 15800, 182, 34123),
        ]
        
        for data in analytics_data:
            cursor.execute(
                "INSERT INTO analytics (date, revenue, orders, visitors) VALUES (?, ?, ?, ?)",
                (data[0].strftime("%Y-%m-%d"), data[1], data[2], data[3])
            )
        
        # Traffic sources
        traffic_data = [
            ("Direct Traffic", 40.0, 95000),
            ("Organic Search", 30.0, 71000),
            ("Social Media", 15.0, 36000),
            ("Referral Traffic", 10.0, 24000),
            ("Email Campaigns", 5.0, 12000),
        ]
        
        cursor.executemany(
            "INSERT INTO traffic_sources (source, percentage, visits) VALUES (?, ?, ?)",
            traffic_data
        )
        
        conn.commit()
        conn.close()
    
    def get_total_sales(self):
        """Get total sales amount"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(total_amount) FROM orders WHERE status = 'Completed'")
        result = cursor.fetchone()[0] or 0
        conn.close()
        return result
    
    def get_total_orders(self):
        """Get total number of orders"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM orders")
        result = cursor.fetchone()[0]
        conn.close()
        return result
    
    def get_total_visitors(self):
        """Get total visitors"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(visitors) FROM analytics")
        result = cursor.fetchone()[0] or 0
        conn.close()
        return result
    
    def get_in_stock_count(self):
        """Get count of products in stock"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM products WHERE stock > 0")
        result = cursor.fetchone()[0]
        conn.close()
        return result
    
    def get_out_of_stock_count(self):
        """Get count of out of stock products"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM products WHERE stock = 0")
        result = cursor.fetchone()[0]
        conn.close()
        return result
    
    def get_revenue_data(self):
        """Get revenue and orders data for chart"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT date, revenue, orders FROM analytics ORDER BY date")
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_category_sales(self):
        """Get sales by category"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT category, SUM(price * sold) as total_sales
            FROM products
            GROUP BY category
            ORDER BY total_sales DESC
        """)
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_country_distribution(self):
        """Get order distribution by country"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT country, COUNT(*) as count
            FROM orders
            GROUP BY country
            ORDER BY count DESC
            LIMIT 4
        """)
        results = cursor.fetchall()
        conn.close()
        
        # Calculate percentages
        total = sum(row[1] for row in results)
        return [(row[0], (row[1] / total * 100)) for row in results]
    
    def get_traffic_sources(self):
        """Get traffic source distribution"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT source, percentage FROM traffic_sources ORDER BY percentage DESC")
        results = cursor.fetchall()
        conn.close()
        return results


class MetricCard(QFrame):
    """Custom widget for displaying metric cards"""
    
    def __init__(self, title, value, change, is_positive=True):
        super().__init__()
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #666; font-size: 13px;")
        layout.addWidget(title_label)
        
        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet("color: #333; font-size: 28px; font-weight: bold;")
        layout.addWidget(value_label)
        
        # Change percentage
        color = "#22c55e" if is_positive else "#ef4444"
        arrow = "↑" if is_positive else "↓"
        change_label = QLabel(f"{arrow} {change}")
        change_label.setStyleSheet(f"color: {color}; font-size: 12px; font-weight: 600;")
        layout.addWidget(change_label)
        
        self.setLayout(layout)


class CircularProgress(QWidget):
    """Custom circular progress widget"""
    
    def __init__(self, percentage=0, size=200):
        super().__init__()
        self.percentage = percentage
        self.size = size
        self.setFixedSize(size, size)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Background circle
        pen = QPen(QColor("#f0f0f0"), 15)
        painter.setPen(pen)
        rect = self.rect().adjusted(15, 15, -15, -15)
        painter.drawArc(rect, 0, 360 * 16)
        
        # Progress arc
        pen = QPen(QColor("#FF8C00"), 15)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        angle = int(self.percentage * 360 / 100 * 16)
        painter.drawArc(rect, 90 * 16, -angle)
        
        # Center text
        painter.setPen(QColor("#333"))
        font = QFont("Arial", 32, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, f"{self.percentage}%")


class EzMartDashboard(QMainWindow):
    """Main dashboard application window"""
    
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.init_ui()
        self.setup_refresh_timer()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("EzMart - E-Commerce Analytics Dashboard")
        self.setGeometry(100, 100, 1600, 900)
        self.setStyleSheet("background-color: #f5f5f5;")
        
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        
        # Main content area
        content_scroll = QScrollArea()
        content_scroll.setWidgetResizable(True)
        content_scroll.setStyleSheet("QScrollArea { border: none; }")
        
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        # Header
        header = self.create_header()
        content_layout.addWidget(header)
        
        # Metric cards
        metrics = self.create_metric_cards()
        content_layout.addWidget(metrics)
        
        # Charts row
        charts_row = QHBoxLayout()
        charts_row.setSpacing(20)
        
        # Revenue chart
        revenue_chart = self.create_revenue_chart()
        charts_row.addWidget(revenue_chart, 2)
        
        # Monthly target
        target_widget = self.create_monthly_target()
        charts_row.addWidget(target_widget, 1)
        
        content_layout.addLayout(charts_row)
        
        # Second row of info
        second_row = QHBoxLayout()
        second_row.setSpacing(20)
        
        # Categories pie chart
        categories_chart = self.create_categories_chart()
        second_row.addWidget(categories_chart, 1)
        
        # Active users
        users_widget = self.create_active_users()
        second_row.addWidget(users_widget, 1)
        
        content_layout.addLayout(second_row)
        
        # Third row
        third_row = QHBoxLayout()
        third_row.setSpacing(20)
        
        # Conversion rate
        conversion_widget = self.create_conversion_rate()
        third_row.addWidget(conversion_widget, 2)
        
        # Traffic sources
        traffic_widget = self.create_traffic_sources()
        third_row.addWidget(traffic_widget, 1)
        
        content_layout.addLayout(third_row)
        
        # Inventory section
        inventory_widget = self.create_inventory_section()
        content_layout.addWidget(inventory_widget)
        
        content_layout.addStretch()
        content_widget.setLayout(content_layout)
        content_scroll.setWidget(content_widget)
        
        main_layout.addWidget(content_scroll)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
    
    def create_sidebar(self):
        """Create navigation sidebar"""
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #1a1a2e;
                color: white;
            }
            QPushButton {
                text-align: left;
                padding: 15px 20px;
                border: none;
                color: #b4b4b4;
                font-size: 14px;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #252542;
                color: white;
            }
            QPushButton#active {
                background-color: #FF8C00;
                color: white;
                border-radius: 10px;
                margin: 0 10px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # Logo
        logo = QLabel("🛒 EzMart")
        logo.setStyleSheet("font-size: 24px; font-weight: bold; color: #FF8C00; padding: 30px 20px;")
        layout.addWidget(logo)
        
        # Menu items
        menu_items = [
            ("📊 Dashboard", True),
            ("📦 Orders", False),
            ("🏷️ Products", False),
            ("👥 Customers", False),
            ("📈 Reports", False),
            ("🎫 Discounts", False),
            ("🔗 Integrations", False),
            ("❓ Help", False),
            ("⚙️ Settings", False),
        ]
        
        for item, is_active in menu_items:
            btn = QPushButton(item)
            if is_active:
                btn.setObjectName("active")
            layout.addWidget(btn)
        
        layout.addStretch()
        sidebar.setLayout(layout)
        return sidebar
    
    def create_header(self):
        """Create header bar"""
        header = QFrame()
        header.setStyleSheet("background-color: white; border-radius: 12px; padding: 15px;")
        header.setFixedHeight(80)
        
        layout = QHBoxLayout()
        
        # Search bar
        search = QLineEdit()
        search.setPlaceholderText("🔍 Search stock, order, etc")
        search.setStyleSheet("""
            QLineEdit {
                padding: 10px 15px;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                font-size: 14px;
                background-color: #f9f9f9;
            }
        """)
        search.setFixedWidth(400)
        layout.addWidget(search)
        
        layout.addStretch()
        
        # Notifications
        notif_btn = QPushButton("🔔")
        notif_btn.setStyleSheet("""
            QPushButton {
                background-color: #f9f9f9;
                border: none;
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        layout.addWidget(notif_btn)
        
        # Profile
        profile_label = QLabel("👤 Marcus George\nAdmin")
        profile_label.setStyleSheet("font-size: 12px; color: #666; padding-left: 15px;")
        layout.addWidget(profile_label)
        
        header.setLayout(layout)
        return header
    
    def create_metric_cards(self):
        """Create top metric cards"""
        container = QWidget()
        layout = QHBoxLayout()
        layout.setSpacing(20)
        
        # Get data from database
        total_sales = self.db.get_total_sales()
        total_orders = self.db.get_total_orders()
        total_visitors = self.db.get_total_visitors()
        in_stock = self.db.get_in_stock_count()
        out_of_stock = self.db.get_out_of_stock_count()
        
        # Create cards
        card1 = MetricCard("Total Sales", f"${total_sales:,.0f}", "3.34%", True)
        card2 = MetricCard("Total Orders", f"{total_orders:,}", "2.89%", False)
        card3 = MetricCard("Total Visitors", f"{total_visitors:,}", "8.02%", True)
        card4 = MetricCard("In Stock", f"{in_stock}", "Products", True)
        card5 = MetricCard("Out of Stock", f"{out_of_stock}", "Products", False)
        
        layout.addWidget(card1)
        layout.addWidget(card2)
        layout.addWidget(card3)
        layout.addWidget(card4)
        layout.addWidget(card5)
        
        container.setLayout(layout)
        return container
    
    def create_revenue_chart(self):
        """Create revenue analytics line chart"""
        frame = QFrame()
        frame.setStyleSheet("background-color: white; border-radius: 12px; padding: 20px;")
        
        layout = QVBoxLayout()
        
        title = QLabel("Revenue Analytics")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        layout.addWidget(title)
        
        # Create chart
        chart = QChart()
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.legend().setVisible(True)
        chart.setBackgroundVisible(False)
        
        # Get data
        revenue_data = self.db.get_revenue_data()
        
        # Revenue series
        revenue_series = QLineSeries()
        revenue_series.setName("Revenue")
        
        # Orders series
        orders_series = QLineSeries()
        orders_series.setName("Orders")
        
        categories = []
        for i, (date, revenue, orders) in enumerate(revenue_data):
            revenue_series.append(i, revenue)
            orders_series.append(i, orders)
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            categories.append(date_obj.strftime("%b %d"))
        
        chart.addSeries(revenue_series)
        chart.addSeries(orders_series)
        
        # Axes
        axis_x = QValueAxis()
        axis_x.setRange(0, len(revenue_data) - 1)
        axis_x.setLabelFormat("%d")
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        revenue_series.attachAxis(axis_x)
        orders_series.attachAxis(axis_x)
        
        axis_y = QValueAxis()
        axis_y.setRange(0, 16000)
        axis_y.setLabelFormat("%d")
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        revenue_series.attachAxis(axis_y)
        orders_series.attachAxis(axis_y)
        
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        layout.addWidget(chart_view)
        frame.setLayout(layout)
        return frame
    
    def create_monthly_target(self):
        """Create monthly target progress widget"""
        frame = QFrame()
        frame.setStyleSheet("background-color: white; border-radius: 12px; padding: 20px;")
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("Monthly Target")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Circular progress
        progress = CircularProgress(85, 180)
        layout.addWidget(progress, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Message
        message = QLabel("Great Progress!\nOur achievement increased by $200,000\nlet's reach 100% next month.")
        message.setStyleSheet("font-size: 12px; color: #666; text-align: center;")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message.setWordWrap(True)
        layout.addWidget(message)
        
        # Target and revenue boxes
        boxes_layout = QHBoxLayout()
        
        target_box = QFrame()
        target_box.setStyleSheet("background-color: #f0f0f0; border-radius: 8px; padding: 10px;")
        target_layout = QVBoxLayout()
        target_title = QLabel("Target")
        target_title.setStyleSheet("font-size: 11px; color: #666;")
        target_value = QLabel("$600,000")
        target_value.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
        target_layout.addWidget(target_title)
        target_layout.addWidget(target_value)
        target_box.setLayout(target_layout)
        
        revenue_box = QFrame()
        revenue_box.setStyleSheet("background-color: #fff3e0; border-radius: 8px; padding: 10px;")
        revenue_layout = QVBoxLayout()
        revenue_title = QLabel("Revenue")
        revenue_title.setStyleSheet("font-size: 11px; color: #666;")
        revenue_value = QLabel("$510,000")
        revenue_value.setStyleSheet("font-size: 14px; font-weight: bold; color: #FF8C00;")
        revenue_layout.addWidget(revenue_title)
        revenue_layout.addWidget(revenue_value)
        revenue_box.setLayout(revenue_layout)
        
        boxes_layout.addWidget(target_box)
        boxes_layout.addWidget(revenue_box)
        layout.addLayout(boxes_layout)
        
        frame.setLayout(layout)
        return frame
    
    def create_categories_chart(self):
        """Create top categories pie chart"""
        frame = QFrame()
        frame.setStyleSheet("background-color: white; border-radius: 12px; padding: 20px;")
        
        layout = QVBoxLayout()
        
        title = QLabel("Top Categories")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        layout.addWidget(title)
        
        # Create pie chart
        series = QPieSeries()
        
        # Get data
        categories = self.db.get_category_sales()
        colors = ["#FF8C00", "#4CAF50", "#2196F3", "#E91E63"]
        
        for i, (category, sales) in enumerate(categories):
            slice = series.append(f"{category}\n${sales:,.0f}", sales)
            slice.setColor(QColor(colors[i % len(colors)]))
        
        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignRight)
        chart.setBackgroundVisible(False)
        
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        layout.addWidget(chart_view)
        frame.setLayout(layout)
        return frame
    
    def create_active_users(self):
        """Create active users by country widget"""
        frame = QFrame()
        frame.setStyleSheet("background-color: white; border-radius: 12px; padding: 20px;")
        
        layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Active Users")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        header_layout.addWidget(title)
        
        count = QLabel("2,758")
        count.setStyleSheet("font-size: 16px; font-weight: bold; color: #FF8C00;")
        header_layout.addWidget(count)
        
        change = QLabel("↑ 8.02%")
        change.setStyleSheet("font-size: 12px; color: #22c55e; font-weight: 600;")
        header_layout.addWidget(change)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Country distribution
        countries = self.db.get_country_distribution()
        
        for country, percentage in countries:
            country_layout = QVBoxLayout()
            country_layout.setSpacing(5)
            
            country_header = QHBoxLayout()
            country_label = QLabel(country)
            country_label.setStyleSheet("font-size: 13px; color: #333;")
            country_header.addWidget(country_label)
            country_header.addStretch()
            percent_label = QLabel(f"{percentage:.1f}%")
            percent_label.setStyleSheet("font-size: 12px; color: #666;")
            country_header.addWidget(percent_label)
            country_layout.addLayout(country_header)
            
            progress = QProgressBar()
            progress.setValue(int(percentage))
            progress.setMaximum(100)
            progress.setTextVisible(False)
            progress.setStyleSheet("""
                QProgressBar {
                    border: none;
                    border-radius: 4px;
                    background-color: #f0f0f0;
                    height: 8px;
                }
                QProgressBar::chunk {
                    background-color: #FF8C00;
                    border-radius: 4px;
                }
            """)
            country_layout.addWidget(progress)
            layout.addLayout(country_layout)
        
        layout.addStretch()
        frame.setLayout(layout)
        return frame
    
    def create_conversion_rate(self):
        """Create conversion rate funnel widget"""
        frame = QFrame()
        frame.setStyleSheet("background-color: white; border-radius: 12px; padding: 20px;")
        
        layout = QVBoxLayout()
        
        title = QLabel("Conversion Rate")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        layout.addWidget(title)
        
        # Conversion steps
        steps = [
            ("Product Views", 25000, 9, True),
            ("Add to Cart", 12000, 6, True),
            ("Proceed to Checkout", 8500, 4, True),
            ("Completed Purchases", 6200, 7, True),
            ("Abandoned Carts", 3000, 5, False),
        ]
        
        steps_layout = QHBoxLayout()
        steps_layout.setSpacing(10)
        
        for step_name, value, change, is_positive in steps:
            step_frame = QFrame()
            step_frame.setStyleSheet("""
                QFrame {
                    background-color: #f9f9f9;
                    border-radius: 8px;
                    padding: 15px;
                }
            """)
            
            step_layout = QVBoxLayout()
            
            name_label = QLabel(step_name)
            name_label.setStyleSheet("font-size: 11px; color: #666;")
            name_label.setWordWrap(True)
            step_layout.addWidget(name_label)
            
            value_label = QLabel(f"{value:,}")
            value_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
            step_layout.addWidget(value_label)
            
            color = "#22c55e" if is_positive else "#ef4444"
            arrow = "↑" if is_positive else "↓"
            change_label = QLabel(f"{arrow} {change}%")
            change_label.setStyleSheet(f"font-size: 11px; color: {color}; font-weight: 600;")
            step_layout.addWidget(change_label)
            
            step_frame.setLayout(step_layout)
            steps_layout.addWidget(step_frame)
        
        layout.addLayout(steps_layout)
        frame.setLayout(layout)
        return frame
    
    def create_traffic_sources(self):
        """Create traffic sources widget"""
        frame = QFrame()
        frame.setStyleSheet("background-color: white; border-radius: 12px; padding: 20px;")
        
        layout = QVBoxLayout()
        
        title = QLabel("Traffic Sources")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        layout.addWidget(title)
        
        # Get traffic data
        traffic_data = self.db.get_traffic_sources()
        colors = ["#FF8C00", "#4CAF50", "#2196F3", "#E91E63", "#9C27B0"]
        
        # Create horizontal stacked bar
        bar_container = QFrame()
        bar_container.setFixedHeight(40)
        bar_container.setStyleSheet("background-color: #f0f0f0; border-radius: 8px;")
        layout.addWidget(bar_container)
        
        # Legend
        for i, (source, percentage) in enumerate(traffic_data):
            item_layout = QHBoxLayout()
            
            color_box = QLabel()
            color_box.setFixedSize(12, 12)
            color_box.setStyleSheet(f"background-color: {colors[i]}; border-radius: 2px;")
            item_layout.addWidget(color_box)
            
            source_label = QLabel(source)
            source_label.setStyleSheet("font-size: 12px; color: #666;")
            item_layout.addWidget(source_label)
            
            item_layout.addStretch()
            
            percent_label = QLabel(f"{percentage}%")
            percent_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #333;")
            item_layout.addWidget(percent_label)
            
            layout.addLayout(item_layout)
        
        layout.addStretch()
        frame.setLayout(layout)
        return frame
    
    def create_inventory_section(self):
        """Create inventory management section"""
        frame = QFrame()
        frame.setStyleSheet("background-color: white; border-radius: 12px; padding: 20px;")
        
        layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("📦 Inventory Management")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Stock status
        in_stock = self.db.get_in_stock_count()
        out_stock = self.db.get_out_of_stock_count()
        
        stock_label = QLabel(f"In Stock: {in_stock} | Out of Stock: {out_stock}")
        stock_label.setStyleSheet("font-size: 14px; color: #666;")
        header_layout.addWidget(stock_label)
        
        layout.addLayout(header_layout)
        
        # Products table
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["Product", "Category", "Price", "Stock", "Sold", "Status"])
        table.horizontalHeader().setStretchLastSection(True)
        table.setAlternatingRowColors(True)
        table.setStyleSheet("""
            QTableWidget {
                border: none;
                gridline-color: #e0e0e0;
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 10px;
                border: none;
                font-weight: bold;
                color: #666;
            }
        """)
        
        # Get products from database
        conn = sqlite3.connect(self.db.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name, category, price, stock, sold FROM products ORDER BY category, name")
        products = cursor.fetchall()
        conn.close()
        
        table.setRowCount(len(products))
        
        for row, (name, category, price, stock, sold) in enumerate(products):
            table.setItem(row, 0, QTableWidgetItem(name))
            table.setItem(row, 1, QTableWidgetItem(category))
            table.setItem(row, 2, QTableWidgetItem(f"${price:.2f}"))
            table.setItem(row, 3, QTableWidgetItem(str(stock)))
            table.setItem(row, 4, QTableWidgetItem(str(sold)))
            
            status = "✅ In Stock" if stock > 0 else "❌ Out of Stock"
            status_item = QTableWidgetItem(status)
            if stock == 0:
                status_item.setForeground(QColor("#ef4444"))
            else:
                status_item.setForeground(QColor("#22c55e"))
            table.setItem(row, 5, status_item)
        
        table.resizeColumnsToContents()
        layout.addWidget(table)
        
        frame.setLayout(layout)
        return frame
    
    def setup_refresh_timer(self):
        """Setup timer for auto-refresh"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_data)
        self.timer.start(30000)  # Refresh every 30 seconds
    
    def refresh_data(self):
        """Refresh dashboard data"""
        # In a production app, this would fetch new data
        # For demo, we'll just show the refresh is working
        print("Dashboard data refreshed at", datetime.now().strftime("%H:%M:%S"))


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Set font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Create and show dashboard
    dashboard = EzMartDashboard()
    dashboard.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
