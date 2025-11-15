"""
Configuration settings for SmartDine Desktop Edition
"""
import os
from pathlib import Path

# Application settings
APP_NAME = "SmartDine Desktop Edition"
APP_VERSION = "1.0.0"
APP_AUTHOR = "SmartDine Team"

# Database settings
DATABASE_PATH = "smartdine.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# GUI settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600

# Theme settings
THEME_COLORS = {
    'primary': '#2E86AB',      # Blue
    'secondary': '#A23B72',    # Purple
    'success': '#F18F01',      # Orange
    'warning': '#C73E1D',      # Red
    'info': '#7209B7',         # Dark Purple
    'light': '#F8F9FA',       # Light Gray
    'dark': '#212529',        # Dark Gray
    'white': '#FFFFFF',
    'black': '#000000'
}

# Table status colors
TABLE_STATUS_COLORS = {
    'free': '#28A745',        # Green
    'occupied': '#FFC107',    # Yellow
    'served': '#17A2B8',      # Cyan
    'billed': '#6C757D'       # Gray
}

# Order status colors
ORDER_STATUS_COLORS = {
    'pending': '#FFC107',      # Yellow
    'cooking': '#FD7E14',     # Orange
    'ready': '#20C997',       # Teal
    'served': '#28A745',      # Green
    'cancelled': '#DC3545'    # Red
}

# User roles
USER_ROLES = {
    'admin': 'Administrator',
    'waiter': 'Waiter',
    'chef': 'Chef',
    'cashier': 'Cashier'
}

# Menu categories
MENU_CATEGORIES = [
    'starters',
    'main_course',
    'desserts',
    'beverages'
]

# Payment methods
PAYMENT_METHODS = [
    'cash',
    'card',
    'upi'
]

# File paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
REPORTS_DIR = BASE_DIR / "reports"
ASSETS_DIR = BASE_DIR / "app" / "gui" / "assets"

# Create directories if they don't exist
for directory in [DATA_DIR, LOGS_DIR, REPORTS_DIR, ASSETS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Logging settings
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE_MAX_SIZE = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 5

# Business settings
DEFAULT_TAX_RATE = 8.5  # 8.5%
DEFAULT_SERVICE_CHARGE = 0.0  # 0%
MAX_TABLE_CAPACITY = 20
MIN_TABLE_CAPACITY = 1

# Report settings
REPORT_DATE_FORMAT = "%Y-%m-%d"
REPORT_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
PDF_PAGE_SIZE = "A4"
CHART_DPI = 300

# Security settings
PASSWORD_MIN_LENGTH = 6
SESSION_TIMEOUT = 3600  # 1 hour in seconds
MAX_LOGIN_ATTEMPTS = 3

# Application settings
AUTO_SAVE_INTERVAL = 300  # 5 minutes in seconds
BACKUP_INTERVAL = 86400   # 24 hours in seconds
MAX_BACKUP_FILES = 7

# UI Settings
ANIMATION_DURATION = 200  # milliseconds
TOOLTIP_DELAY = 500       # milliseconds
REFRESH_INTERVAL = 5000   # 5 seconds in milliseconds

# Validation settings
MAX_MENU_ITEM_NAME_LENGTH = 100
MAX_MENU_ITEM_DESCRIPTION_LENGTH = 500
MAX_ORDER_NOTES_LENGTH = 200
MAX_USER_FULL_NAME_LENGTH = 100
MAX_USER_EMAIL_LENGTH = 100

# Export settings
EXPORT_FORMATS = ['PDF', 'Excel', 'CSV']
DEFAULT_EXPORT_FORMAT = 'PDF'

# Notification settings
NOTIFICATION_DURATION = 3000  # 3 seconds
SOUND_ENABLED = True
POPUP_ENABLED = True

# Development settings
DEBUG_MODE = False
VERBOSE_LOGGING = False
ENABLE_PROFILING = False

# Database settings
DB_POOL_SIZE = 5
DB_MAX_OVERFLOW = 10
DB_POOL_TIMEOUT = 30
DB_POOL_RECYCLE = 3600

# Cache settings
CACHE_ENABLED = True
CACHE_TTL = 300  # 5 minutes
CACHE_MAX_SIZE = 1000

# Performance settings
MAX_CONCURRENT_OPERATIONS = 10
BATCH_SIZE = 100
QUERY_TIMEOUT = 30

# Feature flags
FEATURE_ANALYTICS = True
FEATURE_REPORTS = True
FEATURE_BACKUP = True
FEATURE_EXPORT = True
FEATURE_NOTIFICATIONS = True
FEATURE_SOUND = True
