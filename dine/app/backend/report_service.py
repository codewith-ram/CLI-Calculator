"""
Report and analytics service for SmartDine Desktop Edition
"""
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from datetime import datetime, date, timedelta
from database.models import Bill, Order, OrderItem, MenuItem, Table
from database.db_connection import get_db_session


class ReportService:
    """Handles reporting and analytics operations"""
    
    def get_sales_summary(self, start_date: date, end_date: date) -> Dict[str, Any]:
        """Get sales summary for a date range"""
        session = get_db_session()
        try:
            bills = session.query(Bill).filter(
                and_(
                    Bill.created_at >= start_date,
                    Bill.created_at <= end_date
                )
            ).all()
            
            total_revenue = sum(bill.total_amount for bill in bills)
            total_bills = len(bills)
            total_tax = sum(bill.tax_amount for bill in bills)
            total_discount = sum(bill.discount_amount for bill in bills)
            
            return {
                'start_date': start_date,
                'end_date': end_date,
                'total_revenue': total_revenue,
                'total_bills': total_bills,
                'total_tax': total_tax,
                'total_discount': total_discount,
                'average_bill': total_revenue / total_bills if total_bills > 0 else 0
            }
        finally:
            session.close()
    
    def get_top_menu_items(self, start_date: date, end_date: date, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most ordered menu items"""
        session = get_db_session()
        try:
            # Get order items within date range
            order_items = session.query(OrderItem).join(Order).filter(
                and_(
                    Order.created_at >= start_date,
                    Order.created_at <= end_date
                )
            ).all()
            
            # Aggregate by menu item
            item_stats = {}
            for item in order_items:
                menu_item_id = item.menu_item_id
                menu_item_name = item.menu_item.name
                
                if menu_item_id not in item_stats:
                    item_stats[menu_item_id] = {
                        'name': menu_item_name,
                        'total_quantity': 0,
                        'total_revenue': 0.0,
                        'order_count': 0
                    }
                
                item_stats[menu_item_id]['total_quantity'] += item.quantity
                item_stats[menu_item_id]['total_revenue'] += item.total_price
                item_stats[menu_item_id]['order_count'] += 1
            
            # Sort by total quantity and return top items
            sorted_items = sorted(
                item_stats.values(),
                key=lambda x: x['total_quantity'],
                reverse=True
            )
            
            return sorted_items[:limit]
        finally:
            session.close()
    
    def get_revenue_by_date(self, start_date: date, end_date: date) -> List[Dict[str, Any]]:
        """Get daily revenue breakdown"""
        session = get_db_session()
        try:
            # Group bills by date
            daily_revenue = session.query(
                func.date(Bill.created_at).label('date'),
                func.count(Bill.id).label('bill_count'),
                func.sum(Bill.total_amount).label('revenue'),
                func.sum(Bill.tax_amount).label('tax'),
                func.sum(Bill.discount_amount).label('discount')
            ).filter(
                and_(
                    Bill.created_at >= start_date,
                    Bill.created_at <= end_date
                )
            ).group_by(func.date(Bill.created_at)).order_by('date').all()
            
            return [
                {
                    'date': row.date,
                    'bill_count': row.bill_count,
                    'revenue': float(row.revenue or 0),
                    'tax': float(row.tax or 0),
                    'discount': float(row.discount or 0)
                }
                for row in daily_revenue
            ]
        finally:
            session.close()
    
    def get_table_occupancy_report(self, start_date: date, end_date: date) -> Dict[str, Any]:
        """Get table occupancy statistics"""
        session = get_db_session()
        try:
            # Get all orders in date range
            orders = session.query(Order).filter(
                and_(
                    Order.created_at >= start_date,
                    Order.created_at <= end_date
                )
            ).all()
            
            # Calculate table usage
            table_usage = {}
            for order in orders:
                table_id = order.table_id
                table_number = order.table.table_number
                
                if table_id not in table_usage:
                    table_usage[table_id] = {
                        'table_number': table_number,
                        'order_count': 0,
                        'total_revenue': 0.0,
                        'average_order_value': 0.0
                    }
                
                table_usage[table_id]['order_count'] += 1
                table_usage[table_id]['total_revenue'] += order.total_amount
            
            # Calculate averages
            for table_data in table_usage.values():
                if table_data['order_count'] > 0:
                    table_data['average_order_value'] = (
                        table_data['total_revenue'] / table_data['order_count']
                    )
            
            return {
                'start_date': start_date,
                'end_date': end_date,
                'total_tables_used': len(table_usage),
                'table_usage': list(table_usage.values())
            }
        finally:
            session.close()
    
    def get_waiter_performance(self, start_date: date, end_date: date) -> List[Dict[str, Any]]:
        """Get waiter performance statistics"""
        session = get_db_session()
        try:
            # Get orders with waiter info
            orders = session.query(Order).join(User).filter(
                and_(
                    Order.created_at >= start_date,
                    Order.created_at <= end_date
                )
            ).all()
            
            # Aggregate by waiter
            waiter_stats = {}
            for order in orders:
                waiter_id = order.waiter_id
                waiter_name = order.waiter.full_name
                
                if waiter_id not in waiter_stats:
                    waiter_stats[waiter_id] = {
                        'waiter_name': waiter_name,
                        'order_count': 0,
                        'total_revenue': 0.0,
                        'average_order_value': 0.0
                    }
                
                waiter_stats[waiter_id]['order_count'] += 1
                waiter_stats[waiter_id]['total_revenue'] += order.total_amount
            
            # Calculate averages
            for waiter_data in waiter_stats.values():
                if waiter_data['order_count'] > 0:
                    waiter_data['average_order_value'] = (
                        waiter_data['total_revenue'] / waiter_data['order_count']
                    )
            
            return list(waiter_stats.values())
        finally:
            session.close()
    
    def get_category_sales(self, start_date: date, end_date: date) -> List[Dict[str, Any]]:
        """Get sales breakdown by menu category"""
        session = get_db_session()
        try:
            # Get order items with menu categories
            order_items = session.query(OrderItem).join(Order).join(MenuItem).filter(
                and_(
                    Order.created_at >= start_date,
                    Order.created_at <= end_date
                )
            ).all()
            
            # Aggregate by category
            category_stats = {}
            for item in order_items:
                category = item.menu_item.category
                
                if category not in category_stats:
                    category_stats[category] = {
                        'category': category,
                        'total_quantity': 0,
                        'total_revenue': 0.0,
                        'item_count': 0
                    }
                
                category_stats[category]['total_quantity'] += item.quantity
                category_stats[category]['total_revenue'] += item.total_price
                category_stats[category]['item_count'] += 1
            
            return list(category_stats.values())
        finally:
            session.close()
    
    def get_hourly_sales_pattern(self, target_date: date) -> List[Dict[str, Any]]:
        """Get hourly sales pattern for a specific date"""
        session = get_db_session()
        try:
            # Get bills by hour
            hourly_sales = session.query(
                func.strftime('%H', Bill.created_at).label('hour'),
                func.count(Bill.id).label('bill_count'),
                func.sum(Bill.total_amount).label('revenue')
            ).filter(
                func.date(Bill.created_at) == target_date
            ).group_by(func.strftime('%H', Bill.created_at)).order_by('hour').all()
            
            return [
                {
                    'hour': int(row.hour),
                    'bill_count': row.bill_count,
                    'revenue': float(row.revenue or 0)
                }
                for row in hourly_sales
            ]
        finally:
            session.close()


# Global report service instance
report_service = ReportService()
