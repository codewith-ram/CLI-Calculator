"""
SmartDine Desktop Edition - Main Application Entry Point
"""
import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox, QSplashScreen
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QLabel

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import APP_NAME, APP_VERSION
from database.db_connection import init_database
from database.seed_data import seed_database
from gui.main_window import MainWindow
from utils.logger import logger


class SmartDineApp:
    """Main application class for SmartDine Desktop Edition"""
    
    def __init__(self):
        self.app = None
        self.main_window = None
        self.splash = None
    
    def create_splash_screen(self):
        """Create and show splash screen"""
        # Create a simple splash screen
        splash_pixmap = QPixmap(400, 300)
        splash_pixmap.fill(Qt.white)
        
        self.splash = QSplashScreen(splash_pixmap)
        self.splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.SplashScreen)
        
        # Add text to splash screen
        self.splash.showMessage(
            f"{APP_NAME}\nVersion {APP_VERSION}\nLoading...",
            Qt.AlignCenter | Qt.AlignBottom,
            Qt.black
        )
        
        self.splash.show()
        self.app.processEvents()
    
    def initialize_database(self):
        """Initialize database and seed with sample data"""
        try:
            logger.info("Initializing database...")
            init_database()
            
            # Check if database is empty and seed if needed
            from database.db_connection import get_db_session
            from database.models import User
            
            session = get_db_session()
            try:
                user_count = session.query(User).count()
                if user_count == 0:
                    logger.info("Database is empty, seeding with sample data...")
                    seed_database()
                else:
                    logger.info(f"Database already contains {user_count} users")
            finally:
                session.close()
                
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            QMessageBox.critical(
                None,
                "Database Error",
                f"Failed to initialize database:\n{str(e)}"
            )
            return False
        
        return True
    
    def create_main_window(self):
        """Create and show main window"""
        try:
            logger.info("Creating main window...")
            self.main_window = MainWindow()
            self.main_window.show()
            
            # Close splash screen
            if self.splash:
                self.splash.finish(self.main_window)
                self.splash = None
                
        except Exception as e:
            logger.error(f"Error creating main window: {e}")
            QMessageBox.critical(
                None,
                "Application Error",
                f"Failed to create main window:\n{str(e)}"
            )
            return False
        
        return True
    
    def run(self):
        """Run the application"""
        try:
            # Create QApplication
            self.app = QApplication(sys.argv)
            self.app.setApplicationName(APP_NAME)
            self.app.setApplicationVersion(APP_VERSION)
            
            # Set application style
            self.app.setStyle('Fusion')
            
            # Create splash screen
            self.create_splash_screen()
            
            # Initialize database
            if not self.initialize_database():
                return 1
            
            # Small delay to show splash screen
            QTimer.singleShot(1000, self.create_main_window)
            
            # Run application
            logger.info("Starting SmartDine Desktop Edition...")
            return self.app.exec_()
            
        except Exception as e:
            logger.error(f"Fatal error in application: {e}")
            QMessageBox.critical(
                None,
                "Fatal Error",
                f"Application encountered a fatal error:\n{str(e)}"
            )
            return 1
        finally:
            if self.splash:
                self.splash.close()


def main():
    """Main entry point"""
    try:
        # Create and run application
        smartdine_app = SmartDineApp()
        return smartdine_app.run()
    except Exception as e:
        print(f"Failed to start application: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
