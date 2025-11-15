"""
Table management service for SmartDine Desktop Edition
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from database.models import Table, Order
from database.db_connection import get_db_session


class TableService:
    """Handles table management operations"""
    
    def create_table(self, table_number: int, capacity: int) -> bool:
        """Create a new table"""
        session = get_db_session()
        try:
            # Check if table number already exists
            existing_table = session.query(Table).filter(
                Table.table_number == table_number
            ).first()
            
            if existing_table:
                return False
            
            table = Table(
                table_number=table_number,
                capacity=capacity,
                status='free'
            )
            
            session.add(table)
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()
    
    def get_table(self, table_id: int) -> Optional[Dict[str, Any]]:
        """Get table details by ID"""
        session = get_db_session()
        try:
            table = session.query(Table).filter(Table.id == table_id).first()
            if table:
                return {
                    'id': table.id,
                    'table_number': table.table_number,
                    'capacity': table.capacity,
                    'status': table.status,
                    'current_order_id': table.current_order_id
                }
            return None
        finally:
            session.close()
    
    def get_all_tables(self) -> List[Dict[str, Any]]:
        """Get all tables with their current status"""
        session = get_db_session()
        try:
            tables = session.query(Table).order_by(Table.table_number).all()
            
            result = []
            for table in tables:
                table_data = {
                    'id': table.id,
                    'table_number': table.table_number,
                    'capacity': table.capacity,
                    'status': table.status,
                    'current_order_id': table.current_order_id,
                    'current_order': None
                }
                
                # Get current order if exists
                if table.current_order_id:
                    from database.models import Order, User
                    current_order = session.query(Order).filter(Order.id == table.current_order_id).first()
                    if current_order:
                        waiter = session.query(User).filter(User.id == current_order.waiter_id).first()
                        table_data['current_order'] = {
                            'id': current_order.id,
                            'waiter_name': waiter.full_name if waiter else 'Unknown',
                            'total_amount': current_order.total_amount,
                            'created_at': current_order.created_at
                        }
                
                result.append(table_data)
            
            return result
        finally:
            session.close()
    
    def get_tables_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Get tables filtered by status"""
        session = get_db_session()
        try:
            tables = session.query(Table).filter(Table.status == status).order_by(Table.table_number).all()
            
            return [
                {
                    'id': table.id,
                    'table_number': table.table_number,
                    'capacity': table.capacity,
                    'status': table.status,
                    'current_order_id': table.current_order_id
                }
                for table in tables
            ]
        finally:
            session.close()
    
    def update_table_status(self, table_id: int, status: str) -> bool:
        """Update table status"""
        session = get_db_session()
        try:
            table = session.query(Table).filter(Table.id == table_id).first()
            if not table:
                return False
            
            table.status = status
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()
    
    def assign_table_to_order(self, table_id: int, order_id: int) -> bool:
        """Assign a table to an order"""
        session = get_db_session()
        try:
            table = session.query(Table).filter(Table.id == table_id).first()
            if not table or table.status != 'free':
                return False
            
            table.status = 'occupied'
            table.current_order_id = order_id
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()
    
    def free_table(self, table_id: int) -> bool:
        """Free a table (set status to free and clear current order)"""
        session = get_db_session()
        try:
            table = session.query(Table).filter(Table.id == table_id).first()
            if not table:
                return False
            
            table.status = 'free'
            table.current_order_id = None
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()
    
    def get_table_statistics(self) -> Dict[str, Any]:
        """Get table occupancy statistics"""
        session = get_db_session()
        try:
            total_tables = session.query(Table).count()
            free_tables = session.query(Table).filter(Table.status == 'free').count()
            occupied_tables = session.query(Table).filter(Table.status == 'occupied').count()
            served_tables = session.query(Table).filter(Table.status == 'served').count()
            billed_tables = session.query(Table).filter(Table.status == 'billed').count()
            
            return {
                'total_tables': total_tables,
                'free_tables': free_tables,
                'occupied_tables': occupied_tables,
                'served_tables': served_tables,
                'billed_tables': billed_tables,
                'occupancy_rate': (occupied_tables + served_tables + billed_tables) / total_tables * 100 if total_tables > 0 else 0
            }
        finally:
            session.close()
    
    def delete_table(self, table_id: int) -> bool:
        """Delete a table (only if it's free)"""
        session = get_db_session()
        try:
            table = session.query(Table).filter(Table.id == table_id).first()
            if not table or table.status != 'free':
                return False
            
            session.delete(table)
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()
    
    def update_table_capacity(self, table_id: int, new_capacity: int) -> bool:
        """Update table capacity"""
        session = get_db_session()
        try:
            table = session.query(Table).filter(Table.id == table_id).first()
            if not table:
                return False
            
            table.capacity = new_capacity
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()


# Global table service instance
table_service = TableService()
