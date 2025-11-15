"""
Menu management service for SmartDine Desktop Edition
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from database.models import MenuItem
from database.db_connection import get_db_session


class MenuService:
    """Handles menu item operations"""
    
    def create_menu_item(self, name: str, description: str, price: float, 
                        category: str, is_available: bool = True) -> bool:
        """Create a new menu item"""
        session = get_db_session()
        try:
            menu_item = MenuItem(
                name=name,
                description=description,
                price=price,
                category=category,
                is_available=is_available
            )
            session.add(menu_item)
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()
    
    def get_menu_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific menu item by ID"""
        session = get_db_session()
        try:
            item = session.query(MenuItem).filter(MenuItem.id == item_id).first()
            if item:
                return {
                    'id': item.id,
                    'name': item.name,
                    'description': item.description,
                    'price': item.price,
                    'category': item.category,
                    'is_available': item.is_available,
                    'created_at': item.created_at,
                    'updated_at': item.updated_at
                }
            return None
        finally:
            session.close()
    
    def get_all_menu_items(self, category: str = None, available_only: bool = True) -> List[Dict[str, Any]]:
        """Get all menu items, optionally filtered by category and availability"""
        session = get_db_session()
        try:
            query = session.query(MenuItem)
            
            if category:
                query = query.filter(MenuItem.category == category)
            
            if available_only:
                query = query.filter(MenuItem.is_available == True)
            
            items = query.order_by(MenuItem.category, MenuItem.name).all()
            
            return [
                {
                    'id': item.id,
                    'name': item.name,
                    'description': item.description,
                    'price': item.price,
                    'category': item.category,
                    'is_available': item.is_available,
                    'created_at': item.created_at,
                    'updated_at': item.updated_at
                }
                for item in items
            ]
        finally:
            session.close()
    
    def update_menu_item(self, item_id: int, **kwargs) -> bool:
        """Update a menu item"""
        session = get_db_session()
        try:
            item = session.query(MenuItem).filter(MenuItem.id == item_id).first()
            if not item:
                return False
            
            for key, value in kwargs.items():
                if hasattr(item, key) and key != 'id':
                    setattr(item, key, value)
            
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()
    
    def delete_menu_item(self, item_id: int) -> bool:
        """Delete a menu item"""
        session = get_db_session()
        try:
            item = session.query(MenuItem).filter(MenuItem.id == item_id).first()
            if item:
                session.delete(item)
                session.commit()
                return True
            return False
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()
    
    def toggle_availability(self, item_id: int) -> bool:
        """Toggle menu item availability"""
        session = get_db_session()
        try:
            item = session.query(MenuItem).filter(MenuItem.id == item_id).first()
            if item:
                item.is_available = not item.is_available
                session.commit()
                return True
            return False
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()
    
    def get_categories(self) -> List[str]:
        """Get all available menu categories"""
        session = get_db_session()
        try:
            categories = session.query(MenuItem.category).distinct().all()
            return [cat[0] for cat in categories]
        finally:
            session.close()
    
    def search_menu_items(self, search_term: str) -> List[Dict[str, Any]]:
        """Search menu items by name or description"""
        session = get_db_session()
        try:
            items = session.query(MenuItem).filter(
                and_(
                    MenuItem.is_available == True,
                    or_(
                        MenuItem.name.ilike(f"%{search_term}%"),
                        MenuItem.description.ilike(f"%{search_term}%")
                    )
                )
            ).all()
            
            return [
                {
                    'id': item.id,
                    'name': item.name,
                    'description': item.description,
                    'price': item.price,
                    'category': item.category,
                    'is_available': item.is_available
                }
                for item in items
            ]
        finally:
            session.close()


# Global menu service instance
menu_service = MenuService()
