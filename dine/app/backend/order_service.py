"""
Order management service for SmartDine Desktop Edition
"""
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from datetime import datetime
from database.models import Order, OrderItem, Table, MenuItem, User
from database.db_connection import get_db_session


class OrderService:
    """Handles order operations for waiters and chefs"""
    
    def create_order(self, table_id: int, waiter_id: int, order_items: List[Dict[str, Any]], 
                    notes: str = None) -> Optional[int]:
        """Create a new order"""
        session = get_db_session()
        try:
            # Check if table is available
            table = session.query(Table).filter(Table.id == table_id).first()
            if not table or table.status != 'free':
                return None
            
            # Create order
            order = Order(
                table_id=table_id,
                waiter_id=waiter_id,
                notes=notes,
                status='pending'
            )
            session.add(order)
            session.flush()  # Get the order ID
            
            total_amount = 0.0
            
            # Add order items
            for item_data in order_items:
                menu_item = session.query(MenuItem).filter(
                    MenuItem.id == item_data['menu_item_id']
                ).first()
                
                if menu_item and menu_item.is_available:
                    quantity = item_data.get('quantity', 1)
                    unit_price = menu_item.price
                    total_price = unit_price * quantity
                    
                    order_item = OrderItem(
                        order_id=order.id,
                        menu_item_id=menu_item.id,
                        quantity=quantity,
                        unit_price=unit_price,
                        total_price=total_price,
                        special_instructions=item_data.get('special_instructions', '')
                    )
                    session.add(order_item)
                    total_amount += total_price
            
            # Update order total and table status
            order.total_amount = total_amount
            table.status = 'occupied'
            table.current_order_id = order.id
            
            session.commit()
            return order.id
        except Exception:
            session.rollback()
            return None
        finally:
            session.close()
    
    def get_order(self, order_id: int) -> Optional[Dict[str, Any]]:
        """Get order details by ID"""
        session = get_db_session()
        try:
            order = session.query(Order).filter(Order.id == order_id).first()
            if order:
                return {
                    'id': order.id,
                    'table_id': order.table_id,
                    'table_number': order.table.table_number,
                    'waiter_id': order.waiter_id,
                    'waiter_name': order.waiter.full_name,
                    'status': order.status,
                    'total_amount': order.total_amount,
                    'notes': order.notes,
                    'created_at': order.created_at,
                    'updated_at': order.updated_at,
                    'order_items': [
                        {
                            'id': item.id,
                            'menu_item_name': item.menu_item.name,
                            'quantity': item.quantity,
                            'unit_price': item.unit_price,
                            'total_price': item.total_price,
                            'special_instructions': item.special_instructions
                        }
                        for item in order.order_items
                    ]
                }
            return None
        finally:
            session.close()
    
    def get_orders_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Get orders by status (for chef kitchen view)"""
        session = get_db_session()
        try:
            orders = session.query(Order).filter(Order.status == status).order_by(Order.created_at).all()
            
            return [
                {
                    'id': order.id,
                    'table_number': order.table.table_number,
                    'waiter_name': order.waiter.full_name,
                    'status': order.status,
                    'total_amount': order.total_amount,
                    'notes': order.notes,
                    'created_at': order.created_at,
                    'order_items': [
                        {
                            'menu_item_name': item.menu_item.name,
                            'quantity': item.quantity,
                            'special_instructions': item.special_instructions
                        }
                        for item in order.order_items
                    ]
                }
                for order in orders
            ]
        finally:
            session.close()
    
    def update_order_status(self, order_id: int, new_status: str) -> bool:
        """Update order status (for chef workflow)"""
        session = get_db_session()
        try:
            order = session.query(Order).filter(Order.id == order_id).first()
            if not order:
                return False
            
            order.status = new_status
            
            # Update table status based on order status
            if new_status == 'served':
                order.table.status = 'served'
            elif new_status == 'cancelled':
                order.table.status = 'free'
                order.table.current_order_id = None
            
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()
    
    def get_active_orders(self) -> List[Dict[str, Any]]:
        """Get all active orders (pending, cooking, ready)"""
        session = get_db_session()
        try:
            orders = session.query(Order).filter(
                Order.status.in_(['pending', 'cooking', 'ready'])
            ).order_by(Order.created_at).all()
            
            return [
                {
                    'id': order.id,
                    'table_number': order.table.table_number,
                    'waiter_name': order.waiter.full_name,
                    'status': order.status,
                    'total_amount': order.total_amount,
                    'created_at': order.created_at,
                    'order_items_count': len(order.order_items)
                }
                for order in orders
            ]
        finally:
            session.close()
    
    def get_orders_by_waiter(self, waiter_id: int) -> List[Dict[str, Any]]:
        """Get orders for a specific waiter"""
        session = get_db_session()
        try:
            orders = session.query(Order).filter(
                Order.waiter_id == waiter_id
            ).order_by(desc(Order.created_at)).all()
            
            return [
                {
                    'id': order.id,
                    'table_number': order.table.table_number,
                    'status': order.status,
                    'total_amount': order.total_amount,
                    'created_at': order.created_at
                }
                for order in orders
            ]
        finally:
            session.close()
    
    def cancel_order(self, order_id: int) -> bool:
        """Cancel an order"""
        session = get_db_session()
        try:
            order = session.query(Order).filter(Order.id == order_id).first()
            if not order:
                return False
            
            order.status = 'cancelled'
            order.table.status = 'free'
            order.table.current_order_id = None
            
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()
    
    def get_order_statistics(self) -> Dict[str, Any]:
        """Get order statistics for reporting"""
        session = get_db_session()
        try:
            total_orders = session.query(Order).count()
            pending_orders = session.query(Order).filter(Order.status == 'pending').count()
            cooking_orders = session.query(Order).filter(Order.status == 'cooking').count()
            ready_orders = session.query(Order).filter(Order.status == 'ready').count()
            
            return {
                'total_orders': total_orders,
                'pending_orders': pending_orders,
                'cooking_orders': cooking_orders,
                'ready_orders': ready_orders,
                'active_orders': pending_orders + cooking_orders + ready_orders
            }
        finally:
            session.close()


# Global order service instance
order_service = OrderService()
