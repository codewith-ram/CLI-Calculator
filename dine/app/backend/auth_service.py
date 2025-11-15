"""
Authentication service for SmartDine Desktop Edition
"""
import bcrypt
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database.models import User
from database.db_connection import get_db_session


class AuthService:
    """Handles user authentication and authorization"""
    
    def __init__(self):
        self.current_user: Optional[User] = None
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with username and password"""
        session = get_db_session()
        try:
            user = session.query(User).filter(
                User.username == username,
                User.is_active == True
            ).first()
            
            if user and self.verify_password(password, user.password_hash):
                self.current_user = user
                return {
                    'id': user.id,
                    'username': user.username,
                    'role': user.role,
                    'full_name': user.full_name,
                    'email': user.email
                }
            return None
        finally:
            session.close()
    
    def create_user(self, username: str, password: str, role: str, 
                   full_name: str, email: str = None) -> bool:
        """Create a new user"""
        session = get_db_session()
        try:
            # Check if username already exists
            existing_user = session.query(User).filter(User.username == username).first()
            if existing_user:
                return False
            
            # Create new user
            hashed_password = self.hash_password(password)
            new_user = User(
                username=username,
                password_hash=hashed_password,
                role=role,
                full_name=full_name,
                email=email
            )
            
            session.add(new_user)
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user information by ID"""
        session = get_db_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                return {
                    'id': user.id,
                    'username': user.username,
                    'role': user.role,
                    'full_name': user.full_name,
                    'email': user.email,
                    'is_active': user.is_active
                }
            return None
        finally:
            session.close()
    
    def update_user(self, user_id: int, **kwargs) -> bool:
        """Update user information"""
        session = get_db_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                return False
            
            for key, value in kwargs.items():
                if hasattr(user, key) and key != 'id':
                    setattr(user, key, value)
            
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()
    
    def deactivate_user(self, user_id: int) -> bool:
        """Deactivate a user account"""
        return self.update_user(user_id, is_active=False)
    
    def get_all_users(self) -> list:
        """Get all users"""
        session = get_db_session()
        try:
            users = session.query(User).all()
            return [
                {
                    'id': user.id,
                    'username': user.username,
                    'role': user.role,
                    'full_name': user.full_name,
                    'email': user.email,
                    'is_active': user.is_active,
                    'created_at': user.created_at
                }
                for user in users
            ]
        finally:
            session.close()
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get current logged-in user information"""
        if self.current_user:
            return {
                'id': self.current_user.id,
                'username': self.current_user.username,
                'role': self.current_user.role,
                'full_name': self.current_user.full_name,
                'email': self.current_user.email
            }
        return None
    
    def has_permission(self, required_role: str) -> bool:
        """Check if current user has required role permission"""
        if not self.current_user:
            return False
        
        # Define role hierarchy
        role_hierarchy = {
            'admin': ['admin', 'waiter', 'chef', 'cashier'],
            'waiter': ['waiter'],
            'chef': ['chef'],
            'cashier': ['cashier']
        }
        
        return required_role in role_hierarchy.get(self.current_user.role, [])


# Global auth service instance
auth_service = AuthService()
