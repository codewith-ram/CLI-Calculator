"""
Billing and payment service for SmartDine Desktop Edition
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from datetime import datetime, date
from database.models import Bill, Order, OrderItem, Table, User
from database.db_connection import get_db_session


class BillingService:
    """Handles billing and payment operations"""
    
    def create_bill(self, order_id: int, cashier_id: int, tax_rate: float = 0.0,
                   discount_amount: float = 0.0, service_charge: float = 0.0,
                   payment_method: str = 'cash') -> Optional[int]:
        """Create a bill for an order"""
        session = get_db_session()
        try:
            # Get order details
            order = session.query(Order).filter(Order.id == order_id).first()
            if not order or order.status != 'served':
                return None
            
            # Calculate bill amounts
            subtotal = order.total_amount
            tax_amount = subtotal * (tax_rate / 100)
            total_amount = subtotal + tax_amount + service_charge - discount_amount
            
            # Create bill
            bill = Bill(
                order_id=order_id,
                cashier_id=cashier_id,
                subtotal=subtotal,
                tax_rate=tax_rate,
                tax_amount=tax_amount,
                discount_amount=discount_amount,
                service_charge=service_charge,
                total_amount=total_amount,
                payment_method=payment_method,
                payment_status='pending'
            )
            
            session.add(bill)
            session.commit()
            return bill.id
        except Exception:
            session.rollback()
            return None
        finally:
            session.close()
    
    def get_bill(self, bill_id: int) -> Optional[Dict[str, Any]]:
        """Get bill details by ID"""
        session = get_db_session()
        try:
            bill = session.query(Bill).filter(Bill.id == bill_id).first()
            if bill:
                return {
                    'id': bill.id,
                    'order_id': bill.order_id,
                    'table_number': bill.order.table.table_number,
                    'cashier_name': bill.cashier.full_name,
                    'subtotal': bill.subtotal,
                    'tax_rate': bill.tax_rate,
                    'tax_amount': bill.tax_amount,
                    'discount_amount': bill.discount_amount,
                    'service_charge': bill.service_charge,
                    'total_amount': bill.total_amount,
                    'payment_method': bill.payment_method,
                    'payment_status': bill.payment_status,
                    'created_at': bill.created_at,
                    'order_items': [
                        {
                            'menu_item_name': item.menu_item.name,
                            'quantity': item.quantity,
                            'unit_price': item.unit_price,
                            'total_price': item.total_price
                        }
                        for item in bill.order.order_items
                    ]
                }
            return None
        finally:
            session.close()
    
    def get_bill_by_order(self, order_id: int) -> Optional[Dict[str, Any]]:
        """Get bill for a specific order"""
        session = get_db_session()
        try:
            bill = session.query(Bill).filter(Bill.order_id == order_id).first()
            if bill:
                return self.get_bill(bill.id)
            return None
        finally:
            session.close()
    
    def process_payment(self, bill_id: int, payment_method: str = None) -> bool:
        """Process payment for a bill"""
        session = get_db_session()
        try:
            bill = session.query(Bill).filter(Bill.id == bill_id).first()
            if not bill:
                return False
            
            # Update payment details
            if payment_method:
                bill.payment_method = payment_method
            bill.payment_status = 'paid'
            
            # Update table status
            bill.order.table.status = 'billed'
            bill.order.table.current_order_id = None
            
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()
    
    def get_pending_bills(self) -> List[Dict[str, Any]]:
        """Get all pending bills"""
        session = get_db_session()
        try:
            bills = session.query(Bill).filter(
                Bill.payment_status == 'pending'
            ).order_by(Bill.created_at).all()
            
            return [
                {
                    'id': bill.id,
                    'order_id': bill.order_id,
                    'table_number': bill.order.table.table_number,
                    'total_amount': bill.total_amount,
                    'payment_method': bill.payment_method,
                    'created_at': bill.created_at
                }
                for bill in bills
            ]
        finally:
            session.close()
    
    def get_bills_by_date_range(self, start_date: date, end_date: date) -> List[Dict[str, Any]]:
        """Get bills within a date range"""
        session = get_db_session()
        try:
            bills = session.query(Bill).filter(
                and_(
                    Bill.created_at >= start_date,
                    Bill.created_at <= end_date
                )
            ).order_by(desc(Bill.created_at)).all()
            
            return [
                {
                    'id': bill.id,
                    'order_id': bill.order_id,
                    'table_number': bill.order.table.table_number,
                    'subtotal': bill.subtotal,
                    'tax_amount': bill.tax_amount,
                    'discount_amount': bill.discount_amount,
                    'service_charge': bill.service_charge,
                    'total_amount': bill.total_amount,
                    'payment_method': bill.payment_method,
                    'payment_status': bill.payment_status,
                    'created_at': bill.created_at
                }
                for bill in bills
            ]
        finally:
            session.close()
    
    def get_daily_sales_summary(self, target_date: date = None) -> Dict[str, Any]:
        """Get daily sales summary"""
        if target_date is None:
            target_date = date.today()
        
        session = get_db_session()
        try:
            bills = session.query(Bill).filter(
                Bill.created_at >= target_date,
                Bill.created_at < target_date.replace(day=target_date.day + 1) if target_date.day < 28 
                else target_date.replace(month=target_date.month + 1, day=1)
            ).all()
            
            total_bills = len(bills)
            total_revenue = sum(bill.total_amount for bill in bills)
            total_tax = sum(bill.tax_amount for bill in bills)
            total_discount = sum(bill.discount_amount for bill in bills)
            
            # Payment method breakdown
            payment_methods = {}
            for bill in bills:
                method = bill.payment_method
                payment_methods[method] = payment_methods.get(method, 0) + 1
            
            return {
                'date': target_date,
                'total_bills': total_bills,
                'total_revenue': total_revenue,
                'total_tax': total_tax,
                'total_discount': total_discount,
                'average_bill_amount': total_revenue / total_bills if total_bills > 0 else 0,
                'payment_methods': payment_methods
            }
        finally:
            session.close()
    
    def refund_bill(self, bill_id: int) -> bool:
        """Process refund for a bill"""
        session = get_db_session()
        try:
            bill = session.query(Bill).filter(Bill.id == bill_id).first()
            if not bill or bill.payment_status != 'paid':
                return False
            
            bill.payment_status = 'refunded'
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()


# Global billing service instance
billing_service = BillingService()
