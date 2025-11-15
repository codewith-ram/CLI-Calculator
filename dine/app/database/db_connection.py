"""
Database connection and session management for SmartDine Desktop Edition
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from .models import Base


class DatabaseManager:
    """Manages database connection and sessions"""
    
    def __init__(self, db_path: str = "smartdine.db"):
        """Initialize database connection"""
        self.db_path = db_path
        self.engine = None
        self.SessionLocal = None
        self._setup_database()
    
    def _setup_database(self):
        """Setup database engine and session factory"""
        # Create database directory if it doesn't exist
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        # Create SQLite engine with connection pooling
        self.engine = create_engine(
            f"sqlite:///{self.db_path}",
            poolclass=StaticPool,
            connect_args={"check_same_thread": False},
            echo=False  # Set to True for SQL debugging
        )
        
        # Create session factory
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def create_tables(self):
        """Create all database tables"""
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self) -> Session:
        """Get a new database session"""
        return self.SessionLocal()
    
    def close_connection(self):
        """Close database connection"""
        if self.engine:
            self.engine.dispose()


# Global database manager instance
db_manager = DatabaseManager()


def get_db_session() -> Session:
    """Get a database session for dependency injection"""
    return db_manager.get_session()


def init_database():
    """Initialize database with tables"""
    db_manager.create_tables()
